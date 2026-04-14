"""
Developer Agent - Especialista em implementação prática.

Responsável por stack tecnológico, padrões de código
e viabilidade técnica da implementação.
"""

from backend.core.agent import Agent, AgentConfig, AgentOutput, SpecializedAgent
from backend.agents.prompts import get_agent_prompt
from typing import Any, Dict, List
import json


class DeveloperAgent(SpecializedAgent):
    """
    Agente especialista em desenvolvimento e implementação.

    Sugere stack tecnológico, padrões de código e
    pensa na IMPLEMENTAÇÃO REAL.
    """

    def __init__(self, llm_provider: Any):
        """
        Inicializa o Developer Agent.

        Args:
            llm_provider: Provider de LLM
        """
        prompt_data = get_agent_prompt("developer")

        config = AgentConfig(
            name="Developer",
            persona=prompt_data["persona"],
            system_prompt=prompt_data["system_prompt"],
            description=prompt_data["description"],
            responsibilities=[
                "Avaliar viabilidade técnica",
                "Sugerir stack tecnológico",
                "Propor padrões de código",
                "Identificar bibliotecas/frameworks",
                "Avisar sobre complexidade",
                "Sugerir otimizações viáveis"
            ],
            capabilities=prompt_data["capabilities"],
            temperature=0.7  # Um pouco mais criativo para gerar alternativas
        )

        super().__init__(config, llm_provider)

    async def analyze(self, briefing: Dict[str, Any], context: Dict[str, Any]) -> AgentOutput:
        """
        Analisa viabilidade técnica e propõe implementação.

        Args:
            briefing: Descrição do problema
            context: Contexto compartilhado

        Returns:
            AgentOutput com recomendações técnicas
        """
        # Enriquece com propostas anteriores
        enriched_briefing = self._enrich_briefing(briefing, context)

        # Chama implementação padrão
        output = await super().analyze(enriched_briefing, context)

        # Valida tech stack output
        self._validate_tech_output(output)

        return output

    def _enrich_briefing(self, briefing: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enriquece briefing com arquitetura e plano.

        Args:
            briefing: Briefing original
            context: Contexto compartilhado

        Returns:
            Briefing enriquecido
        """
        enriched = briefing.copy()

        # Extrai arquitetura proposta
        agents_output = context.get("agents_output", {})
        if "Architect" in agents_output:
            arch = agents_output["Architect"]
            if isinstance(arch, dict):
                enriched["architecture"] = arch.get("output", {}).get("architecture_type")

        # Extrai plano proposto
        if "Analyst" in agents_output:
            plan = agents_output["Analyst"]
            if isinstance(plan, dict):
                enriched["phases"] = plan.get("output", {}).get("phases")

        # Adiciona experiência com stacks similares
        if self.memory.long_term:
            enriched["proven_stacks"] = self.memory.long_term.get("successful_stacks", [])

        return enriched

    def _validate_tech_output(self, output: AgentOutput) -> None:
        """
        Valida que o output técnico contém elementos esperados.

        Args:
            output: Output do agente
        """
        required_fields = [
            "tech_stack",
            "implementation_strategy",
            "estimated_complexity",
            "potential_challenges"
        ]

        output_data = output.output
        if isinstance(output_data, dict):
            for field in required_fields:
                if field not in output_data:
                    output_data[field] = None

    async def respond_to_debate(self, topic: str, positions: Dict[str, Any]) -> str:
        """
        Responde a debates sobre implementação.

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

Como Desenvolvedor experiente, como você responde?

Considere:
1. Viabilidade de implementação
2. Stack tecnológico apropriado
3. Complexidade real vs estimada
4. Riscos de desenvolvimento
5. Performance possível

Seja prático. O que realmente consegue ser feito?
        """

        response, tokens = await self.llm_provider.call(
            system_prompt=self.config.system_prompt,
            user_prompt=prompt,
            temperature=0.7
        )

        return response

    async def validate(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida uma proposta de implementação.

        Args:
            proposal: Proposta para validar

        Returns:
            Resultado da validação
        """
        prompt = f"""
PROPOSTA DE IMPLEMENTAÇÃO PARA VALIDAR:

{json.dumps(proposal, indent=2, ensure_ascii=False)}

Como Desenvolvedor experiente, valide essa proposta.

Verificar:
1. Stack tecnológico - é apropriado?
2. Padrões de código - seguem boas práticas?
3. Performance - será rápido?
4. Testabilidade - dá pra testar fácil?
5. Complexidade - é realista?
6. Segurança - está protegido?

Responda em JSON:
{
  "status": "approved|approved_with_concerns|rejected",
  "tech_stack_assessment": "Avaliação",
  "complexity_realistic": true,
  "performance_concern": null,
  "testability": "good|fair|poor",
  "critical_issues": ["Problema 1"],
  "recommendations": ["Recomendação 1"],
  "alternative_approaches": ["Alternativa 1"],
  "confidence": 0.85
}
        """

        response, tokens = await self.llm_provider.call(
            system_prompt=self.config.system_prompt,
            user_prompt=prompt,
            temperature=0.7
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

    def get_tech_stack(self) -> Dict[str, Any]:
        """
        Retorna stack tecnológico recomendado.

        Returns:
            Dict com stack
        """
        if not self.last_output:
            return {}

        output = self.last_output.output
        if isinstance(output, dict):
            return output.get("tech_stack", {})

        return {}

    def get_implementation_strategy(self) -> str:
        """
        Retorna estratégia de implementação.

        Returns:
            String com estratégia
        """
        if not self.last_output:
            return ""

        output = self.last_output.output
        if isinstance(output, dict):
            return output.get("implementation_strategy", "")

        return ""

    def get_code_patterns(self) -> List[Dict[str, Any]]:
        """
        Retorna padrões de código recomendados.

        Returns:
            Lista de padrões
        """
        if not self.last_output:
            return []

        output = self.last_output.output
        if isinstance(output, dict):
            return output.get("code_patterns", [])

        return []

    def get_complexity_assessment(self) -> str:
        """
        Retorna avaliação de complexidade.

        Returns:
            Nível de complexidade
        """
        if not self.last_output:
            return "unknown"

        output = self.last_output.output
        if isinstance(output, dict):
            return output.get("estimated_complexity", "unknown")

        return "unknown"
