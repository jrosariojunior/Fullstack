"""
Storage - Módulo de persistência com PostgreSQL e Redis.

Fornece drivers para ambos os bancos e gerenciador unificado.
"""

from backend.storage.postgres_driver import PostgresDriver
from backend.storage.redis_driver import RedisDriver
from backend.storage.storage_manager import StorageManager

__all__ = [
    "PostgresDriver",
    "RedisDriver",
    "StorageManager"
]
