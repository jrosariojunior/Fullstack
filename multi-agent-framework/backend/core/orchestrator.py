"""
Orchestrator - Orquestrador principal do framework.

Coordena a execução de todos os agentes, facilita debate,
gerencia contexto e produz resultado final.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import asyncio
import json

from .agent import Agent, AgentOutput
from .context_manager import ContextManager
from .debate_engine import DebateEngine


class ExecutionPhase(Enum):
    """Fases de execução."""
    INITIALIZATION = "initialization"
    PARALLEL_ANALYSIS = "parallel_analysis"
    CONFLICT_DETECTION = "conflict_detection"
    DEBATE = "debate"
    SYNTHESIS = "synthesis"
    HUMANIZATION = "humanization"
    COMPLETION = "completion"


@dataclass
class ExecutionConfig:
    """Configuração de execução."""
    parallel: bool = True
    max_debate_rounds: int = 3
    token_limit: int = 100000
    timeout_seconds: int = 300
    humanize_output: bool = True


@dataclass
class ExecutionResult:
    """Resultado da execução."""
    execution_id: str
    status: str  # success, partial, failed
    briefing: Dict[str, Any]
    agents_results: Dict[str, AgentOutput] = field(default_factory=dict)
    debate_log: List[Dict[str, Any]] = field(default_factory=list)
    conflicts: List[Dict[str, Any]] = field(default_factory=list)
    final_output: Dict[str, Any] = field(default_factory=dict)
    execution_log: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    started_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    total_tokens_used: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Converte resultado para dicionário."""
        return {
            "execution_id": self.execution_id,
            "status": self.status,
            "briefing": self.briefing,
            "agents_results": {
                name: output.to_dict() if isinstance(output, AgentOutput) else output
                for name, output in self.agents_results.items()
            },
            "debate_log": self.debate_log,
            "conflicts": self.conflicts,
            "final_output": self.final_output,
            "execution_log": self.execution_log,
            "metadata": self.metadata,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "total_tokens_used": self.total_tokens_used
        }


class TeamOrchestrator:
    """
    Orquestrador principal do time de agentes.

    Coordena:
    - Inicialização e configuração
    - Execução paralela de agentes
    - Detecção de conflitos
    - Facilitação de debate
    - Síntese de resultados
    - Humanização de output
    """

    def __init__(
        self,
        agents: Dict[str, Agent],
        llm_provider: Any,
        config: ExecutionConfig = None
    ):
        """
        Inicializa o orquestrador.

        Args:
            agents: Dict de agentes {name: Agent}
            llm_provider: Provider de LLM
            config: Configuração de execução
        """
        self.agents = agents
        self.llm_provider = llm_provider
        self.config = config or ExecutionConfig()

        self.context_manager = ContextManager()
        self.debate_engine = DebateEngine(max_rounds=self.config.max_debate_rounds)

        self.current_phase: Optional[ExecutionPhase] = None
        self.execution_result: Optional[ExecutionResult] = None

    async def execute(
        self,
        briefing: Dict[str, Any],
        constraints: List[Dict[str, Any]] = None,
        preferences: Dict[str, Any] = None
    ) -> ExecutionResult:
        """
        Executa o time de agentes.

        Args:
            briefing: Descrição do problema
            constraints: Restrições
            preferences: Preferências do usuário

        Returns:
            ExecutionResult com análise completa
        """
        # Inicializa resultado
        execution_id = self.context_manager.initialize(briefing, constraints, preferences)
        self.execution_result = ExecutionResult(
            execution_id=execution_id,
            status="running",
            briefing=briefing
        )

        try:
            # Fase 1: Análise Paralela
            await self._phase_parallel_analysis()

            # Fase 2: Detecção de Conflitos
            await self._phase_conflict_detection()

            # Fase 3: Debate (se houver conflitos)
            if self.context_manager.get_unresolved_conflicts():
                await self._phase_debate()

            # Fase 4: Síntese
            await self._phase_synthesis()

            # Fase 5: Humanização
            await self._phase_humanization()

            # Completar
            self.execution_result.status = "success"
            self.execution_result.completed_at = datetime.utcnow()

        except Exception as e:
            self.execution_result.status = "failed"
            self.execution_result.metadata["error"] = str(e)
            print(f"Erro na execução: {e}")

        finally:
            # Finaliza
            self.execution_result.execution_log = self.context_manager.get_history()
            self.execution_result.total_tokens_used = self._count_tokens()

        return self.execution_result

    async def _phase_parallel_analysis(self) -> None:
        """Fase 1: Análise paralela dos agentes."""
        self.current_phase = ExecutionPhase.PARALLEL_ANALYSIS
        print("🔍 Iniciando análise paralela dos agentes...")

        # Atualiza status de todos os agentes
        for agent_name in self.agents:
            self.context_manager.update_agent_status(agent_name, "running")

        # Executa agentes em paralelo se configurado
        if self.config.parallel:
            tasks = []
            for agent_name, agent in self.agents.items():
                task = self._execute_agent(agent_name, agent)
                tasks.append(task)

            # Espera todos completarem (com timeout)
            try:
                await asyncio.wait_for(
                    asyncio.gather(*tasks),
                    timeout=self.config.timeout_seconds
                )
            except asyncio.TimeoutError:
                print("⚠️ Timeout na execução dos agentes")

        else:
            # Executa sequencial
            for agent_name, agent in self.agents.items():
                await self._execute_agent(agent_name, agent)

        # Marca agentes completados
        for agent_name in self.agents:
            if self.context_manager.agents_status.get(agent_name) == "running":
                self.context_manager.update_agent_status(agent_name, "completed")

    async def _execute_agent(self, agent_name: str, agent: Agent) -> None:
        """Executa um agente específico."""
        try:
            output = await agent.execute_analysis(
                self.context_manager.get_briefing(),
                self.context_manager.get_full_context()
            )

            self.context_manager.set_agent_output(agent_name, output.to_dict())
            self.execution_result.agents_results[agent_name] = output
            self.context_manager.update_agent_status(agent_name, "completed")

            print(f"✅ {agent_name} completado")

        except Exception as e:
            print(f"❌ Erro em {agent_name}: {e}")
            self.context_manager.update_agent_status(agent_name, "failed")

    async def _phase_conflict_detection(self) -> None:
        """Fase 2: Detecção de conflitos."""
        self.current_phase = ExecutionPhase.CONFLICT_DETECTION
        print("🔍 Detectando conflitos entre análises...")

        agent_outputs = self.context_manager.get_all_outputs()
        conflicts = await self.debate_engine.detect_conflicts(agent_outputs)

        if conflicts:
            print(f"⚠️ {len(conflicts)} conflito(s) detectado(s)")
            for conflict in conflicts:
                agents = conflict.get("agents", [])
                topic = conflict.get("topic", "Unknown")
                self.context_manager.add_conflict(agents, topic, conflict.get("positions", {}))
        else:
            print("✅ Nenhum conflito detectado")

        self.execution_result.conflicts = self.context_manager.context.conflicts

    async def _phase_debate(self) -> None:
        """Fase 3: Debate sobre conflitos."""
        self.current_phase = ExecutionPhase.DEBATE
        print("💬 Iniciando debate entre agentes...")

        unresolved = self.context_manager.get_unresolved_conflicts()

        for conflict in unresolved:
            print(f"  Debatendo: {conflict['topic']}")

            converged, resolution = await self.debate_engine.facilitate_debate(
                self.agents,
                self.context_manager,
                conflict
            )

            if converged:
                print(f"  ✅ Convergiram para: {resolution}")
                self.context_manager.resolve_conflict(conflict["id"], resolution)
            else:
                print(f"  ⚠️ Não convergiram após {self.debate_engine.current_round} rounds")
                # Escalaria para usuário aqui em produção

    async def _phase_synthesis(self) -> None:
        """Fase 4: Síntese dos resultados."""
        self.current_phase = ExecutionPhase.SYNTHESIS
        print("📊 Sintetizando resultados...")

        # Consolida outputs dos agentes
        final_output = {
            "timestamp": datetime.utcnow().isoformat(),
            "agents": {},
            "synthesis": {},
            "recommendations": []
        }

        for agent_name, output in self.execution_result.agents_results.items():
            if isinstance(output, AgentOutput):
                final_output["agents"][agent_name] = output.output
            else:
                final_output["agents"][agent_name] = output

        # Gera síntese (em produção, isso seria mais sofisticado)
        final_output["synthesis"] = self._synthesize_outputs(final_output["agents"])

        self.context_manager.mark_complete(final_output)
        self.execution_result.final_output = final_output

    def _synthesize_outputs(self, agents_output: Dict[str, Any]) -> Dict[str, Any]:
        """Sintetiza outputs dos agentes em insights principais."""
        synthesis = {
            "key_findings": [],
            "risks_identified": [],
            "recommendations": []
        }

        for agent_name, output in agents_output.items():
            if isinstance(output, dict):
                # Extrai insights principais
                if "recommendation" in output:
                    synthesis["recommendations"].append(output["recommendation"])
                if "risks" in output:
                    synthesis["risks_identified"].extend(output["risks"])

        return synthesis

    async def _phase_humanization(self) -> None:
        """Fase 5: Humanização do output."""
        self.current_phase = ExecutionPhase.HUMANIZATION
        print("✍️ Humanizando output...")

        if self.config.humanize_output and self.llm_provider:
            # Em produção, chamaria o humanizer aqui
            pass

    def _count_tokens(self) -> int:
        """Conta tokens totais usados."""
        total = 0
        for output in self.execution_result.agents_results.values():
            if isinstance(output, AgentOutput):
                total += output.tokens_used
        return total

    def get_result(self) -> Optional[ExecutionResult]:
        """Retorna resultado da última execução."""
        return self.execution_result

    def get_status(self) -> Dict[str, Any]:
        """Retorna status atual."""
        if not self.execution_result:
            return {"status": "idle"}

        return {
            "status": self.execution_result.status,
            "phase": self.current_phase.value if self.current_phase else None,
            "execution_id": self.execution_result.execution_id,
            "agents_completed": sum(
                1 for s in self.context_manager.context.agents_status.values()
                if s == "completed"
            ),
            "total_agents": len(self.agents),
            "conflicts_detected": self.context_manager.get_conflict_count()
        }
