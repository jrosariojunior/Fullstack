"""
QAEngineer Agent - Especialista em testes e confiabilidade.

Responsável por estratégia de testes, identificação de edge cases
e garantia de qualidade.
"""

from backend.core.agent import Agent, AgentConfig, AgentOutput, SpecializedAgent
from backend.agents.prompts import get_agent_prompt
from typing import Any, Dict, List
import json


class QAEngineerAgent(SpecializedAgent):
    """
    Agente especialista em QA e testes.

    Define estratégia de testes, identifica cenários críticos,
    edge cases e garante confiabilidade do sistema.
    """

    def __init__(self, llm_provider: Any):
        """
        Inicializa o QAEngineer Agent.

        Args:
            llm_provider: Provider de LLM
        """
        prompt_data = get_agent_prompt("qa")

        config = AgentConfig(
            name="QAEngineer",
            persona=prompt_data["persona"],
            system_prompt=prompt_data["system_prompt"],
            description=prompt_data["description"],
            responsibilities=[
                "Definir estratégia de testes",
                "Identificar cenários críticos",
                "Especificar testes (unit, integração, e2e)",
                "Avaliar testabilidade do código",
                "Propor automação de testes",
                "Pensar em casos extremos e falhas"
            ],
            capabilities=prompt_data["capabilities"],
            temperature=0.65
        )

        super().__init__(config, llm_provider)

    async def analyze(self, briefing: Dict[str, Any], context: Dict[str, Any]) -> AgentOutput:
        """
        Analisa sistema e propõe estratégia de testes.

        Args:
            briefing: Descrição do problema
            context: Contexto compartilhado

        Returns:
            AgentOutput com estratégia de testes
        """
        # Enriquece briefing com análises anteriores
        enriched_briefing = self._enrich_briefing(briefing, context)

        # Chama implementação padrão
        output = await super().analyze(enriched_briefing, context)

        # Valida testing strategy output
        self._validate_testing_output(output)

        return output

    def _enrich_briefing(self, briefing: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enriquece briefing com arquitetura, plano e tech stack.

        Args:
            briefing: Briefing original
            context: Contexto compartilhado

        Returns:
            Briefing enriquecido
        """
        enriched = briefing.copy()

        # Extrai informações críticas para testes
        agents_output = context.get("agents_output", {})

        # Arquitetura crítica para testar
        if "Architect" in agents_output:
            arch = agents_output["Architect"]
            if isinstance(arch, dict):
                enriched["architecture"] = arch.get("output", {})
                enriched["critical_components"] = arch.get("output", {}).get("main_components", [])

        # Plano para entender escopo
        if "Analyst" in agents_output:
            plan = agents_output["Analyst"]
            if isinstance(plan, dict):
                enriched["phases"] = plan.get("output", {}).get("phases", [])

        # Tech stack para estratégia
        if "Developer" in agents_output:
            dev = agents_output["Developer"]
            if isinstance(dev, dict):
                enriched["tech_stack"] = dev.get("output", {}).get("tech_stack", {})

        # Riscos encontrados pelo Revisor
        if "TechReviewer" in agents_output:
            rev = agents_output["TechReviewer"]
            if isinstance(rev, dict):
                enriched["identified_risks"] = rev.get("output", {}).get("critical_issues", [])

        # Adiciona requisitos de testes
        enriched["test_priorities"] = [
            "Funcionalidade crítica",
            "Fluxos de erro",
            "Performance sob carga",
            "Segurança"
        ]

        return enriched

    def _validate_testing_output(self, output: AgentOutput) -> None:
        """
        Valida que a estratégia contém elementos esperados.

        Args:
            output: Output do agente
        """
        required_fields = [
            "testing_strategy",
            "test_pyramid",
            "critical_scenarios",
            "edge_cases",
            "failure_scenarios"
        ]

        output_data = output.output
        if isinstance(output_data, dict):
            for field in required_fields:
                if field not in output_data:
                    output_data[field] = None

    async def respond_to_debate(self, topic: str, positions: Dict[str, Any]) -> str:
        """
        Responde a debates sobre testes e confiabilidade.

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

Como Engenheiro de QA, como você responde?

Considere:
1. Testabilidade - consegue testar isso?
2. Riscos - que pode dar errado?
3. Confiabilidade - vai ser robusto?
4. Automação - pode ser automatizado?

Pense em casos extremos. Que cenários ninguém mencionou?
        """

        response, tokens = await self.llm_provider.call(
            system_prompt=self.config.system_prompt,
            user_prompt=prompt,
            temperature=0.65
        )

        return response

    async def validate(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida testabilidade de uma proposta.

        Args:
            proposal: Proposta para validar

        Returns:
            Resultado da validação
        """
        prompt = f"""
PROPOSTA PARA AVALIAR TESTABILIDADE:

{json.dumps(proposal, indent=2, ensure_ascii=False)}

Como QA Engineer experiente, valide essa proposta.

Verificar:
1. Testabilidade - dá pra testar fácil?
2. Riscos - que pode quebrar?
3. Edge cases - está cobrindo extremos?
4. Cenários de falha - preparado para erros?
5. Performance testing - testável?
6. Security testing - testável?
7. Automação - pode ser automatizado?
8. Coverage - qual seria a cobertura esperada?

Responda em JSON:
{
  "status": "approved|approved_with_concerns|rejected",
  "testability": "easy|medium|difficult",
  "identified_risks": ["Risco 1"],
  "missing_scenarios": ["Cenário não coberto"],
  "test_coverage_estimate": 85,
  "automation_potential": "high|medium|low",
  "critical_test_cases": ["Teste crítico 1"],
  "recommendations": ["Recomendação 1"],
  "confidence": 0.85
}
        """

        response, tokens = await self.llm_provider.call(
            system_prompt=self.config.system_prompt,
            user_prompt=prompt,
            temperature=0.65
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

    def get_testing_strategy(self) -> Dict[str, Any]:
        """
        Retorna estratégia de testes completa.

        Returns:
            Dict com estratégia
        """
        if not self.last_output:
            return {}

        output = self.last_output.output
        if isinstance(output, dict):
            return {
                "overall": output.get("testing_strategy"),
                "pyramid": output.get("test_pyramid"),
                "critical_scenarios": output.get("critical_scenarios", [])
            }

        return {}

    def get_critical_scenarios(self) -> List[Dict[str, Any]]:
        """
        Retorna cenários críticos que PRECISAM passar.

        Returns:
            Lista de cenários críticos
        """
        if not self.last_output:
            return []

        output = self.last_output.output
        if isinstance(output, dict):
            return output.get("critical_scenarios", [])

        return []

    def get_edge_cases(self) -> List[Dict[str, Any]]:
        """
        Retorna edge cases identificados.

        Returns:
            Lista de edge cases
        """
        if not self.last_output:
            return []

        output = self.last_output.output
        if isinstance(output, dict):
            return output.get("edge_cases", [])

        return []

    def get_coverage_estimate(self) -> int:
        """
        Retorna cobertura de testes estimada.

        Returns:
            Percentual estimado
        """
        if not self.last_output:
            return 0

        output = self.last_output.output
        if isinstance(output, dict):
            return output.get("estimated_coverage", 0)

        return 0

    def get_failure_scenarios(self) -> List[Dict[str, Any]]:
        """
        Retorna cenários de falha para testar.

        Returns:
            Lista de cenários
        """
        if not self.last_output:
            return []

        output = self.last_output.output
        if isinstance(output, dict):
            return output.get("failure_scenarios", [])

        return []
