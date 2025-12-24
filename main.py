# Standard Library Packages
import asyncio
import os

# Third Party Packages
import pandas as pd
from dotenv import load_dotenv
from loguru import logger

# Local Project
from src.helper import format_job_text_message, get_job_metadata
from src.jobs.search import search_jobs_with_retry
from src.telegram.bot import TeleBot

# Envrironmental Variables
load_dotenv()

CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")


# --- Main function --- #
async def main():
    tele_bot = TeleBot()
    job_metadata = get_job_metadata()

    seen_jobs = set()
    for job_title, metadata in job_metadata.items():
        logger.info("Searching for job {}...", job_title)

        search_terms: list[str] = metadata.get("SEARCH_TERMS", [])
        chat_id: str = metadata.get("CHAT_ID", "")

        tasks = [
            asyncio.to_thread(search_jobs_with_retry, search_term)
            for search_term in search_terms
        ]

        results = await asyncio.gather(*tasks)
        final_df = pd.concat(results).drop_duplicates()
        for _, row in final_df.iterrows():
            job_id = row["id"]

            # if job id was processed previously, we will not process it again
            if job_id in seen_jobs:
                logger.info("Skipping job_id of {}...", job_id)
                continue
            else:
                seen_jobs.add(job_id)
                mes = format_job_text_message(row)
                await tele_bot.send_message(mes, CHANNEL_ID, chat_id)


if __name__ == "__main__":
    asyncio.run(main())
