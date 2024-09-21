# localizacao_controller.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.localizacao_service import process_data

router = APIRouter()

# Definindo um modelo de dados para a requisição (latitude e longitude)
class GPSData(BaseModel):
    lat: float
    lng: float

@router.post("/dadosGPS")
def process_request(data: GPSData) -> dict:
    # Chama o service para processar os dados de GPS
    success = process_data(data.lat, data.lng)
    
    if success:
        return {"status": "sucesso", "mensagem": "Dados processados com sucesso!"}
    else:
        raise HTTPException(status_code=500, detail="Erro ao processar os dados")
