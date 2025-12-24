# Standard Library Packages
import os
from typing import Literal

# Third Party Packages
import pandas as pd
from dotenv import load_dotenv
from loguru import logger

# Local Project
from src.jobs.constants import (
    AIML_ENGINEER_ROLES,
    DATA_ENGINEER_ROLES,
    DATA_SCIENTIST_ROLES,
)

# Load environmental variables
load_dotenv()


# --- Constants --- #
required_fields = frozenset(["company", "title", "job_url"])


# --- Functions --- #
def get_job_metadata() -> dict[dict[str, Literal[list[str], str]]]:
    return {
        "AIML_ENGINEER": {
            "SEARCH_TERMS": AIML_ENGINEER_ROLES,
            "CHAT_ID": os.getenv("AIML_ENGINEER_THREAD_ID"),
        },
        "DATA_ENGINEER": {
            "SEARCH_TERMS": DATA_ENGINEER_ROLES,
            "CHAT_ID": os.getenv("DATA_ENGINEER_THREAD_ID"),
        },
        "DATA_SCIENTIST": {
            "SEARCH_TERMS": DATA_SCIENTIST_ROLES,
            "CHAT_ID": os.getenv("DATA_SCIENTIST_THREAD_ID"),
        },
    }


def format_job_text_message(row: pd.Series) -> str:
    logger.info("Processing job: {}", row)
    cleaned_row = row.dropna()

    # Validation check for required fields - Bare minimum is company, title and job_url
    for f in required_fields:
        if f not in cleaned_row:
            return ""
    logger.info("Job {} passed validation check", cleaned_row.get("id", ""))

    def _format_field(str_format: str, field: str):
        logger.info("Filling for formatted string: {}", str_format)
        value = cleaned_row.get(field, "")
        if value:
            return str_format.format(field=value)
        return ""

    def _boldify_text(text: str):
        return f"<b>{text}</b>"

    header_component = f"""
{_boldify_text("Company")}: {cleaned_row['company']} {_format_field("({field})", "company_url")}

{_boldify_text("Job Title")}: {cleaned_row['title']}

{_boldify_text("Application Link")}: {cleaned_row['job_url']} {_format_field("/ {field}", "job_url_direct")}
  """

    output_msg = f"""
{header_component}
  """

    return output_msg
