import { Prato, Vinho } from '@/types';
import { carregarPratos, carregarVinhos } from '@/lib/csv-reader';

// Carregar dados dos CSVs
let pratosCache: Prato[] | null = null;
let vinhosCache: Vinho[] | null = null;

function getPratos(): Prato[] {
  if (!pratosCache) {
    pratosCache = carregarPratos();
  }
  return pratosCache;
}

function getVinhos(): Vinho[] {
  if (!vinhosCache) {
    vinhosCache = carregarVinhos();
  }
  return vinhosCache;
}
 
// Função para buscar prato por nome ou descrição
export function buscarPrato(query: string): Prato | null {
  const pratos = getPratos();
  const queryLower = query.toLowerCase();
  
  return pratos.find(
    prato =>
      prato.nome.toLowerCase().includes(queryLower) ||
      prato.descricao.toLowerCase().includes(queryLower) ||
      prato.ingredientes.some(ing => ing.toLowerCase().includes(queryLower)) ||
      prato.tipo.toLowerCase().includes(queryLower)
  ) || null;
}

// Função para buscar vinhos compatíveis
export function buscarVinhosCompativeis(prato: Prato): Vinho[] {
  const vinhos = getVinhos();
  const vinhosCompativeis: Vinho[] = [];

  for (const vinho of vinhos) {
    let score = 0;

    // Regras básicas de harmonização
    // Carnes vermelhas intensas combinam com tintos
    if (prato.tipo === 'carne vermelha' && prato.intensidade === 'intensa' && vinho.tipo === 'tinto') {
      score += 5;
    }
    
    // Peixes e frutos do mar combinam com brancos
    if ((prato.tipo === 'peixe' || prato.tipo === 'frutos do mar') && vinho.tipo === 'branco') {
      score += 5;
    }
    
    // Carnes brancas combinam com brancos ou tintos leves
    if (prato.tipo === 'carne branca' && (vinho.tipo === 'branco' || vinho.tipo === 'tinto')) {
      score += 4;
    }
    
    // Vegetarianos combinam com brancos ou espumantes
    if (prato.tipo === 'vegetariano' && (vinho.tipo === 'branco' || vinho.tipo === 'espumante')) {
      score += 4;
    }
    
    // Intensidade alta combina com tintos
    if (prato.intensidade === 'intensa' && vinho.tipo === 'tinto') {
      score += 3;
    }
    
    // Intensidade leve combina com brancos ou espumantes
    if (prato.intensidade === 'leve' && (vinho.tipo === 'branco' || vinho.tipo === 'espumante')) {
      score += 3;
    }
    
    // Acidez alta do prato combina com vinhos com acidez
    if (prato.acidez === 'alta' && vinho.tipo === 'branco') {
      score += 2;
    }
    
    // Verificar harmonização por ingredientes
    if (prato.ingredientes.some(ing => 
      vinho.harmonizacao.some(h => 
        ing.toLowerCase().includes(h.toLowerCase()) || 
        h.toLowerCase().includes(ing.toLowerCase())
      )
    )) {
      score += 2;
    }

    if (score > 0) {
      vinhosCompativeis.push({ ...vinho, score } as Vinho & { score: number });
    }
  }

  // Ordenar por score (maior primeiro)
  return vinhosCompativeis.sort((a, b) => {
    const scoreA = (a as Vinho & { score: number }).score || 0;
    const scoreB = (b as Vinho & { score: number }).score || 0;
    return scoreB - scoreA;
  });
}

