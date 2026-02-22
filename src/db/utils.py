# Standard Library Packages
import datetime

# Third Party Packages
from loguru import logger

# Local Project
from src.constants import HOURS_OLD_FALLBACK, HOURS_OLD_MAX
from src.db.pg import PostgresDB
from src.db.repositories import WorkflowRunsRepository

# --- Constants --- #
WORKFLOWRUNS_REPO = WorkflowRunsRepository()


# --- Util Functions --- #
def get_hours_old(db: PostgresDB) -> int:
    try:
        latest_timestamp = WORKFLOWRUNS_REPO._get_latest_timestamp_with_completed(db)
        if latest_timestamp:
            time_diff: datetime.timedelta = (
                datetime.datetime.now(datetime.timezone.utc)
                - latest_timestamp
                - datetime.timedelta(minutes=10)
            )  # add buffer for workflow runtime, which is around 10 minutes
            hours_old: int = (
                int(time_diff.total_seconds() // 3600) + 1
            )  # add 1 to hours_old - since we take floor of the time difference

            # fall-back for hours old
            if hours_old <= 0:
                raise ValueError("'hours_old' is less than or equal to 0")
            return min(hours_old, HOURS_OLD_MAX)
        else:
            raise ValueError("No workflows found in 'workflow_runs' table")
    except ValueError as ve:
        logger.warning("{}. Falling back to {} hours...", ve, HOURS_OLD_FALLBACK)
        return HOURS_OLD_FALLBACK
    except Exception as e:
        logger.error(
            "An unknown error occured: {}. Falling back to {} hours...", e, HOURS_OLD_FALLBACK
        )
        return HOURS_OLD_FALLBACK
