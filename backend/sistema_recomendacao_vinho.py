"""
Sistema de Recomendação de Vinhos
Baseado em similaridade de características e regras de harmonização
"""

import pandas as pd
import numpy as np
import sys
from sklearn.metrics.pairwise import cosine_similarity

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# ============================================================================
# BASES DE DADOS - Carregadas de CSV
# ============================================================================

# Carregar dados dos CSVs
df_pratos = pd.read_csv('pratos.csv')
df_vinhos = pd.read_csv('vinhos.csv')

# Características dos vinhos (conhecimento especializado)
# Mapeamento expandido baseado nos tipos de vinho
caracteristicas_vinhos = {
    # Tintos secos
    'Cabernet Sauvignon': {'acidez': 2, 'intensidade': 3, 'docura': 1, 'tanino': 3},
    'Malbec': {'acidez': 2, 'intensidade': 3, 'docura': 1, 'tanino': 3},
    'Syrah': {'acidez': 2, 'intensidade': 3, 'docura': 1, 'tanino': 3},
    'Zinfandel': {'acidez': 2, 'intensidade': 3, 'docura': 1, 'tanino': 3},
    'Carmenere': {'acidez': 2, 'intensidade': 3, 'docura': 1, 'tanino': 3},
    'Tannat': {'acidez': 2, 'intensidade': 3, 'docura': 1, 'tanino': 3},
    'Tempranillo': {'acidez': 2, 'intensidade': 3, 'docura': 1, 'tanino': 3},
    'Cabernet Franc': {'acidez': 2, 'intensidade': 3, 'docura': 1, 'tanino': 2},
    'Sangiovese': {'acidez': 3, 'intensidade': 2, 'docura': 1, 'tanino': 2},
    'Nebbiolo': {'acidez': 3, 'intensidade': 3, 'docura': 1, 'tanino': 3},
    
    # Tintos suaves/leves
    'Merlot': {'acidez': 2, 'intensidade': 2, 'docura': 1, 'tanino': 2},
    'Pinot Noir': {'acidez': 3, 'intensidade': 2, 'docura': 1, 'tanino': 1},
    'Grenache': {'acidez': 2, 'intensidade': 2, 'docura': 1, 'tanino': 1},
    'Primitivo': {'acidez': 2, 'intensidade': 2, 'docura': 2, 'tanino': 2},
    
    # Brancos secos
    'Chardonnay': {'acidez': 2, 'intensidade': 2, 'docura': 1, 'tanino': 0},
    'Sauvignon Blanc': {'acidez': 3, 'intensidade': 1, 'docura': 1, 'tanino': 0},
    'Verdejo': {'acidez': 2, 'intensidade': 2, 'docura': 1, 'tanino': 0},
    'Pinot Grigio': {'acidez': 3, 'intensidade': 1, 'docura': 1, 'tanino': 0},
    'Alvarinho': {'acidez': 3, 'intensidade': 2, 'docura': 1, 'tanino': 0},
    'Chenin Blanc': {'acidez': 3, 'intensidade': 2, 'docura': 1, 'tanino': 0},
    'Vinho Verde': {'acidez': 3, 'intensidade': 1, 'docura': 1, 'tanino': 0},
    'Albariño': {'acidez': 3, 'intensidade': 2, 'docura': 1, 'tanino': 0},
    
    # Brancos doces/aromáticos
    'Riesling': {'acidez': 3, 'intensidade': 1, 'docura': 3, 'tanino': 0},
    'Gewürztraminer': {'acidez': 2, 'intensidade': 2, 'docura': 2, 'tanino': 0},
    
    # Rosé
    'Rosé': {'acidez': 3, 'intensidade': 1, 'docura': 1, 'tanino': 0},
    
    # Espumantes
    'Prosecco': {'acidez': 3, 'intensidade': 1, 'docura': 1, 'tanino': 0},
    'Espumante Brut': {'acidez': 3, 'intensidade': 2, 'docura': 1, 'tanino': 0},
    
    # Licorosos
    'Sake': {'acidez': 1, 'intensidade': 1, 'docura': 2, 'tanino': 0}
}

# ============================================================================
# PREPARAÇÃO DOS DADOS
# ============================================================================

# Adicionar características ao dataframe de vinhos
for col in ['acidez_vinho', 'intensidade_vinho', 'docura', 'tanino']:
    col_key = col.replace('_vinho', '')
    df_vinhos[col] = df_vinhos['vinho'].apply(
        lambda x: caracteristicas_vinhos[x][col_key]
    )

# ============================================================================
# FUNÇÕES DO SISTEMA
# ============================================================================

def codificar_pratos(df):
    """Converte atributos categóricos dos pratos em valores numéricos"""
    df_encoded = df.copy()

    # Mapear tipo de prato
    # Baseado em intensidade de proteína e peso do prato
    tipo_map = {
        'carne vermelha': 5,    # Proteína mais forte e intensa
        'carne branca': 3,      # Proteína moderada
        'frutos do mar': 2,     # Proteína delicada, sabor do mar
        'peixe': 2,             # Proteína delicada, similar a frutos do mar
        'vegetariano': 1        # Sem proteína animal, mais leve
    }

    # Mapear temperos (expandido)
    tempero_map = {
        'intenso': 3, 
        'picante': 3, 
        'forte': 3,
        'defumado': 3,
        'moderado': 2, 
        'cremoso': 2,
        'terroso': 2,
        'salgado': 2,
        'doce': 2,
        'herbal': 1,
        'cítrico': 1,
        'suave': 1
    }

    # Mapear acidez
    acidez_map = {'baixa': 1, 'média': 2, 'alta': 3}

    # Mapear intensidade
    intensidade_map = {'baixa': 1, 'média': 2, 'alta': 3}

    df_encoded['tipo_prato_num'] = df_encoded['tipo_prato'].map(tipo_map)
    df_encoded['temperos_num'] = df_encoded['temperos'].map(tempero_map)
    df_encoded['acidez_num'] = df_encoded['acidez'].map(acidez_map)
    df_encoded['intensidade_num'] = df_encoded['intensidade_sabor'].map(intensidade_map)

    return df_encoded

def recomendar_vinho(nome_prato, df_pratos, df_vinhos, top_n=5):
    """
    Recomenda vinhos baseado em similaridade e regras de harmonização

    Parâmetros:
    - nome_prato: nome do prato a ser harmonizado
    - df_pratos: DataFrame com informações dos pratos
    - df_vinhos: DataFrame com informações dos vinhos
    - top_n: número de recomendações a retornar

    Retorna: DataFrame com top_n vinhos recomendados e seus scores
    """
    # Encontrar o prato
    prato = df_pratos[df_pratos['nome_prato'] == nome_prato]

    if prato.empty:
        return f"Prato '{nome_prato}' não encontrado na base de dados."

    prato = prato.iloc[0]

    # Codificar o prato
    df_pratos_encoded = codificar_pratos(df_pratos)
    prato_encoded = df_pratos_encoded[df_pratos_encoded['nome_prato'] == nome_prato].iloc[0]

    # Regras de harmonização baseadas no tipo de prato (expandido)
    regras_harmonizacao = {
        'carne vermelha': {
            'tinto seco': 1.0, 
            'tinto suave': 0.8, 
            'tinto leve': 0.7,
            'tinto frutado': 0.8,
            'branco seco': 0.3, 
            'branco doce': 0.2,
            'branco aromático': 0.3,
            'rosé seco': 0.4,
            'espumante': 0.3,
            'licoroso': 0.2
        },
        'carne branca': {
            'branco seco': 0.9, 
            'tinto suave': 0.7, 
            'tinto leve': 0.8,
            'tinto seco': 0.5, 
            'branco doce': 0.6,
            'branco aromático': 0.7,
            'rosé seco': 0.8,
            'espumante': 0.7,
            'tinto frutado': 0.6,
            'licoroso': 0.3
        },
        'peixe': {
            'branco seco': 1.0, 
            'branco doce': 0.6, 
            'branco aromático': 0.8,
            'tinto suave': 0.3, 
            'tinto leve': 0.4,
            'tinto seco': 0.2,
            'rosé seco': 0.7,
            'espumante': 0.8,
            'tinto frutado': 0.3,
            'licoroso': 0.7
        },
        'vegetariano': {
            'branco seco': 0.8, 
            'branco doce': 0.7, 
            'branco aromático': 0.7,
            'tinto suave': 0.6, 
            'tinto leve': 0.7,
            'tinto seco': 0.5,
            'rosé seco': 0.8,
            'espumante': 0.9,
            'tinto frutado': 0.6,
            'licoroso': 0.4
        },
        'frutos do mar': {
            'branco seco': 1.0,
            'branco aromático': 0.8,
            'branco doce': 0.5,
            'rosé seco': 0.7,
            'espumante': 0.9,
            'tinto leve': 0.3,
            'tinto suave': 0.3,
            'tinto seco': 0.2,
            'tinto frutado': 0.3,
            'licoroso': 0.6
        }
    }

    # Criar vetor de características do prato
    features_prato = np.array([
        prato_encoded['acidez_num'],
        prato_encoded['intensidade_num'],
        prato_encoded['temperos_num']
    ]).reshape(1, -1)

    # Calcular similaridade com cada vinho
    resultados = []

    for idx, vinho in df_vinhos.iterrows():
        # Verificar se o vinho existe nas características
        if vinho['vinho'] not in caracteristicas_vinhos:
            continue
            
        # Vetor de características do vinho
        features_vinho = np.array([
            caracteristicas_vinhos[vinho['vinho']]['acidez'],
            caracteristicas_vinhos[vinho['vinho']]['intensidade'],
            caracteristicas_vinhos[vinho['vinho']]['tanino'] if caracteristicas_vinhos[vinho['vinho']]['tanino'] > 0 else 0
        ]).reshape(1, -1)

        # Similaridade de cosseno entre características
        similaridade_features = cosine_similarity(features_prato, features_vinho)[0][0]

        # Score de harmonização baseado em regras
        tipo_prato = prato['tipo_prato']
        tipo_vinho = vinho['tipo_vinho']
        score_regra = regras_harmonizacao.get(tipo_prato, {}).get(tipo_vinho, 0.5)

        # Score final: 40% similaridade de características + 60% regras
        score_final = (similaridade_features * 0.4) + (score_regra * 0.6)

        # Converter para percentual
        percentual_similaridade = round(score_final * 100, 2)

        resultados.append({
            'vinho': vinho['vinho'],
            'tipo_vinho': vinho['tipo_vinho'],
            'similaridade_percentual': percentual_similaridade,
            'score_features': round(similaridade_features * 100, 2),
            'score_regras': round(score_regra * 100, 2)
        })

    # Ordenar por similaridade
    resultados_df = pd.DataFrame(resultados)
    resultados_df = resultados_df.sort_values('similaridade_percentual', ascending=False)

    return resultados_df.head(top_n)

def sistema_recomendacao_vinho(nome_prato_input):
    """
    Interface principal do sistema de recomendação
    """
    print("="*80)
    print("🍷 SISTEMA DE RECOMENDAÇÃO DE VINHOS 🍷")
    print("="*80)
    print(f"\nPrato selecionado: {nome_prato_input}")

    # Buscar informações do prato
    prato = df_pratos[df_pratos['nome_prato'] == nome_prato_input]

    if prato.empty:
        print(f"\n❌ Erro: Prato '{nome_prato_input}' não encontrado.")
        print("\nPratos disponíveis:")
        for p in df_pratos['nome_prato']:
            print(f"  - {p}")
        return

    prato_info = prato.iloc[0]

    print(f"\nCaracterísticas do prato:")
    print(f"  • Tipo: {prato_info['tipo_prato']}")
    print(f"  • Tempero: {prato_info['temperos']}")
    print(f"  • Acidez: {prato_info['acidez']}")
    print(f"  • Intensidade de sabor: {prato_info['intensidade_sabor']}")
    print(f"  • Ingredientes: {prato_info['ingredientes']}")

    # Obter recomendações
    recomendacoes = recomendar_vinho(nome_prato_input, df_pratos, df_vinhos, top_n=3)

    print("\n" + "="*80)
    print("🏆 TOP 3 VINHOS RECOMENDADOS")
    print("="*80)

    for idx, (i, vinho) in enumerate(recomendacoes.iterrows(), 1):
        print(f"\n{idx}º lugar - {vinho['vinho']} ({vinho['tipo_vinho']})")
        print(f"   Similaridade: {vinho['similaridade_percentual']}%")
        print(f"   • Score por características: {vinho['score_features']}%")
        print(f"   • Score por regras de harmonização: {vinho['score_regras']}%")

    print("\n" + "="*80)

    return recomendacoes

# ============================================================================
# EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    # Testar com diferentes pratos da base de dados
    pratos_teste = [
        "Filé ao molho madeira", 
        "Salmão grelhado", 
        "Frango ao curry",
        "Picanha na brasa",
        "Camarão ao alho e óleo",
        "Risoto de limão siciliano"
    ]

    for prato in pratos_teste:
        sistema_recomendacao_vinho(prato)
        print("\n")
