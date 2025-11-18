export interface Prato {
  id: string;
  nome: string;
  descricao: string;
  tipo: string; // tipo_prato do CSV (carne vermelha, peixe, vegetariano, etc.)
  ingredientes: string[];
  intensidade: 'leve' | 'média' | 'intensa';
  acidez?: 'baixa' | 'média' | 'alta';
  temperos?: string;
}

export interface Vinho {
  id: string;
  nome: string;
  tipo: string; // tinto, branco, rosé, espumante, licoroso
  uva: string;
  regiao: string;
  descricao: string;
  harmonizacao: string[];
  tipoCompleto?: string; // tipo_vinho completo do CSV (ex: "tinto seco")
}

export interface Mensagem {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface Recomendacao {
  prato: Prato;
  vinho: Vinho;
  justificativa: string;
  score: number;
}

export interface ChatResponse {
  recomendacao: Recomendacao;
  mensagem: string;
}

