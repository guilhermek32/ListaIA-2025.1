# ListaIA-2025.1

## VineChat - Sistema de Recomendação de Vinhos

MVP de um chat de sugestão de vinhos que utiliza LLM via API.

## Tecnologias

- Next.js 16.0.1
- TypeScript
- React 18

## Como executar

1. Instale as dependências:
```bash
npm install
```

2. Configure as variáveis de ambiente:
```bash
cp .env.example .env
```

3. Execute o servidor de desenvolvimento:
```bash
npm run dev
```

4. Acesse [http://localhost:3000](http://localhost:3000)

## Estrutura do Projeto

- `/app` - Aplicação Next.js (App Router)
- `/app/api` - API Routes
- `/components` - Componentes React
- `/types` - Definições TypeScript
- `/lib` - Utilitários e funções auxiliares
