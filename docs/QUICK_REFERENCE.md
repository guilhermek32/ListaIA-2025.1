# 🍷 VineChat - Quick Reference Guide

## 🚀 Start the System

### Windows (Easiest)
```bash
start.bat
```

### Linux/Mac
```bash
./start.sh
```

### Manual (Both Servers)
```bash
# Terminal 1 - Backend
python api.py

# Terminal 2 - Frontend  
npm run dev
```

## 🧪 Test the System

```bash
# Run automated tests
python test_system.py
```

## 🌐 Access URLs

- **Frontend (Chat Interface):** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Health:** http://localhost:8000/health
- **API Docs:** http://localhost:8000/docs (FastAPI auto-generated)

## 📝 Quick API Examples

### Get Recommendation
```bash
curl -X POST http://localhost:8000/api/recomendacao \
  -H "Content-Type: application/json" \
  -d '{"mensagem": "Sushi"}'
```

### List All Dishes
```bash
curl http://localhost:8000/api/pratos
```

### List All Wines
```bash
curl http://localhost:8000/api/vinhos
```

## 🔧 Common Commands

### Check Dependencies
```bash
# Python
python -c "import fastapi, pandas, dspy; print('✅ OK')"

# Node.js
npm list --depth=0
```

### Reinstall Dependencies
```bash
# Python
uv pip install fastapi uvicorn dspy-ai pandas numpy scikit-learn python-dotenv

# Node.js
npm install
```

### View Logs
```bash
# Backend runs in terminal - logs show in real-time
# Frontend runs in terminal - logs show in real-time
```

## 🗂️ File Structure

```
ListaIA-2025.1/
├── api.py                  # FastAPI backend server
├── start.bat              # Windows startup script
├── start.sh               # Linux/Mac startup script
├── test_system.py         # Automated test suite
├── backend/               # Backend Python code
│   ├── sistema_recomendacao_vinho.py  # ML engine
│   ├── llm.py                         # AI integration
│   ├── sistema_integrado.py           # Combined system
│   ├── pratos.csv                     # 100 dishes
│   ├── vinhos.csv                     # 28 wines
│   └── regras.csv                     # 28 pairing rules
├── app/                   # Next.js app
│   ├── api/
│   │   └── recomendacao/
│   │       └── route.ts              # API proxy
│   ├── page.tsx                      # Home page
│   └── layout.tsx                    # Layout
└── components/
    └── Chat.tsx                      # Chat interface
```

## 📚 Documentation

- `README.md` - Project overview
- `QUICKSTART.md` - Quick start (3 commands)
- `TUTORIAL.md` - Step-by-step tutorial
- `DEPLOYMENT_GUIDE.md` - Full deployment guide
- `INTEGRATION_COMPLETE.md` - Integration status
- `ARQUITETURA.md` - Technical architecture
- `LLM_INTEGRATION.md` - AI/LLM details
- `STRUCTURE.md` - File structure
- `BUGS_FIXED.md` - Bug fixes log

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.10+

# Reinstall dependencies
uv pip install fastapi uvicorn dspy-ai pandas numpy scikit-learn python-dotenv
```

### Frontend won't start
```bash
# Check Node version
node --version  # Should be 18+

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### "Cannot connect to backend"
```bash
# Make sure backend is running first
python api.py

# Check if it's accessible
curl http://localhost:8000/health
```

### "CSV file not found"
```bash
# Run from project root, not backend/
cd ListaIA-2025.1
python api.py  # ✓ Correct
# NOT: cd backend && python ../api.py  # ✗ Wrong
```

## 🎯 Example Dishes to Try

- Sushi
- Feijoada
- Salmão grelhado
- Picanha
- Risotto
- Pizza Margherita
- Bacalhau
- Paella
- Yakisoba
- Ceviche

## ⚙️ Environment Variables

Create `.env` file in project root:

```env
# Required for AI justifications
PERPLEXITY_API_KEY=pplx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Optional
DEBUG=true
LOG_LEVEL=INFO
```

## 📊 Performance

- Backend response (with AI): 2-4 seconds
- Backend response (without AI): <100ms
- Frontend load: ~1 second
- Concurrent users: 10-20 (dev server)

## 🆘 Need Help?

1. Check documentation files
2. Run `python test_system.py` to diagnose issues
3. Check server logs in terminals
4. Verify `.env` file exists with API key

## ✅ Health Check

```bash
# Quick system check
curl http://localhost:8000/health && \
curl http://localhost:3000 && \
echo "✅ System is healthy!"
```

---

**Last Updated:** 2025-11-18  
**Status:** ✅ Fully Operational
