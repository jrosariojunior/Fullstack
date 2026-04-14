"""
Claude Provider - Implementação para Claude API (Anthropic).

Wrapper ao redor da SDK Anthropic oficial.
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


class ClaudeProvider(BaseLLMProvider):
    """
    Provider para Claude API (Anthropic).

    Suporta Claude 3.5 Sonnet e outros modelos.
    """

    def __init__(self, config: LLMConfig):
        """
        Inicializa Claude Provider.

        Args:
            config: Configuração com api_key e modelo
        """
        super().__init__(config)

        if not config.api_key:
            raise LLMException(
                "API key de Claude é obrigatória",
                provider="claude",
                model=config.model
            )

        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=config.api_key)
            self.async_client = anthropic.AsyncAnthropic(api_key=config.api_key)
        except ImportError:
            raise LLMException(
                "Biblioteca 'anthropic' não instalada. Instale com: pip install anthropic",
                provider="claude",
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
        Chama Claude API.

        Args:
            system_prompt: Instrução de sistema (persona)
            user_prompt: Prompt do usuário
            temperature: Criatividade (0-1)
            max_tokens: Limite de tokens

        Returns:
            Tuple (resposta, tokens_usados)

        Raises:
            LLMException: Se houver erro
        """
        try:
            temp = temperature if temperature is not None else self.config.temperature
            max_tok = max_tokens if max_tokens is not None else self.config.max_tokens

            response = await self.async_client.messages.create(
                model=self.config.model,
                max_tokens=max_tok,
                temperature=temp,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

            content = response.content[0].text
            tokens = response.usage.output_tokens + response.usage.input_tokens

            # Registra no histórico
            self.add_to_history(
                {"system": system_prompt, "user": user_prompt},
                content,
                tokens
            )

            return content, tokens

        except json.JSONDecodeError as e:
            raise LLMException(
                f"Erro ao parsear resposta JSON: {str(e)}",
                provider="claude",
                model=self.config.model
            )

        except TimeoutError:
            raise LLMTimeoutError(
                f"Timeout após {self.config.timeout}s",
                provider="claude",
                model=self.config.model
            )

        except Exception as e:
            error_msg = str(e)

            # Detecta rate limit
            if "rate_limit" in error_msg.lower() or "429" in error_msg:
                raise LLMRateLimitError(
                    "Rate limit atingido",
                    provider="claude",
                    model=self.config.model
                )

            # Detecta token limit
            if "token" in error_msg.lower() and "limit" in error_msg.lower():
                raise LLMTokenLimitError(
                    "Token limit excedido",
                    provider="claude",
                    model=self.config.model
                )

            raise LLMException(
                f"Erro chamando Claude: {error_msg}",
                provider="claude",
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
        Chama Claude com resposta estruturada (JSON).

        Args:
            system_prompt: Instrução de sistema
            user_prompt: Prompt do usuário
            output_schema: Schema JSON esperado
            temperature: Criatividade

        Returns:
            Tuple (resposta_json, tokens_usados)
        """
        # Enriquece user_prompt com schema esperado
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
                provider="claude",
                model=self.config.model
            )

    async def stream(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: Optional[float] = None
    ):
        """
        Chama Claude com streaming.

        Args:
            system_prompt: Instrução de sistema
            user_prompt: Prompt do usuário
            temperature: Criatividade

        Yields:
            Chunks de texto conforme chegam
        """
        try:
            temp = temperature if temperature is not None else self.config.temperature

            with self.async_client.messages.stream(
                model=self.config.model,
                max_tokens=self.config.max_tokens,
                temperature=temp,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            ) as stream:
                full_response = ""
                for text in stream.text_stream:
                    full_response += text
                    yield text

                # Registra no histórico ao final
                # Nota: tokens exatos só estão disponíveis ao final
                self.add_to_history(
                    {"system": system_prompt, "user": user_prompt},
                    full_response,
                    0  # Token count é aproximado em streaming
                )

        except Exception as e:
            raise LLMException(
                f"Erro no streaming: {str(e)}",
                provider="claude",
                model=self.config.model
            )

    async def batch_call(
        self,
        prompts: List[Tuple[str, str]],
        temperature: Optional[float] = None
    ) -> List[Tuple[str, int]]:
        """
        Executa múltiplas chamadas (sequencial, não paralelo).

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
                # Continua mesmo se uma chamada falhar
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
            # Faz uma chamada simples para testar
            response = await self.async_client.messages.create(
                model=self.config.model,
                max_tokens=10,
                messages=[
                    {"role": "user", "content": "Responda 'ok'"}
                ]
            )
            return True

        except Exception as e:
            raise LLMConnectionError(
                f"Não conseguiu conectar com Claude: {str(e)}",
                provider="claude",
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
        # Heurística simples: ~4 caracteres por token
        return len(text) // 4

    async def humanize_text(self, text: str) -> str:
        """
        Humaniza texto IA (remove jargão, melhora legibilidade).

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
