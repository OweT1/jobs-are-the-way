# Third Party Packages
import pandas as pd
from loguru import logger
from unstructured.cleaners.core import group_broken_paragraphs

# Local Project
from src.core.config import settings

# --- Constants --- #
required_fields = frozenset(["company", "title", "job_url"])


# --- Functions --- #
def get_job_thread_ids() -> dict[str, str]:
    return {
        "AIML_ENGINEER": settings.aiml_engineer_thread_id,
        "DATA_ENGINEER": settings.data_engineer_thread_id,
        "DATA_SCIENTIST": settings.data_scientist_thread_id,
        "DATA_ANALYST": settings.data_analyst_thread_id,
        "OTHERS": settings.others_thread_id,
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


def format_job_description(row: pd.Series) -> str:
    cleaned_row = row.dropna()

    description = f"""
Job Title: {cleaned_row.get('title', 'No Job Title')}

Job Description:
{group_broken_paragraphs(cleaned_row.get('description', 'No Job Description provided.'))}
"""

    return description
