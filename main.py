# Standard Library Packages
import asyncio
import os

# Third Party Packages
import pandas as pd
from dotenv import load_dotenv
from loguru import logger

# Local Project
from src.constants import ALL_ROLES
from src.helper.job_search import search_jobs_with_retry
from src.helper.llm.llm_client import OpenRouterLLMClient
from src.helper.llm.prompts import get_category_prompt
from src.helper.telegram import TeleBot
from src.utils import format_job_text_message, get_job_thread_ids

# Envrironmental Variables
load_dotenv()

CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")


# --- Main function --- #
async def main():
    tele_bot = TeleBot()
    job_thread_ids = get_job_thread_ids()
    client = OpenRouterLLMClient()

    logger.info("Searching for jobs...")

    tasks = [asyncio.to_thread(search_jobs_with_retry, role) for role in ALL_ROLES]

    results = await asyncio.gather(*tasks)
    final_df = pd.concat(results).drop_duplicates().reset_index(drop=True)

    tasks = [
        client.get_chat_completion(get_category_prompt(job_details=description))
        for description in final_df["description"]
    ]
    results = await asyncio.gather(*tasks)
    final_df["JOB_CATEGORY"] = results

    for _, row in final_df.iterrows():
        mes = format_job_text_message(row)
        job_category = row.get("JOB_CATEGORY", "NOT_RELEVANT")
        thread_id = job_thread_ids.get(job_category)
        if thread_id:
            await tele_bot.send_message(mes, CHANNEL_ID, thread_id)
        else:
            logger.info("Job of {} skipped", mes)


if __name__ == "__main__":
    asyncio.run(main())
