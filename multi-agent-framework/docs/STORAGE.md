# 📦 Storage - Persistência com PostgreSQL + Redis

O framework usa dois bancos de dados de forma complementar:

- **PostgreSQL**: Persistência durável (histórico, lições, auditoria)
- **Redis**: Cache e performance (contexto, estado, cache)

## 🚀 Quick Start

### 1. Inicializar Storage Manager

```python
from backend.storage import StorageManager

storage = StorageManager(
    postgres_url="postgresql+asyncpg://user:pass@localhost/multi_agent_db",
    redis_url="redis://localhost:6379/0"
)

await storage.initialize()
```

### 2. Usar em Execuções

```python
# Iniciar execução
execution_id = await storage.start_execution(briefing)

# Registrar output de agente
await storage.record_agent_output(
    execution_id=execution_id,
    agent_name="Architect",
    output={"architecture": "microservices", "risks": [...]}
)

# Registrar debate
await storage.record_debate(
    execution_id=execution_id,
    round_num=1,
    topic="Arquitetura: Monólito vs Microserviços",
    positions={"Architect": "Microserviços", "Developer": "Monólito"},
    resolution="Microserviços (escalabilidade)"
)

# Finalizar
await storage.end_execution(
    execution_id=execution_id,
    final_output={...},
    total_tokens=15000
)
```

## 📊 Arquitetura

```
StorageManager (Interface Unificada)
    ├─ PostgresDriver (Persistência)
    │   ├─ ExecutionModel
    │   ├─ AgentOutputModel
    │   ├─ DebateModel
    │   ├─ LessonLearnedModel
    │   └─ ExecutionLogModel
    └─ RedisDriver (Cache)
        ├─ Contexto de execução
        ├─ Estado dos agentes
        ├─ Contadores de tokens
        ├─ Sessões de usuário
        └─ Fila de execuções
```

## 🔧 API Completa

### Execuções

```python
# Iniciar
execution_id = await storage.start_execution(briefing)

# Obter
execution = await storage.get_execution(execution_id)

# Histórico
history = await storage.get_execution_history(limit=20)

# Finalizar
await storage.end_execution(execution_id, final_output, tokens)
```

### Agentes

```python
# Registrar output
await storage.record_agent_output(execution_id, "Architect", output)

# Obter outputs
outputs = await storage.get_agent_outputs(execution_id)

# Estado em tempo real
state = await storage.get_agent_state(execution_id, "Architect")
```

### Debates

```python
# Registrar
await storage.record_debate(execution_id, round_num, topic, positions, resolution)

# Obter
debates = await storage.get_debates(execution_id)
```

### Lições Aprendidas

```python
# Salvar
await storage.save_lesson_learned("microservices", "Microserviços escalabilidade superior")

# Recuperar (com cache)
lessons = await storage.get_lessons_learned(use_cache=True)
```

### Logging

```python
# Registrar evento
await storage.log_event(execution_id, {"phase": "debate", "agents": ["Architect", "Developer"]})

# Obter logs
logs = await storage.get_execution_logs(execution_id)
```

### Contexto Compartilhado

```python
# Definir
await storage.set_context(execution_id, {"shared": "data"})

# Obter
context = await storage.get_context(execution_id)

# Atualizar
await storage.update_context(execution_id, {"new_key": "new_value"})
```

### Rastreamento de Tokens

```python
# Registrar tokens
await storage.track_tokens(execution_id, "Architect", 2500)

# Total
total = await storage.get_total_tokens(execution_id)
```

### Sessões de Usuário

```python
# Criar
session_id = await storage.create_user_session("user123", {"data": "..."})

# Obter
session = await storage.get_user_session(session_id)

# Remover
await storage.delete_user_session(session_id)
```

### Rate Limiting

```python
# Verificar
within_limit = await storage.check_rate_limit("user123", limit=100)

# Status
status = await storage.get_rate_limit_status("user123", limit=100)
# {"used": 45, "remaining": 55, "limit": 100}
```

## 📋 Modelos PostgreSQL

### Executions

```sql
CREATE TABLE executions (
    id UUID PRIMARY KEY,
    briefing TEXT NOT NULL,
    status VARCHAR(50),  -- queued, running, completed, failed
    created_at TIMESTAMP,
    completed_at TIMESTAMP,
    final_output JSONB,
    total_tokens INTEGER
);
```

### Agent Outputs

```sql
CREATE TABLE agent_outputs (
    id UUID PRIMARY KEY,
    execution_id UUID REFERENCES executions(id),
    agent_name VARCHAR(100),
    output JSONB,
    tokens_used INTEGER,
    timestamp TIMESTAMP
);
```

### Debates

```sql
CREATE TABLE debates (
    id UUID PRIMARY KEY,
    execution_id UUID REFERENCES executions(id),
    round_num INTEGER,
    topic TEXT,
    positions JSONB,
    resolution TEXT,
    resolved BOOLEAN,
    timestamp TIMESTAMP
);
```

### Lessons Learned

```sql
CREATE TABLE lessons_learned (
    id UUID PRIMARY KEY,
    pattern VARCHAR(200),
    insight TEXT,
    created_at TIMESTAMP,
    used_count INTEGER
);
```

### Execution Logs

```sql
CREATE TABLE execution_logs (
    id UUID PRIMARY KEY,
    execution_id UUID REFERENCES executions(id),
    log_entry JSONB,
    timestamp TIMESTAMP
);
```

## 🔐 Variáveis de Ambiente

```bash
# PostgreSQL
DATABASE_URL=postgresql+asyncpg://multi_agent_user:multi_agent_pass@localhost:5432/multi_agent_db

# Redis
REDIS_URL=redis://localhost:6379/0
```

## 🚀 Migrations (Alembic)

### Inicializar Alembic

```bash
cd multi-agent-framework
alembic init alembic
```

### Criar Migration

```bash
alembic revision --autogenerate -m "Initial schema"
```

### Aplicar Migrations

```bash
alembic upgrade head
```

### Ver History

```bash
alembic history
```

### Rollback

```bash
alembic downgrade -1
```

## 🧪 Testing

```python
import asyncio
from backend.storage import StorageManager

async def test():
    storage = StorageManager(
        postgres_url="postgresql+asyncpg://...",
        redis_url="redis://localhost:6379/0"
    )
    
    await storage.initialize()
    
    # Teste
    exec_id = await storage.start_execution({"description": "Test"})
    print(f"Execution: {exec_id}")
    
    # Cleanup
    await storage.close()

asyncio.run(test())
```

## 🔍 Monitoramento

```python
# Health Check
health = await storage.health_check()
print(health)  # {"postgresql": True, "redis": True, "healthy": True}

# Estatísticas
stats = await storage.get_stats()
print(stats)  # Redis stats
```

## 🧹 Cleanup

```python
# Limpar cache de uma execução
await storage.clear_execution_cache(execution_id)

# Limpar TODO o Redis (cuidado!)
await storage.clear_all_cache()

# Exportar execução completa
export = await storage.export_execution(execution_id)
```

## ⚙️ Performance

### Otimizações

1. **PostgreSQL**:
   - Índices em `execution_id`, `agent_name`, `status`
   - Queries com LIMIT para históricos
   - JSONB para queries flexíveis

2. **Redis**:
   - TTL automático (limpeza)
   - Cache de lições aprendidas (24h)
   - Pipeline para operações batch

### Escalabilidade

- PostgreSQL para replicação e backup
- Redis em cluster para alta disponibilidade
- Particionamento por execution_id se necessário

## 📚 Boas Práticas

1. **Sempre chamar `initialize()` e `close()`**
   ```python
   storage = StorageManager(...)
   await storage.initialize()
   try:
       # Seu código
   finally:
       await storage.close()
   ```

2. **Use cache quando possível**
   ```python
   # Redis cache automático
   lessons = await storage.get_lessons_learned(use_cache=True)
   ```

3. **Registre tudo que importa**
   ```python
   await storage.log_event(execution_id, {"phase": "debate", ...})
   ```

4. **Rate limit for API**
   ```python
   if not await storage.check_rate_limit(user_id):
       raise RateLimitError()
   ```

---

**Pronto para usar! 🚀**
