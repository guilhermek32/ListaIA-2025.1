"""Backend package for wine recommendation system."""

from .llm import configurar_llm, gerar_justificativa_vinho
from .sistema_recomendacao_vinho import recomendar_vinho, sistema_recomendacao_vinho
from .sistema_integrado import sistema_completo_com_justificativa

__all__ = [
    'configurar_llm',
    'gerar_justificativa_vinho',
    'recomendar_vinho',
    'sistema_recomendacao_vinho',
    'sistema_completo_com_justificativa',
]

__version__ = "1.0.0"

