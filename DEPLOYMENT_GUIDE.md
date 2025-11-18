# 🚀 Deployment Guide - VineChat Wine Recommendation System

## ✅ System Status

**Current Phase**: FULLY FUNCTIONAL ✅

- ✅ Backend API (Python FastAPI) - Running on http://localhost:8000
- ✅ Frontend (Next.js) - Running on http://localhost:3000
- ✅ ML Recommendation Engine - Working with 100 dishes, 28 wines
- ✅ AI Justifications (Perplexity LLM) - Configured and operational
- ✅ Full-stack Integration - Frontend ↔ Backend connected

---

## 🎯 Quick Start

### Windows

```bash
# Navigate to project
cd C:\Users\gui\Documents\code\Lista2-IA\ListaIA-2025.1

# Run startup script (starts both servers)
start.bat
```

### Linux/Mac

```bash
# Navigate to project
cd ListaIA-2025.1

# Make script executable
chmod +x start.sh

# Run startup script
./start.sh
```

### Manual Start (for troubleshooting)

**Terminal 1 - Backend API:**
```bash
cd ListaIA-2025.1
python api.py
```

**Terminal 2 - Frontend:**
```bash
cd ListaIA-2025.1
npm run dev
```

---

## 🔧 System Architecture

```
┌─────────────────────────────────────────────────────┐
│                   USER BROWSER                      │
│              http://localhost:3000                  │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│             Next.js Frontend (React)                │
│  - Chat Interface (components/Chat.tsx)             │
│  - API Route Proxy (app/api/recomendacao/route.ts) │
└────────────────────┬────────────────────────────────┘
                     │ HTTP POST /api/recomendacao
                     ▼
┌─────────────────────────────────────────────────────┐
│          Python FastAPI Backend (api.py)            │
│  - Receives dish name                               │
│  - Searches in CSV database                         │
│  - Calculates wine recommendations                  │
│  - Generates AI justification                       │
└────────────────────┬────────────────────────────────┘
                     │
         ┌───────────┴────────────┐
         ▼                        ▼
┌──────────────────┐   ┌──────────────────────┐
│  ML Engine       │   │  Perplexity LLM API  │
│  (scikit-learn)  │   │  (DSPy + Sonar)      │
│  - Similarity    │   │  - Justification     │
│  - Rules         │   │  - Portuguese        │
└──────────────────┘   └──────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│        CSV Databases                │
│  - pratos.csv (100 dishes)          │
│  - vinhos.csv (28 wines)            │
│  - regras.csv (28 pairing rules)    │
└─────────────────────────────────────┘
```

---

## 📊 API Endpoints

### Backend API (http://localhost:8000)

#### Health Check
```bash
GET http://localhost:8000/
GET http://localhost:8000/health
```

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

#### Wine Recommendation
```bash
POST http://localhost:8000/api/recomendacao
Content-Type: application/json

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
    "similaridade": 98.1,
    "score_features": 95.35,
    "score_regras": 100.0
  },
  "justificativa": "A harmonização entre o sushi e o vinho Pinot Grigio...",
  "mensagem": "🍷 **Pinot Grigio** (branco seco)\n\n📊 **Compatibilidade:** 98.1%..."
}
```

#### List Dishes
```bash
GET http://localhost:8000/api/pratos
```

#### List Wines
```bash
GET http://localhost:8000/api/vinhos
```

---

## 🧪 Testing

### Test Backend API

```bash
# Health check
curl http://localhost:8000/health

# Test recommendation
curl -X POST http://localhost:8000/api/recomendacao \
  -H "Content-Type: application/json" \
  -d '{"mensagem": "Sushi"}'

# List all dishes
curl http://localhost:8000/api/pratos

# List all wines
curl http://localhost:8000/api/vinhos
```

### Test Frontend

1. Open browser: http://localhost:3000
2. Type a dish name (e.g., "Sushi", "Feijoada", "Salmão")
3. Click "Enviar"
4. Verify you receive:
   - Wine recommendation
   - Compatibility percentage
   - AI-generated justification in Portuguese

---

## 🔑 Environment Variables

### Required (.env file in project root)

```env
# Perplexity API Key (for AI justifications)
PERPLEXITY_API_KEY=pplx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Optional
DEBUG=true
LOG_LEVEL=INFO
```

### How to Get API Key

1. Visit https://www.perplexity.ai/
2. Sign up for an account
3. Navigate to API settings
4. Generate API key
5. Add to `.env` file

**Note:** System works without API key but justifications will be basic fallback text.

---

## 📦 Dependencies

### Python (Backend)

Installed via `uv pip install`:

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `dspy-ai` - LLM integration framework
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `scikit-learn` - ML algorithms
- `python-dotenv` - Environment variables

### JavaScript (Frontend)

Installed via `npm install`:

- `next` - React framework
- `react` - UI library
- `react-dom` - React DOM renderer
- `typescript` - Type safety

---

## 🐛 Troubleshooting

### Backend Issues

**Problem:** `ModuleNotFoundError`
```bash
# Solution: Install dependencies
cd ListaIA-2025.1
uv pip install dspy-ai numpy pandas python-dotenv scikit-learn fastapi uvicorn[standard]
```

**Problem:** `FileNotFoundError: pratos.csv`
```bash
# Solution: Backend needs to run from correct directory
cd ListaIA-2025.1
python api.py  # NOT from backend/ folder
```

**Problem:** API key errors
```bash
# Solution: Check .env file exists and has correct key
cat .env  # Linux/Mac
type .env  # Windows
```

### Frontend Issues

**Problem:** `Cannot connect to server`
```bash
# Solution: Make sure backend is running first
# Terminal 1:
python api.py

# Terminal 2 (after backend starts):
npm run dev
```

**Problem:** Build errors
```bash
# Solution: Reinstall dependencies
rm -rf node_modules package-lock.json  # Linux/Mac
# or
rd /s node_modules & del package-lock.json  # Windows

npm install
```

### Integration Issues

**Problem:** Frontend can't reach backend
```bash
# Solution: Check CORS settings in api.py
# Should allow http://localhost:3000
```

**Problem:** Wrong API endpoint
```bash
# Frontend calls: http://localhost:8000/api/recomendacao
# Backend expects: POST with {"mensagem": "dish name"}
```

---

## 🎨 Customization

### Add New Dishes

Edit `backend/pratos.csv`:
```csv
101,Pizza Margherita,"tomate, mussarela, manjericão",massa,herbal,média,média
```

Columns: `id_prato,nome_prato,ingredientes,tipo_prato,temperos,acidez,intensidade_sabor`

### Add New Wines

Edit `backend/vinhos.csv`:
```csv
Prosecco,espumante
```

Update characteristics in `backend/sistema_recomendacao_vinho.py`

### Add Pairing Rules

Edit `backend/regras.csv`:
```csv
Prosecco,massa,Pizza
```

---

## 📈 Performance

- **Backend Response Time**: 2-4 seconds (with LLM)
- **Backend Response Time**: <100ms (without LLM)
- **Frontend Load Time**: ~1 second
- **Concurrent Users**: ~10-20 (development server)
- **LLM Cost**: ~$0.002 per recommendation

---

## 🚀 Production Deployment

### Option 1: Cloud Platform (Recommended)

**Backend (Python):**
- Deploy to: Heroku, Railway, Render, Google Cloud Run
- Use: Dockerfile or buildpack
- Expose: Port 8000
- Environment: Add PERPLEXITY_API_KEY

**Frontend (Next.js):**
- Deploy to: Vercel, Netlify, Cloudflare Pages
- Environment: Add PYTHON_API_URL=https://your-backend.com

### Option 2: Docker

```dockerfile
# Backend Dockerfile
FROM python:3.11
WORKDIR /app
COPY backend/ ./backend/
COPY api.py .
COPY pyproject.toml .
RUN pip install fastapi uvicorn dspy-ai pandas numpy scikit-learn python-dotenv
CMD ["python", "api.py"]
```

```dockerfile
# Frontend Dockerfile
FROM node:20
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
CMD ["npm", "start"]
```

### Option 3: VPS (Ubuntu)

```bash
# Install dependencies
sudo apt update
sudo apt install python3 python3-pip nodejs npm

# Clone/upload project
cd /var/www/vinechat

# Setup backend
pip3 install -r requirements.txt
python3 api.py &

# Setup frontend
npm install
npm run build
npm start
```

---

## 📚 Documentation Files

- `README.md` - Project overview
- `QUICKSTART.md` - 3-command start guide
- `TUTORIAL.md` - Detailed tutorial
- `ARQUITETURA.md` - Technical architecture
- `LLM_INTEGRATION.md` - AI integration guide
- `STRUCTURE.md` - File structure
- `BUGS_FIXED.md` - Bug fixes log
- `DEPLOYMENT_GUIDE.md` - This file

---

## ✅ Final Checklist

Before going live:

- [ ] .env file configured with API key
- [ ] Both servers start without errors
- [ ] Can make recommendation via browser
- [ ] AI justifications are generated
- [ ] CSV files are accessible
- [ ] CORS allows frontend domain
- [ ] Error handling works
- [ ] Production environment variables set

---

## 🎉 Success!

Your VineChat system is now fully operational!

**Test it:**
1. Start both servers: `start.bat` (Windows) or `./start.sh` (Linux/Mac)
2. Open browser: http://localhost:3000
3. Type "Sushi" and click "Enviar"
4. Enjoy your wine recommendation! 🍷

**Questions?** Check the documentation files or review the code comments.
