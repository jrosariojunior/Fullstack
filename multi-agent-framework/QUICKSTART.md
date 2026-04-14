# 🚀 Quick Start Guide

Get the Multi-Agent Framework up and running in 5 minutes.

---

## Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Git
- A text editor or IDE

---

## Step 1: Setup Databases

```bash
# Start PostgreSQL and Redis
docker-compose up -d

# Verify they're running
docker ps
```

Expected output:
```
CONTAINER ID   IMAGE            STATUS
...            postgres:15      Up 2 minutes
...            redis:7          Up 2 minutes
```

---

## Step 2: Configure Environment

```bash
# Copy the example configuration
cp .env.example .env

# Edit .env with your settings (if needed)
nano .env
```

Important variables:
- `DATABASE_URL`: PostgreSQL connection (default: localhost)
- `REDIS_URL`: Redis connection (default: localhost:6379)
- `CLAUDE_API_KEY`: Your Anthropic API key (for Claude models)
- `OPENAI_API_KEY`: Your OpenAI API key (optional, for GPT models)

---

## Step 3: Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## Step 4: Start the API Server

```bash
# Start the FastAPI server
uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
✅ Storage inicializado
✅ LLM Provider (claude) inicializado
✅ Agentes criados
✅ Orchestrator inicializado
✅ WebSocket Manager inicializado
✅ Aplicação iniciada com sucesso

INFO:     Application startup complete
```

---

## Step 5: Test the API

### Option A: Using cURL

```bash
# Start an execution
curl -X POST http://localhost:8000/api/execute \
  -H "Content-Type: application/json" \
  -d '{
    "briefing": {
      "description": "I need a scalable microservices architecture for an e-commerce platform"
    },
    "max_debate_rounds": 3,
    "token_limit": 100000
  }'
```

Response (202 Accepted):
```json
{
  "execution_id": "abc123def456...",
  "status": "queued",
  "estimated_duration": "2-5 minutes",
  "status_url": "/api/status/abc123def456..."
}
```

### Option B: Using Python

```python
import requests
import json

response = requests.post(
    "http://localhost:8000/api/execute",
    json={
        "briefing": {
            "description": "I need a microservices architecture"
        }
    }
)

result = response.json()
execution_id = result["execution_id"]
print(f"Execution started: {execution_id}")
```

---

## Step 6: Monitor Execution

### Check Status
```bash
# Replace with your execution_id
curl http://localhost:8000/api/status/abc123def456...
```

Response:
```json
{
  "execution_id": "abc123def456...",
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
  "current_phase": "parallel_analysis"
}
```

### Real-Time Monitoring (WebSocket)

```bash
# In a new terminal, run the example client
python examples/websocket_client.py abc123def456...
```

Output:
```
📡 Connecting to ws://localhost:8000/ws/abc123def456...
✅ Connected to execution stream

📋 Initial Status: running
   Message: Conectado à execução abc123def456...

📊 Phase: parallel_analysis
   Progress: [████████░░░░░░░░░░░░] 40%
   Agents analyzing in parallel...

🔄 Agent: Architect → running

✅ Agent: Architect → completed
   Output summary: {...}

...
```

---

## Step 7: Get Results

```bash
# Wait for execution to complete, then get results
curl http://localhost:8000/api/result/abc123def456...
```

Response includes:
- Agent outputs and analysis
- Debate logs with resolutions
- Final synthesized output
- Token usage statistics
- Execution metadata

---

## Step 8: View Execution History

```bash
# Get recent executions
curl "http://localhost:8000/api/history?limit=10"

# Get statistics
curl "http://localhost:8000/api/history/stats?days=30"

# Search history
curl "http://localhost:8000/api/history/search?query=microservices"
```

---

## 📊 API Reference (Quick)

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/execute` | Start new execution (202) |
| GET | `/api/status/{id}` | Check execution status |
| GET | `/api/status/{id}/agents` | Get agent details |
| GET | `/api/result/{id}` | Get final results |
| GET | `/api/result/{id}/export` | Export as JSON/CSV |
| GET | `/api/history` | Execution history |
| GET | `/api/history/stats` | Statistics |
| GET | `/health` | Health check |
| GET | `/stats` | System stats |
| WS | `/ws/{id}` | Real-time updates |

---

## 🎛️ Interactive Documentation

Visit the built-in Swagger UI:
```
http://localhost:8000/docs
```

This shows:
- All endpoints with descriptions
- Request/response examples
- Try-it-out functionality
- Full schema documentation

---

## 🔍 Debugging

### View API Logs
The API logs all requests and events. Look for:
```
INFO:     Started server process
✅ Cliente conectado para execution_id
🎭 Debate Round 1
✅ Execução concluída
```

### View Database Content
```bash
# Connect to PostgreSQL
docker exec -it multi_agent_db psql -U multi_agent_user -d multi_agent_db

# View executions
SELECT id, status, created_at FROM executions ORDER BY created_at DESC LIMIT 5;

# View agent outputs
SELECT execution_id, agent_name, timestamp FROM agent_outputs;
```

### Check Redis Cache
```bash
# Connect to Redis
docker exec -it multi_agent_redis redis-cli

# View keys
KEYS *

# Check specific execution context
GET execution:{execution_id}:context
```

---

## 🆘 Troubleshooting

### Port Already in Use
```bash
# If port 8000 is in use, use a different port
uvicorn backend.api.main:app --reload --port 8001
```

### Database Connection Failed
```bash
# Check if containers are running
docker ps

# Restart containers
docker-compose restart

# Check logs
docker logs multi_agent_db
docker logs multi_agent_redis
```

### Missing API Key
```bash
# Make sure to set environment variables
export CLAUDE_API_KEY="sk-ant-..."

# Or add to .env file
CLAUDE_API_KEY=sk-ant-...
```

### WebSocket Connection Refused
```bash
# Make sure API is running on correct port
# Update websocket_client.py if needed:
monitor = ExecutionMonitor(execution_id, host="localhost", port=8000)
```

---

## 📚 Next Steps

1. **Read Full Documentation**
   - `IMPLEMENTATION_STATUS.md` - Complete feature list
   - `docs/STORAGE.md` - Database and caching architecture
   - `docs/API.md` - Detailed API specifications

2. **Explore the Code**
   - `backend/core/` - Orchestration engine
   - `backend/agents/` - Agent implementations
   - `backend/llm/` - LLM provider adapters
   - `backend/storage/` - Storage layer

3. **Customize**
   - Add new agents in `backend/agents/`
   - Support new LLM providers in `backend/llm/`
   - Extend API in `backend/api/routes/`
   - Enhance storage in `backend/storage/`

4. **Deploy**
   - Use Docker: `docker build -t multi-agent-framework .`
   - Deploy with Kubernetes
   - Use environment variables for configuration

---

## 💡 Example Briefings to Try

### 1. E-Commerce System
```json
{
  "briefing": {
    "description": "Build a scalable e-commerce platform that handles 1M+ users with real-time inventory and payment processing",
    "requirements": [
      {
        "type": "functional",
        "description": "Shopping cart with persistent sessions",
        "priority": "must"
      },
      {
        "type": "non_functional",
        "description": "99.9% uptime SLA",
        "priority": "must"
      }
    ]
  }
}
```

### 2. SaaS Platform
```json
{
  "briefing": {
    "description": "Multi-tenant SaaS platform for project management with real-time collaboration",
    "requirements": [
      {
        "type": "functional",
        "description": "Real-time updates for team members",
        "priority": "must"
      }
    ],
    "preferences": {
      "tech_stack": ["React", "Python", "PostgreSQL"],
      "architecture_style": ["microservices", "event-driven"]
    }
  }
}
```

### 3. Data Pipeline
```json
{
  "briefing": {
    "description": "Real-time data pipeline processing 10GB/day with ML model inference",
    "constraints": [
      {
        "type": "budget",
        "description": "$5000/month infrastructure"
      }
    ]
  }
}
```

---

## 📞 Getting Help

- **API Issues**: Check `/docs` (Swagger UI)
- **Code Questions**: Review IMPLEMENTATION_STATUS.md
- **Database Issues**: Check docker logs
- **WebSocket Issues**: Test with examples/websocket_client.py

---

**You're ready to go! 🎉**

Start your first execution and watch the agents collaborate in real-time.
