# Quick Start Guide - Wine Recommendation System 🍷

## Install & Run (3 commands)

```bash
# 1. Navigate to project
cd C:\Users\gui\Documents\code\Lista2-IA\ListaIA-2025.1

# 2. Install dependencies (if not done yet)
uv sync

# 3. Run the system
uv run python sistema_recomendacao_vinho.py
```

## Common Commands

### Run with custom dishes
```python
# Edit the end of sistema_recomendacao_vinho.py:
pratos_teste = ["Sushi", "Feijoada", "Paella"]
```

### Interactive mode
```bash
uv run python
```
```python
from sistema_recomendacao_vinho import sistema_recomendacao_vinho
sistema_recomendacao_vinho("Sushi")
```

### List all available dishes
```python
import pandas as pd
df = pd.read_csv('pratos.csv')
print(df['nome_prato'].tolist())
```

## Example Output

```
🍷 SISTEMA DE RECOMENDAÇÃO DE VINHOS 🍷

Prato selecionado: Sushi

🏆 TOP 3 VINHOS RECOMENDADOS

1º lugar - Sake (licoroso)
   Similaridade: 84.29%
   • Score por características: 95.35%
   • Score por regras de harmonização: 70.0%
```

## Quick Customization

### Add a new dish to `pratos.csv`:
```csv
101,Pizza Margherita,"tomate, mussarela, manjericão",vegetariano,herbal,média,média
```

### Add a new wine to `vinhos.csv`:
```csv
Prosecco,espumante
```

## Troubleshooting

| Error | Solution |
|-------|----------|
| Module not found | Run `uv sync` |
| Dish not found | Check spelling or list all dishes |
| File not found | Make sure you're in the project directory |

## Need More Help?

📖 See [TUTORIAL.md](TUTORIAL.md) for detailed instructions

---

🎯 **Goal**: Find the perfect wine for any dish using AI!
