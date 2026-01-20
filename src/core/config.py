# Standard Library Packages
from enum import Enum
from functools import lru_cache  # noqa
from typing import Literal

# Third Party Packages
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Environment(Enum):
    LOCAL: str = "LOCAL"
    DEV: str = "DEV"
    PROD: str = "PROD"


DEFAULT_ENVIRONMENT = Environment.DEV.value
ENVIRONMENTS = [env.value for env in Environment]

DEFAULT_LOCATION = "Singapore"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Ignores extra env vars not defined here
    )

    environment_name: Literal[*ENVIRONMENTS] = DEFAULT_ENVIRONMENT
    openrouter_api_key: str
    openrouter_base_url: str

    # JobSpy
    default_location: str = DEFAULT_LOCATION

    # Telegram
    telegram_bot_api: str
    telegram_channel_id: str
    aiml_engineer_thread_id: str
    data_engineer_thread_id: str
    data_scientist_thread_id: str
    data_analyst_thread_id: str
    software_engineer_thread_id: str
    others_thread_id: str
    aiml_engineer_intern_thread_id: str
    data_engineer_intern_thread_id: str
    data_scientist_intern_thread_id: str
    data_analyst_intern_thread_id: str
    software_engineer_intern_thread_id: str
    others_intern_thread_id: str
    senior_tech_thread_id: str
    not_relevant_thread_id: str

    # Postgres
    postgres_db_url: str


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
