# Standard Library Packages
import asyncio
import time
import uuid
from datetime import datetime

# Third Party Packages
import pandas as pd
from loguru import logger

# Local Project
from src.constants import ALL_ROLES, BIG_TECH_JOB_CATEGORIES
from src.core import settings
from src.db import (
    JobResultsRepository,
    PostgresDB,
    WorkflowRunsRepository,
    get_hours_old,
)
from src.helper import TeleBot, search_jobs
from src.helper.llm import (
    LLMClient,
    OpenRouterFreeModels,
    build_openrouter_cascading_client,
    get_category_prompt,
)
from src.utils import (
    check_blacklist_company,
    format_company_message,
    format_job_description,
    get_job_thread_id,
    is_big_tech,
    postprocess_df,
    preprocess_df,
)

# --- Constants --- #
MAX_API_CALLS_PER_MINUTE = 16
BATCH_SIZE = 4
MAX_BATCH_CALLS_PER_MINUTE = MAX_API_CALLS_PER_MINUTE / BATCH_SIZE
MIN_INTERVAL = 60 / MAX_BATCH_CALLS_PER_MINUTE
TELEGRAM_JOB_BATCH_PER_MSG = 5


# --- Helper functions --- #
async def get_job_category_batch(client: LLMClient, df: pd.DataFrame, model: str) -> list[str]:
    llm_results = []
    for i in range(0, len(df), BATCH_SIZE):
        start_time = time.time()
        temp_df = df.iloc[i : i + BATCH_SIZE]
        tasks = [
            client.get_job_category(
                prompt=get_category_prompt(job_details=format_job_description(row)),
                model=model,
                reasoning_enabled=True,
            )
            for _, row in temp_df.iterrows()
        ]
        res = await asyncio.gather(*tasks)
        llm_results.extend(res)

        time_taken = time.time() - start_time
        await asyncio.sleep(max(0, MIN_INTERVAL - time_taken))
    return llm_results


async def get_job_category_batch_cascade(
    df: pd.DataFrame,
    cascade: list[tuple[LLMClient, str]],
) -> list[str]:
    """Classify jobs by iterating over (client, model) tiers until one succeeds."""
    last_exception = None
    for client, model in cascade:
        try:
            return await get_job_category_batch(client, df, model)
        except Exception as e:
            last_exception = e
            logger.warning(
                "LLM model {} has errored out due to {}. Trying the next (LLMClient, model_name) pair...",
                model,
                e,
            )
    raise last_exception


async def send_tele_msg_batch(
    telegram_bot: TeleBot, df: pd.DataFrame, company: str, thread_id: str
):
    for i in range(0, len(df), TELEGRAM_JOB_BATCH_PER_MSG):
        temp_df = df.iloc[i : i + TELEGRAM_JOB_BATCH_PER_MSG]
        mes = format_company_message(company_df=temp_df, company=company)
        await telegram_bot.send_message(mes, settings.telegram_channel_id, thread_id)


# --- Main function --- #
async def main():
    tele_bot = TeleBot()
    openrouter_client = build_openrouter_cascading_client()
    db = PostgresDB()
    hours_old: int = get_hours_old()
    workflow_id = str(uuid.uuid4())
    workflow_runtime = datetime.now()

    jobs_repo = JobResultsRepository(db)
    workflow_repo = WorkflowRunsRepository(db)

    logger.info("Starting workflow...")
    workflow_repo.upsert_workflow_run(workflow_id, workflow_runtime, False)

    logger.info("Hours old: {}", hours_old)
    logger.info("Searching for jobs...")

    tasks = [asyncio.to_thread(search_jobs, role, hours_old) for role in ALL_ROLES]

    job_results = await asyncio.gather(*tasks)
    final_df = pd.concat(job_results)
    final_df = preprocess_df(final_df)

    # Exit if no jobs were found initially
    if len(final_df) == 0:
        logger.info("Check 1: No jobs were found in the intial stage. Exiting...")
        return

    # De-duplicate dataframe rows against DB
    logger.info("Before de-duplicating against DB: {} rows", len(final_df))
    final_df = await jobs_repo.check_jobs_existence(final_df)
    logger.info("After de-duplicating against DB: {} rows", len(final_df))

    # Exit if no jobs were found after de-duplication
    if len(final_df) == 0:
        logger.info("Check 2: No jobs were found after de-duplicating against DB. Exiting...")
        return

    # Check for blacklisted companies
    logger.info("Before checking for blacklisted companies: {} rows", len(final_df))
    final_df = check_blacklist_company(final_df)
    logger.info("After checking for blacklisted companies: {} rows", len(final_df))

    # Exit if no jobs were found after removing the blacklisted companies
    if len(final_df) == 0:
        logger.info("Check 3: No jobs were found after removing blacklisted companies. Exiting...")
        return

    # Set workflow_id, created_at, updated_at columns for job runs
    final_df["workflow_id"] = workflow_id
    final_df["created_at"] = workflow_runtime
    final_df["updated_at"] = workflow_runtime

    # Iterate through companies
    for group1, company_df in final_df.groupby(["company"]):
        (company,) = group1

        # De-duplicate the df before sending Telegram message - possible multiple workflows running at once
        logger.info("Before deduplicate check for {}: {} rows", company, len(company_df))
        company_df = await jobs_repo.check_jobs_existence(company_df)
        logger.info("After deduplicate check for {}: {} rows", company, len(company_df))

        # Exit if no jobs were found after de-duplication
        if len(company_df) == 0:
            logger.info(
                "Check 4: No jobs were found after dedeplicating from DB for {}. Exiting...",
                company,
            )
            continue

        # Model-tier fallback: try each (client, model_name) pair in order,
        # falling back to the next pair if one fails. Within each pair the
        # cascading client rotates across API keys/providers automatically.
        llm_cascade: list[tuple[LLMClient, str]] = [
            (openrouter_client, OpenRouterFreeModels.NVIDIA_NEMO_3_ULTRA.value),
            (openrouter_client, OpenRouterFreeModels.NVIDIA_NEMO_3_NANO.value),
            (openrouter_client, OpenRouterFreeModels.AVAILABLE.value),
        ]
        llm_results = await get_job_category_batch_cascade(company_df, llm_cascade)

        company_df["job_category"] = llm_results

        # Clean & Process DataFrame
        company_df = postprocess_df(company_df)
        logger.info("df for company {}:", company)
        logger.info(company_df)

        for group2, job_df in company_df.groupby(["job_category"]):
            (job_category,) = group2

            # De-duplicate the df before sending Telegram message - possible multiple workflows running at once
            logger.info(
                "Before deduplicate check for {}, {}: {} rows", company, job_category, len(job_df)
            )
            job_df = await jobs_repo.check_jobs_existence(job_df)
            logger.info(
                "After deduplicate check for {}, {}: {} rows", company, job_category, len(job_df)
            )

            if len(job_df) == 0:
                logger.info(
                    "Check 5: No jobs were found after dedeplicating from DB for {}, {}. Exiting...",
                    company,
                    job_category,
                )
                continue

            logger.info("Sending message to {} channel", job_category)
            await send_tele_msg_batch(
                telegram_bot=tele_bot,
                df=job_df,
                company=company,
                thread_id=get_job_thread_id(job_category),
            )

            # Save to DB
            logger.info("Adding {} rows to 'job_results' table", len(job_df))
            jobs_repo.add_jobs(job_df)
            logger.info("Successfully added {} rows to 'job_results' table", len(job_df))

        logger.info("Checking if {} is big tech...", company)
        if is_big_tech(company):
            logger.info("Sending to big tech thread!")
            big_tech_df = company_df[company_df["job_category"].isin(BIG_TECH_JOB_CATEGORIES)]
            await send_tele_msg_batch(
                telegram_bot=tele_bot,
                df=big_tech_df,
                company=company,
                thread_id=settings.big_tech_thread_id,
            )

    logger.info("Workflow run succeeded. Updating workflow in 'workflow_runs' table.")
    workflow_repo.upsert_workflow_run(workflow_id, workflow_runtime, True)
    logger.info("Successfully updated workflow_run")


if __name__ == "__main__":
    asyncio.run(main())
