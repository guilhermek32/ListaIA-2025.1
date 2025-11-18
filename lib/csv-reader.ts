import { readFileSync } from 'fs';
import { join } from 'path';
import { Prato, Vinho } from '@/types';

// Interface para dados brutos do CSV de pratos
interface PratoCSV {
  id_prato: string;
  nome_prato: string;
  ingredientes: string;
  tipo_prato: string;
  temperos: string;
  acidez: 'baixa' | 'média' | 'alta';
  intensidade_sabor: 'baixa' | 'média' | 'alta';
}

// Interface para dados brutos do CSV de vinhos
interface VinhoCSV {
  vinho: string;
  tipo_vinho: string;
}

// Função para parsear CSV
function parseCSV<T>(content: string, headers: string[]): T[] {
  const lines = content.trim().split('\n');
  const data: T[] = [];

  for (let i = 1; i < lines.length; i++) {
    const line = lines[i].trim();
    if (!line) continue;

    // Parse manual considerando aspas e vírgulas
    const values: string[] = [];
    let current = '';
    let inQuotes = false;

    for (let j = 0; j < line.length; j++) {
      const char = line[j];
      
      if (char === '"') {
        inQuotes = !inQuotes;
      } else if (char === ',' && !inQuotes) {
        values.push(current.trim());
        current = '';
      } else {
        current += char;
      }
    }
    values.push(current.trim()); // Último valor

    if (values.length === headers.length) {
      const obj: any = {};
      headers.forEach((header, index) => {
        obj[header] = values[index];
      });
      data.push(obj as T);
    }
  }

  return data;
}

// Cache para os dados carregados
let pratosCache: Prato[] | null = null;
let vinhosCache: Vinho[] | null = null;

// Função para carregar pratos do CSV
export function carregarPratos(): Prato[] {
  if (pratosCache) {
    return pratosCache;
  }

  try {
    const csvPath = join(process.cwd(), 'db', 'pratos.csv');
    const csvContent = readFileSync(csvPath, 'utf-8');
    
    const headers = ['id_prato', 'nome_prato', 'ingredientes', 'tipo_prato', 'temperos', 'acidez', 'intensidade_sabor'];
    const pratosCSV = parseCSV<PratoCSV>(csvContent, headers);

    pratosCache = pratosCSV.map((p): Prato => ({
      id: p.id_prato,
      nome: p.nome_prato,
      descricao: `${p.nome_prato} com ${p.ingredientes}`,
      tipo: p.tipo_prato,
      ingredientes: p.ingredientes.split(',').map(i => i.trim()),
      intensidade: mapearIntensidade(p.intensidade_sabor),
      // Campos adicionais do CSV que podem ser úteis
      acidez: p.acidez,
      temperos: p.temperos,
    } as Prato & { acidez: string; temperos: string }));

    return pratosCache;
  } catch (error) {
    console.error('Erro ao carregar pratos do CSV:', error);
    return [];
  }
}

// Função para carregar vinhos do CSV
export function carregarVinhos(): Vinho[] {
  if (vinhosCache) {
    return vinhosCache;
  }

  try {
    const csvPath = join(process.cwd(), 'db', 'vinhos.csv');
    const csvContent = readFileSync(csvPath, 'utf-8');
    
    const headers = ['vinho', 'tipo_vinho'];
    const vinhosCSV = parseCSV<VinhoCSV>(csvContent, headers);

    vinhosCache = vinhosCSV.map((v, index): Vinho => {
      const tipoInfo = extrairTipoVinho(v.tipo_vinho);
      
      return {
        id: (index + 1).toString(),
        nome: v.vinho,
        tipo: tipoInfo.tipo,
        uva: v.vinho, // O nome do vinho geralmente é a uva
        regiao: 'Brasil', // Default, pode ser expandido depois
        descricao: `Vinho ${tipoInfo.tipo} ${tipoInfo.caracteristica}`,
        harmonizacao: obterHarmonizacaoPadrao(tipoInfo.tipo),
        tipoCompleto: v.tipo_vinho,
      };
    });

    return vinhosCache;
  } catch (error) {
    console.error('Erro ao carregar vinhos do CSV:', error);
    return [];
  }
}

// Função auxiliar para mapear intensidade
function mapearIntensidade(intensidade: string): 'leve' | 'média' | 'intensa' {
  if (intensidade.toLowerCase() === 'alta') return 'intensa';
  if (intensidade.toLowerCase() === 'média') return 'média';
  return 'leve';
}

// Função para extrair tipo e característica do vinho
function extrairTipoVinho(tipoVinho: string): { tipo: string; caracteristica: string } {
  const partes = tipoVinho.toLowerCase().split(' ');
  const tipo = partes[0]; // tinto, branco, rosé, espumante, licoroso
  const caracteristica = partes.slice(1).join(' ') || 'seco';
  
  return { tipo, caracteristica };
}

// Função para obter harmonização padrão baseada no tipo
function obterHarmonizacaoPadrao(tipo: string): string[] {
  const harmonizacoes: Record<string, string[]> = {
    'tinto': ['carnes vermelhas', 'queijos curados', 'massas com molho vermelho'],
    'branco': ['peixes', 'frutos do mar', 'aves', 'saladas'],
    'rosé': ['aves', 'peixes', 'queijos suaves'],
    'espumante': ['aperitivos', 'frutos do mar', 'sobremesas leves'],
    'licoroso': ['sobremesas', 'queijos azuis'],
  };

  return harmonizacoes[tipo] || ['pratos diversos'];
}

// Função para limpar cache (útil para desenvolvimento)
export function limparCache() {
  pratosCache = null;
  vinhosCache = null;
}

