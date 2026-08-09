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

DEFAULT_BIG_TECH_COMPANIES = (
    "apple,google,meta,microsoft,netflix,amazon,amazon.com,"
    "amazon web services (aws),nvidia,amd,databricks,snowflake,"
    "cursor,openai,binance,ibm,stripe,wise,mastercard,visa,"
    "govtech singapore,palantir technologies,revolut"
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Ignores extra env vars not defined here
    )

    environment_name: Literal[*ENVIRONMENTS] = DEFAULT_ENVIRONMENT
    openrouter_api_key: str
    openrouter_base_url: str

    hf_api_key: str
    hf_base_url: str

    # Optional comma-separated lists of additional keys (fallbacks/rotation).
    # Falls back to the single {provider}_api_key when left empty.
    openrouter_api_keys: str = ""
    hf_api_keys: str = ""

    @property
    def openrouter_keys(self) -> list[str]:
        keys = self._parse_keys(self.openrouter_api_keys)
        return keys or [self.openrouter_api_key]

    @property
    def hf_keys(self) -> list[str]:
        keys = self._parse_keys(self.hf_api_keys)
        return keys or [self.hf_api_key]

    @staticmethod
    def _parse_keys(raw: str) -> list[str]:
        return [key.strip() for key in raw.split(",") if key.strip()]

    # JobSpy
    default_location: str = DEFAULT_LOCATION

    # Comma-separated list of "big tech" companies for the Big Tech thread.
    # Override via the BIG_TECH_COMPANIES env var / GitHub Actions variable.
    big_tech_companies: str = DEFAULT_BIG_TECH_COMPANIES

    @property
    def big_tech_company_set(self) -> frozenset[str]:
        return frozenset(
            company.strip() for company in self.big_tech_companies.split(",") if company.strip()
        )

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
    tech_prog_thread_id: str
    senior_tech_thread_id: str
    not_relevant_thread_id: str
    big_tech_thread_id: str

    # Postgres
    postgres_db_url: str


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
