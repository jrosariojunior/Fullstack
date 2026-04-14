"""
Storage Manager - Orquestração unificada de persistência.

Coordena PostgreSQL (longo prazo) e Redis (curto prazo).
Fornece interface única para toda a camada de storage.
"""

from typing import Optional, Dict, Any, List
from backend.storage.postgres_driver import PostgresDriver
from backend.storage.redis_driver import RedisDriver


class StorageManager:
    """
    Gerenciador unificado de armazenamento.

    - PostgreSQL: Persistência durável (histórico, lições, auditoria)
    - Redis: Cache e performance (contexto, estado, cache)
    """

    def __init__(self, postgres_url: str, redis_url: str = "redis://localhost:6379/0"):
        """
        Inicializa Storage Manager.

        Args:
            postgres_url: URL do PostgreSQL
            redis_url: URL do Redis
        """
        self.postgres = PostgresDriver(postgres_url)
        self.redis = RedisDriver(redis_url)

    async def initialize(self) -> None:
        """Inicializa conexões com ambos os bancos."""
        await self.postgres.initialize()
        await self.redis.initialize()

    async def close(self) -> None:
        """Fecha conexões."""
        await self.postgres.close()
        await self.redis.close()

    # ===== EXECUÇÕES =====

    async def start_execution(self, briefing: Dict[str, Any]) -> str:
        """
        Inicia uma nova execução.

        Args:
            briefing: Descrição do problema

        Returns:
            ID da execução
        """
        # Salva em PostgreSQL
        execution_id = await self.postgres.save_execution({
            "briefing": briefing,
            "status": "running"
        })

        # Cacheia em Redis
        context = {
            "briefing": briefing,
            "agents_status": {},
            "agents_output": {},
            "debates": [],
            "created_at": __import__("datetime").datetime.utcnow().isoformat()
        }
        await self.redis.set_execution_context(execution_id, context)

        return execution_id

    async def end_execution(
        self,
        execution_id: str,
        final_output: Dict[str, Any],
        total_tokens: int
    ) -> None:
        """
        Finaliza uma execução.

        Args:
            execution_id: ID da execução
            final_output: Resultado final
            total_tokens: Total de tokens usados
        """
        # Atualiza em PostgreSQL
        await self.postgres.finalize_execution(execution_id, final_output, total_tokens)

        # Remove do Redis (limpeza)
        await self.redis.delete_execution_context(execution_id)
        await self.redis.reset_tokens(execution_id)
        await self.redis.clear_execution_data(execution_id)

    async def get_execution(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """
        Recupera uma execução.

        Tenta primeiro em Redis (cache), depois PostgreSQL.

        Args:
            execution_id: ID da execução

        Returns:
            Dict com dados da execução
        """
        # Tenta Redis
        context = await self.redis.get_execution_context(execution_id)
        if context:
            return context

        # Fallback para PostgreSQL
        return await self.postgres.get_execution(execution_id)

    async def get_execution_history(self, limit: int = 20, offset: int = 0) -> List[Dict[str, Any]]:
        """Recupera histórico de execuções (PostgreSQL)."""
        return await self.postgres.get_execution_history(limit, offset)

    # ===== AGENTES =====

    async def record_agent_output(
        self,
        execution_id: str,
        agent_name: str,
        output: Dict[str, Any]
    ) -> None:
        """
        Registra output de um agente.

        Armazena em ambos: PostgreSQL (persistência) e Redis (cache).

        Args:
            execution_id: ID da execução
            agent_name: Nome do agente
            output: Output estruturado
        """
        # Salva em PostgreSQL
        await self.postgres.save_agent_output(execution_id, agent_name, output)

        # Cacheia em Redis
        await self.redis.set_agent_state(execution_id, agent_name, {
            "status": "completed",
            "output": output,
            "timestamp": __import__("datetime").datetime.utcnow().isoformat()
        })

        # Incrementa tokens se houver
        tokens = output.get("tokens_used", 0)
        if tokens > 0:
            await self.redis.increment_tokens(execution_id, agent_name, tokens)

    async def get_agent_outputs(self, execution_id: str) -> List[Dict[str, Any]]:
        """Recupera outputs de agentes."""
        return await self.postgres.get_agent_outputs(execution_id)

    async def get_agent_state(self, execution_id: str, agent_name: str) -> Optional[Dict[str, Any]]:
        """Recupera estado em tempo real de um agente (Redis)."""
        return await self.redis.get_agent_state(execution_id, agent_name)

    # ===== DEBATES =====

    async def record_debate(
        self,
        execution_id: str,
        round_num: int,
        topic: str,
        positions: Dict[str, str],
        resolution: Optional[str] = None
    ) -> None:
        """
        Registra um debate.

        Args:
            execution_id: ID da execução
            round_num: Número do round
            topic: Tópico do debate
            positions: Posições dos agentes
            resolution: Resolução (opcional)
        """
        await self.postgres.save_debate(
            execution_id,
            round_num,
            topic,
            positions,
            resolution
        )

    async def get_debates(self, execution_id: str) -> List[Dict[str, Any]]:
        """Recupera debates de uma execução."""
        return await self.postgres.get_debates(execution_id)

    # ===== LIÇÕES APRENDIDAS =====

    async def save_lesson_learned(self, pattern: str, insight: str) -> None:
        """
        Salva lição aprendida.

        Args:
            pattern: Padrão/tipo de problema
            insight: Lição aprendida
        """
        await self.postgres.save_lesson_learned(pattern, insight)
        # Invalida cache
        await self.redis.async_client.delete("lessons_cache")

    async def get_lessons_learned(self, use_cache: bool = True) -> List[Dict[str, Any]]:
        """
        Recupera lições aprendidas.

        Args:
            use_cache: Usar cache do Redis se disponível

        Returns:
            Lista de lições
        """
        if use_cache:
            cached = await self.redis.get_cached_lessons()
            if cached:
                return cached

        # Recupera do PostgreSQL
        lessons = await self.postgres.get_lessons_learned()

        # Cacheia em Redis
        if lessons:
            await self.redis.cache_lessons(lessons)

        return lessons

    # ===== LOGGING =====

    async def log_event(self, execution_id: str, event: Dict[str, Any]) -> None:
        """
        Registra evento de execução.

        Args:
            execution_id: ID da execução
            event: Dict com evento
        """
        await self.postgres.save_log_entry(execution_id, event)

    async def get_execution_logs(self, execution_id: str) -> List[Dict[str, Any]]:
        """Recupera logs de uma execução."""
        return await self.postgres.get_logs(execution_id)

    # ===== CONTEXTO COMPARTILHADO =====

    async def set_context(self, execution_id: str, context: Dict[str, Any]) -> None:
        """Define contexto compartilhado (Redis)."""
        await self.redis.set_execution_context(execution_id, context)

    async def get_context(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """Recupera contexto compartilhado (Redis)."""
        return await self.redis.get_execution_context(execution_id)

    async def update_context(self, execution_id: str, updates: Dict[str, Any]) -> None:
        """Atualiza contexto compartilhado (Redis)."""
        await self.redis.update_execution_context(execution_id, updates)

    # ===== TOKENS =====

    async def track_tokens(self, execution_id: str, agent_name: str, tokens: int) -> int:
        """
        Rastreia tokens usados.

        Args:
            execution_id: ID da execução
            agent_name: Nome do agente
            tokens: Número de tokens

        Returns:
            Total de tokens do agente
        """
        return await self.redis.increment_tokens(execution_id, agent_name, tokens)

    async def get_total_tokens(self, execution_id: str) -> int:
        """Retorna total de tokens usados."""
        return await self.redis.get_tokens_used(execution_id)

    # ===== SESSÕES =====

    async def create_user_session(self, user_id: str, session_data: Dict[str, Any]) -> str:
        """Cria sessão de usuário."""
        return await self.redis.create_session(user_id, session_data)

    async def get_user_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Recupera sessão de usuário."""
        return await self.redis.get_session(session_id)

    async def delete_user_session(self, session_id: str) -> None:
        """Remove sessão de usuário."""
        await self.redis.delete_session(session_id)

    # ===== RATE LIMITING =====

    async def check_rate_limit(self, user_id: str, limit: int = 100) -> bool:
        """Verifica rate limit."""
        return await self.redis.check_rate_limit(user_id, limit)

    async def get_rate_limit_status(self, user_id: str, limit: int = 100) -> Dict[str, int]:
        """Retorna status de rate limit."""
        return await self.redis.get_rate_limit_status(user_id, limit)

    # ===== FILA =====

    async def enqueue_execution(self, execution_data: Dict[str, Any]) -> str:
        """Enfileira execução."""
        return await self.redis.enqueue_execution(execution_data)

    async def dequeue_execution(self) -> Optional[str]:
        """Remove execução da fila."""
        return await self.redis.dequeue_execution()

    async def get_queue_length(self) -> int:
        """Retorna tamanho da fila."""
        return await self.redis.get_queue_length()

    # ===== HEALTH & MONITORING =====

    async def health_check(self) -> Dict[str, bool]:
        """Verifica saúde de ambas as conexões."""
        postgres_ok = True
        redis_ok = await self.redis.health_check()

        try:
            await self.postgres.get_execution_history(limit=1)
        except Exception:
            postgres_ok = False

        return {
            "postgresql": postgres_ok,
            "redis": redis_ok,
            "healthy": postgres_ok and redis_ok
        }

    async def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de ambos os bancos."""
        return {
            "redis": await self.redis.get_stats() if await self.redis.health_check() else None,
            "timestamp": __import__("datetime").datetime.utcnow().isoformat()
        }

    # ===== CLEANUP =====

    async def clear_execution_cache(self, execution_id: str) -> None:
        """Remove cache de uma execução."""
        await self.redis.clear_execution_data(execution_id)

    async def clear_all_cache(self) -> None:
        """
        ⚠️ Limpa TODO o cache Redis.

        Use com cuidado! PostgreSQL é preservado.
        """
        await self.redis.clear_all()

    async def export_execution(self, execution_id: str) -> Dict[str, Any]:
        """
        Exporta execução completa (para backup/análise).

        Args:
            execution_id: ID da execução

        Returns:
            Dict completo com tudo
        """
        execution = await self.postgres.get_execution(execution_id)
        agent_outputs = await self.postgres.get_agent_outputs(execution_id)
        debates = await self.postgres.get_debates(execution_id)
        logs = await self.postgres.get_logs(execution_id)

        return {
            "execution": execution,
            "agent_outputs": agent_outputs,
            "debates": debates,
            "logs": logs,
            "export_timestamp": __import__("datetime").datetime.utcnow().isoformat()
        }
