"""
LLM - Módulo com adaptadores para múltiplos provedores de LLM.

Suporta Claude, OpenAI e pode ser estendido para outros.
"""

from backend.llm.base_provider import (
    BaseLLMProvider,
    LLMConfig,
    LLMResponse,
    LLMException,
    LLMConnectionError,
    LLMRateLimitError,
    LLMTokenLimitError,
    LLMTimeoutError,
    LLMValidationError,
    ModelType
)
from backend.llm.claude_provider import ClaudeProvider
from backend.llm.openai_provider import OpenAIProvider
from backend.llm.llm_factory import (
    LLMFactory,
    get_claude_provider,
    get_openai_provider,
    get_provider_from_env
)

__all__ = [
    "BaseLLMProvider",
    "LLMConfig",
    "LLMResponse",
    "LLMException",
    "LLMConnectionError",
    "LLMRateLimitError",
    "LLMTokenLimitError",
    "LLMTimeoutError",
    "LLMValidationError",
    "ModelType",
    "ClaudeProvider",
    "OpenAIProvider",
    "LLMFactory",
    "get_claude_provider",
    "get_openai_provider",
    "get_provider_from_env"
]
