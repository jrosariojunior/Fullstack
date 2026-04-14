"""
ContextManager - Gerencia contexto compartilhado entre agentes.

Mantém o estado da execução, outputs de agentes e facilita
comunicação entre eles.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4
import json


@dataclass
class ExecutionContext:
    """Contexto compartilhado de uma execução."""

    execution_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)
    briefing: Dict[str, Any] = field(default_factory=dict)
    constraints: List[Dict[str, Any]] = field(default_factory=list)
    preferences: Dict[str, Any] = field(default_factory=dict)

    # Estado dos agentes
    agents_status: Dict[str, str] = field(default_factory=dict)  # {agent_name: status}
    agents_output: Dict[str, Any] = field(default_factory=dict)  # {agent_name: output}

    # Debate e conflitos
    debate_rounds: List[Dict[str, Any]] = field(default_factory=list)
    conflicts: List[Dict[str, Any]] = field(default_factory=list)
    current_debate_round: int = 0

    # Memória compartilhada
    shared_memory: Dict[str, Any] = field(default_factory=dict)

    # Resultado final
    final_output: Optional[Dict[str, Any]] = None
    is_complete: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Converte contexto para dicionário."""
        return {
            "execution_id": self.execution_id,
            "created_at": self.created_at.isoformat(),
            "briefing": self.briefing,
            "constraints": self.constraints,
            "preferences": self.preferences,
            "agents_status": self.agents_status,
            "agents_output": self.agents_output,
            "debate_rounds": self.debate_rounds,
            "conflicts": self.conflicts,
            "current_debate_round": self.current_debate_round,
            "shared_memory": self.shared_memory,
            "final_output": self.final_output,
            "is_complete": self.is_complete
        }


class ContextManager:
    """
    Gerenciador de contexto compartilhado entre agentes.

    Responsabilidades:
    - Manter estado da execução
    - Gerenciar outputs dos agentes
    - Facilitar acesso a informações compartilhadas
    - Registrar debates e conflitos
    """

    def __init__(self):
        self.context = ExecutionContext()
        self.history: List[str] = []  # Log de eventos

    def initialize(self, briefing: Dict[str, Any], constraints: List[Dict[str, Any]] = None,
                   preferences: Dict[str, Any] = None) -> str:
        """
        Inicializa um novo contexto de execução.

        Args:
            briefing: Descrição do problema
            constraints: Restrições técnicas/orçamentárias
            preferences: Preferências do usuário

        Returns:
            execution_id
        """
        self.context = ExecutionContext(
            briefing=briefing,
            constraints=constraints or [],
            preferences=preferences or {}
        )

        self._log(f"Execução inicializada: {self.context.execution_id}")
        return self.context.execution_id

    def update_agent_status(self, agent_name: str, status: str) -> None:
        """
        Atualiza status de um agente.

        Args:
            agent_name: Nome do agente
            status: Novo status (pending, running, completed, failed)
        """
        self.context.agents_status[agent_name] = status
        self._log(f"Status atualizado: {agent_name} → {status}")

    def set_agent_output(self, agent_name: str, output: Any) -> None:
        """
        Define output de um agente.

        Args:
            agent_name: Nome do agente
            output: Output estruturado
        """
        self.context.agents_output[agent_name] = output
        self._log(f"Output recebido de {agent_name}")

    def get_agent_output(self, agent_name: str) -> Optional[Any]:
        """Recupera output de um agente."""
        return self.context.agents_output.get(agent_name)

    def get_all_outputs(self) -> Dict[str, Any]:
        """Retorna todos os outputs dos agentes."""
        return self.context.agents_output.copy()

    def get_briefing(self) -> Dict[str, Any]:
        """Retorna briefing."""
        return self.context.briefing.copy()

    def add_to_shared_memory(self, key: str, value: Any) -> None:
        """
        Adiciona informação à memória compartilhada.

        Args:
            key: Chave
            value: Valor
        """
        self.context.shared_memory[key] = value
        self._log(f"Memória compartilhada atualizada: {key}")

    def get_from_shared_memory(self, key: str, default: Any = None) -> Any:
        """Recupera informação da memória compartilhada."""
        return self.context.shared_memory.get(key, default)

    def add_conflict(self, agents: List[str], topic: str, positions: Dict[str, Any]) -> None:
        """
        Registra um conflito entre agentes.

        Args:
            agents: Lista de nomes de agentes envolvidos
            topic: Tópico do conflito
            positions: Posições de cada agente
        """
        conflict = {
            "id": str(uuid4()),
            "agents": agents,
            "topic": topic,
            "positions": positions,
            "timestamp": datetime.utcnow().isoformat(),
            "resolved": False,
            "resolution": None
        }

        self.context.conflicts.append(conflict)
        self._log(f"Conflito detectado: {topic} (agentes: {', '.join(agents)})")

    def resolve_conflict(self, conflict_id: str, resolution: str) -> None:
        """
        Marca conflito como resolvido.

        Args:
            conflict_id: ID do conflito
            resolution: Resolução escolhida
        """
        for conflict in self.context.conflicts:
            if conflict["id"] == conflict_id:
                conflict["resolved"] = True
                conflict["resolution"] = resolution
                self._log(f"Conflito resolvido: {conflict['topic']}")
                break

    def start_debate_round(self) -> None:
        """Inicia novo round de debate."""
        self.context.current_debate_round += 1
        self._log(f"Debate round {self.context.current_debate_round} iniciado")

    def add_debate_position(self, agent_name: str, position: str, topic: str) -> None:
        """
        Adiciona posição de agente ao debate.

        Args:
            agent_name: Nome do agente
            position: Posição/argumentação
            topic: Tópico do debate
        """
        debate_entry = {
            "round": self.context.current_debate_round,
            "agent": agent_name,
            "position": position,
            "topic": topic,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.context.debate_rounds.append(debate_entry)
        self._log(f"{agent_name} posicionou-se no debate")

    def get_debate_history(self, round_num: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Retorna histórico de debate.

        Args:
            round_num: Round específico (None = todos)

        Returns:
            Lista de debate entries
        """
        if round_num is None:
            return self.context.debate_rounds.copy()

        return [d for d in self.context.debate_rounds if d["round"] == round_num]

    def get_conflict_count(self) -> int:
        """Retorna número total de conflitos."""
        return len(self.context.conflicts)

    def get_unresolved_conflicts(self) -> List[Dict[str, Any]]:
        """Retorna conflitos não resolvidos."""
        return [c for c in self.context.conflicts if not c.get("resolved")]

    def mark_complete(self, final_output: Dict[str, Any]) -> None:
        """
        Marca execução como completa.

        Args:
            final_output: Output final consolidado
        """
        self.context.final_output = final_output
        self.context.is_complete = True
        self._log("Execução concluída")

    def get_context_summary(self) -> Dict[str, Any]:
        """Retorna resumo do contexto."""
        return {
            "execution_id": self.context.execution_id,
            "agents_completed": sum(1 for s in self.context.agents_status.values() if s == "completed"),
            "total_agents": len(self.context.agents_status),
            "conflicts_detected": self.get_conflict_count(),
            "conflicts_resolved": sum(1 for c in self.context.conflicts if c.get("resolved")),
            "debate_rounds": self.context.current_debate_round,
            "is_complete": self.context.is_complete
        }

    def get_full_context(self) -> Dict[str, Any]:
        """Retorna contexto completo."""
        return self.context.to_dict()

    def _log(self, message: str) -> None:
        """Registra evento no histórico."""
        timestamp = datetime.utcnow().isoformat()
        log_entry = f"[{timestamp}] {message}"
        self.history.append(log_entry)

    def get_history(self) -> List[str]:
        """Retorna histórico de eventos."""
        return self.history.copy()

    def export_to_json(self) -> str:
        """Exporta contexto para JSON."""
        return json.dumps(self.get_full_context(), indent=2, ensure_ascii=False, default=str)

    def export_to_file(self, filepath: str) -> None:
        """Exporta contexto para arquivo JSON."""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.export_to_json())
