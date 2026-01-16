# Third Party Packages
import numpy as np
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
from src.constants import NON_RELEVANT_CHANNEL_CATEGORIES, REQUIRED_FIELDS
from src.core.config import settings
from src.db.job_results import _get_table_columns


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


def get_job_thread_id(job_category: str) -> dict[str, str]:
    job_thread_ids = {
        "AIML_ENGINEER": settings.aiml_engineer_thread_id,
        "DATA_ENGINEER": settings.data_engineer_thread_id,
        "DATA_SCIENTIST": settings.data_scientist_thread_id,
        "DATA_ANALYST": settings.data_analyst_thread_id,
        "SOFTWARE_ENGINEER": settings.software_engineer_thread_id,
        "OTHERS": settings.others_thread_id,
        "AIML_ENGINEER_INTERN": settings.aiml_engineer_intern_thread_id,
        "DATA_ENGINEER_INTERN": settings.data_engineer_intern_thread_id,
        "DATA_SCIENTIST_INTERN": settings.data_scientist_intern_thread_id,
        "DATA_ANALYST_INTERN": settings.data_analyst_intern_thread_id,
        "SOFTWARE_ENGINEER_INTERN": settings.software_engineer_intern_thread_id,
        "OTHERS_INTERN": settings.others_intern_thread_id,
        "SENIOR_TECH": settings.senior_tech_thread_id,
        "NOT_RELEVANT": settings.not_relevant_thread_id,
    }
    return job_thread_ids.get(job_category, settings.not_relevant_thread_id)


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
    header_component = (
        f"{_boldify_text('Company')}: {company} {_format_field('({field})', company_url)}"
    )

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


def process_df(final_df: pd.DataFrame) -> pd.DataFrame:
    def _clean_df(df):
        return df.dropna(subset=list(REQUIRED_FIELDS))

    def _add_intern(df):
        def _process_job_category(job_category: str, job_title: str):
            if (
                job_category not in NON_RELEVANT_CHANNEL_CATEGORIES
                and "intern" in job_title.lower()
                and not job_category.endswith("_INTERN")
            ):
                logger.debug(
                    "Job Title of {} with job category {} processed as Intern role",
                    job_title,
                    job_category,
                )
                return job_category + "_INTERN"
            return job_category

        df["job_category"] = df.apply(
            lambda row: _process_job_category(
                job_category=row["job_category"], job_title=row["title"]
            ),
            axis=1,
        )
        return df

    def _validate_senior_role(df):
        def _check_senior_role(job_category: str, job_title: str):
            if (
                job_category not in NON_RELEVANT_CHANNEL_CATEGORIES
                and "senior" in job_title.lower()
            ):
                logger.debug(
                    "Job Title of {} with job category {} processed as Senior role",
                    job_title,
                    job_category,
                )
                return "SENIOR_TECH"
            return job_category

        df["job_category"] = df.apply(
            lambda row: _check_senior_role(
                job_category=row["job_category"], job_title=row["title"]
            ),
            axis=1,
        )
        return df

    # DB processing
    def _rename_cols(df):
        df = df.rename(columns={"id": "job_id"})
        return df

    def _filter_cols(df):
        table_cols = _get_table_columns()
        df = df.filter(items=table_cols, axis=1)
        return df

    def _replace_nan(df):
        df = df.replace({np.nan: None})
        return df

    final_df = _clean_df(final_df)
    final_df = _add_intern(final_df)
    final_df = _validate_senior_role(final_df)
    final_df = _rename_cols(final_df)
    final_df = _filter_cols(final_df)
    final_df = _replace_nan(final_df)
    return final_df
