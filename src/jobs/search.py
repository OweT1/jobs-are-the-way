import os

import pandas as pd
from dotenv import load_dotenv
from jobspy import scrape_jobs
from loguru import logger

# Load environmental variables
load_dotenv()

HOURS_OLD = int(os.getenv("HOURS_OLD"))
DEFAULT_lOCATION = os.getenv("DEFAULT_LOCATION")


# --- Functions --- #
def search_jobs(
    search_term: str, hours_old: int = HOURS_OLD, location: str = DEFAULT_lOCATION
) -> pd.DataFrame:
    jobs = scrape_jobs(
        site_name="all",
        search_term=search_term,
        google_search_term=f"{search_term} jobs in {location} since {hours_old} hours ago",
        location=location,
        country_indeed=location,
        hours_old=hours_old,
        linkedin_fetch_description=True,  # gets more info such as description, direct job url (slower)
    )
    logger.info("Found {} jobs for search term {}", len(jobs), search_term)
    return jobs
