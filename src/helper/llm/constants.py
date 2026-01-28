# Standard Library Packages
from enum import Enum


class OpenRouterFreeModels(Enum):
    DEEPSEEK_R1 = "deepseek/deepseek-r1-0528:free"
    DEEPSEEK_R1T2 = "tngtech/deepseek-r1t2-chimera:free"
    OPENAI_20B = "openai/gpt-oss-20b:free"
    OPENAI_120B = "openai/gpt-oss-120b:free"
    GEMINI = "google/gemini-2.0-flash-exp:free"


class HuggingFaceFreeModels(Enum):
    DEEPSEEK = "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B:nscale"
