# Third Party Packages
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

# Local Project
from src.core.config import settings
from src.db.base import Base


class PostgresDB:
    def __init__(self):
        self.database_url = settings.postgres_db_url

        self.engine = create_async_engine(self.database_url, echo=True)
        self.session = async_sessionmaker(self.engine, expire_on_commit=False)

    async def setup(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        print("postgresdb successfully set-up!")
