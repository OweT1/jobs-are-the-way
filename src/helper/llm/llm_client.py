# Standard Library Packages
import os

# Third Party Packages
from dotenv import load_dotenv
from loguru import logger
from openai import AsyncOpenAI

# Local Project
from src.helper.llm.constants import OpenRouterFreeModels

load_dotenv()

# Environmental Variables
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


# --- LLM Functions --- #
class OpenRouterLLMClient:
    def __init__(
        self,
        api_key: str = OPENROUTER_API_KEY,
        base_url: str = "https://openrouter.ai/api/v1",
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
