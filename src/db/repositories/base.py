# Standard Library Packages

# Third Party Packages
from loguru import logger
from sqlalchemy import delete, func, text

# Local Project
from src.constants import DB_CLEAN_UP_DAYS_THRESHOLD
from src.db.models import Base
from src.db.pg import PostgresDB
from src.helper.retry import db_retry_decorator


class BaseRepository:
    def __init__(self, table: Base):
        self.table = table

    def _get_table_columns(self) -> list[str]:
        cols = self.table.__table__.columns
        col_names = [col.key for col in cols]
        return col_names

    @db_retry_decorator
    def delete_old_transactions(self, db: PostgresDB):
        with db.session() as session:
            stmt = delete(self.table).where(
                self.table.updated_at
                < func.now() - text(f"INTERVAL '{DB_CLEAN_UP_DAYS_THRESHOLD} days'")
            )
            result = session.execute(stmt)
            logger.info("Deleted {} number of rows", result.rowcount)
            session.commit()
