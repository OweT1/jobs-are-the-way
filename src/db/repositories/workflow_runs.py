# Standard Library Packages
import datetime

# Third Party Packages
from loguru import logger
from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert

# Local Project
from src.db.models import WorkflowRuns
from src.db.pg import PostgresDB
from src.db.repositories.base import BaseRepository
from src.helper.retry import db_retry_decorator


# --- DB Functions --- #
class WorkflowRunsRepository(BaseRepository):
    def __init__(self):
        super().__init__(WorkflowRuns)

    @db_retry_decorator
    def _get_latest_timestamp_with_completed(self, db: PostgresDB) -> datetime.datetime:
        with db.session() as session:
            stmt = select(func.max(self.table.updated_at)).where(WorkflowRuns.completed)
            latest_timestamp = session.execute(stmt).scalar_one_or_none()
        return latest_timestamp

    @db_retry_decorator
    def upsert_workflow_run(
        self,
        db: PostgresDB,
        workflow_id: str,
        workflow_runtime: datetime.datetime,
        workflow_is_completed: bool,
    ):
        workflow_details = {
            "id": workflow_id,
            "completed": workflow_is_completed,
            "created_at": workflow_runtime,
            "updated_at": workflow_runtime,
        }

        with db.session() as session:
            stmt = insert(WorkflowRuns).values(workflow_details)
            session.execute(
                stmt.on_conflict_do_update(
                    index_elements=["id"],  # The column(s) that define the conflict
                    set_=workflow_details,
                )
            )  # upsert
            session.commit()

        logger.info("Workflow has successfully been updated to WorkflowRuns table")
