# Third Party Packages
from loguru import logger
from openai import AsyncOpenAI

# Local Project
from src.core.config import settings
from src.utils import create_retry_decorator


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
        self, prompt: str, model: str, reasoning_enabled: bool = True, **kwargs
    ):
        retry_decorator = create_retry_decorator()

        @retry_decorator
        async def _get_chat_completion(
            client: AsyncOpenAI, prompt: str, model: str, reasoning_enabled: bool, **kwargs
        ):
            logger.info("Calling LLM with prompt {}", prompt)

            # Create the chat.completions.create kwargs
            completions_kwargs = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
            }
            completions_kwargs.update(kwargs)

            # Add reasoning if enabled
            if reasoning_enabled:
                completions_kwargs["extra_body"] = {"reasoning": {"enabled": True}}

            response = await client.chat.completions.create(**completions_kwargs)
            logger.info("Response generated: {}", response)

            # Extract the assistant message with reasoning_details
            response = response.choices[0].message
            return response.content

        return await _get_chat_completion(
            client=self.client,
            prompt=prompt,
            model=model,
            reasoning_enabled=reasoning_enabled,
            **kwargs,
        )
