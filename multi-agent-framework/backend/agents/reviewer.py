"""
TechReviewer Agent - Especialista em validação crítica.

Responsável por questionar decisões, validar trade-offs
e garantir qualidade técnica.
"""

from backend.core.agent import Agent, AgentConfig, AgentOutput, SpecializedAgent
from backend.agents.prompts import get_agent_prompt
from typing import Any, Dict, List
import json


class TechReviewerAgent(SpecializedAgent):
    """
    Agente especialista em revisão técnica crítica.

    Valida coerência entre componentes, identifica riscos
    e questiona decisões técnicas.
    """

    def __init__(self, llm_provider: Any):
        """
        Inicializa o TechReviewer Agent.

        Args:
            llm_provider: Provider de LLM
        """
        prompt_data = get_agent_prompt("reviewer")

        config = AgentConfig(
            name="TechReviewer",
            persona=prompt_data["persona"],
            system_prompt=prompt_data["system_prompt"],
            description=prompt_data["description"],
            responsibilities=[
                "Validar coerência entre componentes",
                "Identificar riscos técnicos não mencionados",
                "Questionar decisões arbitrárias",
                "Verificar performance e scalability",
                "Avaliar segurança rigorosamente",
                "Detectar inconsistências"
            ],
            capabilities=prompt_data["capabilities"],
            temperature=0.5  # Menos criativo, mais crítico
        )

        super().__init__(config, llm_provider)

    async def analyze(self, briefing: Dict[str, Any], context: Dict[str, Any]) -> AgentOutput:
        """
        Analisa e valida todas as propostas anteriores.

        Args:
            briefing: Descrição do problema
            context: Contexto compartilhado (inclui arquitetura, plano, tech)

        Returns:
            AgentOutput com validação crítica
        """
        # Enriquece briefing com todas as propostas
        enriched_briefing = self._enrich_briefing(briefing, context)

        # Chama implementação padrão
        output = await super().analyze(enriched_briefing, context)

        # Valida review output
        self._validate_review_output(output)

        return output

    def _enrich_briefing(self, briefing: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enriquece briefing com TODAS as propostas para validar.

        Args:
            briefing: Briefing original
            context: Contexto compartilhado

        Returns:
            Briefing enriquecido para revisão
        """
        enriched = briefing.copy()

        # Extrai todas as propostas anteriores
        agents_output = context.get("agents_output", {})

        enriched["architecture_proposal"] = agents_output.get("Architect")
        enriched["plan_proposal"] = agents_output.get("Analyst")
        enriched["tech_proposal"] = agents_output.get("Developer")

        # Adiciona checklist de revisão
        enriched["review_checklist"] = [
            "coerência entre arquitetura, plano e tech",
            "riscos técnicos não mencionados",
            "performance e bottlenecks",
            "segurança (OWASP, autenticação, autorização)",
            "escalabilidade (consegue crescer?)",
            "manutenibilidade",
            "custo operacional",
            "trade-offs justificados"
        ]

        return enriched

    def _validate_review_output(self, output: AgentOutput) -> None:
        """
        Valida que a revisão contém elementos esperados.

        Args:
            output: Output do agente
        """
        required_fields = [
            "validation_status",
            "critical_issues",
            "concerns",
            "recommendations"
        ]

        output_data = output.output
        if isinstance(output_data, dict):
            for field in required_fields:
                if field not in output_data:
                    output_data[field] = None

    async def respond_to_debate(self, topic: str, positions: Dict[str, Any]) -> str:
        """
        Responde a debates com rigor crítico.

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

Como Revisor Técnico, como você responde?

Seja crítico mas construtivo. Procure:
1. Inconsistências nas posições
2. Riscos não mencionados
3. Trade-offs não justificados
4. Viabilidade real (não no papel)

Questione arbitrariedades. O que está errado?
        """

        response, tokens = await self.llm_provider.call(
            system_prompt=self.config.system_prompt,
            user_prompt=prompt,
            temperature=0.5
        )

        return response

    async def validate(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida qualquer proposta rigorosamente.

        Args:
            proposal: Proposta para validar

        Returns:
            Resultado da validação (crítico e detalhado)
        """
        prompt = f"""
PROPOSTA PARA VALIDAR RIGOROSAMENTE:

{json.dumps(proposal, indent=2, ensure_ascii=False)}

Como Revisor Técnico experiente, valide essa proposta.

Não aprove nada por padrão. Questione:
1. Coerência - faz sentido junto?
2. Completude - negligenciou algo crítico?
3. Realismo - é implementável?
4. Riscos - identifica os reais?
5. Segurança - está protegido?
6. Performance - vai ser rápido?
7. Escalabilidade - consegue crescer?
8. Custo - é economicamente viável?

Responda em JSON:
{
  "status": "approved|approved_with_concerns|rejected",
  "executive_summary": "Resumo executivo",
  "critical_issues": [
    {
      "issue": "Descrição",
      "severity": "critical|high|medium",
      "must_fix": true
    }
  ],
  "concerns": ["Preocupação 1"],
  "inconsistencies": ["Inconsistência 1"],
  "security_review": "Avaliação de segurança",
  "performance_assessment": "Avaliação de performance",
  "recommendations": ["Recomendação 1"],
  "approved_aspects": ["O que está bom"],
  "confidence": 0.8
}
        """

        response, tokens = await self.llm_provider.call(
            system_prompt=self.config.system_prompt,
            user_prompt=prompt,
            temperature=0.5
        )

        try:
            result = json.loads(response)
        except json.JSONDecodeError:
            result = {
                "status": "rejected",
                "issues": ["Parse error"],
                "recommendations": ["Reenviar com formato correto"]
            }

        return result

    def get_critical_issues(self) -> List[Dict[str, Any]]:
        """
        Retorna problemas críticos encontrados.

        Returns:
            Lista de problemas críticos
        """
        if not self.last_output:
            return []

        output = self.last_output.output
        if isinstance(output, dict):
            return output.get("critical_issues", [])

        return []

    def get_validation_status(self) -> str:
        """
        Retorna status da validação.

        Returns:
            Status (approved, approved_with_concerns, rejected)
        """
        if not self.last_output:
            return "unknown"

        output = self.last_output.output
        if isinstance(output, dict):
            return output.get("validation_status", "unknown")

        return "unknown"

    def has_blockers(self) -> bool:
        """
        Verifica se há bloqueadores críticos.

        Returns:
            True se há problemas críticos
        """
        critical_issues = self.get_critical_issues()
        return len(critical_issues) > 0

    def get_recommendations(self) -> List[str]:
        """
        Retorna recomendações de melhoria.

        Returns:
            Lista de recomendações
        """
        if not self.last_output:
            return []

        output = self.last_output.output
        if isinstance(output, dict):
            return output.get("recommendations", [])

        return []
