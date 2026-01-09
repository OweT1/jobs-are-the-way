# Third Party Packages
import pandas as pd
from jobspy import scrape_jobs
from loguru import logger

# Local Project
from src.core.config import settings
from src.utils import create_retry_decorator


# --- Functions --- #
def search_jobs(
    search_term: str,
    hours_old: int = settings.hours_old,
    location: str = settings.default_location,
) -> pd.DataFrame:
    retry_decorator = create_retry_decorator()

    @retry_decorator
    def _search_jobs() -> pd.DataFrame:
        jobs = scrape_jobs(
            site_name=["indeed", "linkedin", "zip_recruiter", "google"],
            search_term=search_term,
            google_search_term=f"{search_term} jobs in {location} since {hours_old} hours ago",
            location=location,
            country_indeed=location,
            hours_old=hours_old,
            linkedin_fetch_description=True,  # gets more info such as description, direct job url (slower)
            # proxies=["208.195.175.46:65095", "208.195.175.45:65095"],
        )
        logger.info("Found {} jobs for search term {}", len(jobs), search_term)
        return jobs

    return _search_jobs()
