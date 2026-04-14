"""
DebateEngine - Motor de debate entre agentes.

Coordena discussão entre agentes sobre tópicos conflitantes,
facilita convergência e escala para usuário se necessário.
"""

from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class DebateRound:
    """Uma rodada de debate."""

    round_number: int
    topic: str
    participants: List[str]
    positions: Dict[str, str]  # {agent_name: position}
    timestamp: datetime
    convergence_detected: bool = False
    resolution: Optional[str] = None


class DebateEngine:
    """
    Motor de debate entre agentes.

    Responsabilidades:
    - Detectar conflitos nas análises dos agentes
    - Organizar debate estruturado
    - Contar rounds e aplicar limite (máx 3)
    - Detectar convergência
    - Escalar para usuário se não convergir
    """

    def __init__(self, max_rounds: int = 3):
        """
        Inicializa o motor de debate.

        Args:
            max_rounds: Número máximo de rounds de debate
        """
        self.max_rounds = max_rounds
        self.debate_history: List[DebateRound] = []
        self.current_round = 0

    async def detect_conflicts(self, agent_outputs: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Detecta conflitos entre outputs dos agentes.

        Analisa as saídas e identifica posições contraditórias ou inconsistentes.

        Args:
            agent_outputs: {agent_name: output_dict}

        Returns:
            Lista de conflitos detectados
        """
        conflicts = []

        # Extrai posições principais de cada agente
        positions = self._extract_positions(agent_outputs)

        # Detecta contradições
        contradictions = self._find_contradictions(positions)
        conflicts.extend(contradictions)

        # Detecta inconsistências
        inconsistencies = self._find_inconsistencies(agent_outputs)
        conflicts.extend(inconsistencies)

        return conflicts

    def _extract_positions(self, outputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extrai posições principais de cada agente.

        Args:
            outputs: Outputs dos agentes

        Returns:
            Dict com posições principais
        """
        positions = {}

        for agent_name, output in outputs.items():
            # Tenta extrair a "posição" principal
            if isinstance(output, dict):
                # Procura por campo que indique posição
                if "architecture_type" in output:
                    positions[agent_name] = output.get("architecture_type")
                elif "recommendation" in output:
                    positions[agent_name] = output.get("recommendation")
                elif "decision" in output:
                    positions[agent_name] = output.get("decision")
                else:
                    # Pega primeira key importante
                    for key in ["proposed", "analysis", "plan"]:
                        if key in output:
                            positions[agent_name] = output[key]
                            break

        return positions

    def _find_contradictions(self, positions: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Encontra contradições entre posições.

        Args:
            positions: Posições dos agentes

        Returns:
            Lista de contradições
        """
        contradictions = []

        # Agrupa agentes por tipo de posição
        position_groups = {}
        for agent, position in positions.items():
            if position:
                pos_key = str(position)
                if pos_key not in position_groups:
                    position_groups[pos_key] = []
                position_groups[pos_key].append(agent)

        # Se há 2+ grupos diferentes, há contradição
        if len(position_groups) > 1:
            for pos_key, agents in position_groups.items():
                if len(agents) == 1:  # Agente sozinho em posição
                    conflicting_agents = [a for g in position_groups.values() for a in g if a != agents[0]]
                    contradictions.append({
                        "type": "contradiction",
                        "topic": f"Position disagreement: {pos_key}",
                        "agents": [agents[0]] + conflicting_agents[:2],  # Pega 3 agentes
                        "positions": {a: pos_key for a in [agents[0]] + conflicting_agents[:2]},
                        "severity": "high" if len(agents) == 1 else "medium"
                    })

        return contradictions

    def _find_inconsistencies(self, outputs: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Encontra inconsistências nos outputs.

        Args:
            outputs: Outputs dos agentes

        Returns:
            Lista de inconsistências
        """
        inconsistencies = []

        # Procura por campos conflitantes
        for agent1_name, output1 in outputs.items():
            for agent2_name, output2 in outputs.items():
                if agent1_name >= agent2_name:
                    continue

                if isinstance(output1, dict) and isinstance(output2, dict):
                    # Compara campos críticos
                    if "risks" in output1 and "risks" in output2:
                        # Se um agente detecta riscos que o outro ignora
                        risks1 = set(str(r) for r in output1.get("risks", []))
                        risks2 = set(str(r) for r in output2.get("risks", []))

                        if risks1 != risks2:
                            inconsistencies.append({
                                "type": "risk_assessment_mismatch",
                                "agents": [agent1_name, agent2_name],
                                "severity": "medium"
                            })

        return inconsistencies

    async def facilitate_debate(
        self,
        agents: Dict[str, Any],
        context_manager: Any,
        conflict: Dict[str, Any]
    ) -> Tuple[bool, Optional[str]]:
        """
        Facilita debate sobre um conflito.

        Args:
            agents: Dict de agentes disponíveis
            context_manager: Gerenciador de contexto
            conflict: Conflito a debater

        Returns:
            (converged, resolution) - True se convergiu, string de resolução
        """
        topic = conflict.get("topic", "Unknown")
        involved_agents = conflict.get("agents", [])

        # Inicia novo round
        self.current_round += 1
        context_manager.start_debate_round()

        if self.current_round > self.max_rounds:
            return False, None  # Não convergiu

        # Coleta posições dos agentes envolvidos
        positions = {}
        for agent_name in involved_agents:
            if agent_name in agents:
                agent = agents[agent_name]
                position = await agent.respond_to_debate(topic, positions)
                positions[agent_name] = position
                context_manager.add_debate_position(agent_name, position, topic)

        # Detecta convergência
        converged = self._check_convergence(positions)

        if converged:
            # Sintetiza resolução
            resolution = self._synthesize_resolution(positions, involved_agents)
            return True, resolution

        if self.current_round >= self.max_rounds:
            # Atingiu limite, precisa de decisão do usuário
            return False, None

        # Continua debate (recursivo)
        return await self.facilitate_debate(agents, context_manager, conflict)

    def _check_convergence(self, positions: Dict[str, str]) -> bool:
        """
        Verifica se há convergência nas posições.

        Args:
            positions: Posições dos agentes

        Returns:
            True se convergiu
        """
        if not positions:
            return False

        # Remove posições muito diferentes
        unique_positions = set(positions.values())

        # Convergência = todos falam a mesma coisa (permitindo pequenas variações)
        if len(unique_positions) == 1:
            return True

        # Se houver apenas 2 posições e elas são complementares, também é convergência
        if len(unique_positions) == 2:
            # Aqui poderia haver lógica mais sofisticada
            # Por agora, assumimos que 2+ posições diferentes = sem convergência
            pass

        return False

    def _synthesize_resolution(self, positions: Dict[str, str], agents: List[str]) -> str:
        """
        Sintetiza resolução baseada nas posições.

        Args:
            positions: Posições dos agentes
            agents: Nomes dos agentes

        Returns:
            String com resolução sintetizada
        """
        # Se todos concordam
        unique_pos = set(positions.values())
        if len(unique_pos) == 1:
            return list(unique_pos)[0]

        # Se não, cria síntese
        return f"Síntese de múltiplas perspectivas: {', '.join(unique_pos)}"

    def get_debate_status(self) -> Dict[str, Any]:
        """Retorna status atual do debate."""
        return {
            "current_round": self.current_round,
            "max_rounds": self.max_rounds,
            "rounds_remaining": max(0, self.max_rounds - self.current_round),
            "total_debates": len(self.debate_history),
            "can_continue": self.current_round < self.max_rounds
        }

    def reset(self) -> None:
        """Reseta engine para novo debate."""
        self.debate_history = []
        self.current_round = 0

    def export_debate_log(self) -> str:
        """Exporta log de debates em JSON."""
        log_data = {
            "total_rounds": self.current_round,
            "max_rounds": self.max_rounds,
            "debates": [
                {
                    "round": d.round_number,
                    "topic": d.topic,
                    "participants": d.participants,
                    "positions": d.positions,
                    "converged": d.convergence_detected,
                    "resolution": d.resolution
                }
                for d in self.debate_history
            ]
        }

        return json.dumps(log_data, indent=2, ensure_ascii=False, default=str)
