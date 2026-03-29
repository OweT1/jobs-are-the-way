# Standard Library Packages
import json

# Third Party Packages
from loguru import logger
from openai import AsyncOpenAI
from pydantic import BaseModel

# Local Project
from src.constants import JOB_CATEGORIES


class LLMClient:
    def __init__(
        self,
        api_key: str,
        base_url: str,
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.client = AsyncOpenAI(base_url=base_url, api_key=api_key)

    async def get_chat_completion(
        self,
        prompt: str,
        model: str,
        reasoning_enabled: bool = True,
        response_format: BaseModel | dict | None = None,
        **kwargs,
    ) -> BaseModel | str:
        logger.info("Calling LLM with prompt {}", prompt)

        # @llm_retry_decorator
        async def _get_chat_completion(response_format=response_format):
            try:
                # Create the chat.completions.create kwargs
                if issubclass(response_format, BaseModel):
                    response_schema = response_format.model_json_schema()
                    response_schema["additionalProperties"] = False
                    response_format = {
                        "type": "json_schema",
                        "json_schema": {
                            "name": response_schema["title"],
                            "strict": True,
                            "schema": response_schema,
                        },
                    }

                completions_kwargs = {
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "response_format": response_format,
                }
                completions_kwargs.update(kwargs)

                # Add reasoning if enabled
                if reasoning_enabled:
                    completions_kwargs["extra_body"] = {"reasoning": {"enabled": True}}

                response = await self.client.chat.completions.create(**completions_kwargs)
                logger.info("Response Generated: {}", response)

                # Extract the message, checking for any network errors on the API
                choice = response.choices[0]
                if hasattr(choice, "error"):
                    logger.info("LLM Error detected.")
                    error = choice.error
                    error_msg = error["message"]
                    error_code = error["code"]
                    raise Exception(f"Error code: {error_code}, Error Message: {error_msg}")

                response_content = choice.message.content.strip()
                response_content_parsed = json.loads(response_content)
                job_category = response_content_parsed["job_category"]
                if job_category not in JOB_CATEGORIES:
                    logger.info("LLM Wrong Output detected.")
                    raise ValueError(f"LLM Response content should be in {JOB_CATEGORIES}.")
                return job_category
            except Exception as e:
                logger.error("Exception occurred: {}", e)
                raise Exception(e)

        return await _get_chat_completion()
