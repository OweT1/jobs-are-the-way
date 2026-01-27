# Third Party Packages
from loguru import logger
from openai import AsyncOpenAI

# Local Project
from src.helper.retry import llm_retry_decorator


class LLMClient:
    def __init__(
        self,
        api_key: str,
        base_url: str,
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.client = AsyncOpenAI(base_url=base_url, api_key=api_key)

    @llm_retry_decorator
    async def get_chat_completion(
        self, prompt: str, model: str, reasoning_enabled: bool = True, **kwargs
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

        response = await self.client.chat.completions.create(**completions_kwargs)
        logger.info("Response generated: {}", response)

        # Extract the assistant message with reasoning_details
        response = response.choices[0].message
        return response.content
