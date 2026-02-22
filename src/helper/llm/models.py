# Third Party Packages
from pydantic import BaseModel, Field

# Local Project
from src.constants import JOB_CATEGORIES


class ResponseOutput(BaseModel):
    JOB_CATEGORY: str = Field(
        ..., description=f"Category of Job. Must strictly fall under {JOB_CATEGORIES}"
    )
    REASONING: str = Field(..., description="Reasoning for Job Category choice.")
