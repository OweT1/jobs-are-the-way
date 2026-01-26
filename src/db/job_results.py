# Standard Library Packages
import asyncio
import datetime

# Third Party Packages
import pandas as pd
from loguru import logger
from sqlalchemy import exists, func, select
from sqlalchemy.dialects.postgresql import insert

# Local Project
from src.constants import HOURS_OLD_FALLBACK, HOURS_OLD_MAX
from src.db.models import JobResults
from src.db.pg import PostgresDB
from src.helper.retry import db_retry_decorator


# --- DB Functions --- #
def _get_table_columns() -> list[str]:
    cols = JobResults.__table__.columns
    col_names = [col.key for col in cols]
    return col_names


@db_retry_decorator
def add_jobs(db: PostgresDB, jobs_df: pd.DataFrame):
    jobs_list = jobs_df.to_dict(orient="records")

    with db.session() as session:
        stmt = insert(JobResults).values(jobs_list)
        session.execute(stmt.on_conflict_do_nothing(index_elements=["job_id"]))  # upsert
        session.commit()

    logger.info("df of {} rows has successfully been added to the JobResults table", len(jobs_list))


@db_retry_decorator
def _check_job_existence_by_id(db: PostgresDB, job_id: str) -> bool:
    with db.session() as session:
        stmt = select(exists().where(JobResults.job_id == job_id))
        existence: bool = session.scalar(stmt)
    return existence


async def check_jobs_existence(db: PostgresDB, jobs_df: pd.DataFrame) -> pd.DataFrame:
    tasks = [
        asyncio.to_thread(_check_job_existence_by_id, db, job_id) for job_id in jobs_df["job_id"]
    ]

    results = await asyncio.gather(*tasks)
    boolean_filter = [not res for res in results]
    jobs_df = jobs_df.iloc[boolean_filter]
    return jobs_df


@db_retry_decorator
def _get_latest_timestamp(db: PostgresDB) -> datetime.datetime:
    with db.session() as session:
        stmt = select(func.max(JobResults.updated_at))
        latest_timestamp = session.execute(stmt).scalar_one_or_none()
    return latest_timestamp


def get_hours_old(db: PostgresDB) -> int:
    latest_timestamp = _get_latest_timestamp(db)
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
        logger.warning("'hours_old' is less than or equal to 0.")
        return HOURS_OLD_FALLBACK
    return min(hours_old, HOURS_OLD_MAX)
