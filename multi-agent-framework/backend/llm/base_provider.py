"""
Base Provider - Interface abstrata para provedores de LLM.

Define a interface que todos os provedores (Claude, OpenAI, etc)
devem implementar.
"""

from abc import ABC, abstractmethod
from typing import Tuple, Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum


class ModelType(Enum):
    """Tipos de modelos suportados."""
    CLAUDE = "claude"
    GPT4 = "gpt4"
    GPT35 = "gpt35"
    CUSTOM = "custom"


@dataclass
class LLMResponse:
    """Resposta estruturada do LLM."""
    content: str
    tokens_used: int
    model: str
    stop_reason: Optional[str] = None
    cached: bool = False
    input_tokens: int = 0
    output_tokens: int = 0


@dataclass
class LLMConfig:
    """Configuração de um provider de LLM."""
    provider: str
    model: str
    api_key: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 4096
    timeout: int = 60
    max_retries: int = 3
    base_url: Optional[str] = None
    custom_headers: Optional[Dict[str, str]] = None


class BaseLLMProvider(ABC):
    """
    Interface abstrata para provedores de LLM.

    Todos os provedores (Claude, OpenAI, etc) devem implementar
    essa interface para funcionar com o framework.
    """

    def __init__(self, config: LLMConfig):
        """
        Inicializa o provider.

        Args:
            config: Configuração do provider
        """
        self.config = config
        self.request_count = 0
        self.total_tokens_used = 0
        self.call_history: List[Dict[str, Any]] = []

    @abstractmethod
    async def call(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> Tuple[str, int]:
        """
        Chama o LLM com prompts.

        Args:
            system_prompt: Prompt system (define persona/comportamento)
            user_prompt: Prompt do usuário (a tarefa)
            temperature: Controla criatividade (0=determinístico, 1=criativo)
            max_tokens: Limite de tokens na resposta

        Returns:
            Tuple (resposta_texto, tokens_usados)

        Raises:
            LLMException: Se houver erro na chamada
        """
        pass

    @abstractmethod
    async def call_structured(
        self,
        system_prompt: str,
        user_prompt: str,
        output_schema: Dict[str, Any],
        temperature: Optional[float] = None
    ) -> Tuple[Dict[str, Any], int]:
        """
        Chama LLM com resposta estruturada (JSON Schema).

        Args:
            system_prompt: Prompt system
            user_prompt: Prompt do usuário
            output_schema: Schema JSON esperado
            temperature: Controla criatividade

        Returns:
            Tuple (resposta_json, tokens_usados)

        Raises:
            LLMException: Se houver erro
        """
        pass

    @abstractmethod
    async def stream(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: Optional[float] = None
    ):
        """
        Chama LLM com streaming (respostas em tempo real).

        Args:
            system_prompt: Prompt system
            user_prompt: Prompt do usuário
            temperature: Controla criatividade

        Yields:
            Chunks de texto conforme chegam

        Raises:
            LLMException: Se houver erro
        """
        pass

    @abstractmethod
    async def batch_call(
        self,
        prompts: List[Tuple[str, str]],
        temperature: Optional[float] = None
    ) -> List[Tuple[str, int]]:
        """
        Executa múltiplas chamadas ao LLM (com otimização).

        Args:
            prompts: Lista de (system_prompt, user_prompt)
            temperature: Controla criatividade

        Returns:
            Lista de (resposta, tokens_usados)

        Raises:
            LLMException: Se houver erro
        """
        pass

    @abstractmethod
    async def validate_connection(self) -> bool:
        """
        Valida que o provider está funcional.

        Returns:
            True se conseguiu conectar

        Raises:
            LLMException: Se não conseguir conectar
        """
        pass

    def get_config(self) -> LLMConfig:
        """Retorna configuração do provider."""
        return self.config

    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de uso."""
        return {
            "provider": self.config.provider,
            "model": self.config.model,
            "request_count": self.request_count,
            "total_tokens_used": self.total_tokens_used,
            "avg_tokens_per_request": (
                self.total_tokens_used / self.request_count
                if self.request_count > 0 else 0
            ),
            "call_history_length": len(self.call_history)
        }

    def reset_stats(self) -> None:
        """Reseta estatísticas."""
        self.request_count = 0
        self.total_tokens_used = 0
        self.call_history = []

    def add_to_history(self, request: Dict[str, Any], response: str, tokens: int) -> None:
        """
        Adiciona chamada ao histórico.

        Args:
            request: Request (prompts)
            response: Response do LLM
            tokens: Tokens usados
        """
        self.request_count += 1
        self.total_tokens_used += tokens
        self.call_history.append({
            "request": request,
            "response": response,
            "tokens": tokens,
            "timestamp": __import__("datetime").datetime.utcnow().isoformat()
        })

    def get_call_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retorna histórico das últimas N chamadas."""
        return self.call_history[-limit:]

    def clear_history(self) -> None:
        """Limpa histórico de chamadas."""
        self.call_history = []


class LLMException(Exception):
    """Exceção base para erros de LLM."""

    def __init__(self, message: str, provider: str = None, model: str = None):
        self.message = message
        self.provider = provider
        self.model = model
        super().__init__(f"[{provider}/{model}] {message}" if provider else message)


class LLMConnectionError(LLMException):
    """Erro ao conectar com LLM."""
    pass


class LLMRateLimitError(LLMException):
    """Rate limit atingido."""
    pass


class LLMValidationError(LLMException):
    """Erro de validação (config, schema, etc)."""
    pass


class LLMTimeoutError(LLMException):
    """Timeout na chamada ao LLM."""
    pass


class LLMTokenLimitError(LLMException):
    """Token limit excedido."""
    pass
