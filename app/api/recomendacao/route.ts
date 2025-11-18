import { NextRequest, NextResponse } from 'next/server';

const PYTHON_API_URL = process.env.PYTHON_API_URL || 'http://localhost:8000';

export async function POST(request: NextRequest) {
  try {
    const { mensagem } = await request.json();

    if (!mensagem || typeof mensagem !== 'string') {
      return NextResponse.json(
        { error: 'Mensagem é obrigatória' },
        { status: 400 }
      );
    }

    // Forward request to Python FastAPI backend
    const response = await fetch(`${PYTHON_API_URL}/api/recomendacao`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ mensagem }),
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`Python API error: ${error}`);
    }

    const data = await response.json();
    
    return NextResponse.json(data);
  } catch (error) {
    console.error('Erro ao processar recomendação:', error);
    return NextResponse.json(
      { error: 'Erro ao processar recomendação. Verifique se o servidor Python está rodando.' },
      { status: 500 }
    );
  }
}

