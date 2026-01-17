# Standard Library Packages
import datetime
import uuid

# Third Party Packages
from sqlalchemy import Column, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID  # noqa

# Local Project
from src.db.base import Base


# define JobResults table - stores all the unique job search results
class JobResults(Base):
    __tablename__ = "job_results"

    # id = Column(UUID(as_uuid=False), default=uuid.uuid4)
    job_id = Column(Text, primary_key=True, default=str(uuid.uuid4()))
    company = Column(Text, nullable=False)
    company_url = Column(Text, default="")
    title = Column(Text, nullable=False)
    description = Column(Text, default="")
    job_url = Column(Text, nullable=False)
    job_category = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.datetime.now)
