# Standard Library Packages
from typing import Sequence

# Local Project
from src.core.config import settings

from .base import LLMClient
from .cascading import CascadingLLMClient
from .huggingface import HuggingFaceLLMClient
from .openrouter import OpenRouterLLMClient


# LLM Client Pools
def build_client_pool() -> list[LLMClient]:
    """Builds an ordered list of LLM clients, one per configured API key.

    Providers with multiple keys (e.g. comma-separated `OPENROUTER_API_KEYS`)
    are expanded once per key so a key that runs out of quota falls through to
    the next key or provider at the model-tier level.
    """
    clients: list[LLMClient] = []

    # Openrouter Clients will go first
    for api_key in settings.openrouter_keys:
        clients.append(OpenRouterLLMClient(api_key=api_key))

    for api_key in settings.hf_keys:
        clients.append(HuggingFaceLLMClient(api_key=api_key))

    return clients


def build_openrouter_client_pool() -> list[OpenRouterLLMClient]:
    """Builds an ordered list of LLM clients, one per configured API key.

    Providers with multiple keys (e.g. comma-separated `OPENROUTER_API_KEYS`)
    are expanded once per key so a key that runs out of quota falls through to
    the next key or provider at the model-tier level.
    """
    clients: list[OpenRouterLLMClient] = []

    for api_key in settings.openrouter_keys:
        clients.append(OpenRouterLLMClient(api_key=api_key))

    return clients


# Cascading LLM Clients
def build_cascading_client(
    clients: Sequence[LLMClient] | None = None,
) -> CascadingLLMClient:
    """Builds a CascadingLLMClient over the configured pool (or a custom one).

    Model-tier fallback (preferred vs. fallback model) is handled separately by
    the caller, so this client only rotates across keys/providers per model.
    """
    return CascadingLLMClient(clients if clients is not None else build_client_pool())


def build_openrouter_cascading_client(
    clients: Sequence[LLMClient] | None = None,
) -> CascadingLLMClient:
    """Builds a CascadingLLMClient over the configured pool (or a custom one).

    Model-tier fallback (preferred vs. fallback model) is handled separately by
    the caller, so this client only rotates across keys/providers per model.
    """
    return CascadingLLMClient(clients if clients is not None else build_openrouter_client_pool())
