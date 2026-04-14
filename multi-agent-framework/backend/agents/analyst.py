"""
Analyst Agent - Especialista em planejamento e estruturação.

Responsável por quebrar projetos em fases, priorizar requisitos
e criar roadmaps realistas.
"""

from backend.core.agent import Agent, AgentConfig, AgentOutput, SpecializedAgent
from backend.agents.prompts import get_agent_prompt
from typing import Any, Dict, List
import json


class AnalystAgent(SpecializedAgent):
    """
    Agente especialista em análise e planejamento.

    Quebra projetos complexos em fases gerenciáveis,
    prioriza requisitos e cria planos realistas.
    """

    def __init__(self, llm_provider: Any):
        """
        Inicializa o Analyst Agent.

        Args:
            llm_provider: Provider de LLM
        """
        prompt_data = get_agent_prompt("analyst")

        config = AgentConfig(
            name="Analyst",
            persona=prompt_data["persona"],
            system_prompt=prompt_data["system_prompt"],
            description=prompt_data["description"],
            responsibilities=[
                "Estruturar requisitos do briefing",
                "Quebrar projeto em fases",
                "Identificar dependências entre tarefas",
                "Criar timeline e milestones",
                "Priorizar funcionalidades (MoSCoW)",
                "Estimar esforço e complexidade"
            ],
            capabilities=prompt_data["capabilities"],
            temperature=0.6
        )

        super().__init__(config, llm_provider)

    async def analyze(self, briefing: Dict[str, Any], context: Dict[str, Any]) -> AgentOutput:
        """
        Analisa briefing e cria plano de projeto.

        Args:
            briefing: Descrição do problema
            context: Contexto compartilhado (inclui arquitetura do Architect)

        Returns:
            AgentOutput com plano estruturado
        """
        # Enriquece briefing com análises anteriores
        enriched_briefing = self._enrich_briefing(briefing, context)

        # Chama implementação padrão
        output = await super().analyze(enriched_briefing, context)

        # Valida plan output
        self._validate_plan_output(output)

        return output

    def _enrich_briefing(self, briefing: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enriquece briefing com arquitetura proposta e contexto.

        Args:
            briefing: Briefing original
            context: Contexto compartilhado

        Returns:
            Briefing enriquecido
        """
        enriched = briefing.copy()

        # Extrai arquitetura do Architect (se disponível)
        agents_output = context.get("agents_output", {})
        if "Architect" in agents_output:
            arch_output = agents_output["Architect"]
            if isinstance(arch_output, dict):
                enriched["proposed_architecture"] = arch_output.get("output", {})

        # Adiciona preferências de timeline
        enriched["timeline_preference"] = briefing.get("constraints", {})

        # Histórico de velocidade
        if self.memory.long_term:
            enriched["team_velocity"] = self.memory.long_term.get("avg_velocity")

        return enriched

    def _validate_plan_output(self, output: AgentOutput) -> None:
        """
        Valida que o plan contém elementos esperados.

        Args:
            output: Output do agente
        """
        required_fields = [
            "requirements_breakdown",
            "phases",
            "critical_path",
            "total_estimated_weeks"
        ]

        output_data = output.output
        if isinstance(output_data, dict):
            for field in required_fields:
                if field not in output_data:
                    output_data[field] = None

    async def respond_to_debate(self, topic: str, positions: Dict[str, Any]) -> str:
        """
        Responde a debates sobre planejamento.

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

Como Analista, como você responde?

Considere:
1. Viabilidade de cronograma
2. Dependências reais
3. Estimativas realistas
4. Riscos de planejamento

Seja prático e baseie-se em experiência real com projetos similares.
        """

        response, tokens = await self.llm_provider.call(
            system_prompt=self.config.system_prompt,
            user_prompt=prompt,
            temperature=0.6
        )

        return response

    async def validate(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida um plano proposto.

        Args:
            proposal: Plano para validar

        Returns:
            Resultado da validação
        """
        prompt = f"""
PLANO PARA VALIDAR:

{json.dumps(proposal, indent=2, ensure_ascii=False)}

Como Analista experiente, valide esse plano.

Verificar:
1. Realismo das estimativas
2. Dependências - estão certas?
3. Caminho crítico - identificado corretamente?
4. Riscos de planejamento - negligenciou algo?
5. Paralelização - pode ser mais eficiente?
6. Timeline - é executável?

Responda em JSON:
{
  "status": "approved|approved_with_concerns|rejected",
  "realistic": true,
  "critical_issues": ["Problema 1"],
  "recommendations": ["Recomendação 1"],
  "suggested_optimizations": ["Otimização 1"],
  "confidence": 0.85
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
                "issues": ["Parse error"],
                "recommendations": []
            }

        return result

    def get_phases(self) -> List[Dict[str, Any]]:
        """
        Retorna fases do plano.

        Returns:
            Lista de fases
        """
        if not self.last_output:
            return []

        output = self.last_output.output
        if isinstance(output, dict):
            return output.get("phases", [])

        return []

    def get_critical_path(self) -> List[str]:
        """
        Retorna caminho crítico do projeto.

        Returns:
            Lista de tarefas no caminho crítico
        """
        if not self.last_output:
            return []

        output = self.last_output.output
        if isinstance(output, dict):
            return output.get("critical_path", [])

        return []

    def estimate_duration(self) -> float:
        """
        Retorna estimativa de duração total do projeto.

        Returns:
            Semanas estimadas
        """
        if not self.last_output:
            return 0

        output = self.last_output.output
        if isinstance(output, dict):
            return output.get("total_estimated_weeks", 0)

        return 0
