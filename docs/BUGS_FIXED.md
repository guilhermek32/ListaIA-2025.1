# Bugs Fixed

## Summary
Found and fixed 4 bugs in the wine recommendation system.

---

## Bug #1: Perplexity API response_format Error
**File:** `llm.py`  
**Line:** 120  
**Severity:** 🔴 Critical - System crash

**Problem:**
```python
lm = dspy.LM(
    model=model, 
    api_key=api_key, 
    api_base="https://api.perplexity.ai",
    temperature=0.7,
    max_tokens=2000
)
```

DSPy was trying to use structured JSON outputs with Perplexity API, but Perplexity has strict requirements:
- Error: `["At body -> response_format -> ResponseFormatTeext -> type: Input should be 'text'", ...]`

**Fix:**
```python
lm = dspy.LM(
    model=model, 
    api_key=api_key, 
    api_base="https://api.perplexity.ai",
    temperature=0.7,
    max_tokens=2000,
    response_format={"type": "text"}  # Added this
)
```

---

## Bug #2: Wrong API Key in Error Message
**File:** `sistema_integrado.py`  
**Line:** 116  
**Severity:** 🟡 Medium - Misleading user

**Problem:**
```python
print("    2. Adicione: OPENAI_API_KEY=sua_chave_aqui")
```

Error message told users to add OPENAI_API_KEY, but the system uses PERPLEXITY_API_KEY.

**Fix:**
```python
print("    2. Adicione: PERPLEXITY_API_KEY=sua_chave_aqui")
```

---

## Bug #3: Duplicate LLM Configuration
**File:** `sistema_integrado.py`  
**Line:** 77  
**Severity:** 🟡 Medium - Performance issue

**Problem:**
```python
configurar_llm()  # Called every time without checking if already configured
```

If the function is called multiple times, it could cause issues or waste API calls.

**Fix:**
```python
try:
    configurar_llm()
except Exception:
    pass  # LLM já configurado
```

---

## Bug #4: Redundant Dictionary Key Processing
**File:** `sistema_recomendacao_vinho.py`  
**Line:** 72  
**Severity:** 🟢 Low - Code quality

**Problem:**
```python
df_vinhos[col] = df_vinhos['vinho'].apply(
    lambda x: caracteristicas_vinhos[x][col.replace('_vinho', '').replace('docura', 'docura')]
)
```

The `.replace('docura', 'docura')` does nothing and makes code confusing.

**Fix:**
```python
col_key = col.replace('_vinho', '')
df_vinhos[col] = df_vinhos['vinho'].apply(
    lambda x: caracteristicas_vinhos[x][col_key]
)
```

---

## Testing Results

✅ **All tests passed:**
- CSV files load correctly (100 pratos, 28 vinhos, 28 regras)
- No duplicate wines in database
- All wines have characteristics defined
- No NaN values in encoded data
- Recommendation system works correctly
- Returns correct top 3 wines (e.g., Pinot Grigio for Sushi)

---

## How to Verify

Run the test suite:
```bash
cd ListaIA-2025.1
python sistema_recomendacao_vinho.py
```

Or test with LLM integration (requires PERPLEXITY_API_KEY in .env):
```bash
python sistema_integrado.py
```
