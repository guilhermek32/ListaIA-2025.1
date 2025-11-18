# 📁 Project Structure

## Overview

The project has been reorganized with a clear separation between backend logic and documentation/configuration files.

## Current Structure

```
ListaIA-2025.1/
│
├── 📂 backend/                          # All backend files
│   ├── 🐍 __init__.py                   # Package initialization
│   ├── 🤖 llm.py                        # LLM integration (DSPy + Perplexity)
│   ├── 🍷 sistema_recomendacao_vinho.py # Core recommendation engine
│   ├── 🔗 sistema_integrado.py          # Integrated system (KNN + LLM)
│   ├── ⚙️  main.py                       # Alternative entry point
│   ├── ⚙️  config.py                     # Configuration settings
│   ├── 🧩 dspy_modules.py               # DSPy module definitions
│   ├── 🛠️  utils.py                      # Utility functions
│   ├── 📊 pratos.csv                    # 100 dishes database
│   ├── 📊 vinhos.csv                    # 28 wines database
│   ├── 📊 regras.csv                    # 28 harmonization rules
│   └── 📖 README.md                     # Backend documentation
│
├── 📂 __pycache__/                      # Python cache (auto-generated)
├── 📂 .venv/                            # Virtual environment
│
├── 🚀 run.py                            # Main launcher script
├── 📄 .env                              # Environment variables (gitignored)
├── 📄 .env.example                      # Environment template
├── 📄 .gitignore                        # Git ignore rules
├── 📄 .python-version                   # Python version spec
├── 📄 pyproject.toml                    # Project configuration
├── 📄 uv.lock                           # Dependency lock file
│
└── 📚 Documentation Files
    ├── README.md                        # Main project README
    ├── QUICKSTART.md                    # Quick start guide
    ├── TUTORIAL.md                      # Detailed tutorial
    ├── BUGS_FIXED.md                    # Bug fixes documentation
    ├── ARQUITETURA.md                   # Architecture overview
    ├── LLM_INTEGRATION.md               # LLM integration details
    ├── PERPLEXITY_MIGRATION.md          # Migration guide
    ├── EXEMPLO_SAIDA.md                 # Output examples
    ├── INDEX.md                         # Documentation index
    └── STRUCTURE.md                     # This file
```

## File Descriptions

### Backend Folder (`backend/`)

#### Core System Files
- **`llm.py`** - LLM integration using DSPy framework with Perplexity API
  - Configure LLM with `configurar_llm()`
  - Generate justifications with `gerar_justificativa_vinho()`
  
- **`sistema_recomendacao_vinho.py`** - Wine recommendation engine
  - KNN-based similarity matching
  - Cosine similarity for feature comparison
  - Domain rules for wine-food pairing
  - Main function: `recomendar_vinho()`
  
- **`sistema_integrado.py`** - Complete integrated system
  - Combines recommendations with LLM justifications
  - Main function: `sistema_completo_com_justificativa()`

#### Supporting Files
- **`main.py`** - Alternative entry point with examples
- **`config.py`** - Configuration and settings management
- **`dspy_modules.py`** - DSPy module definitions
- **`utils.py`** - Utility functions and helpers
- **`__init__.py`** - Package initialization and exports

#### Data Files
- **`pratos.csv`** - 100 dishes with characteristics
  - Columns: nome_prato, tipo_prato, temperos, acidez, intensidade_sabor, ingredientes
  
- **`vinhos.csv`** - 28 wine types
  - Columns: vinho, tipo_vinho
  
- **`regras.csv`** - 28 harmonization rules
  - Wine-food pairing expert knowledge

### Root Level Files

#### Executables
- **`run.py`** - Main launcher script
  - Run from project root
  - Automatically adds backend to Python path
  - Includes example usage

#### Configuration
- **`.env`** - Environment variables (not in git)
  - PERPLEXITY_API_KEY
  - DEBUG, LOG_LEVEL, etc.
  
- **`.env.example`** - Template for .env file
- **`pyproject.toml`** - Python project configuration
- **`uv.lock`** - Locked dependencies
- **`.python-version`** - Python version specification
- **`.gitignore`** - Git ignore patterns

#### Documentation
- **`README.md`** - Main project documentation
- **`QUICKSTART.md`** - Quick start guide
- **`TUTORIAL.md`** - Step-by-step tutorial
- **`BUGS_FIXED.md`** - List of fixed bugs
- **`ARQUITETURA.md`** - System architecture
- **`LLM_INTEGRATION.md`** - LLM integration details
- **`STRUCTURE.md`** - This file

## Import Paths

### From Project Root
```python
# Add backend to path
import sys
sys.path.insert(0, 'backend')

# Now import normally
from sistema_integrado import sistema_completo_com_justificativa
```

### From Backend Folder
```python
# Direct imports when in backend/
from llm import configurar_llm, gerar_justificativa_vinho
from sistema_recomendacao_vinho import recomendar_vinho
from sistema_integrado import sistema_completo_com_justificativa
```

### As Package
```python
# If installed as package
from backend import configurar_llm, recomendar_vinho
```

## Running the System

### Option 1: From Root (Recommended)
```bash
python run.py
```

### Option 2: Direct Backend
```bash
cd backend
python sistema_integrado.py
```

### Option 3: Individual Modules
```bash
cd backend
python sistema_recomendacao_vinho.py  # Recommendations only
python llm.py                          # LLM only
python main.py                         # Alternative entry
```

## Data Flow

```
User Input (Dish Name)
        ↓
[sistema_integrado.py]
        ↓
[sistema_recomendacao_vinho.py]
        ↓
    ┌───────────────────────┐
    │  Load Data            │
    │  - pratos.csv         │
    │  - vinhos.csv         │
    │  - regras.csv         │
    └───────────────────────┘
        ↓
    ┌───────────────────────┐
    │  Calculate Scores     │
    │  - Feature similarity │
    │  - Rule-based match   │
    └───────────────────────┘
        ↓
    Top 3 Wines
        ↓
[llm.py] (if enabled)
        ↓
    ┌───────────────────────┐
    │  Generate             │
    │  Justification        │
    │  (via Perplexity)     │
    └───────────────────────┘
        ↓
Final Output (Recommendations + Justification)
```

## Dependencies Location

All dependencies defined in `pyproject.toml`:
- pandas
- numpy
- scikit-learn
- dspy-ai
- python-dotenv

Installed in `.venv/` virtual environment.

## Changes from Previous Structure

### Before
```
src/
├── listaia_2025_1/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   └── ...
├── llm.py
├── sistema_recomendacao_vinho.py
├── pratos.csv
└── ...
```

### After
```
backend/
├── __init__.py
├── llm.py
├── sistema_recomendacao_vinho.py
├── sistema_integrado.py
├── config.py
├── main.py
├── pratos.csv
├── vinhos.csv
└── regras.csv
```

**Benefits:**
- ✅ Clearer organization
- ✅ All backend files in one place
- ✅ Data files with code that uses them
- ✅ Easier to navigate
- ✅ Simpler imports
- ✅ Better for future API development

## Future Extensions

The backend folder is ready for:
- 🔮 REST API (FastAPI/Flask)
- 🔮 GraphQL endpoint
- 🔮 Database integration
- 🔮 Caching layer
- 🔮 Message queue support
- 🔮 Frontend integration

Simply keep all backend logic in `backend/` and add new folders for frontend, API, etc.
