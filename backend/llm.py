"""
Sistema de Justificativa de Recomendação de Vinhos usando DSPy
Gera explicações em português sobre por que um vinho foi recomendado para um prato
"""

import dspy
import os
import sys
from typing import Optional
from dotenv import load_dotenv

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Carregar variáveis de ambiente
load_dotenv()


class WineRecommendationSignature(dspy.Signature):
    """Gera justificativa detalhada em português para recomendação de vinho."""
    
    nome_prato = dspy.InputField(desc="Nome do prato")
    tipo_prato = dspy.InputField(desc="Tipo do prato (carne vermelha, peixe, etc)")
    temperos = dspy.InputField(desc="Temperos do prato")
    acidez = dspy.InputField(desc="Acidez do prato")
    intensidade_sabor = dspy.InputField(desc="Intensidade de sabor do prato")
    ingredientes = dspy.InputField(desc="Ingredientes principais do prato")
    
    vinho_recomendado = dspy.InputField(desc="Nome do vinho recomendado")
    tipo_vinho = dspy.InputField(desc="Tipo do vinho (tinto seco, branco seco, etc)")
    similaridade_percentual = dspy.InputField(desc="Percentual de similaridade")
    score_caracteristicas = dspy.InputField(desc="Score baseado em características")
    score_regras = dspy.InputField(desc="Score baseado em regras de harmonização")
    
    justificativa = dspy.OutputField(
        desc="Justificativa detalhada em português sobre por que este vinho harmoniza perfeitamente com o prato. "
             "Deve mencionar as características do prato, do vinho, e explicar a harmonização de forma educativa e elegante. "
             "Use 2-3 parágrafos com linguagem sofisticada mas acessível."
    )


class WineJustificationModule(dspy.Module):
    """Módulo DSPy para gerar justificativas de recomendação de vinhos."""
    
    def __init__(self):
        super().__init__()
        # Use Predict instead of ChainOfThought for better compatibility
        self.generate_justification = dspy.Predict(WineRecommendationSignature)
    
    def forward(
        self,
        nome_prato: str,
        tipo_prato: str,
        temperos: str,
        acidez: str,
        intensidade_sabor: str,
        ingredientes: str,
        vinho_recomendado: str,
        tipo_vinho: str,
        similaridade_percentual: float,
        score_caracteristicas: float,
        score_regras: float
    ):
        """
        Gera justificativa para a recomendação de vinho.
        
        Args:
            nome_prato: Nome do prato
            tipo_prato: Tipo do prato
            temperos: Temperos utilizados
            acidez: Nível de acidez
            intensidade_sabor: Intensidade do sabor
            ingredientes: Ingredientes principais
            vinho_recomendado: Nome do vinho recomendado
            tipo_vinho: Tipo do vinho
            similaridade_percentual: Score de similaridade
            score_caracteristicas: Score por características
            score_regras: Score por regras
            
        Returns:
            Predição com justificativa
        """
        result = self.generate_justification(
            nome_prato=nome_prato,
            tipo_prato=tipo_prato,
            temperos=temperos,
            acidez=acidez,
            intensidade_sabor=intensidade_sabor,
            ingredientes=ingredientes,
            vinho_recomendado=vinho_recomendado,
            tipo_vinho=tipo_vinho,
            similaridade_percentual=str(similaridade_percentual),
            score_caracteristicas=str(score_caracteristicas),
            score_regras=str(score_regras)
        )
        
        return result


def configurar_llm(model: str = "sonar", api_key: Optional[str] = None):
    """
    Configura o modelo de linguagem para o DSPy.
    
    Args:
        model: Nome do modelo (default: perplexity/llama-3.1-sonar-large-128k-online)
        api_key: Chave da API Perplexity (opcional, usa variável de ambiente se não fornecida)
    """
    if api_key is None:
        api_key = os.getenv("PERPLEXITY_API_KEY")
    
    if not api_key:
        raise ValueError(
            "API key não encontrada. Configure PERPLEXITY_API_KEY no arquivo .env ou passe como parâmetro."
        )
    
    # Perplexity requires specific configuration without structured outputs
    lm = dspy.LM(
        model=model, 
        api_key=api_key, 
        api_base="https://api.perplexity.ai",
        temperature=0.7,
        max_tokens=2000,
        response_format={"type": "text"}
    )
    dspy.configure(lm=lm)
    print(f"✅ Modelo {model} configurado com sucesso!")
    return lm


def gerar_justificativa_vinho(
    nome_prato: str,
    caracteristicas_prato: dict,
    vinho_info: dict
) -> str:
    """
    Função principal para gerar justificativa de recomendação de vinho.
    
    Args:
        nome_prato: Nome do prato
        caracteristicas_prato: Dicionário com características do prato
        vinho_info: Dicionário com informações do vinho recomendado
        
    Returns:
        Justificativa em português
    """
    # Inicializar módulo
    justifier = WineJustificationModule()
    
    # Gerar justificativa
    resultado = justifier(
        nome_prato=nome_prato,
        tipo_prato=caracteristicas_prato.get('tipo_prato', ''),
        temperos=caracteristicas_prato.get('temperos', ''),
        acidez=caracteristicas_prato.get('acidez', ''),
        intensidade_sabor=caracteristicas_prato.get('intensidade_sabor', ''),
        ingredientes=caracteristicas_prato.get('ingredientes', ''),
        vinho_recomendado=vinho_info.get('vinho', ''),
        tipo_vinho=vinho_info.get('tipo_vinho', ''),
        similaridade_percentual=vinho_info.get('similaridade_percentual', 0),
        score_caracteristicas=vinho_info.get('score_features', 0),
        score_regras=vinho_info.get('score_regras', 0)
    )
    
    return resultado.justificativa


# ============================================================================
# EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    import sys
    
    # Configurar LLM
    try:
        configurar_llm()
    except ValueError as e:
        print(f"❌ Erro: {e}")
        print("\n💡 Para usar este sistema, você precisa:")
        print("1. Criar um arquivo .env na raiz do projeto")
        print("2. Adicionar sua chave: PERPLEXITY_API_KEY=sua_chave_aqui")
        print("\nOu execute: cp .env.example .env e edite o arquivo")
        print("\nObtenha sua chave em: https://www.perplexity.ai/settings/api")
        sys.exit(1)
    
    # Exemplo de uso
    print("\n" + "="*80)
    print("🍷 GERADOR DE JUSTIFICATIVAS DE HARMONIZAÇÃO")
    print("="*80 + "\n")
    
    # Exemplo: Sushi com Pinot Grigio
    exemplo_prato = {
        'tipo_prato': 'peixe',
        'temperos': 'suave',
        'acidez': 'alta',
        'intensidade_sabor': 'baixa',
        'ingredientes': 'arroz, peixe cru'
    }
    
    exemplo_vinho = {
        'vinho': 'Pinot Grigio',
        'tipo_vinho': 'branco seco',
        'similaridade_percentual': 98.14,
        'score_features': 95.35,
        'score_regras': 100.0
    }
    
    print(f"📍 Prato: Sushi")
    print(f"🍾 Vinho: {exemplo_vinho['vinho']}")
    print(f"📊 Similaridade: {exemplo_vinho['similaridade_percentual']}%\n")
    print("-" * 80)
    
    justificativa = gerar_justificativa_vinho(
        nome_prato="Sushi",
        caracteristicas_prato=exemplo_prato,
        vinho_info=exemplo_vinho
    )
    
    print("\n📝 JUSTIFICATIVA DA HARMONIZAÇÃO:\n")
    print(justificativa)
    print("\n" + "="*80)
