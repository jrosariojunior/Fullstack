# 🤖 Multi-Agent Framework

Framework de orquestração de agentes colaborativos que utiliza 6 especialistas (personas distintas) para resolver problemas complexos através de debate estruturado.

## ⚡ Quick Start

### Requisitos
- Python 3.11+
- PostgreSQL
- Redis

### Instalação

```bash
# Clone / download
cd multi-agent-framework

# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows

# Instale dependências
pip install -r requirements.txt

# Configure banco de dados
docker-compose up -d

# Inicie servidor
uvicorn backend.api.main:app --reload
```

## 🎯 Uso

### Via Python Library

```python
from backend.core.orchestrator import TeamOrchestrator

team = TeamOrchestrator(
    llm_provider="claude",
    model="claude-3-5-sonnet-20241022"
)

result = team.execute(
    briefing="Quero um sistema de e-commerce...",
    max_debate_rounds=3,
    parallel=True,
    token_limit=100000
)

print(result.final_output)
```

### Via API REST

```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "briefing": {
      "description": "Quero um sistema de e-commerce..."
    }
  }'
```

## 📊 Arquitetura

```
BRIEFING → ANÁLISE PARALELA (6 agentes) → DEBATE (máx 3 loops) → SÍNTESE → HUMANIZAÇÃO → RESULTADO
```

### 6 Agentes

1. **Arquiteto** - Design e escalabilidade
2. **Analista** - Planejamento e estrutura
3. **Desenvolvedor** - Implementação técnica
4. **Revisor** - Validação crítica
5. **QA Engineer** - Testes e confiabilidade
6. **Orquestrador** - Coordena debate

## 📁 Estrutura

```
multi-agent-framework/
├── backend/
│   ├── core/           # Motor principal
│   ├── agents/         # 6 agentes
│   ├── llm/            # Adaptadores LLM
│   ├── humanizer/      # Humanização
│   ├── storage/        # PostgreSQL + Redis
│   ├── api/            # FastAPI
│   ├── config/         # Configurações
│   └── utils/          # Utilidades
├── lib/
│   ├── python/         # Lib Python
│   ├── node/           # Binding Node.js
│   └── go/             # Binding Go
├── tests/
├── docs/
└── requirements.txt
```

## 🔌 API Endpoints

- `POST /execute` - Inicia execução
- `GET /status/{id}` - Status em tempo real
- `GET /result/{id}` - Resultado completo
- `GET /history` - Histórico de execuções
- `POST /debates/{id}/resolve` - Resolve conflitos

## 📚 Documentação

Veja `/docs` para especificações detalhadas.

## 🛠️ Tech Stack

- **Backend:** Python 3.11+ (FastAPI)
- **Banco de Dados:** PostgreSQL + Redis
- **LLM:** Agnóstico (Claude API, OpenAI, etc)
- **Deploy:** Docker

## 📝 Status

- ✅ Briefing finalizado
- ✅ Arquitetura definida
- ⏳ Implementação em progresso

---

**Framework criado com rigor de engenharia de software sênior.**
