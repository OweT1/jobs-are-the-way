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
from src.helper.llm.client.openrouter import OpenRouterLLMClient
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
LLM_MODEL: str = OpenRouterFreeModels.DEEPSEEK.value
MAX_API_CALLS_PER_MINUTE = 16
MIN_INTERVAL = 60 / MAX_API_CALLS_PER_MINUTE


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

    # De-duplicate dataframe rows against DB
    logger.info("Before deduplicating against DB: {} rows", len(final_df))
    final_df = await check_jobs_existence(db, final_df)
    logger.info("After deduplicating against DB: {} rows", len(final_df))

    # Exit if no jobs were found
    if len(final_df) == 0:
        return

    llm_results = []
    for _, row in final_df.iterrows():
        start_time = time.time()
        res = await client.get_chat_completion(
            prompt=get_category_prompt(job_details=format_job_description(row)),
            model=LLM_MODEL,
            reasoning_enabled=True,
        )

        llm_results.append(res)
        time_taken = time.time() - start_time
        await asyncio.sleep(max(0, MIN_INTERVAL - time_taken))
    final_df["job_category"] = llm_results

    # Clean & Process Dataframe
    final_df = process_df(final_df)
    logger.info("Final df:")
    logger.info(final_df)

    for job_category in get_unique_objs(final_df["job_category"]):
        job_df = final_df[final_df["job_category"] == job_category]
        thread_id = get_job_thread_id(job_category)
        logger.info("Sending message to {} channel", job_category)
        for company in get_unique_objs(job_df["company"]):
            company_df = job_df[job_df["company"] == company]
            mes = format_company_message(company_df=company_df, company=company)
            await tele_bot.send_message(mes, settings.telegram_channel_id, thread_id)

    # Add the current dataframe rows to the database
    logger.info("Adding {} rows to 'job_results' table", len(final_df))
    add_jobs(db, final_df)


if __name__ == "__main__":
    asyncio.run(main())
