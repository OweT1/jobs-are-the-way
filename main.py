# Standard Library Packages
import asyncio

# Third Party Packages
import pandas as pd
from loguru import logger

# Local Project
from src.constants import ALL_ROLES
from src.core.config import settings
from src.helper.job_search import search_jobs_with_retry
from src.helper.llm.llm_client import OpenRouterLLMClient
from src.helper.llm.prompts import get_category_prompt
from src.helper.telegram import TeleBot
from src.utils import (
    format_job_description,
    format_job_text_message,
    get_job_thread_ids,
)


# --- Main function --- #
async def main():
    tele_bot = TeleBot()
    job_thread_ids = get_job_thread_ids()
    client = OpenRouterLLMClient()

    logger.info("Searching for jobs...")

    tasks = [asyncio.to_thread(search_jobs_with_retry, role) for role in ALL_ROLES]

    results = await asyncio.gather(*tasks)
    final_df = (
        pd.concat(results)
        .drop_duplicates(subset=["id"], keep="first")
        .reset_index(drop=True)
    )

    tasks = [
        client.get_chat_completion(
            get_category_prompt(job_details=format_job_description(row))
        )
        for _, row in final_df.iterrows()
    ]
    results = await asyncio.gather(*tasks)
    final_df["JOB_CATEGORY"] = results

    for _, row in final_df.iterrows():
        mes = format_job_text_message(row)
        job_category = row.get("JOB_CATEGORY", "NOT_RELEVANT")
        thread_id = job_thread_ids.get(job_category)
        if thread_id:
            await tele_bot.send_message(mes, settings.telegram_channel_id, thread_id)
        else:  # If not relevant
            logger.info("Job of {} skipped", mes)


if __name__ == "__main__":
    asyncio.run(main())
