"""
LLM Factory - Factory pattern para criar providers de LLM.

Permite instanciar o provider correto baseado em string de config.
"""

from typing import Optional, Dict, Any
from backend.llm.base_provider import BaseLLMProvider, LLMConfig, LLMException
from backend.llm.claude_provider import ClaudeProvider
from backend.llm.openai_provider import OpenAIProvider


class LLMFactory:
    """
    Factory para criar providers de LLM.

    Exemplo:
        provider = LLMFactory.create("claude", api_key="sk-...", model="claude-3-5-sonnet")
        response, tokens = await provider.call(system_prompt, user_prompt)
    """

    # Provedores suportados
    SUPPORTED_PROVIDERS = {
        "claude": ClaudeProvider,
        "openai": OpenAIProvider,
    }

    # Modelos padrão por provider
    DEFAULT_MODELS = {
        "claude": "claude-3-5-sonnet-20241022",
        "openai": "gpt-4",
    }

    # Configurações padrão por provider
    DEFAULT_CONFIGS = {
        "claude": {
            "temperature": 0.7,
            "max_tokens": 4096,
            "timeout": 60,
        },
        "openai": {
            "temperature": 0.7,
            "max_tokens": 4096,
            "timeout": 60,
        }
    }

    @classmethod
    def create(
        cls,
        provider: str,
        api_key: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> BaseLLMProvider:
        """
        Cria um provider de LLM.

        Args:
            provider: Nome do provider ("claude", "openai")
            api_key: API Key do provider
            model: Modelo específico (opcional, usa default se não informado)
            temperature: Criatividade (0-1 ou 0-2 para OpenAI)
            max_tokens: Limite de tokens
            **kwargs: Configurações adicionais

        Returns:
            Provider de LLM inicializado

        Raises:
            LLMException: Se provider não suportado ou configuração inválida

        Example:
            # Com Claude
            provider = LLMFactory.create(
                provider="claude",
                api_key="sk-ant-...",
                model="claude-3-5-sonnet-20241022"
            )

            # Com OpenAI
            provider = LLMFactory.create(
                provider="openai",
                api_key="sk-...",
                model="gpt-4"
            )
        """
        # Valida provider
        if provider not in cls.SUPPORTED_PROVIDERS:
            raise LLMException(
                f"Provider '{provider}' não suportado. "
                f"Suportados: {list(cls.SUPPORTED_PROVIDERS.keys())}",
                provider=provider
            )

        # Usa modelo padrão se não informado
        if model is None:
            model = cls.DEFAULT_MODELS[provider]

        # Monta config com defaults + valores informados
        default_config = cls.DEFAULT_CONFIGS[provider].copy()
        if temperature is not None:
            default_config["temperature"] = temperature
        if max_tokens is not None:
            default_config["max_tokens"] = max_tokens
        default_config.update(kwargs)

        # Cria config
        config = LLMConfig(
            provider=provider,
            model=model,
            api_key=api_key,
            **default_config
        )

        # Valida config
        cls._validate_config(config)

        # Instancia provider
        provider_class = cls.SUPPORTED_PROVIDERS[provider]

        try:
            return provider_class(config)
        except Exception as e:
            raise LLMException(
                f"Erro ao criar provider {provider}: {str(e)}",
                provider=provider,
                model=model
            )

    @classmethod
    def create_from_dict(cls, config_dict: Dict[str, Any]) -> BaseLLMProvider:
        """
        Cria um provider a partir de dicionário de configuração.

        Args:
            config_dict: Dict com chaves:
                - provider: "claude" ou "openai"
                - api_key: API key
                - model: Modelo (opcional)
                - temperature: Criatividade (opcional)
                - max_tokens: Limite de tokens (opcional)

        Returns:
            Provider de LLM inicializado

        Example:
            config = {
                "provider": "claude",
                "api_key": "sk-ant-...",
                "model": "claude-3-5-sonnet-20241022",
                "temperature": 0.7
            }
            provider = LLMFactory.create_from_dict(config)
        """
        config_dict = config_dict.copy()  # Não modifica original

        provider = config_dict.pop("provider")
        api_key = config_dict.pop("api_key")

        return cls.create(provider, api_key, **config_dict)

    @classmethod
    def create_from_env(cls, provider: str) -> BaseLLMProvider:
        """
        Cria provider usando variáveis de ambiente.

        Args:
            provider: Nome do provider

        Returns:
            Provider de LLM inicializado

        Raises:
            LLMException: Se variável de ambiente não encontrada

        Example:
            # Assume CLAUDE_API_KEY definida
            provider = LLMFactory.create_from_env("claude")

            # Assume OPENAI_API_KEY definida
            provider = LLMFactory.create_from_env("openai")
        """
        import os

        # Mapa de variáveis de ambiente por provider
        env_vars = {
            "claude": "CLAUDE_API_KEY",
            "openai": "OPENAI_API_KEY"
        }

        if provider not in env_vars:
            raise LLMException(
                f"Provider '{provider}' não suportado",
                provider=provider
            )

        env_var = env_vars[provider]
        api_key = os.getenv(env_var)

        if not api_key:
            raise LLMException(
                f"Variável de ambiente '{env_var}' não definida",
                provider=provider
            )

        return cls.create(provider, api_key)

    @classmethod
    def list_supported_providers(cls) -> list:
        """Retorna lista de provedores suportados."""
        return list(cls.SUPPORTED_PROVIDERS.keys())

    @classmethod
    def get_default_model(cls, provider: str) -> str:
        """
        Retorna modelo padrão para um provider.

        Args:
            provider: Nome do provider

        Returns:
            String com modelo padrão
        """
        if provider not in cls.DEFAULT_MODELS:
            raise LLMException(f"Provider '{provider}' desconhecido")
        return cls.DEFAULT_MODELS[provider]

    @classmethod
    def _validate_config(cls, config: LLMConfig) -> None:
        """
        Valida configuração do LLM.

        Args:
            config: Configuração a validar

        Raises:
            LLMException: Se configuração inválida
        """
        # Valida temperature
        if not 0 <= config.temperature <= 2:
            raise LLMException(
                f"Temperature inválida: {config.temperature} (deve estar entre 0 e 2)",
                provider=config.provider,
                model=config.model
            )

        # Valida max_tokens
        if config.max_tokens < 1:
            raise LLMException(
                f"max_tokens inválido: {config.max_tokens} (deve ser > 0)",
                provider=config.provider,
                model=config.model
            )

        # Valida timeout
        if config.timeout < 1:
            raise LLMException(
                f"timeout inválido: {config.timeout} (deve ser > 0)",
                provider=config.provider,
                model=config.model
            )

        # Valida max_retries
        if config.max_retries < 0:
            raise LLMException(
                f"max_retries inválido: {config.max_retries} (deve ser >= 0)",
                provider=config.provider,
                model=config.model
            )


# Aliases para facilitar uso
def get_claude_provider(api_key: str, model: Optional[str] = None) -> ClaudeProvider:
    """Helper para criar Claude provider."""
    return LLMFactory.create("claude", api_key, model=model)


def get_openai_provider(api_key: str, model: Optional[str] = None) -> OpenAIProvider:
    """Helper para criar OpenAI provider."""
    return LLMFactory.create("openai", api_key, model=model)


def get_provider_from_env(provider: str) -> BaseLLMProvider:
    """Helper para criar provider a partir de variáveis de ambiente."""
    return LLMFactory.create_from_env(provider)
