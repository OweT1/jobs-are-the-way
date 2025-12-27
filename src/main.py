# Standard Library Packages
import asyncio
import time  # noqa

# Third Party Packages
import pandas as pd
from loguru import logger

# Local Project
from src.constants import ALL_ROLES
from src.core.config import settings
from src.helper.job_search import search_jobs_with_retry
from src.helper.llm.constants import OpenRouterFreeModels
from src.helper.llm.llm_client import OpenRouterLLMClient
from src.helper.llm.prompts import get_category_prompt
from src.helper.telegram import TeleBot
from src.utils import (
    format_job_description,
    format_job_text_message,
    get_job_thread_ids,
)

# --- Constants --- #
LLM_MODEL: str = OpenRouterFreeModels.XIAOMI.value
MAX_API_CALLS_PER_MINUTE = 16
NOT_RELEVANT_CHANNEL_CATEGORIES = frozenset(["NOT_RELEVANT", "SENIOR_TECH"])


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
        client.get_chat_completion_with_retry(
            prompt=get_category_prompt(job_details=format_job_description(row)),
            model=LLM_MODEL,
            reasoning_enabled=True,
        )
        for _, row in final_df.iterrows()
    ]
    # if (
    #     LLM_MODEL != OpenRouterFreeModels.XIAOMI.value
    # ):  # need to do rate limiting - max 16 api calls per minute
    #     results = []
    #     for i in range(0, len(tasks), MAX_API_CALLS_PER_MINUTE):
    #         start_time = time.time()
    #         tmp_tasks = tasks[i : i + MAX_API_CALLS_PER_MINUTE]
    #         tmp_results = await asyncio.gather(*tmp_tasks)
    #         results.append(tmp_results)
    #         time_taken = time.time() - start_time
    #         sleep_time = 60 - time_taken if time_taken < 60 else 0
    #         await asyncio.sleep(sleep_time)

    # else:  # Other models no need to rate limit
    #     results = await asyncio.gather(*tasks)

    results = await asyncio.gather(*tasks)
    final_df["JOB_CATEGORY"] = results

    for _, row in final_df.iterrows():
        mes = format_job_text_message(row)
        job_category = row.get("JOB_CATEGORY", "NOT_RELEVANT")
        thread_id = job_thread_ids.get(job_category)
        logger.info("Sending message to {} channel", job_category)

        if job_category in NOT_RELEVANT_CHANNEL_CATEGORIES:
            await tele_bot.send_message_with_retry(
                mes, settings.non_relevant_channel_id
            )
        else:
            await tele_bot.send_message_with_retry(
                mes, settings.telegram_channel_id, thread_id
            )


if __name__ == "__main__":
    asyncio.run(main())
