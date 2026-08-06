# Standard Library Packages
from typing import Sequence

# Third Party Packages
from loguru import logger

# Local Project
from src.errors import is_rate_limit_error

from .base import LLMClient


class CascadingLLMClient:
    """Coordinates multiple LLM clients, each with its own API key.

    Clients are tried in order per call, using the model supplied by the
    caller. The cascade is request-specific and rate-limit-driven: only when a
    client raises a rate-limit / quota error does it fail over to the next
    key/provider. Any non-rate-limit error propagates immediately, matching the
    original "error out" behaviour.

    This is intentionally key/rotation-only: model-tier fallback (e.g. a
    preferred model then a fallback model) stays in the caller, so both layers
    compose cleanly.
    """

    def __init__(self, clients: Sequence[LLMClient]):
        if not clients:
            raise ValueError("CascadingLLMClient requires at least one client.")
        self.clients = clients

    async def get_chat_completion(
        self,
        prompt: str,
        model: str,
        reasoning_enabled: bool = True,
        response_format=None,
        **kwargs,
    ) -> str:
        last_exception = None
        for client in self.clients:
            try:
                return await client.get_chat_completion(
                    prompt=prompt,
                    model=model,
                    reasoning_enabled=reasoning_enabled,
                    response_format=response_format,
                    **kwargs,
                )
            except Exception as e:
                if not is_rate_limit_error(e):
                    raise
                last_exception = e
                logger.warning(
                    "Rate limited on {} with model {} ({}). Trying next client...",
                    client,
                    model,
                    e,
                )
        raise last_exception

    async def get_job_category(
        self, prompt: str, model: str, reasoning_enabled: bool = True
    ) -> str:
        last_exception = None
        for client in self.clients:
            try:
                return await client.get_job_category(
                    prompt=prompt, model=model, reasoning_enabled=reasoning_enabled
                )
            except Exception as e:
                if not is_rate_limit_error(e):
                    raise
                last_exception = e
                logger.warning(
                    "Rate limited on {} with model {} ({}). Trying next client...",
                    client,
                    model,
                    e,
                )
        raise last_exception

    def __repr__(self) -> str:
        return f"CascadingLLMClient(clients={len(self.clients)})"
