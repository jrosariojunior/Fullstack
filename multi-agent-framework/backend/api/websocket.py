"""
WebSocket - Gerenciador de conexões WebSocket para real-time updates.

Permite que clientes se conectem e recebam atualizações em tempo real
conforme a execução progride.
"""

import json
import asyncio
from typing import Set, Dict, Any, Optional
from datetime import datetime
from fastapi import WebSocket, WebSocketDisconnect, status
from dataclasses import dataclass, asdict


@dataclass
class WSMessage:
    """Mensagem de WebSocket."""
    type: str  # progress, agent_update, debate, complete, error
    execution_id: str
    data: Dict[str, Any]
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()

    def to_json(self) -> str:
        """Converte para JSON string."""
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        return json.dumps(data)

    @classmethod
    def from_json(cls, json_str: str) -> "WSMessage":
        """Cria a partir de JSON string."""
        data = json.loads(json_str)
        timestamp = datetime.fromisoformat(data.pop("timestamp"))
        return cls(**data, timestamp=timestamp)


class ConnectionManager:
    """
    Gerencia conexões WebSocket.

    Mantém conexões ativas, envia broadcasts e gerencia desconexões.
    """

    def __init__(self):
        """Inicializa manager."""
        # connections[execution_id] = {websocket, ...}
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self.client_info: Dict[WebSocket, Dict[str, Any]] = {}

    async def connect(self, websocket: WebSocket, execution_id: str) -> None:
        """
        Aceita nova conexão WebSocket.

        Args:
            websocket: Conexão WebSocket
            execution_id: ID da execução sendo monitorada
        """
        await websocket.accept()

        # Inicializa set para essa execução se não existir
        if execution_id not in self.active_connections:
            self.active_connections[execution_id] = set()

        # Adiciona conexão
        self.active_connections[execution_id].add(websocket)

        # Registra informações do cliente
        self.client_info[websocket] = {
            "execution_id": execution_id,
            "connected_at": datetime.utcnow().isoformat(),
            "last_heartbeat": datetime.utcnow()
        }

        print(f"✅ Cliente conectado para {execution_id}")

    async def disconnect(self, websocket: WebSocket, execution_id: str) -> None:
        """
        Remove conexão desconectada.

        Args:
            websocket: Conexão WebSocket
            execution_id: ID da execução
        """
        if execution_id in self.active_connections:
            self.active_connections[execution_id].discard(websocket)

            # Se nenhuma conexão reste, remove execução
            if not self.active_connections[execution_id]:
                del self.active_connections[execution_id]

        # Remove informações do cliente
        self.client_info.pop(websocket, None)

        print(f"❌ Cliente desconectado de {execution_id}")

    async def send_personal(self, websocket: WebSocket, message: WSMessage) -> None:
        """
        Envia mensagem para um cliente específico.

        Args:
            websocket: Conexão WebSocket
            message: Mensagem para enviar
        """
        try:
            await websocket.send_text(message.to_json())
        except Exception as e:
            print(f"⚠️ Erro ao enviar mensagem pessoal: {str(e)}")

    async def broadcast(self, execution_id: str, message: WSMessage) -> None:
        """
        Envia mensagem para todos os clientes de uma execução.

        Args:
            execution_id: ID da execução
            message: Mensagem para enviar
        """
        if execution_id not in self.active_connections:
            return

        disconnected = []

        for websocket in self.active_connections[execution_id]:
            try:
                await websocket.send_text(message.to_json())
            except Exception as e:
                print(f"⚠️ Erro ao fazer broadcast: {str(e)}")
                disconnected.append(websocket)

        # Remove conexões que falharam
        for websocket in disconnected:
            await self.disconnect(websocket, execution_id)

    async def send_progress(
        self,
        execution_id: str,
        phase: str,
        percentage: int,
        message: str
    ) -> None:
        """
        Envia atualização de progresso.

        Args:
            execution_id: ID da execução
            phase: Fase atual
            percentage: Percentual de conclusão
            message: Mensagem descritiva
        """
        msg = WSMessage(
            type="progress",
            execution_id=execution_id,
            data={
                "phase": phase,
                "percentage": percentage,
                "message": message
            }
        )
        await self.broadcast(execution_id, msg)

    async def send_agent_update(
        self,
        execution_id: str,
        agent_name: str,
        status: str,
        output: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Envia atualização de agente.

        Args:
            execution_id: ID da execução
            agent_name: Nome do agente
            status: Status (running, completed, failed)
            output: Output do agente (opcional)
        """
        msg = WSMessage(
            type="agent_update",
            execution_id=execution_id,
            data={
                "agent_name": agent_name,
                "status": status,
                "output": output,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        await self.broadcast(execution_id, msg)

    async def send_debate(
        self,
        execution_id: str,
        round_num: int,
        topic: str,
        positions: Dict[str, str],
        resolution: Optional[str] = None
    ) -> None:
        """
        Envia atualização de debate.

        Args:
            execution_id: ID da execução
            round_num: Número do round
            topic: Tópico do debate
            positions: Posições dos agentes
            resolution: Resolução (se houver)
        """
        msg = WSMessage(
            type="debate",
            execution_id=execution_id,
            data={
                "round": round_num,
                "topic": topic,
                "positions": positions,
                "resolution": resolution,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        await self.broadcast(execution_id, msg)

    async def send_completion(
        self,
        execution_id: str,
        status: str,
        final_output: Dict[str, Any],
        total_tokens: int
    ) -> None:
        """
        Envia notificação de conclusão.

        Args:
            execution_id: ID da execução
            status: Status final (completed, failed)
            final_output: Output final
            total_tokens: Total de tokens
        """
        msg = WSMessage(
            type="complete",
            execution_id=execution_id,
            data={
                "status": status,
                "final_output": final_output,
                "total_tokens": total_tokens,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        await self.broadcast(execution_id, msg)

    async def send_error(
        self,
        execution_id: str,
        error: str,
        details: Optional[str] = None
    ) -> None:
        """
        Envia notificação de erro.

        Args:
            execution_id: ID da execução
            error: Mensagem de erro
            details: Detalhes adicionais
        """
        msg = WSMessage(
            type="error",
            execution_id=execution_id,
            data={
                "error": error,
                "details": details,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        await self.broadcast(execution_id, msg)

    async def send_heartbeat(self, execution_id: str) -> None:
        """
        Envia heartbeat para manter conexão viva.

        Args:
            execution_id: ID da execução
        """
        msg = WSMessage(
            type="heartbeat",
            execution_id=execution_id,
            data={"timestamp": datetime.utcnow().isoformat()}
        )
        await self.broadcast(execution_id, msg)

    def get_connection_count(self, execution_id: str) -> int:
        """Retorna número de conexões para execução."""
        return len(self.active_connections.get(execution_id, set()))

    def get_active_executions(self) -> list:
        """Retorna lista de execuções com conexões ativas."""
        return list(self.active_connections.keys())

    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de conexões."""
        total_connections = sum(len(conns) for conns in self.active_connections.values())

        return {
            "active_executions": len(self.active_connections),
            "total_connections": total_connections,
            "connections_by_execution": {
                exec_id: len(conns)
                for exec_id, conns in self.active_connections.items()
            }
        }


async def websocket_endpoint(
    websocket: WebSocket,
    execution_id: str,
    manager: ConnectionManager,
    storage = None
) -> None:
    """
    Handler do endpoint WebSocket.

    Args:
        websocket: Conexão WebSocket
        execution_id: ID da execução
        manager: Gerenciador de conexões
        storage: StorageManager
    """
    await manager.connect(websocket, execution_id)

    try:
        # Envia status inicial
        if storage:
            execution = await storage.get_execution(execution_id)
            if execution:
                initial_msg = WSMessage(
                    type="initial",
                    execution_id=execution_id,
                    data={
                        "status": execution.get("status"),
                        "message": f"Conectado à execução {execution_id}"
                    }
                )
                await manager.send_personal(websocket, initial_msg)

        # Loop para receber mensagens do cliente
        while True:
            data = await websocket.receive_text()

            try:
                # Parseia mensagem do cliente
                msg_data = json.loads(data)
                msg_type = msg_data.get("type")

                # Processa baseado no tipo
                if msg_type == "ping":
                    # Cliente enviou ping, responde com pong
                    pong_msg = WSMessage(
                        type="pong",
                        execution_id=execution_id,
                        data={"timestamp": datetime.utcnow().isoformat()}
                    )
                    await manager.send_personal(websocket, pong_msg)

                elif msg_type == "get_status":
                    # Cliente quer status atual
                    if storage:
                        status_data = await storage.get_status(execution_id)
                        status_msg = WSMessage(
                            type="status",
                            execution_id=execution_id,
                            data=status_data
                        )
                        await manager.send_personal(websocket, status_msg)

            except json.JSONDecodeError:
                # Mensagem inválida, ignora
                pass

    except WebSocketDisconnect:
        # Cliente desconectou
        await manager.disconnect(websocket, execution_id)

    except Exception as e:
        print(f"❌ Erro em WebSocket: {str(e)}")
        await manager.disconnect(websocket, execution_id)
