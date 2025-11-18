# VineChat - Sistema de Recomendação de Vinhos 🍷

Sistema inteligente de recomendação de vinhos que combina machine learning com inteligência artificial para sugerir harmonizações perfeitas entre pratos e vinhos.

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

1. **Node.js 18+** - [Download Node.js](https://nodejs.org/)
2. **Python 3.10+** - [Download Python](https://www.python.org/downloads/)
3. **UV** - Gerenciador de pacotes Python rápido

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

## 🚀 Tutorial Completo

### Passo 1: Clone ou Navegue até o Projeto

```bash
cd C:\Users\gui\Documents\code\Lista2-IA\ListaIA-2025.1
```

### Passo 2: Configure as Variáveis de Ambiente

Copie o arquivo de exemplo e configure suas chaves API:

```bash
cp .env.example .env
```

Edite o arquivo `.env` e adicione suas chaves:

```env
# API Key para Perplexity AI (recomendações inteligentes)
PERPLEXITY_API_KEY=sua_chave_perplexity_aqui

# API Key para Google Gemini (opcional)
LLM_API_KEY=sua_chave_gemini_aqui
LLM_MODEL=gemini-pro
```

### Passo 3: Instale as Dependências do Backend (Python)

Sincronize todas as dependências Python usando UV:

```bash
uv sync
```

Isso irá instalar:
- `fastapi` - Framework web para a API
- `uvicorn` - Servidor ASGI
- `pandas` - Manipulação de dados
- `numpy` - Operações numéricas
- `scikit-learn` - Algoritmos de machine learning
- `dspy-ai` - Framework para LLMs
- `python-dotenv` - Gerenciamento de variáveis de ambiente

### Passo 4: Instale as Dependências do Frontend (Next.js)

```bash
npm install
```

### Passo 5: Execute o Sistema

**Opção A: Usando o script de inicialização (Windows)**

```bash
start.bat
```

Este script irá:
1. Verificar a existência do arquivo `.env`
2. Iniciar o servidor backend (Python/FastAPI) na porta 8000
3. Iniciar o servidor frontend (Next.js) na porta 3000
4. Abrir automaticamente o navegador

**Opção B: Execução manual**

Terminal 1 - Backend:
```bash
uv run python api.py
```

Terminal 2 - Frontend:
```bash
npm run dev
```

### Passo 6: Acesse o Sistema

Abra seu navegador em: [http://localhost:3000](http://localhost:3000)

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentação API**: http://localhost:8000/docs

## 🏗️ Tecnologias

### Frontend
- Next.js 16.0.1
- TypeScript
- React 18
- Tailwind CSS

### Backend
- FastAPI
- Python 3.10+
- Scikit-learn
- Pandas & NumPy
- DSPy-AI

## 📁 Estrutura do Projeto

```
ListaIA-2025.1/
├── app/                    # Aplicação Next.js (App Router)
│   ├── api/               # API Routes
│   └── page.tsx           # Página principal
├── backend/               # Servidor Python/FastAPI
│   └── api.py            # API de recomendação
├── components/            # Componentes React
│   └── Chat.tsx          # Interface de chat
├── db/                    # Base de dados (CSV)
│   ├── pratos.csv        # 100 pratos catalogados
│   ├── vinhos.csv        # 29 tipos de vinhos
│   └── regras.csv        # Regras de harmonização
├── lib/                   # Utilitários
│   ├── csv-reader.ts     # Leitor de CSV
│   ├── data.ts           # Funções de dados
│   └── llm.ts            # Integração com LLM
├── types/                 # Definições TypeScript
├── docs/                  # Documentação
├── api.py                 # Servidor backend
├── pyproject.toml         # Configuração Python
├── package.json           # Configuração Node.js
└── .env                   # Variáveis de ambiente
```

## 📊 Como Funciona

1. **Interface de Chat**: Usuário descreve um prato ou preferência
2. **Backend API**: Processa a requisição usando machine learning
3. **Algoritmo de Recomendação**: 
   - Analisa características do prato (tipo, tempero, acidez, intensidade)
   - Calcula similaridade com vinhos usando cosseno
   - Aplica regras clássicas de harmonização
   - Combina scores (40% características + 60% regras)
4. **LLM**: Gera justificativa personalizada e natural
5. **Resposta**: Retorna TOP 3 vinhos com scores e explicações

## 🔧 Scripts Disponíveis

```bash
# Frontend
npm run dev          # Inicia servidor de desenvolvimento
npm run build        # Build para produção
npm run start        # Inicia servidor de produção

# Backend
uv run python api.py              # Inicia API backend
uv run python test_system.py     # Testa sistema completo
```

## 🐛 Solução de Problemas

### Erro: "ModuleNotFoundError: No module named..."

**Solução:**
```bash
uv sync
```

### Erro: "Port 3000 already in use"

**Solução:**
Mate o processo ou use outra porta:
```bash
npm run dev -- -p 3001
```

### Erro: API Key não configurada

**Solução:**
Verifique se o arquivo `.env` existe e contém as chaves corretas:
```bash
cat .env  # Linux/Mac
type .env  # Windows
```

## 📚 Documentação Adicional

Consulte a pasta `/docs` para documentação detalhada:

- `TUTORIAL.md` - Tutorial completo do sistema Python
- `SETUP.md` - Guia de configuração detalhado
- `API_DOCUMENTATION.md` - Documentação da API
- `ARQUITETURA.md` - Arquitetura do sistema
- `QUICKSTART.md` - Início rápido

## 🎯 Próximos Passos

1. Explore a interface de chat
2. Teste diferentes tipos de pratos
3. Adicione novos pratos em `db/pratos.csv`
4. Personalize as regras de harmonização
5. Ajuste os pesos do algoritmo

## 📞 Suporte

- **Documentação UV**: https://docs.astral.sh/uv/
- **FastAPI**: https://fastapi.tiangolo.com/
- **Next.js**: https://nextjs.org/docs
- **Scikit-learn**: https://scikit-learn.org/stable/

---

**Desenvolvido com ❤️ para amantes de vinho e boa comida!**

Versão: 1.0.0 | Novembro 2024
