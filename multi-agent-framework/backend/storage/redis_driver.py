"""
Redis Driver - Camada de cache e memória de curto prazo.

Armazena contexto de execução, estado dos agentes,
contadores de tokens e sessões em tempo real.
"""

import json
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta


class RedisDriver:
    """
    Driver para Redis.

    Gerencia cache, contexto de execução e memória de curto prazo.
    """

    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        """
        Inicializa driver Redis.

        Args:
            redis_url: URL de conexão (redis://host:port/db)
        """
        self.redis_url = redis_url
        self.client = None
        self.async_client = None

    async def initialize(self) -> None:
        """Inicializa conexão com Redis."""
        try:
            import redis.asyncio as redis
            self.async_client = await redis.from_url(self.redis_url, decode_responses=True)
            await self.async_client.ping()  # Testa conexão
        except ImportError:
            raise Exception("Biblioteca 'redis' não instalada. Instale com: pip install redis")
        except Exception as e:
            raise Exception(f"Erro ao conectar com Redis: {str(e)}")

    async def close(self) -> None:
        """Fecha conexão com Redis."""
        if self.async_client:
            await self.async_client.close()

    # ===== CONTEXTO DE EXECUÇÃO =====

    async def set_execution_context(self, execution_id: str, context: Dict[str, Any], ttl: int = 3600) -> None:
        """
        Armazena contexto de execução.

        Args:
            execution_id: ID da execução
            context: Contexto compartilhado
            ttl: Tempo de vida em segundos (1 hora por padrão)
        """
        key = f"execution:{execution_id}:context"
        await self.async_client.setex(
            key,
            ttl,
            json.dumps(context, default=str)
        )

    async def get_execution_context(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """Recupera contexto de execução."""
        key = f"execution:{execution_id}:context"
        data = await self.async_client.get(key)
        return json.loads(data) if data else None

    async def update_execution_context(self, execution_id: str, updates: Dict[str, Any]) -> None:
        """Atualiza contexto de execução."""
        context = await self.get_execution_context(execution_id)
        if context:
            context.update(updates)
            await self.set_execution_context(execution_id, context)

    async def delete_execution_context(self, execution_id: str) -> None:
        """Remove contexto de execução."""
        key = f"execution:{execution_id}:context"
        await self.async_client.delete(key)

    # ===== ESTADO DOS AGENTES =====

    async def set_agent_state(self, execution_id: str, agent_name: str, state: Dict[str, Any]) -> None:
        """
        Define estado de um agente.

        Args:
            execution_id: ID da execução
            agent_name: Nome do agente
            state: Estado do agente
        """
        key = f"execution:{execution_id}:agents:{agent_name}"
        await self.async_client.setex(
            key,
            3600,  # 1 hora
            json.dumps(state, default=str)
        )

    async def get_agent_state(self, execution_id: str, agent_name: str) -> Optional[Dict[str, Any]]:
        """Recupera estado de um agente."""
        key = f"execution:{execution_id}:agents:{agent_name}"
        data = await self.async_client.get(key)
        return json.loads(data) if data else None

    async def get_all_agents_state(self, execution_id: str) -> Dict[str, Any]:
        """Recupera estado de todos os agentes."""
        pattern = f"execution:{execution_id}:agents:*"
        keys = await self.async_client.keys(pattern)

        agents_state = {}
        for key in keys:
            agent_name = key.split(":")[-1]
            data = await self.async_client.get(key)
            if data:
                agents_state[agent_name] = json.loads(data)

        return agents_state

    # ===== CONTADORES DE TOKENS =====

    async def increment_tokens(self, execution_id: str, agent_name: str, tokens: int) -> int:
        """
        Incrementa contador de tokens.

        Args:
            execution_id: ID da execução
            agent_name: Nome do agente
            tokens: Número de tokens

        Returns:
            Total de tokens do agente
        """
        key = f"execution:{execution_id}:tokens:{agent_name}"
        total = await self.async_client.incrby(key, tokens)
        await self.async_client.expire(key, 3600)  # TTL 1 hora
        return total

    async def get_tokens_used(self, execution_id: str, agent_name: Optional[str] = None) -> int:
        """
        Recupera tokens usados.

        Args:
            execution_id: ID da execução
            agent_name: Nome do agente (None = total)

        Returns:
            Número de tokens
        """
        if agent_name:
            key = f"execution:{execution_id}:tokens:{agent_name}"
            data = await self.async_client.get(key)
            return int(data) if data else 0
        else:
            # Total de todos os agentes
            pattern = f"execution:{execution_id}:tokens:*"
            keys = await self.async_client.keys(pattern)
            total = 0
            for key in keys:
                data = await self.async_client.get(key)
                if data:
                    total += int(data)
            return total

    async def reset_tokens(self, execution_id: str) -> None:
        """Reseta contadores de tokens."""
        pattern = f"execution:{execution_id}:tokens:*"
        keys = await self.async_client.keys(pattern)
        if keys:
            await self.async_client.delete(*keys)

    # ===== CACHE DE LIÇÕES =====

    async def cache_lessons(self, lessons: List[Dict[str, Any]]) -> None:
        """
        Cacheia lições aprendidas.

        Args:
            lessons: Lista de lições
        """
        key = "lessons_cache"
        await self.async_client.setex(
            key,
            86400,  # 24 horas
            json.dumps(lessons, default=str)
        )

    async def get_cached_lessons(self) -> Optional[List[Dict[str, Any]]]:
        """Recupera lições em cache."""
        key = "lessons_cache"
        data = await self.async_client.get(key)
        return json.loads(data) if data else None

    # ===== SESSÕES DE USUÁRIO =====

    async def create_session(self, user_id: str, session_data: Dict[str, Any], ttl: int = 86400) -> str:
        """
        Cria sessão de usuário.

        Args:
            user_id: ID do usuário
            session_data: Dados da sessão
            ttl: Tempo de vida em segundos

        Returns:
            Session ID
        """
        import uuid
        session_id = str(uuid.uuid4())
        key = f"session:{session_id}"

        session_data["user_id"] = user_id
        session_data["created_at"] = datetime.utcnow().isoformat()

        await self.async_client.setex(
            key,
            ttl,
            json.dumps(session_data, default=str)
        )

        return session_id

    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Recupera sessão de usuário."""
        key = f"session:{session_id}"
        data = await self.async_client.get(key)
        return json.loads(data) if data else None

    async def delete_session(self, session_id: str) -> None:
        """Remove sessão."""
        key = f"session:{session_id}"
        await self.async_client.delete(key)

    # ===== FILA DE EXECUÇÕES =====

    async def enqueue_execution(self, execution_data: Dict[str, Any]) -> str:
        """
        Adiciona execução à fila.

        Args:
            execution_data: Dados da execução

        Returns:
            ID da execução enfileirada
        """
        import uuid
        execution_id = str(uuid.uuid4())

        # Armazena dados
        await self.set_execution_context(execution_id, execution_data)

        # Adiciona à fila
        queue_key = "executions:queue"
        await self.async_client.rpush(queue_key, execution_id)

        return execution_id

    async def dequeue_execution(self) -> Optional[str]:
        """Remove execução da fila."""
        queue_key = "executions:queue"
        return await self.async_client.lpop(queue_key)

    async def get_queue_length(self) -> int:
        """Retorna tamanho da fila."""
        queue_key = "executions:queue"
        return await self.async_client.llen(queue_key)

    # ===== RATE LIMITING =====

    async def check_rate_limit(
        self,
        user_id: str,
        limit: int = 100,
        window_seconds: int = 3600
    ) -> bool:
        """
        Valida rate limit.

        Args:
            user_id: ID do usuário
            limit: Limite de requisições
            window_seconds: Janela de tempo

        Returns:
            True se dentro do limite
        """
        key = f"ratelimit:{user_id}"
        current = await self.async_client.get(key)
        current_count = int(current) if current else 0

        if current_count >= limit:
            return False

        # Incrementa contador
        await self.async_client.incr(key)
        await self.async_client.expire(key, window_seconds)

        return True

    async def get_rate_limit_status(self, user_id: str, limit: int = 100) -> Dict[str, int]:
        """Retorna status de rate limit."""
        key = f"ratelimit:{user_id}"
        current = await self.async_client.get(key)
        current_count = int(current) if current else 0

        return {
            "used": current_count,
            "remaining": max(0, limit - current_count),
            "limit": limit
        }

    # ===== HEALTH CHECK =====

    async def health_check(self) -> bool:
        """Verifica saúde da conexão."""
        try:
            await self.async_client.ping()
            return True
        except Exception:
            return False

    async def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do Redis."""
        info = await self.async_client.info()
        return {
            "connected_clients": info.get("connected_clients"),
            "used_memory": info.get("used_memory_human"),
            "used_memory_peak": info.get("used_memory_peak_human"),
            "total_commands_processed": info.get("total_commands_processed"),
            "uptime_in_seconds": info.get("uptime_in_seconds")
        }

    async def clear_all(self) -> None:
        """
        ⚠️ CUIDADO: Limpa TUDO do Redis.

        Use apenas em desenvolvimento ou testes!
        """
        await self.async_client.flushdb()

    async def clear_execution_data(self, execution_id: str) -> None:
        """Limpa dados de uma execução específica."""
        pattern = f"execution:{execution_id}:*"
        keys = await self.async_client.keys(pattern)
        if keys:
            await self.async_client.delete(*keys)
