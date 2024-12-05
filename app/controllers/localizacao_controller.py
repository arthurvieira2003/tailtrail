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
        # Log da requisição recebida
        logger.info(f"Requisição recebida - Body: {[{'latitude': p.latitude, 'longitude': p.longitude} for p in path]}")
        
        # Processa o caminho
        result = process_data(path)
        
        # Determina o código de status baseado no resultado
        status_code = 200 if result.get('is_safe', False) else 400
        
        # Prepara resposta
        response_content = {
            "message": "Caminho processado com sucesso" if result.get('is_safe', False) else "Caminho contém anomalias",
            "processed": result.get('processed', False),
            "is_safe": result.get('is_safe', False),
            "total_points": result.get('total_points', 0),
            "total_distance": result.get('total_distance', 0),
            "safety_flags": result.get('safety_flags', {}),
            "speeds": result.get('speeds', [])
        }
        
        # Log da resposta
        logger.info(f"Resposta enviada - Status: {status_code}, Content: {response_content}")
        
        # Retorna resposta JSON
        return JSONResponse(
            status_code=status_code,
            content=response_content
        )
    
    except Exception as e:
        error_response = {
            "message": "Erro ao processar caminho",
            "error": str(e)
        }
        # Log do erro
        logger.error(f"Erro na requisição - {error_response}")
        
        return JSONResponse(
            status_code=500,
            content=error_response
        )