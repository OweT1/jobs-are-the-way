# Standard Library Packages
from enum import Enum


class OpenRouterFreeModels(Enum):
    DEEPSEEK = "deepseek/deepseek-r1-0528:free"
    OPENAI = "openai/gpt-oss-20b:free"
    GEMINI = "google/gemini-2.0-flash-exp:free"


class HuggingFaceFreeModels(Enum):
    DEEPSEEK = "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B:nscale"
