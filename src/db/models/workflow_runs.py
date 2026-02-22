# Standard Library Packages
import datetime
import uuid

# Third Party Packages
from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy.dialects.postgresql import UUID  # noqa
from sqlalchemy.orm import relationship

# Local Project
from src.db.models.base import Base


# define JobResults table - stores all the unique job search results
class WorkflowRuns(Base):
    __tablename__ = "workflow_runs"

    id = Column(UUID(as_uuid=False), default=uuid.uuid4, primary_key=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.datetime.now)

    # Foreign relationship
    job = relationship("JobResults", back_populates="workflow")
