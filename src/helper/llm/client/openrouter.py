# Local Project
from src.core.config import settings
from src.helper.llm.client.base import LLMClient


class OpenRouterLLMClient(LLMClient):
    def __init__(
        self,
        api_key: str = settings.openrouter_api_key,
        base_url: str = settings.openrouter_base_url,
    ):
        super().__init__(api_key, base_url)
