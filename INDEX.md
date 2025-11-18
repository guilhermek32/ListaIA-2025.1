# 🍷 Sistema de Recomendação de Vinhos com IA - Índice Completo

## 📚 Documentação Principal

### Para Começar Rápido
- **[QUICKSTART.md](QUICKSTART.md)** - Comece em 3 comandos (2 minutos)
- **[README.md](README.md)** - Visão geral do projeto

### Guias Completos
- **[TUTORIAL.md](TUTORIAL.md)** - Tutorial passo a passo completo (15 minutos)
- **[LLM_INTEGRATION.md](LLM_INTEGRATION.md)** - Integração com IA/LLM usando DSPy
- **[ARQUITETURA.md](ARQUITETURA.md)** - Arquitetura técnica do sistema

### Exemplos e Referências
- **[EXEMPLO_SAIDA.md](EXEMPLO_SAIDA.md)** - Exemplos de saída do sistema

---

## 💻 Código Fonte

### Sistema de Recomendação (ML)
- **[sistema_recomendacao_vinho.py](sistema_recomendacao_vinho.py)** - Sistema principal
  - Análise de similaridade (cosine similarity)
  - Regras de harmonização
  - Recomendação de top vinhos

### Integração com IA
- **[llm.py](llm.py)** - Módulo DSPy para justificativas
  - Configuração de LLM (OpenAI GPT)
  - Geração de justificativas em português
  - Chain-of-Thought reasoning

- **[sistema_integrado.py](sistema_integrado.py)** - Sistema completo
  - Combina ML + IA
  - Interface unificada
  - Tratamento de erros

### Outros
- **[knn.py](knn.py)** - Placeholder para futuras implementações

---

## 📊 Bases de Dados

- **[pratos.csv](pratos.csv)** - 100 pratos com características
  - Campos: id_prato, nome_prato, ingredientes, tipo_prato, temperos, acidez, intensidade_sabor

- **[vinhos.csv](vinhos.csv)** - 29 variedades de vinhos
  - Campos: vinho, tipo_vinho

- **[regras.csv](regras.csv)** - Regras de harmonização
  - Exemplos de harmonizações perfeitas

---

## 🚀 Como Usar

### Opção 1: Sistema Básico (Sem IA)
```bash
uv run python sistema_recomendacao_vinho.py
```

**Características:**
- ✅ Recomendação de vinhos
- ✅ Scores de similaridade
- ✅ Top 3 vinhos
- ❌ Sem justificativas IA

### Opção 2: Sistema Completo (Com IA)
```bash
# 1. Configure API key
echo "PERPLEXITY_API_KEY=pplx-your-key" >> .env

# 2. Execute
uv run python sistema_integrado.py
```

**Características:**
- ✅ Recomendação de vinhos
- ✅ Scores de similaridade
- ✅ Top 3 vinhos
- ✅ Justificativas IA em português (Perplexity Sonar)

### Opção 3: Modo Interativo
```python
from sistema_integrado import sistema_completo_com_justificativa

# Qualquer prato da base de dados
sistema_completo_com_justificativa("Sushi", usar_llm=True)
```

---

## 📖 Guias por Perfil

### 👨‍🎓 Iniciante
1. Leia [QUICKSTART.md](QUICKSTART.md)
2. Execute o sistema básico
3. Explore [TUTORIAL.md](TUTORIAL.md) para aprender mais

### 👨‍💻 Desenvolvedor
1. Leia [ARQUITETURA.md](ARQUITETURA.md)
2. Entenda a estrutura do código
3. Veja [LLM_INTEGRATION.md](LLM_INTEGRATION.md) para IA
4. Personalize conforme necessário

### 🔬 Pesquisador/Cientista de Dados
1. Analise [sistema_recomendacao_vinho.py](sistema_recomendacao_vinho.py)
2. Estude os algoritmos de similaridade
3. Experimente com diferentes pesos e features
4. Teste novos modelos LLM

### 🍷 Sommelier/Entusiasta
1. Use [QUICKSTART.md](QUICKSTART.md) para começar
2. Teste com seus pratos favoritos
3. Adicione novos pratos e vinhos às bases
4. Compartilhe suas descobertas!

---

## 🛠️ Estrutura do Projeto

```
ListaIA-2025.1/
│
├── 📚 DOCUMENTAÇÃO
│   ├── README.md              # Visão geral
│   ├── QUICKSTART.md          # Início rápido
│   ├── TUTORIAL.md            # Tutorial completo
│   ├── LLM_INTEGRATION.md     # Guia de IA
│   ├── ARQUITETURA.md         # Arquitetura técnica
│   ├── EXEMPLO_SAIDA.md       # Exemplos
│   └── INDEX.md               # Este arquivo
│
├── 💻 CÓDIGO
│   ├── sistema_recomendacao_vinho.py  # Sistema ML
│   ├── llm.py                         # Módulo IA
│   ├── sistema_integrado.py           # Sistema completo
│   └── knn.py                         # Futuro
│
├── 📊 DADOS
│   ├── pratos.csv             # 100 pratos
│   ├── vinhos.csv             # 29 vinhos
│   └── regras.csv             # Harmonizações
│
├── ⚙️ CONFIGURAÇÃO
│   ├── .env                   # Variáveis (criar)
│   ├── .env.example           # Template
│   ├── pyproject.toml         # Deps Python
│   └── uv.lock                # Lock file
│
└── 📁 OUTROS
    └── src/listaia_2025_1/    # Boilerplate backend
```

---

## 🎯 Casos de Uso

### 1. Restaurante
**Objetivo:** Sugerir vinhos para pratos do cardápio

**Como usar:**
1. Adicione pratos do cardápio em `pratos.csv`
2. Execute sistema_integrado.py
3. Use as justificativas nas cartas de vinhos

### 2. App de Delivery
**Objetivo:** Recomendação automática de vinhos

**Como usar:**
1. Integre via API (criar endpoint)
2. Chame `recomendar_vinho()` programaticamente
3. Exiba resultados no app

### 3. E-commerce de Vinhos
**Objetivo:** Sugestões personalizadas

**Como usar:**
1. Pergunte ao usuário que prato vai preparar
2. Gere recomendações + justificativas
3. Link direto para compra

### 4. Educação/Cursos
**Objetivo:** Ensinar harmonização

**Como usar:**
1. Use as justificativas IA como material didático
2. Mostre os scores (ML vs Regras)
3. Explique o processo de harmonização

---

## 🔧 Troubleshooting Rápido

| Problema | Solução | Documento |
|----------|---------|-----------|
| "Module not found" | `uv sync` | [QUICKSTART.md](QUICKSTART.md) |
| "API key não encontrada" | Configure `.env` com `PERPLEXITY_API_KEY` | [LLM_INTEGRATION.md](LLM_INTEGRATION.md) |
| "Prato não encontrado" | Verifique nome exato | [TUTORIAL.md](TUTORIAL.md) |
| Encoding error | Código já corrigido | [llm.py](llm.py) |
| Justificativa muito curta | Ajuste prompt | [LLM_INTEGRATION.md](LLM_INTEGRATION.md) |

---

## 📈 Próximos Passos

### Curto Prazo
- [ ] Adicionar mais pratos à base
- [ ] Testar com amigos e família
- [ ] Explorar diferentes configurações

### Médio Prazo
- [ ] Criar interface web (Streamlit/Flask)
- [ ] API REST para integração
- [ ] Cache de justificativas IA
- [ ] Suporte multi-idioma

### Longo Prazo
- [ ] App mobile
- [ ] Integração com APIs de vinícolas
- [ ] Sistema de avaliação de usuários
- [ ] ML para aprender preferências

---

## 🤝 Contribuindo

Ideias de contribuição:

1. **Dados**: Adicione mais pratos e vinhos
2. **Código**: Melhore algoritmos
3. **Documentação**: Traduza para outros idiomas
4. **Design**: Crie interface gráfica
5. **Testes**: Valide recomendações com especialistas

---

## 📞 Recursos Adicionais

### Bibliotecas Usadas
- [Pandas](https://pandas.pydata.org/) - Manipulação de dados
- [NumPy](https://numpy.org/) - Computação numérica
- [Scikit-learn](https://scikit-learn.org/) - Machine Learning
- [DSPy](https://dspy-docs.vercel.app/) - LLM Programming
- [Perplexity](https://www.perplexity.ai/) - Sonar API for AI

### Conceitos de Harmonização
- [Wine Folly - Wine Pairing](https://winefolly.com/tips/wine-pairing/)
- [Wine & Food Pairing Guide](https://www.decanter.com/learn/wine-food-pairing/)

### Sobre Vinhos
- [Wine Spectator](https://www.winespectator.com/)
- [Vivino](https://www.vivino.com/)

---

## 📝 Licença

MIT License - Use livremente!

---

## 📅 Histórico

- **Nov 2024** - Versão inicial
  - Sistema de recomendação ML
  - Integração DSPy + OpenAI
  - Documentação completa
  - 100 pratos, 29 vinhos

---

**Desenvolvido com ❤️ para amantes de vinho e boa comida!**

🍷 Saúde! / Cheers! / Salud! / À votre santé!
