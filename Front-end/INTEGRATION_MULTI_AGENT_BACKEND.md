# 🔗 Integration Guide - Frontend + Multi-Agent Backend

**Status:** ✅ Complete  
**Version:** 1.0  
**Last Updated:** April 2026

Complete guide to integrating this front-end framework with the multi-agent-framework backend. Includes architecture, API contracts, WebSocket communication, and deployment.

---

## 📋 Table of Contents

1. [Integration Overview](#integration-overview)
2. [Architecture](#architecture)
3. [API Contracts](#api-contracts)
4. [WebSocket Communication](#websocket-communication)
5. [Authentication Flow](#authentication-flow)
6. [Data Models & Sync](#data-models--sync)
7. [Real-Time Features](#real-time-features)
8. [Error Handling](#error-handling)
9. [Deployment](#deployment)
10. [Testing Integration](#testing-integration)
11. [Troubleshooting](#troubleshooting)

---

## 🎯 Integration Overview

### What is Being Integrated?

**Frontend System (This Framework):**
- 5 specialized agents working together
- Next.js + React + TypeScript
- Real-time UI updates
- Project management dashboards
- Client-facing interfaces

**Backend System (multi-agent-framework):**
- 7-phase execution engine
- Agent coordination system
- Multi-agent debate and consensus
- Project execution and monitoring
- WebSocket real-time communication

### Integration Goal

Create a seamless system where:
- Frontend agents can trigger backend agent execution
- Backend agents can report progress to frontend in real-time
- Frontend displays backend agent activities and results
- Users can monitor multi-agent collaboration as it happens
- All data stays synchronized between frontend and backend

---

## 🏗️ Architecture

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT (BROWSER)                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           Frontend Agents (UI Layer)                     │  │
│  │  ┌──────────────┬──────────────┬──────────────────────┐ │  │
│  │  │   Briefing   │  Front-end   │  SEO / UX/UI / QA   │ │  │
│  │  │   Agent      │   Agent      │  Agents             │ │  │
│  │  └──────────────┴──────────────┴──────────────────────┘ │  │
│  │                 ↓                                         │  │
│  │  ┌──────────────────────────────────────────────────────┐ │  │
│  │  │  Project Management Dashboard                        │ │  │
│  │  │  • Project Status                                   │ │  │
│  │  │  • Agent Progress                                  │ │  │
│  │  │  • Phase Tracking                                 │ │  │
│  │  └──────────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            ↕                                    │
│             HTTP + WebSocket Communication                      │
│                            ↕                                    │
├─────────────────────────────────────────────────────────────────┤
│                    NEXT.JS SERVER LAYER                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  API Routes (Next.js)                                   │  │
│  │  • /api/projects/*                                      │  │
│  │  • /api/agents/*                                        │  │
│  │  • /api/execution/*                                     │  │
│  │  • /api/status/*                                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  WebSocket Handler                                      │  │
│  │  • /ws/execution/:id                                   │  │
│  │  • Real-time agent updates                            │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────┬──────────────────────────┘
                                       ↕
                            HTTP + WebSocket
                                       ↕
┌──────────────────────────────────────────────────────────────────┐
│                 BACKEND (multi-agent-framework)                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │           Multi-Agent Execution Engine                  │   │
│  │  ┌──────────────┬──────────────┬──────────────────────┐ │   │
│  │  │ Architect    │ Analyst      │ Developer / Designer│ │   │
│  │  │ Agent        │ Agent        │ / SEO / QA Agents  │ │   │
│  │  └──────────────┴──────────────┴──────────────────────┘ │   │
│  │                ↓                                         │   │
│  │  ┌──────────────────────────────────────────────────────┐ │   │
│  │  │  7-Phase Execution Workflow                         │ │   │
│  │  │  1. Briefing Analysis                              │ │   │
│  │  │  2. Architecture Design                            │ │   │
│  │  │  3. Implementation Planning                        │ │   │
│  │  │  4. Code Generation (if enabled)                  │ │   │
│  │  │  5. Testing & QA                                  │ │   │
│  │  │  6. Documentation                                 │ │   │
│  │  │  7. Deployment & Monitoring                       │ │   │
│  │  └──────────────────────────────────────────────────────┘ │   │
│  └──────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Real-Time Communication                              │   │
│  │  • WebSocket updates to frontend                      │   │
│  │  • Agent state changes                                │   │
│  │  • Progress notifications                             │   │
│  │  • Debate/Discussion streaming                        │   │
│  └──────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Data Storage                                          │   │
│  │  • PostgreSQL (projects, results)                      │   │
│  │  • Redis (cache, real-time state)                     │   │
│  │  • File storage (documents, outputs)                  │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
1. USER INPUT (Frontend)
   ↓
   User submits project briefing in frontend dashboard
   
2. CREATE EXECUTION (Frontend → Backend)
   ↓
   POST /api/execute
   {
     briefing: "...",
     config: { ... }
   }
   ↓
   Backend creates execution_id and starts agents
   
3. AGENT EXECUTION (Backend)
   ↓
   Multi-agent framework processes briefing through 7 phases
   Each agent contributes analysis and decisions
   
4. REAL-TIME UPDATES (Backend → Frontend)
   ↓
   WebSocket: /ws/execution/:execution_id
   Updates sent for:
   • Agent status changes
   • Phase transitions
   • Decision points
   • Results completion
   
5. FRONTEND DISPLAY (Frontend UI)
   ↓
   Dashboard updates in real-time showing:
   • Current phase
   • Active agents
   • Progress percentage
   • Agent outputs/results
   
6. STORE RESULTS (Backend → Database)
   ↓
   Final results stored in PostgreSQL
   Results cached in Redis for quick access
   
7. RETRIEVE & DISPLAY (Frontend)
   ↓
   User retrieves completed project
   Results displayed in formatted dashboard
```

---

## 📡 API Contracts

### 1. Create Execution

**Endpoint:** `POST /api/execute`

**Request:**
```json
{
  "briefing": {
    "project_name": "E-commerce Platform",
    "description": "Build an online store with product catalog...",
    "objectives": ["Increase sales", "Improve UX"],
    "target_audience": "Online shoppers aged 25-45",
    "budget": 100000,
    "timeline": "3 months",
    "requirements": "Must-haves: product catalog, shopping cart, checkout...",
    "success_metrics": "100K monthly visitors, 2% conversion rate"
  },
  "config": {
    "phases": [1, 2, 3, 4, 5, 6],
    "agents": ["architect", "analyst", "developer", "designer", "qa"],
    "enable_debate": true,
    "debate_rounds": 2
  }
}
```

**Response:**
```json
{
  "execution_id": "exec_abc123def456",
  "status": "started",
  "created_at": "2026-04-13T10:00:00Z",
  "estimated_duration": 120,
  "phases": [
    {
      "phase_id": 1,
      "name": "Briefing Analysis",
      "status": "in_progress"
    }
  ]
}
```

### 2. Get Execution Status

**Endpoint:** `GET /api/execute/:execution_id/status`

**Response:**
```json
{
  "execution_id": "exec_abc123def456",
  "status": "processing",
  "current_phase": 2,
  "phase_name": "Architecture Design",
  "progress_percent": 25,
  "agents_active": ["architect", "analyst"],
  "started_at": "2026-04-13T10:00:00Z",
  "estimated_completion": "2026-04-13T12:00:00Z",
  "timeline": [
    {
      "phase": 1,
      "status": "completed",
      "duration": 20
    },
    {
      "phase": 2,
      "status": "in_progress",
      "duration": 15,
      "elapsed": 8
    }
  ]
}
```

### 3. Get Execution Results

**Endpoint:** `GET /api/execute/:execution_id/result`

**Response:**
```json
{
  "execution_id": "exec_abc123def456",
  "status": "completed",
  "briefing_analysis": {
    "goals": ["Increase sales", "Improve UX"],
    "target_personas": ["Online shopper", "Mobile user"],
    "key_requirements": ["Product catalog", "Checkout"],
    "market_analysis": "..."
  },
  "architecture": {
    "tech_stack": {
      "frontend": "Next.js + React + TypeScript",
      "backend": "Node.js + PostgreSQL",
      "deployment": "Vercel"
    },
    "system_design": "...",
    "api_design": "...",
    "data_models": "..."
  },
  "implementation_plan": {
    "phases": [...],
    "timeline": "...",
    "resources": "..."
  },
  "design_system": {
    "colors": "...",
    "components": "...",
    "pages": "..."
  },
  "code_generated": {
    "frontend": "...",
    "backend": "...",
    "database": "..."
  },
  "testing_strategy": "...",
  "deployment_guide": "...",
  "completion_time": "2026-04-13T12:00:00Z"
}
```

### 4. Get Agent Outputs

**Endpoint:** `GET /api/execute/:execution_id/agents/:agent_name`

**Response:**
```json
{
  "agent": "architect",
  "status": "completed",
  "phase": 2,
  "output": {
    "system_architecture": "...",
    "tech_recommendations": "...",
    "trade_offs": "...",
    "confidence": 0.95
  },
  "duration": 15,
  "tokens_used": 2500,
  "timestamp": "2026-04-13T10:15:00Z"
}
```

### 5. Get Execution History

**Endpoint:** `GET /api/execute/history?limit=10&status=completed`

**Response:**
```json
{
  "total": 42,
  "executions": [
    {
      "execution_id": "exec_abc123def456",
      "briefing_title": "E-commerce Platform",
      "status": "completed",
      "created_at": "2026-04-13T10:00:00Z",
      "completed_at": "2026-04-13T12:00:00Z",
      "duration": 120
    }
    // ... more executions
  ]
}
```

---

## 🔌 WebSocket Communication

### WebSocket Connection

**Endpoint:** `ws://localhost:3000/ws/execution/:execution_id`

**Connection:**
```javascript
// Frontend code
const ws = new WebSocket(
  `ws://localhost:3000/ws/execution/${executionId}`
);

ws.onopen = () => {
  console.log('Connected to execution stream');
};

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  handleExecutionUpdate(message);
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

ws.onclose = () => {
  console.log('Disconnected from execution stream');
};
```

### Message Types

**1. Phase Started**
```json
{
  "type": "phase_started",
  "phase_id": 2,
  "phase_name": "Architecture Design",
  "timestamp": "2026-04-13T10:05:00Z"
}
```

**2. Agent Started**
```json
{
  "type": "agent_started",
  "agent": "architect",
  "phase": 2,
  "timestamp": "2026-04-13T10:05:30Z"
}
```

**3. Agent Progress**
```json
{
  "type": "agent_progress",
  "agent": "architect",
  "phase": 2,
  "status": "analyzing_requirements",
  "progress_percent": 25,
  "timestamp": "2026-04-13T10:06:00Z"
}
```

**4. Agent Output**
```json
{
  "type": "agent_output",
  "agent": "architect",
  "phase": 2,
  "output_type": "analysis",
  "content": "...",
  "timestamp": "2026-04-13T10:07:00Z"
}
```

**5. Agent Debate**
```json
{
  "type": "debate",
  "agents": ["architect", "analyst"],
  "topic": "technology_stack",
  "messages": [
    {
      "agent": "architect",
      "message": "I recommend Next.js for frontend...",
      "timestamp": "2026-04-13T10:08:00Z"
    },
    {
      "agent": "analyst",
      "message": "I agree, but we should also consider...",
      "timestamp": "2026-04-13T10:08:30Z"
    }
  ]
}
```

**6. Decision Made**
```json
{
  "type": "decision",
  "topic": "tech_stack_frontend",
  "decision": "Next.js 14 with React and TypeScript",
  "reasoning": "Best performance and developer experience",
  "agents_consensus": ["architect", "analyst", "developer"],
  "timestamp": "2026-04-13T10:09:00Z"
}
```

**7. Phase Completed**
```json
{
  "type": "phase_completed",
  "phase_id": 2,
  "phase_name": "Architecture Design",
  "duration": 15,
  "results_summary": "...",
  "timestamp": "2026-04-13T10:20:00Z"
}
```

**8. Execution Completed**
```json
{
  "type": "execution_completed",
  "execution_id": "exec_abc123def456",
  "status": "completed",
  "total_duration": 120,
  "timestamp": "2026-04-13T12:00:00Z"
}
```

---

## 🔐 Authentication Flow

### Frontend to Backend Authentication

**1. User Login (Frontend)**
```typescript
// src/lib/api.ts
async function login(email: string, password: string) {
  const response = await fetch('/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  
  const { token, refreshToken } = await response.json();
  
  // Store tokens
  localStorage.setItem('token', token);
  localStorage.setItem('refreshToken', refreshToken);
  
  return token;
}
```

**2. Token Management**
```typescript
// src/lib/api.ts
class APIClient {
  private token: string | null = null;
  
  constructor() {
    this.token = localStorage.getItem('token');
  }
  
  async fetch(endpoint: string, options: RequestInit = {}) {
    const headers = {
      ...options.headers,
      'Authorization': `Bearer ${this.token}`
    };
    
    const response = await fetch(endpoint, { ...options, headers });
    
    if (response.status === 401) {
      // Token expired, try refresh
      await this.refreshToken();
      return this.fetch(endpoint, options);
    }
    
    return response;
  }
  
  async refreshToken() {
    const refreshToken = localStorage.getItem('refreshToken');
    const response = await fetch('/api/auth/refresh', {
      method: 'POST',
      body: JSON.stringify({ refreshToken })
    });
    
    const { token } = await response.json();
    this.token = token;
    localStorage.setItem('token', token);
  }
}
```

**3. Backend Verification**
```typescript
// backend (FastAPI middleware)
@app.middleware("http")
async def verify_token(request: Request, call_next):
    auth_header = request.headers.get("Authorization")
    
    if not auth_header:
        return JSONResponse({"error": "Missing auth"}, status_code=401)
    
    try:
        token = auth_header.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        request.state.user_id = payload["sub"]
    except:
        return JSONResponse({"error": "Invalid token"}, status_code=401)
    
    return await call_next(request)
```

**4. WebSocket Authentication**
```typescript
// Backend WebSocket handler
@app.websocket("/ws/execution/{execution_id}")
async def websocket_endpoint(websocket: WebSocket, execution_id: str):
    # Verify token from query params or headers
    token = websocket.query_params.get("token")
    
    if not verify_token(token):
        await websocket.close(code=4001, reason="Unauthorized")
        return
    
    await websocket.accept()
    # Start streaming execution updates
    await stream_execution_updates(websocket, execution_id)
```

---

## 💾 Data Models & Sync

### Database Schema (PostgreSQL)

```sql
-- Projects/Executions
CREATE TABLE executions (
  id VARCHAR PRIMARY KEY,
  user_id VARCHAR NOT NULL,
  briefing JSONB NOT NULL,
  config JSONB NOT NULL,
  status VARCHAR NOT NULL,
  current_phase INTEGER,
  progress_percent INTEGER,
  started_at TIMESTAMP,
  completed_at TIMESTAMP,
  results JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Agent Outputs
CREATE TABLE agent_outputs (
  id VARCHAR PRIMARY KEY,
  execution_id VARCHAR NOT NULL,
  agent VARCHAR NOT NULL,
  phase INTEGER,
  output_type VARCHAR,
  content JSONB,
  tokens_used INTEGER,
  duration INTEGER,
  timestamp TIMESTAMP DEFAULT NOW(),
  FOREIGN KEY (execution_id) REFERENCES executions(id)
);

-- Decisions/Debates
CREATE TABLE decisions (
  id VARCHAR PRIMARY KEY,
  execution_id VARCHAR NOT NULL,
  phase INTEGER,
  topic VARCHAR,
  decision TEXT,
  reasoning TEXT,
  agents_involved TEXT[],
  consensus BOOLEAN,
  timestamp TIMESTAMP DEFAULT NOW(),
  FOREIGN KEY (execution_id) REFERENCES executions(id)
);

-- Agent States
CREATE TABLE agent_states (
  id VARCHAR PRIMARY KEY,
  execution_id VARCHAR NOT NULL,
  agent VARCHAR NOT NULL,
  status VARCHAR,
  current_task VARCHAR,
  progress_percent INTEGER,
  timestamp TIMESTAMP DEFAULT NOW(),
  FOREIGN KEY (execution_id) REFERENCES executions(id)
);
```

### Data Sync Strategy

**Real-Time:**
- WebSocket for live updates (agent progress, phase changes)
- Redis pub/sub for internal backend communication
- PostgreSQL transactions for critical operations

**Caching:**
- Redis caches execution status (5-minute TTL)
- Redis caches agent outputs (until execution completes)
- Browser localStorage for UI state

**Conflict Resolution:**
- Last-write-wins for independent updates
- Operational transformation for collaborative edits
- Version numbers for optimistic locking

---

## ⚡ Real-Time Features

### Live Execution Dashboard

**Component:** `<ExecutionDashboard executionId={id} />`

```typescript
// src/components/education/ExecutionDashboard.tsx
export function ExecutionDashboard({ executionId }: Props) {
  const [execution, setExecution] = useState<Execution | null>(null);
  const [agents, setAgents] = useState<AgentState[]>([]);
  
  useEffect(() => {
    const ws = new WebSocket(`ws://.../ws/execution/${executionId}`);
    
    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      
      switch (message.type) {
        case 'phase_started':
          setExecution(prev => ({
            ...prev,
            current_phase: message.phase_id,
            progress_percent: calculateProgress(message.phase_id)
          }));
          break;
          
        case 'agent_progress':
          setAgents(prev => prev.map(agent =>
            agent.name === message.agent
              ? { ...agent, progress: message.progress_percent }
              : agent
          ));
          break;
          
        case 'agent_output':
          // Display output in real-time
          addAgentOutput(message.agent, message.content);
          break;
          
        case 'decision':
          addDecision(message);
          break;
      }
    };
    
    return () => ws.close();
  }, [executionId]);
  
  return (
    <div className="execution-dashboard">
      <PhaseProgressBar phase={execution?.current_phase} />
      <AgentStatusCards agents={agents} />
      <AgentOutputs outputs={execution?.outputs} />
      <DecisionLog decisions={execution?.decisions} />
    </div>
  );
}
```

### Agent Status Cards

```typescript
// Shows real-time agent status
<AgentCard
  agent="architect"
  status="processing"
  progress={45}
  task="Analyzing requirements"
/>

<AgentCard
  agent="analyst"
  status="waiting"
  progress={0}
  task="Waiting for architect output"
/>
```

### Live Output Streaming

```typescript
// Outputs appear in real-time as agent processes
<AgentOutputs>
  <Output agent="architect" type="analysis">
    "Based on the requirements, I recommend..."
  </Output>
  <Output agent="analyst" type="input">
    "I agree with architect's recommendation..."
  </Output>
</AgentOutputs>
```

---

## 🚨 Error Handling

### API Error Responses

```json
{
  "error": "invalid_briefing",
  "message": "Briefing is missing required field: objectives",
  "status": 400,
  "details": {
    "missing_fields": ["objectives"],
    "required_fields": ["objectives", "target_audience", ...]
  }
}
```

### WebSocket Error Handling

```typescript
ws.onerror = (error) => {
  // Handle connection errors
  showNotification('Connection error. Retrying...');
  
  // Implement exponential backoff retry
  setTimeout(() => {
    reconnectWebSocket();
  }, Math.pow(2, retryCount) * 1000);
};

ws.onclose = (event) => {
  if (event.code === 1000) {
    // Normal closure
  } else if (event.code === 4001) {
    // Unauthorized
    redirectToLogin();
  } else {
    // Unexpected closure, retry
    retryConnection();
  }
};
```

### Handling Interrupted Executions

```typescript
// Resume interrupted execution
async function resumeExecution(executionId: string) {
  const response = await fetch(`/api/execute/${executionId}/resume`, {
    method: 'POST'
  });
  
  if (response.ok) {
    const data = await response.json();
    // Reconnect WebSocket at current state
    connectToExecution(executionId);
  }
}
```

---

## 🚀 Deployment

### Frontend Deployment (Vercel)

```bash
# Environment variables (.env.production)
NEXT_PUBLIC_API_URL=https://api.example.com
NEXT_PUBLIC_WS_URL=wss://api.example.com
NEXTAUTH_URL=https://app.example.com
NEXTAUTH_SECRET=your_secret

# Deploy
vercel deploy --prod
```

### Backend Deployment (Docker)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### WebSocket Configuration

**For Production:**
```nginx
# Nginx proxy configuration
location /ws/ {
    proxy_pass http://backend:8000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_read_timeout 86400;
}
```

---

## 🧪 Testing Integration

### Integration Tests

```typescript
// tests/integration/execution.test.ts
describe('Execution Integration', () => {
  it('should create execution and stream updates via WebSocket', async () => {
    // 1. Create execution
    const res = await api.post('/api/execute', {
      briefing: mockBriefing,
      config: mockConfig
    });
    const { execution_id } = await res.json();
    
    // 2. Connect WebSocket
    const ws = new WebSocket(`ws://localhost/ws/execution/${execution_id}`);
    
    // 3. Listen for updates
    const updates: any[] = [];
    ws.onmessage = (event) => {
      updates.push(JSON.parse(event.data));
    };
    
    // 4. Wait for completion
    await waitForExecution(execution_id, 300000); // 5 min timeout
    
    // 5. Verify updates received
    expect(updates).toContainEqual(
      expect.objectContaining({ type: 'phase_started' })
    );
    expect(updates).toContainEqual(
      expect.objectContaining({ type: 'execution_completed' })
    );
  });
});
```

### E2E Tests

```typescript
// tests/e2e/execution-flow.spec.ts
test('Complete execution flow', async ({ page }) => {
  // 1. Navigate to project creation
  await page.goto('/dashboard');
  
  // 2. Fill briefing form
  await page.fill('[name="project_name"]', 'Test Project');
  await page.fill('[name="description"]', 'Test description');
  // ... fill other fields
  
  // 3. Submit
  await page.click('button:has-text("Create Project")');
  
  // 4. Wait for execution to start
  await page.waitForSelector('[data-testid="execution-dashboard"]');
  
  // 5. Monitor progress
  await page.waitForFunction(() => {
    const progress = document.querySelector('[data-testid="progress"]');
    return progress && parseInt(progress.textContent) === 100;
  }, { timeout: 300000 });
  
  // 6. Verify results
  await expect(page.locator('[data-testid="completion-message"]')).toBeVisible();
});
```

---

## 🔧 Troubleshooting

### WebSocket Connection Issues

**Problem:** WebSocket connection fails  
**Solution:**
```typescript
// Check backend is running
// Check firewall allows WebSocket
// Verify CORS headers
// Check browser console for errors
```

### Auth Token Expiration

**Problem:** Requests fail with 401 Unauthorized  
**Solution:**
```typescript
// Implement automatic token refresh
// Use refresh token endpoint
// Handle retry logic
// Redirect to login if refresh fails
```

### Data Sync Issues

**Problem:** Frontend and backend data out of sync  
**Solution:**
```typescript
// Force full sync on reconnection
// Implement version numbers
// Use ETag for caching
// Clear cache on major updates
```

### Performance Issues

**Problem:** Slow execution updates or lag  
**Solution:**
```typescript
// Reduce message frequency (batch updates)
// Implement compression for large messages
// Use Redis pub/sub for internal communication
// Monitor token usage and optimize prompts
```

---

## 📊 Monitoring & Logging

### Frontend Monitoring

```typescript
// src/lib/monitoring.ts
export function setupMonitoring() {
  // Error tracking
  Sentry.init({
    dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
    environment: process.env.NODE_ENV
  });
  
  // Performance monitoring
  initPerformanceMonitoring();
  
  // Analytics
  analytics.init({
    writeKey: process.env.NEXT_PUBLIC_ANALYTICS_KEY
  });
}
```

### Backend Logging

```python
# backend/logging_config.py
import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

# Log execution progress
logger.info("execution_started", extra={
    "execution_id": execution_id,
    "phase": 1
})
```

---

## ✅ Integration Checklist

### Before Deploying

- [ ] API endpoints all implemented and tested
- [ ] WebSocket connection working reliably
- [ ] Authentication flow complete
- [ ] Error handling for all scenarios
- [ ] Frontend and backend databases synced
- [ ] Real-time updates streaming correctly
- [ ] Monitoring and logging configured
- [ ] Load testing completed
- [ ] Security audit passed
- [ ] Documentation complete

### Deployment Steps

- [ ] Deploy backend to production
- [ ] Configure WebSocket proxy (Nginx/load balancer)
- [ ] Deploy frontend to Vercel
- [ ] Verify API endpoints from frontend
- [ ] Test WebSocket connection from frontend
- [ ] Monitor logs for errors
- [ ] Run smoke tests
- [ ] Notify team of deployment

---

**Version:** 1.0 | **Status:** ✅ Complete | **Last Updated:** April 2026

