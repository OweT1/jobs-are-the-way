# Standard Library Packages
from enum import Enum
from typing import Literal

# Third Party Packages
from pydantic import BaseModel

# Local Project
from src.constants import JOB_CATEGORIES


# --- LLM Client Model Enums --- #
class OpenRouterFreeModels(Enum):
    DEEPSEEK_R1 = "deepseek/deepseek-r1-0528:free"
    OPENAI_20B = "openai/gpt-oss-20b:free"
    OPENAI_120B = "openai/gpt-oss-120b:free"
    GEMINI = "google/gemini-2.0-flash-exp:free"
    NVIDIA = "nvidia/nemotron-3-nano-30b-a3b:free"
    AVAILABLE = "openrouter/free"


class HuggingFaceFreeModels(Enum):
    DEEPSEEK = "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B:nscale"


# --- LLM Output Formats --- #
class JobCategoryOutput(BaseModel):
    job_category: Literal[*JOB_CATEGORIES]
