# Guia de Configuração - VineChat

## Instalação

1. Instale as dependências:
```bash
npm install
```

## Configuração de Variáveis de Ambiente

Crie um arquivo `.env.local` na raiz do projeto com as seguintes variáveis:

```env
# API Key para Google Gemini
LLM_API_KEY=sua_chave_api_gemini_aqui
LLM_MODEL=gemini-pro
```

### Configuração do Google Gemini

O sistema está configurado para usar o Google Gemini como LLM. Para obter uma API key:

1. Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crie uma nova API key
3. Configure no arquivo `.env.local`:

```env
LLM_API_KEY=AIzaSy...sua_chave_aqui
LLM_MODEL=gemini-pro
```

#### Modelos disponíveis do Gemini:
- `gemini-pro` - Modelo padrão (recomendado)
- `gemini-pro-vision` - Para análise de imagens (não usado neste projeto)

**Nota:** Se você não configurar a API key, o sistema funcionará com respostas pré-definidas (modo de desenvolvimento).

## Executando o Projeto

```bash
npm run dev
```

Acesse [http://localhost:3000](http://localhost:3000)

## Estrutura do Projeto

```
VineChat/
├── app/
│   ├── api/
│   │   └── recomendacao/
│   │       └── route.ts      # API route para processar recomendações
│   ├── globals.css           # Estilos globais
│   ├── layout.tsx            # Layout raiz
│   └── page.tsx              # Página principal
├── components/
│   └── Chat.tsx              # Componente de chat
├── db/
│   ├── pratos.csv            # Base de dados de pratos (CSV)
│   └── vinhos.csv            # Base de dados de vinhos (CSV)
├── lib/
│   ├── csv-reader.ts         # Leitor de arquivos CSV
│   ├── data.ts               # Funções de busca e recomendação
│   └── llm.ts                # Integração com LLM
├── types/
│   └── index.ts              # Definições TypeScript
└── package.json
```

## Como Funciona

1. **Frontend (Chat)**: Interface de chat onde o usuário descreve um prato
2. **API Route**: Recebe a mensagem e processa a recomendação
3. **Algoritmo de Recomendação**: Busca pratos e vinhos compatíveis na base de dados
4. **LLM**: Gera justificativa personalizada para a harmonização
5. **Resposta**: Retorna a recomendação com justificativa ao usuário

## Base de Dados (CSV)

O sistema utiliza arquivos CSV localizados em `/db` como banco de dados:

- **`db/pratos.csv`**: Contém 100 pratos com informações detalhadas
  - Campos: id_prato, nome_prato, ingredientes, tipo_prato, temperos, acidez, intensidade_sabor
  
- **`db/vinhos.csv`**: Contém 29 tipos de vinhos
  - Campos: vinho, tipo_vinho

Os dados são carregados automaticamente na inicialização e ficam em cache para melhor performance.

## Próximos Passos

- [ ] Integração com banco de dados real
- [ ] Sistema de autenticação
- [ ] Histórico de conversas
- [ ] Avaliação de recomendações
- [ ] Algoritmo de recomendação mais sofisticado
- [ ] Suporte a múltiplos idiomas

