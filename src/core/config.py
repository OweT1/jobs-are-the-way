# Standard Library Packages
import os
from functools import lru_cache

# Third Party Packages
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY")

    hours_old: int = os.getenv("HOURS_OLD")
    default_location: str = os.getenv("Singapore")

    telegram_bot_api: str = os.getenv("TELEGRAM_BOT_API")
    telegram_channel_id: str = os.getenv("TELEGRAM_CHANNEL_ID")
    aiml_engineer_thread_id: int = os.getenv("AIML_ENGINEER_THREAD_ID")
    data_engineer_thread_id: int = os.getenv("DATA_ENGINEER_THREAD_ID")
    data_scientist_thread_id: int = os.getenv("DATA_SCIENTIST_THREAD_ID")
    data_analyst_thread_id: int = os.getenv("DATA_ANALYST_THREAD_ID")
    others_thread_id: int = os.getenv("OTHERS_THREAD_ID")


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
