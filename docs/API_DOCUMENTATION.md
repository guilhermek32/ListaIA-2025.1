# 🚀 API Documentation

## Wine Recommendation API

FastAPI backend that connects the Next.js frontend with the Python recommendation engine.

## 📍 Base URL

```
http://localhost:8000
```

## 🔌 Endpoints

### 1. Health Check
**GET** `/`

Returns API status and configuration.

**Response:**
```json
{
  "status": "online",
  "service": "Wine Recommendation API",
  "version": "1.0.0",
  "llm_available": true,
  "dishes_count": 100,
  "wines_count": 28
}
```

---

### 2. Detailed Health Check
**GET** `/health`

Returns detailed system health information.

**Response:**
```json
{
  "status": "healthy",
  "llm_configured": true,
  "database": {
    "pratos": 100,
    "vinhos": 28
  }
}
```

---

### 3. Wine Recommendation (Main Endpoint)
**POST** `/api/recomendacao`

Get wine recommendation with AI-generated justification.

**Request Body:**
```json
{
  "mensagem": "Sushi"
}
```

**Response:**
```json
{
  "prato": "Sushi",
  "vinho": {
    "nome": "Pinot Grigio",
    "tipo": "branco seco",
    "similaridade": 98.14,
    "score_features": 95.35,
    "score_regras": 100.0
  },
  "justificativa": "O Pinot Grigio harmoniza perfeitamente com Sushi devido à sua acidez refrescante...",
  "mensagem": "🍷 **Pinot Grigio** (branco seco)\n\n📊 **Compatibilidade:** 98.1%\n\n✨ **Justificativa:**\n..."
}
```

**Error Response (Dish Not Found):**
```json
{
  "prato": "",
  "vinho": {
    "nome": "",
    "tipo": "",
    "similaridade": 0,
    "score_features": 0,
    "score_regras": 0
  },
  "justificativa": "",
  "mensagem": "Desculpe, não encontrei informações sobre \"Pizza\". Tente mencionar um prato específico..."
}
```

---

### 4. List Dishes
**GET** `/api/pratos`

Returns list of available dishes.

**Response:**
```json
{
  "total": 100,
  "pratos": [
    "Sushi",
    "Salmão grelhado",
    "Picanha na brasa",
    ...
  ],
  "message": "Total de 100 pratos disponíveis"
}
```

---

### 5. List Wines
**GET** `/api/vinhos`

Returns list of all wines.

**Response:**
```json
{
  "total": 28,
  "vinhos": [
    {
      "vinho": "Cabernet Sauvignon",
      "tipo_vinho": "tinto seco"
    },
    {
      "vinho": "Pinot Grigio",
      "tipo_vinho": "branco seco"
    },
    ...
  ]
}
```

---

## 🔧 How It Works

### Request Flow

```
Frontend (Next.js)
      ↓
POST /api/recomendacao
      ↓
FastAPI Backend (api.py)
      ↓
┌─────────────────────────┐
│ 1. Parse dish name      │
│ 2. Search in CSV        │
│ 3. Find matches         │
└─────────────────────────┘
      ↓
Python Backend (backend/)
      ↓
┌─────────────────────────┐
│ sistema_recomendacao_   │
│ vinho.py                │
│ - KNN similarity        │
│ - Rule-based scoring    │
└─────────────────────────┘
      ↓
┌─────────────────────────┐
│ llm.py                  │
│ - Generate              │
│   justification         │
│ - Perplexity API        │
└─────────────────────────┘
      ↓
Response to Frontend
```

### Scoring Algorithm

```python
Final Score = (40% × Feature Similarity) + (60% × Rule-Based Score)
```

- **Feature Similarity**: Cosine similarity between dish and wine characteristics
- **Rule-Based Score**: Expert wine-pairing knowledge

---

## 🚀 Running the API

### Option 1: Direct Python
```bash
python api.py
```

### Option 2: Uvicorn
```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### Option 3: With uv
```bash
uv run python api.py
```

---

## 🔑 Environment Variables

Required in `.env`:
```env
PERPLEXITY_API_KEY=your_perplexity_api_key_here
```

Optional:
```env
DEBUG=False
LOG_LEVEL=INFO
```

---

## 🧪 Testing the API

### Using cURL

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Get Recommendation:**
```bash
curl -X POST http://localhost:8000/api/recomendacao \
  -H "Content-Type: application/json" \
  -d '{"mensagem": "Sushi"}'
```

**List Dishes:**
```bash
curl http://localhost:8000/api/pratos
```

### Using Python

```python
import requests

# Get recommendation
response = requests.post(
    "http://localhost:8000/api/recomendacao",
    json={"mensagem": "Salmão grelhado"}
)
print(response.json())
```

### Using JavaScript/TypeScript (Frontend)

```typescript
const response = await fetch('http://localhost:8000/api/recomendacao', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ mensagem: 'Sushi' }),
});

const data = await response.json();
console.log(data);
```

---

## 📊 Response Schema

### RecomendacaoResponse

```typescript
interface RecomendacaoResponse {
  prato: string;              // Dish name
  vinho: VinhoResponse;       // Wine details
  justificativa: string;      // AI-generated justification
  mensagem: string;           // Formatted message for display
}

interface VinhoResponse {
  nome: string;               // Wine name
  tipo: string;               // Wine type (e.g., "branco seco")
  similaridade: number;       // Overall similarity (0-100)
  score_features: number;     // Feature-based score (0-100)
  score_regras: number;       // Rule-based score (0-100)
}
```

---

## ⚡ Performance

- **Average Response Time**: 2-5 seconds (with LLM)
- **Without LLM**: < 100ms
- **Concurrent Requests**: Supports multiple simultaneous requests
- **Caching**: DataFrames cached in memory for fast access

---

## 🛡️ CORS Configuration

The API allows requests from:
- `http://localhost:3000`
- `http://127.0.0.1:3000`

To add more origins, edit `api.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://your-domain.com"],
    ...
)
```

---

## 🐛 Error Handling

### 400 Bad Request
```json
{
  "detail": "Mensagem é obrigatória"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Erro ao processar recomendação: <error message>"
}
```

---

## 📝 Logs

The API logs to console:
```
🍷 Wine Recommendation API
================================================================================
📊 Loaded 100 dishes and 28 wines
🤖 LLM Status: ✅ Available
================================================================================
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## 🔗 Integration with Frontend

The Next.js frontend automatically connects to the API:

1. **Frontend runs on**: `http://localhost:3000`
2. **API runs on**: `http://localhost:8000`
3. **Frontend calls**: `http://localhost:8000/api/recomendacao`

Make sure both servers are running:
```bash
# Terminal 1: Backend API
python api.py

# Terminal 2: Frontend
npm run dev
```

---

## 📚 Dependencies

- **FastAPI**: Modern web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **pandas**: Data manipulation
- **scikit-learn**: ML algorithms
- **dspy-ai**: LLM framework

Install with:
```bash
uv sync
# or
pip install fastapi uvicorn[standard] pandas scikit-learn dspy-ai python-dotenv
```

---

## 🎯 Future Improvements

- [ ] Add authentication (API keys)
- [ ] Implement rate limiting
- [ ] Add request caching (Redis)
- [ ] Support for batch requests
- [ ] WebSocket support for streaming responses
- [ ] Add Swagger/OpenAPI documentation UI
- [ ] Add metrics and monitoring
- [ ] Docker containerization

---

**Made with 🍷 and 🐍**
