# Third Party Packages
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Local Project
from src.core.config import settings
from src.db.models.base import Base


class PostgresDB:
    def __init__(self):
        self.database_url = settings.postgres_db_url

        self.engine = create_engine(self.database_url, echo=True)
        self.session = sessionmaker(self.engine, expire_on_commit=False)

    def setup(self):
        Base.metadata.create_all(self.engine)
        logger.info("DB successfully set-up!")
