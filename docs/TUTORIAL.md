# Tutorial: Sistema de Recomendação de Vinhos 🍷

Este tutorial explica como executar o sistema de recomendação de vinhos que utiliza machine learning para sugerir harmonizações perfeitas entre pratos e vinhos.

## 📋 Pré-requisitos

Antes de começar, você precisa ter instalado:

1. **Python 3.10+** - [Download Python](https://www.python.org/downloads/)
2. **UV** - Gerenciador de pacotes Python rápido

### Instalando o UV

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Verificar instalação:**
```bash
uv --version
```

## 📁 Estrutura do Projeto

```
ListaIA-2025.1/
├── sistema_recomendacao_vinho.py    # Script principal
├── pratos.csv                        # Base de dados com 100 pratos
├── vinhos.csv                        # Base de dados com 29 vinhos
├── regras.csv                        # Regras de harmonização
└── pyproject.toml                    # Configuração do projeto
```

## 🚀 Passo a Passo para Execução

### Passo 1: Clone ou Navegue até o Diretório do Projeto

```bash
cd C:\Users\gui\Documents\code\Lista2-IA\ListaIA-2025.1
```

Ou no Linux/macOS:
```bash
cd ~/path/to/ListaIA-2025.1
```

### Passo 2: Sincronize as Dependências

O UV irá instalar automaticamente todas as bibliotecas necessárias:

```bash
uv sync
```

Isso irá instalar:
- `pandas` - Manipulação de dados
- `numpy` - Operações numéricas
- `scikit-learn` - Algoritmos de machine learning
- `dspy-ai` - Framework para LLMs (opcional)

### Passo 3: Execute o Sistema

**Opção A: Executar o script completo**

```bash
uv run python sistema_recomendacao_vinho.py
```

Isso irá mostrar recomendações para 6 pratos de exemplo:
- Filé ao molho madeira
- Salmão grelhado
- Frango ao curry
- Picanha na brasa
- Camarão ao alho e óleo
- Risoto de limão siciliano

**Opção B: Usar modo interativo**

```bash
uv run python
```

Então, no console Python:

```python
from sistema_recomendacao_vinho import sistema_recomendacao_vinho

# Recomendação para um prato específico
sistema_recomendacao_vinho("Sushi")
```

## 📊 Entendendo a Saída

O sistema exibe para cada prato:

```
================================================================================
🍷 SISTEMA DE RECOMENDAÇÃO DE VINHOS 🍷
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
```

### Interpretação dos Scores:

- **Similaridade**: Score final (40% características + 60% regras)
- **Score por características**: Similaridade cosseno entre prato e vinho
- **Score por regras**: Match baseado em regras clássicas de harmonização

## 🔧 Personalizando o Sistema

### 1. Modificar Pratos para Teste

Edite o final do arquivo `sistema_recomendacao_vinho.py`:

```python
if __name__ == "__main__":
    pratos_teste = [
        "Seu prato 1",
        "Seu prato 2",
        # Adicione mais pratos aqui
    ]
    
    for prato in pratos_teste:
        sistema_recomendacao_vinho(prato)
        print("\n")
```

### 2. Adicionar Novos Pratos

Edite o arquivo `pratos.csv`:

```csv
id_prato,nome_prato,ingredientes,tipo_prato,temperos,acidez,intensidade_sabor
101,Meu Prato Novo,"ingrediente1, ingrediente2",carne vermelha,intenso,baixa,alta
```

**Tipos de prato válidos:**
- `carne vermelha`
- `carne branca`
- `peixe`
- `vegetariano`
- `frutos do mar`

**Temperos válidos:**
- `intenso`, `picante`, `forte`, `defumado`
- `moderado`, `cremoso`, `terroso`, `salgado`, `doce`
- `herbal`, `cítrico`, `suave`

**Acidez/Intensidade válidas:**
- `baixa`, `média`, `alta`

### 3. Adicionar Novos Vinhos

Edite o arquivo `vinhos.csv`:

```csv
vinho,tipo_vinho
Seu Vinho Novo,tinto seco
```

**Tipos de vinho válidos:**
- `tinto seco`, `tinto suave`, `tinto leve`, `tinto frutado`
- `branco seco`, `branco doce`, `branco aromático`
- `rosé seco`
- `espumante`
- `licoroso`

Depois, adicione as características do vinho no arquivo `sistema_recomendacao_vinho.py`:

```python
caracteristicas_vinhos = {
    # ... vinhos existentes ...
    'Seu Vinho Novo': {'acidez': 2, 'intensidade': 3, 'docura': 1, 'tanino': 3},
}
```

Escala de 0-3:
- **acidez**: 1 (baixa) - 3 (alta)
- **intensidade**: 1 (leve) - 3 (forte)
- **docura**: 1 (seco) - 3 (doce)
- **tanino**: 0 (sem tanino/branco) - 3 (alto tanino/tinto)

## 💡 Exemplos de Uso

### Exemplo 1: Recomendação Simples

```python
from sistema_recomendacao_vinho import recomendar_vinho, df_pratos, df_vinhos

resultado = recomendar_vinho("Sushi", df_pratos, df_vinhos, top_n=5)
print(resultado)
```

### Exemplo 2: Listar Todos os Pratos Disponíveis

```python
import pandas as pd

df_pratos = pd.read_csv('pratos.csv')
print("Pratos disponíveis:")
for i, prato in enumerate(df_pratos['nome_prato'], 1):
    print(f"{i}. {prato}")
```

### Exemplo 3: Análise de Características

```python
from sistema_recomendacao_vinho import codificar_pratos
import pandas as pd

df_pratos = pd.read_csv('pratos.csv')
df_encoded = codificar_pratos(df_pratos)

# Ver como os pratos foram codificados numericamente
print(df_encoded[['nome_prato', 'acidez_num', 'intensidade_num', 'temperos_num']].head())
```

## 🐛 Solução de Problemas

### Erro: "ModuleNotFoundError: No module named 'sklearn'"

**Solução:**
```bash
uv add scikit-learn
uv sync
```

### Erro: "Prato 'X' não encontrado na base de dados"

**Solução:**
1. Verifique a grafia exata do prato
2. Liste todos os pratos disponíveis:
```python
import pandas as pd
print(pd.read_csv('pratos.csv')['nome_prato'].tolist())
```

### Erro: "FileNotFoundError: pratos.csv"

**Solução:**
Certifique-se de estar no diretório correto:
```bash
cd C:\Users\gui\Documents\code\Lista2-IA\ListaIA-2025.1
```

### UV não é reconhecido (Windows)

**Solução:**
Reinicie o terminal PowerShell ou adicione o UV ao PATH:
```powershell
$env:Path += ";$env:USERPROFILE\.cargo\bin"
```

## 📚 Como o Sistema Funciona

### 1. Codificação de Características
O sistema converte atributos categóricos (tipo de prato, tempero, etc.) em valores numéricos.

### 2. Cálculo de Similaridade
Usa **similaridade de cosseno** para comparar vetores de características entre pratos e vinhos.

### 3. Regras de Harmonização
Aplica conhecimento especializado sobre quais tipos de vinho combinam com cada tipo de prato.

### 4. Score Final
Combina 40% de similaridade de características com 60% de regras de harmonização.

## 🎯 Próximos Passos

1. **Expandir a base de dados**: Adicione seus pratos favoritos
2. **Ajustar pesos**: Modifique os percentuais de características vs regras
3. **Implementar filtros**: Adicione preferências do usuário (ex: só vinhos tintos)
4. **Criar interface web**: Use Flask ou Streamlit para criar uma interface gráfica

## 📞 Suporte

Para mais informações sobre as bibliotecas usadas:

- **Pandas**: https://pandas.pydata.org/docs/
- **NumPy**: https://numpy.org/doc/
- **Scikit-learn**: https://scikit-learn.org/stable/
- **UV**: https://docs.astral.sh/uv/

---

**Desenvolvido com ❤️ para amantes de vinho e boa comida!**

Data: Novembro 2024
