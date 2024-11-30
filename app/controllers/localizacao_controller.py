from fastapi import APIRouter, HTTPException
from app.services.localizacao_service import process_data
from app.Messaging.Requests.GPSData import GPSData  
import logging
from fastapi.responses import JSONResponse
from typing import List


router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/dadosGPS")
async def process_gps_path(path: List[GPSData]):
    """
    Endpoint para processar caminho GPS
    
    :param path: Lista de pontos GPS
    :return: Resposta JSON com resultados de processamento
    """
    try:
        # Processa o caminho
        result = process_data(path)
        
        # Determina o código de status baseado no resultado
        status_code = 200 if result.get('is_safe', False) else 400
        
        # Retorna resposta JSON
        return JSONResponse(
            status_code=status_code,
            content={
                "message": "Caminho processado com sucesso" if result.get('is_safe', False) else "Caminho contém anomalias",
                "processed": result.get('processed', False),
                "is_safe": result.get('is_safe', False),
                "total_points": result.get('total_points', 0),
                "total_distance": result.get('total_distance', 0),
                "safety_flags": result.get('safety_flags', {}),
                "speeds": result.get('speeds', [])
            }
        )
    
    except Exception as e:
        # Trata exceções não esperadas
        return JSONResponse(
            status_code=500,
            content={
                "message": "Erro ao processar caminho",
                "error": str(e)
            }
        )