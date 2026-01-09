# Third Party Packages
import pandas as pd
from loguru import logger
from tenacity import (
    RetryCallState,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)
from unstructured.cleaners.core import group_broken_paragraphs

# Local Project
from src.core.config import settings


# --- Functions --- #
def _retry_state_before_sleep(retry_state: RetryCallState):
    logger.error(
        "Retrying {}: attempt {} ended with: {}",
        retry_state.fn,
        retry_state.attempt_number,
        retry_state.outcome,
    )


def create_retry_decorator(max_attempts=3, initial_wait=1, max_wait=10, exceptions=()):
    if exceptions:
        return retry(
            stop=stop_after_attempt(max_attempts),
            wait=wait_exponential(multiplier=initial_wait, min=initial_wait, max=max_wait),
            retry=retry_if_exception_type(exceptions),
            reraise=True,  # Reraise the final exception after all attempts fail
            before_sleep=_retry_state_before_sleep,
        )
    else:
        return retry(
            stop=stop_after_attempt(max_attempts),
            wait=wait_exponential(multiplier=initial_wait, min=initial_wait, max=max_wait),
            reraise=True,  # Reraise the final exception after all attempts fail
            before_sleep=_retry_state_before_sleep,
        )


def get_job_thread_ids() -> dict[str, str]:
    return {
        "AIML_ENGINEER": settings.aiml_engineer_thread_id,
        "DATA_ENGINEER": settings.data_engineer_thread_id,
        "DATA_SCIENTIST": settings.data_scientist_thread_id,
        "DATA_ANALYST": settings.data_analyst_thread_id,
        "OTHERS": settings.others_thread_id,
    }


def _boldify_text(text: str):
    return f"<b>{text}</b>"


def _format_field(str_format: str, value: str):
    logger.info("Filling for formatted string: {}", str_format)
    if value:
        return str_format.format(field=value)
    return ""


def get_unique_objs(rows: pd.Series) -> list:
    return list(rows.dropna().unique())


def format_job_description(row: pd.Series) -> str:
    cleaned_row = row.dropna()

    description = f"""
Job Title: {cleaned_row.get("title", "No Job Title")}

Job Description:
{group_broken_paragraphs(cleaned_row.get("description", "No Job Description provided."))}
"""

    return description


def format_company_message(company_df: pd.DataFrame, company: str) -> str:
    logger.info("Processing company {}, using {}", company, company_df)
    company_urls = get_unique_objs(company_df["company_url"])
    company_url = company_urls[0] if company_urls else ""
    header_component = f"""
    {_boldify_text("Company")}: {company} {_format_field("({field})", company_url)}
    """

    job_messages = []
    for job_title in get_unique_objs(company_df["title"]):
        urls: list[str] = get_unique_objs(company_df[company_df["title"] == job_title]["job_url"])
        output_url: str = " | ".join(urls)

        job_message = f"""
{_boldify_text("Job Title")}: {job_title}
{_boldify_text("Application Link")}: {output_url}
        """
        job_messages.append(job_message)

    body_component = "\n".join(job_messages)

    output_msg = f"""
{header_component}
{body_component}
  """

    return output_msg
