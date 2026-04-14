"""
Agent - Classe base para todos os agentes.

Cada agente é um especialista com sua própria persona, memória e capacidades.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import uuid4
import json


@dataclass
class AgentMemory:
    """Memória de um agente (curto + longo prazo)."""

    short_term: Dict[str, Any] = field(default_factory=dict)
    long_term: Dict[str, Any] = field(default_factory=dict)

    def add_short_term(self, key: str, value: Any) -> None:
        """Adiciona informação à memória de curto prazo."""
        self.short_term[key] = value

    def add_long_term(self, key: str, value: Any) -> None:
        """Adiciona informação à memória de longo prazo."""
        self.long_term[key] = value

    def get_short_term(self, key: str, default: Any = None) -> Any:
        """Recupera informação da memória de curto prazo."""
        return self.short_term.get(key, default)

    def get_long_term(self, key: str, default: Any = None) -> Any:
        """Recupera informação da memória de longo prazo."""
        return self.long_term.get(key, default)

    def clear_short_term(self) -> None:
        """Limpa memória de curto prazo (entre execuções)."""
        self.short_term.clear()


@dataclass
class AgentOutput:
    """Output estruturado de um agente."""

    agent_name: str
    agent_id: str
    output: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.utcnow)
    tokens_used: int = 0
    confidence: float = 0.9  # 0 a 1
    thinking_process: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Converte output para dicionário."""
        return {
            "agent_name": self.agent_name,
            "agent_id": self.agent_id,
            "output": self.output,
            "timestamp": self.timestamp.isoformat(),
            "tokens_used": self.tokens_used,
            "confidence": self.confidence,
            "thinking_process": self.thinking_process
        }


@dataclass
class AgentConfig:
    """Configuração de um agente."""

    name: str
    persona: str
    system_prompt: str
    description: str
    responsibilities: list[str]
    capabilities: list[str] = field(default_factory=list)
    temperature: float = 0.7
    max_tokens: int = 4096


class Agent(ABC):
    """
    Classe base abstrata para todos os agentes.

    Cada agente é um especialista com:
    - Uma persona/identidade clara
    - Um prompt system que define seu comportamento
    - Memória de curto e longo prazo
    - Capacidade de processar input e gerar output estruturado
    """

    def __init__(self, config: AgentConfig, llm_provider=None):
        """
        Inicializa um agente.

        Args:
            config: Configuração do agente (nome, persona, prompt, etc)
            llm_provider: Provider de LLM (Claude, OpenAI, etc)
        """
        self.config = config
        self.agent_id = str(uuid4())
        self.llm_provider = llm_provider
        self.memory = AgentMemory()
        self.last_output: Optional[AgentOutput] = None
        self.execution_count = 0
        self.total_tokens_used = 0

    def __repr__(self) -> str:
        return f"<Agent {self.config.name} ({self.agent_id[:8]})>"

    @abstractmethod
    async def analyze(self, briefing: Dict[str, Any], context: Dict[str, Any]) -> AgentOutput:
        """
        Analisa o briefing e contexto, retorna análise estruturada.

        Args:
            briefing: Descrição do problema
            context: Contexto compartilhado com outros agentes

        Returns:
            AgentOutput com análise do agente
        """
        pass

    @abstractmethod
    async def respond_to_debate(self, topic: str, positions: Dict[str, Any]) -> str:
        """
        Responde a um ponto de debate.

        Args:
            topic: Tópico do debate
            positions: Posições dos outros agentes

        Returns:
            Posição do agente em resposta
        """
        pass

    @abstractmethod
    async def validate(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida uma proposta de outro agente.

        Args:
            proposal: Proposta para validar

        Returns:
            Resultado da validação
        """
        pass

    async def execute_analysis(self, briefing: Dict[str, Any], context: Dict[str, Any]) -> AgentOutput:
        """
        Executa análise e registra execução.

        Args:
            briefing: Briefing do problema
            context: Contexto compartilhado

        Returns:
            AgentOutput com resultado
        """
        self.memory.add_short_term("current_briefing", briefing)
        self.memory.add_short_term("current_context", context)

        output = await self.analyze(briefing, context)

        self.last_output = output
        self.execution_count += 1
        self.total_tokens_used += output.tokens_used

        return output

    def get_memory_context(self) -> Dict[str, Any]:
        """Retorna contexto de memória para enviar ao LLM."""
        return {
            "short_term_memory": self.memory.short_term,
            "long_term_memory": self.memory.long_term,
            "previous_outputs": self.last_output.to_dict() if self.last_output else None
        }

    def update_long_term_memory(self, insights: Dict[str, Any]) -> None:
        """
        Atualiza memória de longo prazo com lições aprendidas.

        Args:
            insights: Insights para guardar
        """
        for key, value in insights.items():
            self.memory.add_long_term(key, value)

    def reset_short_term_memory(self) -> None:
        """Limpa memória de curto prazo (entre execuções)."""
        self.memory.clear_short_term()

    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do agente."""
        return {
            "agent_name": self.config.name,
            "agent_id": self.agent_id,
            "execution_count": self.execution_count,
            "total_tokens_used": self.total_tokens_used,
            "avg_tokens_per_execution": (
                self.total_tokens_used / self.execution_count
                if self.execution_count > 0 else 0
            ),
            "has_output": self.last_output is not None
        }


class SpecializedAgent(Agent):
    """
    Agente especializado com comportamento padrão.

    Pode ser subclassificado para criar agentes específicos
    ou usado diretamente com prompt customizado.
    """

    async def analyze(self, briefing: Dict[str, Any], context: Dict[str, Any]) -> AgentOutput:
        """Implementação padrão de análise."""
        if not self.llm_provider:
            raise RuntimeError(f"Agente {self.config.name} não tem LLM provider configurado")

        # Prepara prompt para o LLM
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(briefing, context)

        # Chama LLM
        response, tokens_used = await self.llm_provider.call(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )

        # Parseia resposta
        output = self._parse_response(response)

        return AgentOutput(
            agent_name=self.config.name,
            agent_id=self.agent_id,
            output=output,
            tokens_used=tokens_used,
            thinking_process=response
        )

    async def respond_to_debate(self, topic: str, positions: Dict[str, Any]) -> str:
        """Responde a debate."""
        if not self.llm_provider:
            raise RuntimeError(f"Agente {self.config.name} não tem LLM provider configurado")

        prompt = f"""
        Tópico de debate: {topic}

        Posições dos outros agentes:
        {json.dumps(positions, indent=2, ensure_ascii=False)}

        Como especialista em {self.config.persona}, qual é sua resposta?
        Seja direto e justifique sua posição.
        """

        response, _ = await self.llm_provider.call(
            system_prompt=self.config.system_prompt,
            user_prompt=prompt
        )

        return response

    async def validate(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Valida uma proposta."""
        if not self.llm_provider:
            raise RuntimeError(f"Agente {self.config.name} não tem LLM provider configurado")

        prompt = f"""
        Proposta para validar:
        {json.dumps(proposal, indent=2, ensure_ascii=False)}

        Valide essa proposta como um {self.config.persona} experiente.
        Retorne em JSON com campos: status (approved/concerns/rejected), issues (list), recommendations (list)
        """

        response, tokens_used = await self.llm_provider.call(
            system_prompt=self.config.system_prompt,
            user_prompt=prompt
        )

        try:
            result = json.loads(response)
        except json.JSONDecodeError:
            result = {
                "status": "concerns",
                "issues": ["Não conseguiu parsear resposta"],
                "recommendations": []
            }

        return result

    def _build_system_prompt(self) -> str:
        """Constrói prompt system para o LLM."""
        return f"""
        {self.config.system_prompt}

        Você é um {self.config.persona}.

        Suas responsabilidades:
        {chr(10).join(f"- {r}" for r in self.config.responsibilities)}

        Suas capacidades:
        {chr(10).join(f"- {c}" for c in self.config.capabilities)}

        Responda de forma clara, estruturada e justifique suas decisões.
        """

    def _build_user_prompt(self, briefing: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Constrói prompt de usuário."""
        return f"""
        BRIEFING:
        {json.dumps(briefing, indent=2, ensure_ascii=False)}

        CONTEXTO COMPARTILHADO:
        {json.dumps(context, indent=2, ensure_ascii=False)}

        Faça sua análise e retorne em formato JSON.
        """

    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parseia resposta do LLM para JSON."""
        try:
            # Tenta extrair JSON da resposta
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
        except (json.JSONDecodeError, ValueError):
            pass

        # Se não conseguir parsear, retorna resposta como texto
        return {
            "analysis": response,
            "format": "text"
        }
