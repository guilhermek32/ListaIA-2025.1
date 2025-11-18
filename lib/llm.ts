import { Prato, Vinho, Recomendacao } from '@/types';

// Função para gerar justificativa usando LLM
export async function gerarJustificativa(
  prato: Prato,
  vinho: Vinho
): Promise<string> {
  const tipoPrato = prato.tipo || 'prato';
  const temperos = prato.temperos ? ` Temperos: ${prato.temperos}.` : '';
  const acidez = prato.acidez ? ` Acidez: ${prato.acidez}.` : '';
  const tipoVinhoCompleto = vinho.tipoCompleto || vinho.tipo;
  
  const prompt = `Você é um sommelier experiente. Explique de forma clara e convincente por que o vinho "${vinho.nome}" (${tipoVinhoCompleto}) harmoniza perfeitamente com o prato "${prato.nome}" (${tipoPrato}).

Considere:
- Tipo de prato: ${tipoPrato}
- Ingredientes principais: ${prato.ingredientes.join(', ')}${temperos}${acidez}
- Intensidade do sabor: ${prato.intensidade}
- Características do vinho: ${vinho.descricao}
- Tipo de vinho: ${tipoVinhoCompleto}

Forneça uma justificativa profissional e acessível em português, com 2-3 frases explicando a harmonização.`;

  try {
    const apiKey = process.env.LLM_API_KEY;
    const model = process.env.LLM_MODEL || 'gemini-pro';
    
    // Construir o prompt completo com instruções do sistema
    const promptCompleto = `Você é um sommelier experiente e educado, especializado em harmonização de vinhos e pratos.

${prompt}`;

    if (!apiKey) {
      // Fallback para resposta sem LLM (para desenvolvimento)
      return `O ${vinho.nome} harmoniza perfeitamente com ${prato.nome} devido às suas características complementares. O ${vinho.tipo} ${vinho.descricao.toLowerCase()} equilibra os sabores do prato, criando uma experiência gastronômica harmoniosa.`;
    }

    // API do Google Gemini
    const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`;

    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        contents: [
          {
            parts: [
              {
                text: promptCompleto
              }
            ]
          }
        ],
        generationConfig: {
          temperature: 0.7,
          maxOutputTokens: 200,
          topP: 0.8,
          topK: 40
        }
      })
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Gemini API error: ${response.statusText} - ${errorText}`);
    }

    const data = await response.json();
    
    // Extrair resposta do formato Gemini
    const textoResposta = data.candidates?.[0]?.content?.parts?.[0]?.text;
    
    if (!textoResposta) {
      throw new Error('Resposta vazia da API Gemini');
    }

    return textoResposta.trim();
  } catch (error) {
    console.error('Erro ao gerar justificativa:', error);
    // Fallback
    return `O ${vinho.nome} harmoniza perfeitamente com ${prato.nome} devido às suas características complementares. O ${vinho.tipo} ${vinho.descricao.toLowerCase()} equilibra os sabores do prato, criando uma experiência gastronômica harmoniosa.`;
  }
}

// Função para processar recomendação completa
export async function processarRecomendacao(
  prato: Prato,
  vinho: Vinho
): Promise<Recomendacao> {
  const justificativa = await gerarJustificativa(prato, vinho);

  return {
    prato,
    vinho,
    justificativa,
    score: 0.85 // Score simulado (em produção, calcular baseado em algoritmo)
  };
}

