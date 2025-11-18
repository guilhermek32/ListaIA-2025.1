"""
Sistema Integrado de Recomendação de Vinhos com Justificativa por LLM
Combina o sistema de recomendação com geração de justificativas usando DSPy
"""

import pandas as pd
import sys
from sistema_recomendacao_vinho import (
    recomendar_vinho, 
    df_pratos, 
    df_vinhos,
    sistema_recomendacao_vinho
)
from llm import configurar_llm, gerar_justificativa_vinho

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def sistema_completo_com_justificativa(nome_prato: str, usar_llm: bool = True):
    """
    Sistema completo que recomenda vinhos e gera justificativas usando LLM.
    
    Args:
        nome_prato: Nome do prato para harmonização
        usar_llm: Se True, gera justificativa com LLM; se False, apenas recomendação
    """
    print("="*80)
    print("🍷 SISTEMA COMPLETO DE RECOMENDAÇÃO E JUSTIFICATIVA")
    print("="*80)
    print(f"\nPrato selecionado: {nome_prato}")
    
    # Buscar informações do prato
    prato = df_pratos[df_pratos['nome_prato'] == nome_prato]
    
    if prato.empty:
        print(f"\n❌ Erro: Prato '{nome_prato}' não encontrado.")
        print("\nPratos disponíveis:")
        for p in df_pratos['nome_prato'].head(10):
            print(f"  - {p}")
        print(f"  ... e mais {len(df_pratos) - 10} pratos")
        return
    
    prato_info = prato.iloc[0]
    
    # Mostrar características do prato
    print(f"\nCaracterísticas do prato:")
    print(f"  • Tipo: {prato_info['tipo_prato']}")
    print(f"  • Tempero: {prato_info['temperos']}")
    print(f"  • Acidez: {prato_info['acidez']}")
    print(f"  • Intensidade de sabor: {prato_info['intensidade_sabor']}")
    print(f"  • Ingredientes: {prato_info['ingredientes']}")
    
    # Obter recomendações
    recomendacoes = recomendar_vinho(nome_prato, df_pratos, df_vinhos, top_n=3)
    
    print("\n" + "="*80)
    print("🏆 TOP 3 VINHOS RECOMENDADOS")
    print("="*80)
    
    # Mostrar recomendações
    for idx, (i, vinho) in enumerate(recomendacoes.iterrows(), 1):
        print(f"\n{idx}º lugar - {vinho['vinho']} ({vinho['tipo_vinho']})")
        print(f"   Similaridade: {vinho['similaridade_percentual']}%")
        print(f"   • Score por características: {vinho['score_features']}%")
        print(f"   • Score por regras de harmonização: {vinho['score_regras']}%")
    
    # Gerar justificativa para o primeiro colocado usando LLM
    if usar_llm:
        print("\n" + "="*80)
        print("🤖 JUSTIFICATIVA GERADA POR IA")
        print("="*80)
        
        try:
            # Configurar LLM se ainda não foi configurado
            try:
                configurar_llm()
            except Exception:
                pass  # LLM já configurado
            
            # Pegar o primeiro vinho recomendado
            melhor_vinho = recomendacoes.iloc[0]
            
            # Preparar dados para a justificativa
            caracteristicas_prato = {
                'tipo_prato': prato_info['tipo_prato'],
                'temperos': prato_info['temperos'],
                'acidez': prato_info['acidez'],
                'intensidade_sabor': prato_info['intensidade_sabor'],
                'ingredientes': prato_info['ingredientes']
            }
            
            vinho_info = {
                'vinho': melhor_vinho['vinho'],
                'tipo_vinho': melhor_vinho['tipo_vinho'],
                'similaridade_percentual': melhor_vinho['similaridade_percentual'],
                'score_features': melhor_vinho['score_features'],
                'score_regras': melhor_vinho['score_regras']
            }
            
            print(f"\n🔄 Gerando justificativa para: {melhor_vinho['vinho']}...\n")
            
            # Gerar justificativa
            justificativa = gerar_justificativa_vinho(
                nome_prato=nome_prato,
                caracteristicas_prato=caracteristicas_prato,
                vinho_info=vinho_info
            )
            
            print("📝 JUSTIFICATIVA DA HARMONIZAÇÃO:\n")
            print(justificativa)
            
        except ValueError as e:
            print(f"\n⚠️  Aviso: Não foi possível gerar justificativa com LLM")
            print(f"    Motivo: {e}")
            print("\n💡 Para habilitar justificativas com IA:")
            print("    1. Crie um arquivo .env na raiz do projeto")
            print("    2. Adicione: PERPLEXITY_API_KEY=sua_chave_aqui")
            print("    3. Execute novamente o sistema")
        except Exception as e:
            print(f"\n⚠️  Erro ao gerar justificativa: {e}")
    
    print("\n" + "="*80)
    return recomendacoes


# ============================================================================
# EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    # Lista de pratos para testar
    pratos_teste = [
        "Sushi",
        "Filé ao molho madeira",
        "Feijoada"
    ]
    
    print("\n🍷 Bem-vindo ao Sistema Integrado de Recomendação de Vinhos!")
    print("="*80)
    print("\nEste sistema:")
    print("  ✓ Analisa características do prato")
    print("  ✓ Recomenda os 3 melhores vinhos")
    print("  ✓ Gera justificativa detalhada usando IA (requer OpenAI API key)")
    print("\n" + "="*80 + "\n")
    
    for prato in pratos_teste:
        sistema_completo_com_justificativa(prato, usar_llm=True)
        print("\n\n")
