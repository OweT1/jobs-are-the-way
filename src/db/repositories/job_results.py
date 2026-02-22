# Standard Library Packages
import asyncio

# Third Party Packages
import pandas as pd
from loguru import logger
from sqlalchemy import exists, select
from sqlalchemy.dialects.postgresql import insert

# Local Project
from src.db.models import JobResults
from src.db.pg import PostgresDB
from src.db.repositories.base import BaseRepository
from src.helper.retry import db_retry_decorator


# --- DB Functions --- #
class JobResultsRepository(BaseRepository):
    def __init__(self):
        super().__init__(JobResults)

    @db_retry_decorator
    def add_jobs(self, db: PostgresDB, jobs_df: pd.DataFrame):
        jobs_list = jobs_df.to_dict(orient="records")

        with db.session() as session:
            stmt = insert(JobResults).values(jobs_list)
            session.execute(stmt.on_conflict_do_nothing(index_elements=["job_id"]))  # upsert
            session.commit()

        logger.info(
            "df of {} rows has successfully been added to the JobResults table", len(jobs_list)
        )

    @db_retry_decorator
    def _check_job_existence_by_id(self, db: PostgresDB, job_id: str) -> bool:
        with db.session() as session:
            stmt = select(exists().where(JobResults.job_id == job_id))
            existence: bool = session.scalar(stmt)
        return existence

    async def check_jobs_existence(self, db: PostgresDB, jobs_df: pd.DataFrame) -> pd.DataFrame:
        tasks = [
            asyncio.to_thread(self._check_job_existence_by_id, db, job_id)
            for job_id in jobs_df["job_id"]
        ]

        results = await asyncio.gather(*tasks)
        boolean_filter = [not res for res in results]
        jobs_df = jobs_df.iloc[boolean_filter]
        return jobs_df
