# Standard Library Packages
import os

# Third Party Packages
import pandas as pd
from dotenv import load_dotenv
from jobspy import scrape_jobs
from loguru import logger
from tenacity import RetryCallState, retry, stop_after_attempt, wait_exponential

# Load environmental variables
load_dotenv()

HOURS_OLD = int(os.getenv("HOURS_OLD"))
DEFAULT_lOCATION = os.getenv("DEFAULT_LOCATION")


# --- Functions --- #
def retry_state_before_sleep(retry_state: RetryCallState):
    logger.error(
        "Retrying {}: attempt {} ended with: {}",
        retry_state.fn,
        retry_state.attempt_number,
        retry_state.outcome,
    )


def create_retry_decorator(max_attempts=3, initial_wait=1, max_wait=10):
    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=initial_wait, min=initial_wait, max=max_wait),
        reraise=True,  # Reraise the final exception after all attempts fail
        before_sleep=retry_state_before_sleep,
    )


def search_jobs_with_retry(
    search_term: str, hours_old: int = HOURS_OLD, location: str = DEFAULT_lOCATION
) -> pd.DataFrame:
    retry_decorator = create_retry_decorator()

    @retry_decorator
    def search_jobs() -> pd.DataFrame:
        jobs = scrape_jobs(
            site_name=["indeed", "linkedin", "zip_recruiter", "google"],
            search_term=search_term,
            google_search_term=f"{search_term} jobs in {location} since {hours_old} hours ago",
            location=location,
            country_indeed=location,
            hours_old=hours_old,
            linkedin_fetch_description=True,  # gets more info such as description, direct job url (slower)
            proxies=["208.195.175.46:65095", "208.195.175.45:65095"],
        )
        logger.info("Found {} jobs for search term {}", len(jobs), search_term)
        return jobs

    return search_jobs()
