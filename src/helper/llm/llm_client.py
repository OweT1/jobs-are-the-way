# Third Party Packages
from loguru import logger
from openai import AsyncOpenAI

# Local Project
from src.core.config import settings
from src.helper.llm.constants import OpenRouterFreeModels


# --- LLM Functions --- #
class OpenRouterLLMClient:
    def __init__(
        self,
        api_key: str = settings.openrouter_api_key,
        base_url: str = settings.openrouter_base_url,
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.client = AsyncOpenAI(base_url=base_url, api_key=api_key)

    async def get_chat_completion(
        self, prompt: str, model: str = OpenRouterFreeModels.XIAOMI.value, **kwargs
    ):
        logger.info("Calling LLM with prompt {}", prompt)
        response = await self.client.chat.completions.create(
            model=model, messages=[{"role": "user", "content": prompt}], **kwargs
        )

        # Extract the assistant message with reasoning_details
        response = response.choices[0].message
        return response.content
