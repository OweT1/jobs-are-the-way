# Standard Library Packages
import asyncio
import time

# Third Party Packages
import pandas as pd
from loguru import logger

# Local Project
from src.constants import ALL_ROLES
from src.core.config import settings
from src.db.job_results import add_jobs, check_jobs_existence, get_hours_old
from src.db.pg import PostgresDB
from src.helper.job_search import search_jobs
from src.helper.llm.client import LLMClient, OpenRouterLLMClient
from src.helper.llm.constants import OpenRouterFreeModels
from src.helper.llm.prompts import get_category_prompt
from src.helper.telegram import TeleBot
from src.utils import (
    format_company_message,
    format_job_description,
    get_job_thread_id,
    get_unique_objs,
    preprocess_df,
    process_df,
)

# --- Constants --- #
LLM_MODEL: str = OpenRouterFreeModels.NVIDIA.value
FALLBACK_MODEL: str = OpenRouterFreeModels.AVAILABLE.value
MAX_API_CALLS_PER_MINUTE = 16
BATCH_SIZE = 4
MAX_BATCH_CALLS_PER_MINUTE = MAX_API_CALLS_PER_MINUTE / BATCH_SIZE
MIN_INTERVAL = 60 / MAX_BATCH_CALLS_PER_MINUTE


# --- Helper functions --- #
async def get_llm_batch_calls(client: LLMClient, df: pd.DataFrame, model: str) -> list[str]:
    llm_results = []
    for i in range(0, len(df), BATCH_SIZE):
        start_time = time.time()
        temp_df = df.iloc[i : i + BATCH_SIZE]
        tasks = [
            client.get_chat_completion(
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


# --- Main function --- #
async def main():
    tele_bot = TeleBot()
    client = OpenRouterLLMClient()
    db = PostgresDB()
    hours_old: int = get_hours_old(db=db)

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
    final_df = await check_jobs_existence(db, final_df)
    logger.info("After de-duplicating against DB: {} rows", len(final_df))

    # Exit if no jobs were found after de-duplication
    if len(final_df) == 0:
        logger.info("Check 2: No jobs were found after de-duplicating against DB. Exiting...")
        return

    save_df = pd.DataFrame()
    for company in get_unique_objs(final_df["company"]):
        company_df = final_df[final_df["company"] == company]
        try:
            llm_results = await get_llm_batch_calls(client, company_df, LLM_MODEL)
        except Exception as e:
            logger.warning(
                "Current LLM model {} has errored out due to {}. Defaulting to openrouter available models...",
                LLM_MODEL,
                e,
            )
            llm_results = await get_llm_batch_calls(client, company_df, FALLBACK_MODEL)

        company_df["job_category"] = llm_results

        # Clean & Process DataFrame
        company_df = process_df(company_df)
        logger.info("df for company {}:", company)
        logger.info(company_df)

        for job_category in get_unique_objs(company_df["job_category"]):
            job_df = company_df[company_df["job_category"] == job_category]
            thread_id = get_job_thread_id(job_category)
            logger.info("Sending message to {} channel", job_category)

            mes = format_company_message(company_df=job_df, company=company)
            await tele_bot.send_message(mes, settings.telegram_channel_id, thread_id)

        save_df = pd.concat([save_df, company_df], axis=0)

    logger.info("Adding {} rows to 'job_results' table", len(save_df))
    add_jobs(db, save_df)
    logger.info("Successfully added {} rows to 'job_results' table", len(save_df))


if __name__ == "__main__":
    asyncio.run(main())
