# Migration to Perplexity Sonar API

## Summary

The wine recommendation system has been updated to use **Perplexity Sonar API** instead of OpenAI GPT for generating wine pairing justifications.

## What Changed

### 1. API Provider
- **Before:** OpenAI GPT-4o-mini
- **After:** Perplexity Sonar Large (llama-3.1-sonar-large-128k-online)

### 2. Configuration
- **Before:** `OPENAI_API_KEY` in `.env`
- **After:** `PERPLEXITY_API_KEY` in `.env`

### 3. Get API Key
- **Before:** https://platform.openai.com/api-keys
- **After:** https://www.perplexity.ai/settings/api

## Why Perplexity Sonar?

### ✅ Advantages

1. **Real-time Information Access**
   - Sonar models can access current web information
   - Perfect for wine recommendations (latest vintages, reviews, availability)
   - More accurate and up-to-date wine knowledge

2. **Cost-Effective**
   - ~$0.002 per justification (similar to GPT-4o-mini)
   - No separate charges for web access
   - Transparent pricing

3. **Specialized in Factual Content**
   - Designed for accurate, factual responses
   - Excellent for educational content like wine pairing
   - Reduced hallucinations

4. **Competitive Quality**
   - Based on LLama 3.1
   - High-quality Portuguese generation
   - Natural, fluent text

### 📊 Comparison

| Feature | OpenAI GPT-4o-mini | Perplexity Sonar Large |
|---------|-------------------|----------------------|
| **Cost per request** | ~$0.002 | ~$0.002 |
| **Response time** | 2-5s | 2-4s |
| **Web access** | ❌ No | ✅ Yes |
| **Wine knowledge** | Training cutoff | Real-time |
| **Portuguese** | ✅ Excellent | ✅ Excellent |
| **Context window** | 128K tokens | 128K tokens |

## Migration Steps

### For New Users

Simply follow the updated documentation:

1. Get Perplexity API key: https://www.perplexity.ai/settings/api
2. Add to `.env`: `PERPLEXITY_API_KEY=pplx-your-key`
3. Run: `uv run python sistema_integrado.py`

### For Existing Users

If you were using OpenAI:

1. **Get Perplexity API Key**
   ```bash
   # Visit: https://www.perplexity.ai/settings/api
   ```

2. **Update .env file**
   ```bash
   # Add (you can keep OpenAI key for reference)
   PERPLEXITY_API_KEY=pplx-your-actual-key
   ```

3. **That's it!**
   The system automatically uses Perplexity now.

### Optional: Keep Both APIs

You can keep both API keys and switch between them:

```python
from llm import configurar_llm

# Use Perplexity (default)
configurar_llm(model="perplexity/llama-3.1-sonar-large-128k-online")

# Or use OpenAI if you prefer
configurar_llm(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)
```

## Available Sonar Models

### Recommended for Production

**sonar-large-128k-online** (default)
- Best balance of quality and cost
- $1.00 per 1M tokens (input/output)
- ~$0.002 per justification
- Access to real-time web info

### Alternative Models

**sonar-small-128k-online**
- Faster, cheaper
- $0.20 per 1M tokens
- ~$0.0004 per justification
- Good for high-volume use

**sonar-huge-128k-online**
- Most powerful
- $5.00 per 1M tokens
- ~$0.01 per justification
- Best quality, higher cost

### Usage

```python
from llm import configurar_llm

# Small (fast & cheap)
configurar_llm(model="perplexity/llama-3.1-sonar-small-128k-online")

# Large (balanced - default)
configurar_llm(model="perplexity/llama-3.1-sonar-large-128k-online")

# Huge (highest quality)
configurar_llm(model="perplexity/llama-3.1-sonar-huge-128k-online")
```

## Code Changes

### llm.py

```python
# Before
def configurar_llm(model: str = "gpt-4o-mini", api_key: Optional[str] = None):
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY")
    lm = dspy.LM(model=model, api_key=api_key)

# After
def configurar_llm(model: str = "perplexity/llama-3.1-sonar-large-128k-online", api_key: Optional[str] = None):
    if api_key is None:
        api_key = os.getenv("PERPLEXITY_API_KEY")
    lm = dspy.LM(model=model, api_key=api_key, api_base="https://api.perplexity.ai")
```

### .env.example

```bash
# Before
OPENAI_API_KEY=sk-your-key

# After
PERPLEXITY_API_KEY=pplx-your-key
# OPENAI_API_KEY=sk-your-key  # Optional
```

## Testing

Test the new integration:

```bash
# Test standalone LLM module
uv run python llm.py

# Test integrated system
uv run python sistema_integrado.py
```

Expected output:
```
✅ Modelo perplexity/llama-3.1-sonar-large-128k-online configurado com sucesso!

🔄 Gerando justificativa para: Pinot Grigio...

📝 JUSTIFICATIVA DA HARMONIZAÇÃO:

O Pinot Grigio é uma escolha excepcional para acompanhar sushi...
```

## Troubleshooting

### Error: "API key não encontrada"

**Solution:**
```bash
# Check your .env file
cat .env

# Should contain:
PERPLEXITY_API_KEY=pplx-your-actual-key
```

### Error: "Invalid API key"

**Solution:**
1. Verify key at: https://www.perplexity.ai/settings/api
2. Make sure it starts with `pplx-`
3. Check for extra spaces or quotes

### Different output style?

Sonar models may have slightly different writing styles than GPT. This is normal and actually beneficial for wine content (more factual, less flowery).

## Benefits for Wine Recommendations

### Real-Time Wine Information

Sonar can access:
- Latest wine reviews and ratings
- Current vintage availability
- Recent sommelier recommendations
- Up-to-date wine region information
- New wine releases and trends

### Example Improvement

**Before (GPT-4o-mini):**
> "O Cabernet Sauvignon é conhecido por seus taninos robustos..."

**After (Sonar):**
> "O Cabernet Sauvignon é conhecido por seus taninos robustos... Segundo especialistas recentes da Wine Spectator, este vinho tem apresentado excelentes safras nos últimos anos..."

### More Accurate Pairing Advice

- Access to current sommelier best practices
- Recent food and wine pairing trends
- Updated harmonization techniques

## Cost Comparison (1000 requests)

| Provider | Model | Cost |
|----------|-------|------|
| OpenAI | gpt-4o-mini | ~$2.00 |
| Perplexity | sonar-small | ~$0.40 |
| Perplexity | sonar-large | ~$2.00 |
| Perplexity | sonar-huge | ~$10.00 |

**Recommendation:** Use `sonar-large` for similar cost to GPT-4o-mini but with web access.

## Future Enhancements

With Perplexity Sonar, we can now:

1. **Dynamic Wine Database**
   - Query for new wines not in our CSV
   - Get real-time wine information
   - Access professional reviews

2. **Seasonal Recommendations**
   - Adjust based on current season
   - Consider wine availability
   - Seasonal food pairing trends

3. **Regional Variations**
   - Local wine recommendations
   - Regional pairing traditions
   - Country-specific preferences

4. **Price-Aware Suggestions**
   - Current wine prices
   - Budget-friendly alternatives
   - Best value recommendations

## Documentation Updated

All documentation has been updated:

- ✅ README.md
- ✅ LLM_INTEGRATION.md
- ✅ INDEX.md
- ✅ ARQUITETURA.md
- ✅ .env.example
- ✅ llm.py
- ✅ This migration guide

## Support

For questions about:

- **Perplexity API:** https://docs.perplexity.ai/
- **Pricing:** https://www.perplexity.ai/api
- **Support:** support@perplexity.ai

---

**Migration completed:** November 2024
**Status:** ✅ Production ready
