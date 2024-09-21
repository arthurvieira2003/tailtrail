from fastapi import APIRouter
from app.services.localizacao_service import process_data

router = APIRouter()

@router.post("/fodaseTaFunfando")
def process_request() -> dict:
    success = process_data()
    return {"Sucesso": success}
