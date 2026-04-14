"""
OpenAI Provider - Implementação para OpenAI API.

Suporta GPT-4, GPT-4 Turbo, GPT-3.5 Turbo, etc.
"""

import json
from typing import Tuple, Optional, Dict, Any, List
from backend.llm.base_provider import (
    BaseLLMProvider,
    LLMConfig,
    LLMResponse,
    LLMException,
    LLMConnectionError,
    LLMRateLimitError,
    LLMTokenLimitError,
    LLMTimeoutError
)


class OpenAIProvider(BaseLLMProvider):
    """
    Provider para OpenAI API (GPT-4, GPT-3.5, etc).

    Wrapper ao redor da SDK OpenAI oficial.
    """

    def __init__(self, config: LLMConfig):
        """
        Inicializa OpenAI Provider.

        Args:
            config: Configuração com api_key e modelo
        """
        super().__init__(config)

        if not config.api_key:
            raise LLMException(
                "API key de OpenAI é obrigatória",
                provider="openai",
                model=config.model
            )

        try:
            from openai import AsyncOpenAI, OpenAI
            self.client = OpenAI(api_key=config.api_key)
            self.async_client = AsyncOpenAI(api_key=config.api_key)
        except ImportError:
            raise LLMException(
                "Biblioteca 'openai' não instalada. Instale com: pip install openai",
                provider="openai",
                model=config.model
            )

    async def call(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> Tuple[str, int]:
        """
        Chama OpenAI API.

        Args:
            system_prompt: Instrução de sistema (persona)
            user_prompt: Prompt do usuário
            temperature: Criatividade (0-2)
            max_tokens: Limite de tokens

        Returns:
            Tuple (resposta, tokens_usados)

        Raises:
            LLMException: Se houver erro
        """
        try:
            temp = temperature if temperature is not None else self.config.temperature
            max_tok = max_tokens if max_tokens is not None else self.config.max_tokens

            response = await self.async_client.chat.completions.create(
                model=self.config.model,
                max_tokens=max_tok,
                temperature=temp,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )

            content = response.choices[0].message.content
            tokens = response.usage.total_tokens

            # Registra no histórico
            self.add_to_history(
                {"system": system_prompt, "user": user_prompt},
                content,
                tokens
            )

            return content, tokens

        except TimeoutError:
            raise LLMTimeoutError(
                f"Timeout após {self.config.timeout}s",
                provider="openai",
                model=self.config.model
            )

        except Exception as e:
            error_msg = str(e)

            # Detecta rate limit
            if "rate_limit" in error_msg.lower() or "429" in error_msg:
                raise LLMRateLimitError(
                    "Rate limit atingido",
                    provider="openai",
                    model=self.config.model
                )

            # Detecta token limit
            if "token" in error_msg.lower() and "exceeds" in error_msg.lower():
                raise LLMTokenLimitError(
                    "Token limit excedido",
                    provider="openai",
                    model=self.config.model
                )

            # Detecta autenticação
            if "401" in error_msg or "authentication" in error_msg.lower():
                raise LLMConnectionError(
                    "Erro de autenticação (API key inválida?)",
                    provider="openai",
                    model=self.config.model
                )

            raise LLMException(
                f"Erro chamando OpenAI: {error_msg}",
                provider="openai",
                model=self.config.model
            )

    async def call_structured(
        self,
        system_prompt: str,
        user_prompt: str,
        output_schema: Dict[str, Any],
        temperature: Optional[float] = None
    ) -> Tuple[Dict[str, Any], int]:
        """
        Chama OpenAI com resposta estruturada (JSON).

        Args:
            system_prompt: Instrução de sistema
            user_prompt: Prompt do usuário
            output_schema: Schema JSON esperado
            temperature: Criatividade

        Returns:
            Tuple (resposta_json, tokens_usados)
        """
        # Enriquece prompt com schema
        enhanced_prompt = f"""{user_prompt}

RESPONDA OBRIGATORIAMENTE EM JSON COM ESTE FORMATO:
{json.dumps(output_schema, indent=2, ensure_ascii=False)}

Retorne APENAS o JSON, sem markdown ou explicações adicionais.
        """

        response_text, tokens = await self.call(
            system_prompt,
            enhanced_prompt,
            temperature
        )

        # Tenta parsear JSON
        try:
            # Remove markdown code blocks se houver
            json_str = response_text
            if "```json" in json_str:
                json_str = json_str.split("```json")[1].split("```")[0]
            elif "```" in json_str:
                json_str = json_str.split("```")[1].split("```")[0]

            result = json.loads(json_str.strip())
            return result, tokens

        except json.JSONDecodeError as e:
            raise LLMException(
                f"Resposta não é JSON válido: {response_text[:100]}...",
                provider="openai",
                model=self.config.model
            )

    async def stream(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: Optional[float] = None
    ):
        """
        Chama OpenAI com streaming.

        Args:
            system_prompt: Instrução de sistema
            user_prompt: Prompt do usuário
            temperature: Criatividade

        Yields:
            Chunks de texto conforme chegam
        """
        try:
            temp = temperature if temperature is not None else self.config.temperature

            with self.async_client.chat.completions.create(
                model=self.config.model,
                max_tokens=self.config.max_tokens,
                temperature=temp,
                stream=True,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            ) as stream:
                full_response = ""
                async for chunk in stream:
                    if chunk.choices[0].delta.content:
                        text = chunk.choices[0].delta.content
                        full_response += text
                        yield text

                # Registra no histórico ao final
                self.add_to_history(
                    {"system": system_prompt, "user": user_prompt},
                    full_response,
                    0  # Token count em streaming é aproximado
                )

        except Exception as e:
            raise LLMException(
                f"Erro no streaming: {str(e)}",
                provider="openai",
                model=self.config.model
            )

    async def batch_call(
        self,
        prompts: List[Tuple[str, str]],
        temperature: Optional[float] = None
    ) -> List[Tuple[str, int]]:
        """
        Executa múltiplas chamadas (sequencial).

        Args:
            prompts: Lista de (system_prompt, user_prompt)
            temperature: Criatividade

        Returns:
            Lista de (resposta, tokens_usados)
        """
        results = []

        for system_prompt, user_prompt in prompts:
            try:
                response, tokens = await self.call(
                    system_prompt,
                    user_prompt,
                    temperature
                )
                results.append((response, tokens))
            except LLMException:
                results.append(("", 0))

        return results

    async def validate_connection(self) -> bool:
        """
        Valida que a API Key está funcional.

        Returns:
            True se conseguiu conectar

        Raises:
            LLMConnectionError: Se não conseguir
        """
        try:
            response = await self.async_client.chat.completions.create(
                model=self.config.model,
                max_tokens=10,
                messages=[
                    {"role": "user", "content": "Responda 'ok'"}
                ]
            )
            return True

        except Exception as e:
            raise LLMConnectionError(
                f"Não conseguiu conectar com OpenAI: {str(e)}",
                provider="openai",
                model=self.config.model
            )

    def count_tokens(self, text: str) -> int:
        """
        Estima número de tokens em um texto.

        Args:
            text: Texto para contar

        Returns:
            Número aproximado de tokens
        """
        # Heurística: ~4 caracteres por token para OpenAI também
        return len(text) // 4

    async def humanize_text(self, text: str) -> str:
        """
        Humaniza texto IA.

        Args:
            text: Texto para humanizar

        Returns:
            Texto humanizado
        """
        humanization_prompt = f"""
Reescreva o texto abaixo de forma mais natural e humanizada.
Remova jargão técnico excessivo.
Melhore a legibilidade.
Mantenha o significado e a precisão.

TEXTO ORIGINAL:
{text}

TEXTO HUMANIZADO:
        """

        response, _ = await self.call(
            system_prompt="Você é um editor experiente em reescrever texto técnico de forma humanizada.",
            user_prompt=humanization_prompt,
            temperature=0.7
        )

        return response.strip()


# Mapeamento de modelos OpenAI
OPENAI_MODELS = {
    "gpt4": "gpt-4",
    "gpt4-turbo": "gpt-4-turbo-preview",
    "gpt35": "gpt-3.5-turbo",
    "gpt4-vision": "gpt-4-vision-preview"
}
