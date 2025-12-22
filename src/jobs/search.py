import os
from dotenv import load_dotenv

from jobspy import scrape_jobs
from loguru import logger
import pandas as pd

# Load environmental variables
load_dotenv()

HOURS_OLD = int(os.getenv("HOURS_OLD"))
DEFAULT_lOCATION = os.getenv("DEFAULT_LOCATION")

# --- Functions --- #
def search_jobs(search_term: str, hours_old: int = HOURS_OLD, location: str = DEFAULT_lOCATION) -> pd.DataFrame:
  jobs = scrape_jobs(
      site_name="all",
      search_term=search_term,
      google_search_term=f"{search_term} jobs in {location} since {hours_old} hours ago",
      location=location,
      country_indeed=location,
      hours_old=hours_old,
      
      # linkedin_fetch_description=True # gets more info such as description, direct job url (slower)
      # proxies=["208.195.175.46:65095", "208.195.175.45:65095", "localhost"],
  )
  logger.info("Found {} jobs for search term {}", len(jobs), search_term)
  return jobs