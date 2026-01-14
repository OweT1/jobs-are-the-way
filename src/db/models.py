# Standard Library Packages
import datetime
import uuid

# Third Party Packages
from sqlalchemy import Column, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID

# Local Project
from src.db.base import Base


# define JobResults table - stores all the unique job search results
class JobResults(Base):
    __tablename__ = "job_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company = Column(Text, nullable=False)
    company_url = Column(Text)
    title = Column(Text, nullable=False)
    description = Column(Text)
    job_url = Column(Text, nullable=False)
    job_category = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.datetime.now)
