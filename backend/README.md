# 🍷 Wine Recommendation System

Sistema inteligente de recomendação de vinhos com justificativas geradas por IA.

## 📁 Project Structure

```
ListaIA-2025.1/
├── backend/                    # Backend logic and data
│   ├── __init__.py            # Package initialization
│   ├── llm.py                 # LLM integration (DSPy + Perplexity)
│   ├── sistema_recomendacao_vinho.py  # Recommendation engine
│   ├── sistema_integrado.py   # Integrated system
│   ├── main.py                # Alternative entry point
│   ├── config.py              # Configuration
│   ├── dspy_modules.py        # DSPy modules
│   ├── utils.py               # Utilities
│   ├── pratos.csv             # Dishes database (100 records)
│   ├── vinhos.csv             # Wines database (28 records)
│   ├── regras.csv             # Harmonization rules
│   └── README.md              # Backend documentation
├── .env                       # Environment variables (create from .env.example)
├── .env.example               # Environment template
├── pyproject.toml             # Python project configuration
├── run.py                     # Main launcher script
├── README.md                  # This file
├── QUICKSTART.md              # Quick start guide
├── TUTORIAL.md                # Detailed tutorial
├── BUGS_FIXED.md              # Bug fixes documentation
└── docs/                      # Documentation files
    ├── ARQUITETURA.md
    ├── LLM_INTEGRATION.md
    ├── PERPLEXITY_MIGRATION.md
    └── EXEMPLO_SAIDA.md
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

### 2. Configure API Key

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your Perplexity API key
# PERPLEXITY_API_KEY=your_key_here
```

Get your API key at: https://www.perplexity.ai/settings/api

### 3. Run the System

```bash
# Run from project root
python run.py

# Or run directly in backend folder
cd backend
python sistema_integrado.py
```

## 🎯 Features

- ✅ **Smart Recommendations**: KNN-based similarity + domain rules
- ✅ **AI Justifications**: Natural language explanations via Perplexity LLM
- ✅ **100 Dishes Database**: Comprehensive food database
- ✅ **28 Wine Types**: Curated wine selection
- ✅ **Harmonization Rules**: Expert food-wine pairing knowledge
- ✅ **Dual Scoring**: Feature similarity + rule-based scoring

## 📊 How It Works

1. **Input**: User provides a dish name
2. **Feature Matching**: System analyzes dish characteristics (acidity, intensity, seasoning)
3. **KNN Algorithm**: Finds similar wines using cosine similarity
4. **Rule Application**: Applies expert harmonization rules
5. **Scoring**: Combines similarity (40%) + rules (60%)
6. **LLM Justification**: Generates natural language explanation

### Scoring Formula
```
Final Score = (40% × Feature Similarity) + (60% × Rule-Based Score)
```

## 🔧 Usage Examples

### Basic Recommendation
```python
from backend import recomendar_vinho
from backend.sistema_recomendacao_vinho import df_pratos, df_vinhos

recommendations = recomendar_vinho("Sushi", df_pratos, df_vinhos, top_n=3)
print(recommendations)
```

### Full System with AI
```python
from backend import sistema_completo_com_justificativa

# Requires PERPLEXITY_API_KEY in .env
sistema_completo_com_justificativa("Sushi", usar_llm=True)
```

### Generate Justification Only
```python
from backend import configurar_llm, gerar_justificativa_vinho

configurar_llm()

justification = gerar_justificativa_vinho(
    nome_prato="Sushi",
    caracteristicas_prato={...},
    vinho_info={...}
)
```

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide
- **[TUTORIAL.md](TUTORIAL.md)** - Detailed tutorial
- **[backend/README.md](backend/README.md)** - Backend documentation
- **[BUGS_FIXED.md](BUGS_FIXED.md)** - Fixed bugs list
- **[ARQUITETURA.md](ARQUITETURA.md)** - Architecture overview
- **[LLM_INTEGRATION.md](LLM_INTEGRATION.md)** - LLM integration details

## 🧪 Testing

```bash
# Test recommendation system only
cd backend
python sistema_recomendacao_vinho.py

# Test integrated system with LLM
cd backend
python sistema_integrado.py

# Test LLM module standalone
cd backend
python llm.py
```

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
PERPLEXITY_API_KEY=your_perplexity_api_key_here
DEBUG=False
LOG_LEVEL=INFO
```

## 🛠️ Technology Stack

- **Python 3.11+**
- **pandas** - Data manipulation
- **numpy** - Numerical operations
- **scikit-learn** - KNN and similarity calculations
- **DSPy** - LLM framework
- **Perplexity API** - LLM provider (llama-3.1-sonar)
- **python-dotenv** - Environment management

## 📈 Performance

- Recommendation: < 100ms
- LLM Justification: 2-5 seconds
- Database: 100 dishes, 28 wines

## 🐛 Known Issues

All known bugs have been fixed. See [BUGS_FIXED.md](BUGS_FIXED.md) for details.

## 📝 License

Educational project - Free to use and modify

## 👥 Contributors

- AI/ML Implementation
- Wine Domain Knowledge Integration
- Natural Language Generation

## 🤝 Contributing

This is an educational project. Feel free to fork and experiment!

## 📞 Support

For issues or questions, check the documentation in the `docs/` folder or review the code comments.

---

**Made with 🍷 and 🤖**
