"""
Architect Agent - Especialista em arquitetura de sistemas.

Responsável por propor arquiteturas robustas, escaláveis e mantíveis.
"""

from backend.core.agent import Agent, AgentConfig, AgentOutput, SpecializedAgent
from backend.agents.prompts import get_agent_prompt
from typing import Any, Dict
import json


class ArchitectAgent(SpecializedAgent):
    """
    Agente especialista em arquitetura de sistemas.

    Analisa requisitos e propõe arquiteturas que consideram:
    - Escalabilidade horizontal e vertical
    - Resiliência e tolerância a falhas
    - Segurança desde o design
    - Manutenibilidade
    - Custo operacional
    """

    def __init__(self, llm_provider: Any):
        """
        Inicializa o Architect Agent.

        Args:
            llm_provider: Provider de LLM (Claude, OpenAI, etc)
        """
        prompt_data = get_agent_prompt("architect")

        config = AgentConfig(
            name="Architect",
            persona=prompt_data["persona"],
            system_prompt=prompt_data["system_prompt"],
            description=prompt_data["description"],
            responsibilities=[
                "Analisar requisitos e propor arquitetura",
                "Identificar riscos técnicos",
                "Sugerir padrões arquiteturais",
                "Definir estrutura de componentes",
                "Pensar em escalabilidade desde o início",
                "Avaliar trade-offs arquiteturais"
            ],
            capabilities=prompt_data["capabilities"],
            temperature=0.6  # Menos criativo, mais preciso
        )

        super().__init__(config, llm_provider)

    async def analyze(self, briefing: Dict[str, Any], context: Dict[str, Any]) -> AgentOutput:
        """
        Analisa briefing e propõe arquitetura.

        Args:
            briefing: Descrição do problema
            context: Contexto compartilhado

        Returns:
            AgentOutput com análise arquitetural
        """
        # Enriquece o briefing com contexto
        enriched_briefing = self._enrich_briefing(briefing, context)

        # Chama implementação padrão
        output = await super().analyze(enriched_briefing, context)

        # Valida output
        self._validate_architecture_output(output)

        return output

    def _enrich_briefing(self, briefing: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enriquece briefing com contexto e informações adicionais.

        Args:
            briefing: Briefing original
            context: Contexto compartilhado

        Returns:
            Briefing enriquecido
        """
        enriched = briefing.copy()

        # Extrai requisitos não-funcionais
        requirements = briefing.get("requirements", [])
        non_functional = [r for r in requirements if r.get("type") == "non_functional"]

        enriched["non_functional_requirements"] = non_functional

        # Extrai constraints
        constraints = briefing.get("constraints", [])
        enriched["technical_constraints"] = [c for c in constraints if c.get("type") == "technical"]
        enriched["budget_constraints"] = [c for c in constraints if c.get("type") == "budget"]

        # Adiciona histórico de lições aprendidas
        if self.memory.long_term:
            enriched["lessons_learned"] = self.memory.long_term

        return enriched

    def _validate_architecture_output(self, output: AgentOutput) -> None:
        """
        Valida que o output contém elementos esperados.

        Args:
            output: Output do agente
        """
        required_fields = [
            "architecture_type",
            "main_components",
            "scalability_strategy",
            "risks",
            "justification"
        ]

        output_data = output.output
        if isinstance(output_data, dict):
            for field in required_fields:
                if field not in output_data:
                    # Adiciona campo vazio se não existir
                    output_data[field] = None

    async def respond_to_debate(self, topic: str, positions: Dict[str, Any]) -> str:
        """
        Responde a debates sobre arquitetura.

        Args:
            topic: Tópico do debate
            positions: Posições dos outros agentes

        Returns:
            Resposta do agente
        """
        prompt = f"""
TÓPICO DE DEBATE: {topic}

POSIÇÕES DOS OUTROS AGENTES:
{json.dumps(positions, indent=2, ensure_ascii=False)}

Como Arquiteto, como você responde?

Considere:
1. Viabilidade técnica
2. Escalabilidade
3. Riscos
4. Trade-offs com outras posições

Seja direto e justifique baseado em princípios de arquitetura.
Não mude sua posição sem razão sólida.
        """

        response, tokens = await self.llm_provider.call(
            system_prompt=self.config.system_prompt,
            user_prompt=prompt,
            temperature=0.6
        )

        return response

    async def validate(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida uma proposta de arquitetura.

        Args:
            proposal: Proposta para validar

        Returns:
            Resultado da validação
        """
        prompt = f"""
PROPOSTA DE ARQUITETURA PARA VALIDAR:

{json.dumps(proposal, indent=2, ensure_ascii=False)}

Como Arquiteto experiente, valide essa proposta.

Verificar:
1. Escalabilidade - consegue crescer?
2. Resiliência - tolera falhas?
3. Segurança - protege dados?
4. Manutenibilidade - fácil de manter?
5. Performance - será rápido?
6. Custo - é economicamente viável?

Responda em JSON:
{
  "status": "approved|approved_with_concerns|rejected",
  "strengths": ["Força 1", "Força 2"],
  "weaknesses": ["Fraqueza 1", "Fraqueza 2"],
  "critical_issues": ["Problema crítico 1"],
  "recommendations": ["Recomendação 1"],
  "confidence": 0.9
}
        """

        response, tokens = await self.llm_provider.call(
            system_prompt=self.config.system_prompt,
            user_prompt=prompt,
            temperature=0.6
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

    def get_recommendations(self) -> Dict[str, Any]:
        """
        Retorna recomendações arquiteturais acumuladas.

        Returns:
            Recomendações do agente
        """
        if not self.last_output:
            return {}

        output = self.last_output.output
        if isinstance(output, dict):
            return {
                "architecture": output.get("architecture_type"),
                "components": output.get("main_components", []),
                "risks": output.get("risks", []),
                "scalability": output.get("scalability_strategy")
            }

        return {}
