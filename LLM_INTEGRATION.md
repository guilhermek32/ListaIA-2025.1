# LLM Integration - Wine Recommendation Justification

## Overview

This module uses **DSPy** to generate Portuguese justifications for wine recommendations using **Perplexity Sonar API** (Large Language Models).

## Files Created

1. **`llm.py`** - DSPy module for generating wine pairing justifications
2. **`sistema_integrado.py`** - Complete system combining recommendations + LLM justifications

## Setup

### 1. Get a Perplexity API Key

Visit [Perplexity API Settings](https://www.perplexity.ai/settings/api) and create a new key.

### 2. Configure Environment

Create or edit `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your key:

```env
PERPLEXITY_API_KEY=pplx-your-actual-key-here
```

### 3. Install Dependencies

```bash
uv sync
```

## Usage

### Option 1: Standalone LLM Module

```bash
uv run python llm.py
```

**Example output:**
```
================================================================================
🍷 GERADOR DE JUSTIFICATIVAS DE HARMONIZAÇÃO
================================================================================

📍 Prato: Sushi
🍾 Vinho: Pinot Grigio
📊 Similaridade: 98.14%

--------------------------------------------------------------------------------

📝 JUSTIFICATIVA DA HARMONIZAÇÃO:

O Pinot Grigio é uma escolha excepcional para acompanhar sushi devido à sua 
natureza delicada e refrescante que complementa perfeitamente os sabores sutis 
do peixe cru. A alta acidez do vinho equilibra a textura cremosa do arroz, 
enquanto sua intensidade leve não sobrepõe o sabor delicado do peixe...
```

### Option 2: Integrated System

```bash
uv run python sistema_integrado.py
```

This runs the complete workflow:
1. Analyzes dish characteristics
2. Recommends top 3 wines
3. Generates AI justification for the best match

### Option 3: Programmatic Use

```python
from llm import configurar_llm, gerar_justificativa_vinho

# Configure LLM
configurar_llm(model="perplexity/llama-3.1-sonar-large-128k-online")

# Prepare data
caracteristicas_prato = {
    'tipo_prato': 'peixe',
    'temperos': 'suave',
    'acidez': 'alta',
    'intensidade_sabor': 'baixa',
    'ingredientes': 'arroz, peixe cru'
}

vinho_info = {
    'vinho': 'Pinot Grigio',
    'tipo_vinho': 'branco seco',
    'similaridade_percentual': 98.14,
    'score_features': 95.35,
    'score_regras': 100.0
}

# Generate justification
justificativa = gerar_justificativa_vinho(
    nome_prato="Sushi",
    caracteristicas_prato=caracteristicas_prato,
    vinho_info=vinho_info
)

print(justificativa)
```

### Option 4: Custom Dish

```python
from sistema_integrado import sistema_completo_com_justificativa

# Any dish from the database
sistema_completo_com_justificativa("Feijoada", usar_llm=True)
sistema_completo_com_justificativa("Picanha na brasa", usar_llm=True)
```

## How It Works

### DSPy Signature

The system uses a **DSPy Signature** that defines:

**Inputs:**
- `nome_prato` - Dish name
- `tipo_prato` - Dish type (meat, fish, etc)
- `temperos` - Seasonings
- `acidez` - Acidity level
- `intensidade_sabor` - Flavor intensity
- `ingredientes` - Main ingredients
- `vinho_recomendado` - Recommended wine
- `tipo_vinho` - Wine type
- `similaridade_percentual` - Similarity score
- `score_caracteristicas` - Features score
- `score_regras` - Rules score

**Output:**
- `justificativa` - Detailed Portuguese explanation (3-4 paragraphs)

### Chain of Thought

Uses `dspy.ChainOfThought` to:
1. Analyze dish and wine characteristics
2. Consider harmonization principles
3. Generate educational, elegant explanation
4. Mention both algorithmic and expert-based scores

## Configuration Options

### Change LLM Model

```python
from llm import configurar_llm

# Use Sonar Large (default - most capable)
configurar_llm(model="perplexity/llama-3.1-sonar-large-128k-online")

# Use Sonar Small (faster, cheaper)
configurar_llm(model="perplexity/llama-3.1-sonar-small-128k-online")

# Use Sonar Huge (most powerful)
configurar_llm(model="perplexity/llama-3.1-sonar-huge-128k-online")
```

### Pass API Key Directly

```python
configurar_llm(model="perplexity/llama-3.1-sonar-large-128k-online", api_key="pplx-your-key")
```

## Cost Considerations

Approximate costs per request (as of November 2024):

| Model | Input (per 1M tokens) | Output (per 1M tokens) | Est. per justification |
|-------|----------------------|------------------------|------------------------|
| sonar-small-128k-online | $0.20 | $0.20 | ~$0.0004 |
| sonar-large-128k-online | $1.00 | $1.00 | ~$0.002 |
| sonar-huge-128k-online | $5.00 | $5.00 | ~$0.01 |

**Recommendation:** Use `sonar-large-128k-online` (default) for balanced quality and cost.

**Note:** Sonar models have access to real-time web information, making them excellent for wine recommendations!

## Error Handling

The system gracefully handles errors:

1. **Missing API Key:**
```
❌ Erro: API key não encontrada
💡 Para usar este sistema, você precisa:
   1. Criar um arquivo .env na raiz do projeto
   2. Adicionar sua chave: PERPLEXITY_API_KEY=sua_chave_aqui

Obtenha sua chave em: https://www.perplexity.ai/settings/api
```

2. **API Errors:**
```
⚠️  Erro ao gerar justificativa: Rate limit exceeded
```

3. **Network Issues:**
```
⚠️  Erro ao gerar justificativa: Connection timeout
```

## Integration with Wine Recommendation System

The integrated system (`sistema_integrado.py`) combines:

1. **Machine Learning** (Cosine Similarity)
   - Analyzes numerical features
   - Compares dish and wine vectors

2. **Expert Rules** (Harmonization Knowledge)
   - Red wines with red meat: 100% match
   - White wines with fish: 100% match
   - etc.

3. **AI Justification** (DSPy + Perplexity Sonar)
   - Explains why the pairing works
   - Educational tone
   - Portuguese language
   - Mentions specific characteristics
   - Can access real-time wine information

## Example Output

```
================================================================================
🍷 SISTEMA COMPLETO DE RECOMENDAÇÃO E JUSTIFICATIVA
================================================================================

Prato selecionado: Filé ao molho madeira

Características do prato:
  • Tipo: carne vermelha
  • Tempero: intenso
  • Acidez: baixa
  • Intensidade de sabor: alta
  • Ingredientes: filé mignon, molho madeira, cogumelos

================================================================================
🏆 TOP 3 VINHOS RECOMENDADOS
================================================================================

1º lugar - Cabernet Sauvignon (tinto seco)
   Similaridade: 99.13%
   • Score por características: 97.82%
   • Score por regras de harmonização: 100.0%

2º lugar - Malbec (tinto seco)
   Similaridade: 99.13%
   
3º lugar - Syrah (tinto seco)
   Similaridade: 99.13%

================================================================================
🤖 JUSTIFICATIVA GERADA POR IA
================================================================================

✅ Modelo perplexity/llama-3.1-sonar-large-128k-online configurado com sucesso!

🔄 Gerando justificativa para: Cabernet Sauvignon...

📝 JUSTIFICATIVA DA HARMONIZAÇÃO:

O Cabernet Sauvignon é uma escolha magistral para acompanhar o Filé ao molho 
madeira, uma harmonização que celebra a robustez e complexidade de ambos os 
elementos. Este vinho tinto seco apresenta taninos estruturados e uma 
intensidade aromática que se entrelaçam perfeitamente com os sabores intensos 
do filé mignon e do molho madeira rico em cogumelos.

A baixa acidez do prato encontra um parceiro ideal na acidez moderada do 
Cabernet Sauvignon, criando um equilíbrio que não sobrecarrega o paladar. 
Os taninos marcantes do vinho complementam a textura macia da carne, enquanto 
as notas terrosas dos cogumelos dialogam harmoniosamente com os toques de 
especiarias e frutas escuras presentes no vinho.

Com uma similaridade impressionante de 99.13%, esta harmonização demonstra 
tanto excelência técnica (score de características de 97.82%) quanto 
alinhamento perfeito com as regras clássicas de harmonização (100%). 
O resultado é uma experiência gastronômica onde vinho e prato se elevam 
mutuamente, transformando uma refeição em uma celebração dos sentidos.
```

## Troubleshooting

### Issue: Unicode/Encoding Errors on Windows

**Solution:** The code automatically configures UTF-8 encoding for Windows.

### Issue: Rate Limit Errors

**Solution:** Add delay between requests:
```python
import time
time.sleep(1)  # Wait 1 second between requests
```

### Issue: Justification Too Short/Long

**Solution:** Modify the signature description in `llm.py`:
```python
justificativa = dspy.OutputField(
    desc="Justificativa detalhada... Use 5-6 parágrafos..."  # Adjust here
)
```

## Advanced Usage

### Batch Processing

```python
from sistema_integrado import sistema_completo_com_justificativa

pratos = ["Sushi", "Feijoada", "Picanha na brasa", "Salmão grelhado"]

for prato in pratos:
    print(f"\n{'='*80}\nProcessando: {prato}\n{'='*80}")
    sistema_completo_com_justificativa(prato, usar_llm=True)
    time.sleep(1)  # Rate limiting
```

### Save Results to File

```python
import json

resultado = sistema_completo_com_justificativa("Sushi", usar_llm=True)

# Save to JSON
output = {
    "prato": "Sushi",
    "vinhos": resultado.to_dict('records')
}

with open("recomendacao.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
```

## Next Steps

1. **Fine-tune prompts** - Adjust signature descriptions for better output
2. **Add caching** - Save justifications to avoid repeated API calls
3. **Support multiple languages** - Add English, Spanish, etc.
4. **Web interface** - Create Flask/Streamlit app
5. **A/B testing** - Compare different models and prompts

## References

- [DSPy Documentation](https://dspy-docs.vercel.app/)
- [Perplexity API Documentation](https://docs.perplexity.ai/)
- [Perplexity Sonar Models](https://docs.perplexity.ai/docs/model-cards)
- [Wine Pairing Guide](https://winefolly.com/tips/wine-pairing/)

---

**Created:** November 2024
**Author:** Sistema de Recomendação de Vinhos
**License:** MIT
