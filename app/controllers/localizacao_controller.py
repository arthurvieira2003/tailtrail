from fastapi import APIRouter, HTTPException
from app.services.localizacao_service import process_data
from app.Messaging.Requests.GPSData import GPSData  
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/dadosGPS")
def process_request(data: GPSData) -> dict:
    try:
        success = process_data(data.latitude, data.longitude)
        if success:
            logger.info("Dados processados com sucesso: %s", data)
            return {"status": "sucesso", "mensagem": "Dados processados com sucesso!"}
        else:
            logger.error("Erro ao processar dados: %s", data)
            raise HTTPException(status_code=500, detail="Erro ao processar os dados")
    except Exception as e:
        logger.exception("Exceção durante o processamento dos dados")
        raise HTTPException(status_code=500, detail="Erro inesperado no servidor")