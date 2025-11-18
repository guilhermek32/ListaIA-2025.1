import { NextRequest, NextResponse } from 'next/server';
import { buscarPrato, buscarVinhosCompativeis } from '@/lib/data';
import { processarRecomendacao } from '@/lib/llm';

export async function POST(request: NextRequest) {
  try {
    const { mensagem } = await request.json();

    if (!mensagem || typeof mensagem !== 'string') {
      return NextResponse.json(
        { error: 'Mensagem é obrigatória' },
        { status: 400 }
      );
    }

    // Buscar prato mencionado na mensagem
    const prato = buscarPrato(mensagem);

    if (!prato) {
      return NextResponse.json({
        recomendacao: null,
        mensagem: 'Desculpe, não encontrei informações sobre esse prato. Tente mencionar um prato específico como "salmão grelhado", "picanha" ou "risotto".'
      });
    }

    // Buscar vinhos compatíveis
    const vinhosCompativeis = buscarVinhosCompativeis(prato);

    if (vinhosCompativeis.length === 0) {
      return NextResponse.json({
        recomendacao: null,
        mensagem: 'Não encontrei vinhos compatíveis para este prato.'
      });
    }

    // Selecionar o melhor vinho (primeiro da lista ordenada)
    const vinhoRecomendado = vinhosCompativeis[0];

    // Processar recomendação com LLM para gerar justificativa
    const recomendacao = await processarRecomendacao(prato, vinhoRecomendado);

    // Gerar mensagem de resposta
    const mensagemResposta = `Para o prato "${prato.nome}", recomendo o ${vinhoRecomendado.nome} (${vinhoRecomendado.tipo}, ${vinhoRecomendado.uva}). ${recomendacao.justificativa}`;

    return NextResponse.json({
      recomendacao,
      mensagem: mensagemResposta
    });
  } catch (error) {
    console.error('Erro ao processar recomendação:', error);
    return NextResponse.json(
      { error: 'Erro ao processar recomendação' },
      { status: 500 }
    );
  }
}

