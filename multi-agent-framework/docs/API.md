# 🌐 API REST - Documentação Completa

API RESTful para orquestração de agentes colaborativos.

## 🚀 Quick Start

### Iniciar servidor

```bash
cd multi-agent-framework
uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Acessar documentação

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 📍 Base URL

```
http://localhost:8000/api
```

## 🔐 Autenticação

Atualmente a API não requer autenticação. Em produção, implemente JWT ou OAuth2.

## ⚡ Endpoints

### 1. POST /execute

**Inicia execução do time de agentes.**

```bash
curl -X POST http://localhost:8000/api/execute \
  -H "Content-Type: application/json" \
  -d '{
    "briefing": {
      "description": "Quero um sistema de e-commerce escalável com microserviços",
      "requirements": [
        {
          "type": "functional",
          "description": "Carrinho de compras com persistência",
          "priority": "must"
        },
        {
          "type": "non_functional",
          "description": "Latência < 100ms",
          "priority": "must"
        }
      ]
    },
    "parallel": true,
    "max_debate_rounds": 3,
    "token_limit": 100000
  }'
```

**Response (202 Accepted):**

```json
{
  "execution_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "queued",
  "estimated_duration": "2-5 minutes",
  "status_url": "/api/status/550e8400-e29b-41d4-a716-446655440000"
}
```

**Schema:**

```
POST /api/execute
{
  "briefing": {
    "description": string (min 10 chars),
    "requirements": [
      {
        "type": "functional|non_functional",
        "description": string,
        "priority": "must|should|could|wont"
      }
    ],
    "constraints": [
      {
        "type": "technical|budget|time",
        "description": string
      }
    ],
    "preferences": {
      "tech_stack": [string],
      "architecture_style": [string]
    }
  },
  "parallel": boolean,
  "max_debate_rounds": integer (1-10),
  "token_limit": integer (1000+),
  "humanize_output": boolean,
  "llm_provider": "claude|openai",
  "llm_model": string
}
```

---

### 2. GET /status/{execution_id}

**Status em tempo real da execução.**

```bash
curl http://localhost:8000/api/status/550e8400-e29b-41d4-a716-446655440000
```

**Response:**

```json
{
  "execution_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "running",
  "progress": {
    "total_agents": 6,
    "completed_agents": 3,
    "percentage": 50
  },
  "agents_status": {
    "Architect": "completed",
    "Analyst": "completed",
    "Developer": "running",
    "TechReviewer": "pending",
    "QAEngineer": "pending"
  },
  "current_phase": "parallel_analysis",
  "estimated_completion": null,
  "queue_position": null
}
```

**Query Parameters:**

- `include_queue` (bool): Incluir posição na fila (padrão: true)

**Status Possíveis:**
- `queued`: Aguardando processamento
- `running`: Em execução
- `completed`: Concluída
- `failed`: Falhou

---

### 3. GET /result/{execution_id}

**Resultado completo da execução.**

```bash
curl http://localhost:8000/api/result/550e8400-e29b-41d4-a716-446655440000
```

**Response:**

```json
{
  "execution_id": "550e8400-e29b-41d4-a716-446655440000",
  "briefing": {...},
  "status": "completed",
  "results": {
    "Architect": {
      "agent_name": "Architect",
      "agent_id": "arch-123",
      "output": {
        "architecture_type": "microservices",
        "main_components": [...],
        "risks": [...]
      },
      "tokens_used": 2500,
      "confidence": 0.95
    },
    ...
  },
  "debate_log": [
    {
      "round": 1,
      "topic": "Arquitetura: Monólito vs Microserviços",
      "participants": ["Architect", "Developer"],
      "positions": {
        "Architect": "Microserviços para escalabilidade",
        "Developer": "Monólito para simplicidade"
      },
      "resolution": "Microserviços com fallback monolítico"
    }
  ],
  "conflicts": [],
  "final_output": {...},
  "execution_log": ["Execução iniciada...", "Análise paralela..."],
  "metadata": {
    "started_at": "2025-01-15T10:30:00Z",
    "completed_at": "2025-01-15T10:35:00Z",
    "total_tokens_used": 15000,
    "duration_seconds": 300,
    "status": "completed"
  }
}
```

**Query Parameters:**

- `include_logs` (bool): Incluir logs detalhados (padrão: true)

---

### 4. GET /history

**Histórico de execuções com paginação.**

```bash
curl "http://localhost:8000/api/history?limit=20&offset=0"
```

**Response:**

```json
{
  "total": 1234,
  "limit": 20,
  "offset": 0,
  "executions": [
    {
      "execution_id": "550e8400-e29b-41d4-a716-446655440000",
      "briefing_summary": "Sistema de e-commerce escalável...",
      "status": "completed",
      "created_at": "2025-01-15T10:30:00Z",
      "completed_at": "2025-01-15T10:35:00Z",
      "tokens_used": 15000,
      "agents_completed": 5,
      "total_agents": 6
    },
    ...
  ]
}
```

**Query Parameters:**

- `limit` (int): Registros por página (padrão: 20, máx: 100)
- `offset` (int): Offset para paginação (padrão: 0)
- `status` (str): Filtrar por status (queued|running|completed|failed)

---

### 5. GET /health

**Health check da aplicação.**

```bash
curl http://localhost:8000/api/health
```

**Response:**

```json
{
  "status": "healthy",
  "postgresql": true,
  "redis": true,
  "llm_provider": true,
  "timestamp": "2025-01-15T10:30:00Z"
}
```

---

### 6. GET /stats

**Estatísticas gerais da aplicação.**

```bash
curl http://localhost:8000/api/stats
```

**Response:**

```json
{
  "uptime_seconds": 3600,
  "total_executions": 1234,
  "completed_executions": 1100,
  "failed_executions": 34,
  "total_tokens_processed": 15312500,
  "avg_tokens_per_execution": 12500,
  "queue_length": 5,
  "redis_memory": "128.5MB",
  "timestamp": "2025-01-15T10:30:00Z"
}
```

---

## 🔄 Fluxo Típico

```
1. POST /execute
   ↓
   Retorna: execution_id, status_url
   ↓
2. Polling: GET /status/{execution_id}
   ↓
   Aguarda: status = "completed"
   ↓
3. GET /result/{execution_id}
   ↓
   Retorna: resultado completo
```

---

## 🔧 Exemplos Completos

### Python (requests)

```python
import requests
import time

BASE_URL = "http://localhost:8000/api"

# 1. Iniciar execução
briefing = {
    "description": "Sistema de e-commerce com pagamento integrado",
    "requirements": [
        {
            "type": "functional",
            "description": "Integração com Stripe",
            "priority": "must"
        }
    ]
}

response = requests.post(
    f"{BASE_URL}/execute",
    json={"briefing": briefing}
)

execution = response.json()
exec_id = execution["execution_id"]
print(f"Execução iniciada: {exec_id}")

# 2. Acompanhar progresso
while True:
    status_resp = requests.get(f"{BASE_URL}/status/{exec_id}")
    status_data = status_resp.json()
    
    print(f"Status: {status_data['status']}")
    print(f"Progresso: {status_data['progress']['percentage']}%")
    
    if status_data["status"] in ["completed", "failed"]:
        break
    
    time.sleep(2)

# 3. Obter resultado
result_resp = requests.get(f"{BASE_URL}/result/{exec_id}")
result = result_resp.json()

print(f"Resultado final:")
print(result["final_output"])
```

### JavaScript/Node.js

```javascript
const BASE_URL = "http://localhost:8000/api";

async function executeTeam() {
  // 1. Iniciar
  const briefing = {
    description: "Sistema de IoT para monitoramento",
    requirements: [
      {
        type: "non_functional",
        description: "Latência < 50ms",
        priority: "must"
      }
    ]
  };

  const execResponse = await fetch(`${BASE_URL}/execute`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ briefing })
  });

  const { execution_id } = await execResponse.json();
  console.log(`Execution: ${execution_id}`);

  // 2. Acompanhar
  let status = "running";
  while (status !== "completed") {
    const statusResponse = await fetch(`${BASE_URL}/status/${execution_id}`);
    const { status: currentStatus, progress } = await statusResponse.json();
    
    console.log(`${progress.percentage}% - ${currentStatus}`);
    status = currentStatus;
    
    await new Promise(resolve => setTimeout(resolve, 2000));
  }

  // 3. Resultado
  const resultResponse = await fetch(`${BASE_URL}/result/${execution_id}`);
  const result = await resultResponse.json();
  
  console.log("Final output:", result.final_output);
}

executeTeam();
```

### cURL

```bash
# 1. Executar
EXECUTION=$(curl -s -X POST http://localhost:8000/api/execute \
  -H "Content-Type: application/json" \
  -d '{
    "briefing": {
      "description": "Sistema de IA para análise de sentimentos"
    }
  }')

EXEC_ID=$(echo $EXECUTION | grep -o '"execution_id":"[^"]*' | cut -d'"' -f4)
echo "Execution ID: $EXEC_ID"

# 2. Status
curl http://localhost:8000/api/status/$EXEC_ID

# 3. Resultado
curl http://localhost:8000/api/result/$EXEC_ID > resultado.json
```

---

## ⚠️ Tratamento de Erros

### Códigos de Status HTTP

| Código | Significado |
|--------|------------|
| 200 | OK - Sucesso |
| 202 | Accepted - Execução enfileirada |
| 400 | Bad Request - Dados inválidos |
| 404 | Not Found - Recurso não encontrado |
| 429 | Too Many Requests - Rate limit |
| 503 | Service Unavailable - Serviço indisponível |

### Exemplo de Erro

```json
{
  "error": "Execução não encontrada",
  "detail": "Execution 550e8400-e29b-41d4-a716-446655440000 not found",
  "error_code": "NOT_FOUND",
  "timestamp": "2025-01-15T10:30:00Z"
}
```

---

## 🚦 Rate Limiting

- Limite: 100 requisições por hora por IP
- Header de resposta: `X-RateLimit-Remaining`

---

## 📊 Pagination

```
GET /history?limit=20&offset=40
```

- `limit`: 1-100 (padrão: 20)
- `offset`: ≥ 0 (padrão: 0)

Resposta inclui:
- `total`: Total de registros
- `limit`: Limit usado
- `offset`: Offset usado
- `executions`: Array de registros

---

## 🔍 Boas Práticas

1. **Use polling com exponential backoff**
   ```python
   wait_time = 1
   max_wait = 60
   while not completed:
       time.sleep(wait_time)
       wait_time = min(wait_time * 1.5, max_wait)
   ```

2. **Implemente timeout**
   ```python
   max_wait_time = 600  # 10 minutos
   elapsed = 0
   while elapsed < max_wait_time:
       # ...
       elapsed += wait_time
   ```

3. **Trate rate limits**
   ```python
   if response.status_code == 429:
       retry_after = int(response.headers.get("Retry-After", 60))
       time.sleep(retry_after)
   ```

---

## 📚 Swagger/OpenAPI

Todos os endpoints estão documentados no Swagger:

http://localhost:8000/docs

Aqui você pode:
- Ver todos os endpoints
- Ver schemas detalhados
- Testar requests diretamente

---

**Pronto para integrar a API! 🚀**
