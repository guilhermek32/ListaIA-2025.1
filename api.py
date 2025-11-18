"""
FastAPI Backend for Wine Recommendation System
Connects Next.js frontend with Python recommendation engine
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

# Change to backend directory for CSV loading
os.chdir(backend_path)

from sistema_recomendacao_vinho import recomendar_vinho, df_pratos, df_vinhos
from llm import configurar_llm, gerar_justificativa_vinho

# Initialize FastAPI app
app = FastAPI(
    title="Wine Recommendation API",
    description="API for wine recommendation with AI-generated justifications",
    version="1.0.0"
)

# Configure CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class RecomendacaoRequest(BaseModel):
    mensagem: str

class VinhoResponse(BaseModel):
    nome: str
    tipo: str
    similaridade: float
    score_features: float
    score_regras: float

class RecomendacaoResponse(BaseModel):
    prato: str
    vinho: VinhoResponse
    justificativa: str
    mensagem: str

# Initialize LLM (try to configure, fallback if no API key)
try:
    configurar_llm()
    LLM_AVAILABLE = True
    print("✅ LLM configured successfully")
except Exception as e:
    LLM_AVAILABLE = False
    print(f"⚠️ LLM not available: {e}")

def buscar_prato_no_csv(query: str) -> Optional[dict]:
    """Find dish in CSV by name or similar text"""
    query_lower = query.lower()
    
    # Try exact match first
    prato = df_pratos[df_pratos['nome_prato'].str.lower() == query_lower]
    if not prato.empty:
        return prato.iloc[0].to_dict()
    
    # Try partial match
    prato = df_pratos[df_pratos['nome_prato'].str.lower().str.contains(query_lower, na=False)]
    if not prato.empty:
        return prato.iloc[0].to_dict()
    
    # Try searching in ingredients
    prato = df_pratos[df_pratos['ingredientes'].str.lower().str.contains(query_lower, na=False)]
    if not prato.empty:
        return prato.iloc[0].to_dict()
    
    return None

@app.get("/")
def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Wine Recommendation API",
        "version": "1.0.0",
        "llm_available": LLM_AVAILABLE,
        "dishes_count": len(df_pratos),
        "wines_count": len(df_vinhos)
    }

@app.get("/health")
def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "llm_configured": LLM_AVAILABLE,
        "database": {
            "pratos": len(df_pratos),
            "vinhos": len(df_vinhos)
        }
    }

@app.post("/api/recomendacao", response_model=RecomendacaoResponse)
async def recomendar(request: RecomendacaoRequest):
    """
    Main recommendation endpoint
    Receives a dish name and returns the top wine recommendation with AI justification
    """
    try:
        mensagem = request.mensagem.strip()
        
        if not mensagem:
            raise HTTPException(status_code=400, detail="Mensagem é obrigatória")
        
        # Search for dish in database
        prato_data = buscar_prato_no_csv(mensagem)
        
        if not prato_data:
            return RecomendacaoResponse(
                prato="",
                vinho=VinhoResponse(
                    nome="",
                    tipo="",
                    similaridade=0,
                    score_features=0,
                    score_regras=0
                ),
                justificativa="",
                mensagem=f'Desculpe, não encontrei informações sobre "{mensagem}". Tente mencionar um prato específico como "Sushi", "Salmão grelhado", "Picanha" ou "Risotto".'
            )
        
        nome_prato = prato_data['nome_prato']
        
        # Get wine recommendations
        recomendacoes = recomendar_vinho(nome_prato, df_pratos, df_vinhos, top_n=1)
        
        if recomendacoes.empty:
            return RecomendacaoResponse(
                prato=nome_prato,
                vinho=VinhoResponse(
                    nome="",
                    tipo="",
                    similaridade=0,
                    score_features=0,
                    score_regras=0
                ),
                justificativa="",
                mensagem=f"Não encontrei vinhos compatíveis para {nome_prato}."
            )
        
        # Get top recommendation
        melhor_vinho = recomendacoes.iloc[0]
        
        # Prepare wine response
        vinho_response = VinhoResponse(
            nome=melhor_vinho['vinho'],
            tipo=melhor_vinho['tipo_vinho'],
            similaridade=float(melhor_vinho['similaridade_percentual']),
            score_features=float(melhor_vinho['score_features']),
            score_regras=float(melhor_vinho['score_regras'])
        )
        
        # Generate justification with LLM (if available)
        justificativa = ""
        if LLM_AVAILABLE:
            try:
                caracteristicas_prato = {
                    'tipo_prato': prato_data['tipo_prato'],
                    'temperos': prato_data['temperos'],
                    'acidez': prato_data['acidez'],
                    'intensidade_sabor': prato_data['intensidade_sabor'],
                    'ingredientes': prato_data['ingredientes']
                }
                
                vinho_info = {
                    'vinho': melhor_vinho['vinho'],
                    'tipo_vinho': melhor_vinho['tipo_vinho'],
                    'similaridade_percentual': melhor_vinho['similaridade_percentual'],
                    'score_features': melhor_vinho['score_features'],
                    'score_regras': melhor_vinho['score_regras']
                }
                
                justificativa = gerar_justificativa_vinho(
                    nome_prato=nome_prato,
                    caracteristicas_prato=caracteristicas_prato,
                    vinho_info=vinho_info
                )
            except Exception as e:
                print(f"Erro ao gerar justificativa: {e}")
                justificativa = f"O {melhor_vinho['vinho']} harmoniza perfeitamente com {nome_prato} devido às suas características complementares."
        else:
            justificativa = f"O {melhor_vinho['vinho']} harmoniza perfeitamente com {nome_prato} devido às suas características complementares."
        
        # Build response message
        mensagem_resposta = f"🍷 **{melhor_vinho['vinho']}** ({melhor_vinho['tipo_vinho']})\n\n"
        mensagem_resposta += f"📊 **Compatibilidade:** {melhor_vinho['similaridade_percentual']:.1f}%\n\n"
        mensagem_resposta += f"✨ **Justificativa:**\n{justificativa}"
        
        return RecomendacaoResponse(
            prato=nome_prato,
            vinho=vinho_response,
            justificativa=justificativa,
            mensagem=mensagem_resposta
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro ao processar recomendação: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erro ao processar recomendação: {str(e)}")

@app.get("/api/pratos")
def listar_pratos():
    """List all available dishes"""
    pratos = df_pratos['nome_prato'].tolist()
    return {
        "total": len(pratos),
        "pratos": pratos[:20],  # Return first 20 for preview
        "message": f"Total de {len(pratos)} pratos disponíveis"
    }

@app.get("/api/vinhos")
def listar_vinhos():
    """List all available wines"""
    vinhos = df_vinhos[['vinho', 'tipo_vinho']].to_dict('records')
    return {
        "total": len(vinhos),
        "vinhos": vinhos
    }

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*80)
    print("🍷 Wine Recommendation API")
    print("="*80)
    print(f"📊 Loaded {len(df_pratos)} dishes and {len(df_vinhos)} wines")
    print(f"🤖 LLM Status: {'✅ Available' if LLM_AVAILABLE else '⚠️ Not configured'}")
    print("="*80 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
