import logging
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
import json
from app.controllers import localizacao_controller
from app.Infra.logging_config import setup_logging
from app.services.localizacao_service import process_data
from app.Messaging.Requests.GPSData import GPSData

setup_logging()

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

active_connections = []

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        active_connections.remove(websocket)

@app.post("/dadosGPS")
async def process_request(data: GPSData):
    try:
        success = process_data(data.latitude, data.longitude)
        if success:
            for connection in active_connections:
                await connection.send_text(json.dumps({
                    "latitude": data.latitude,
                    "longitude": data.longitude
                }))
            return {"status": "sucesso", "mensagem": "Dados processados com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro inesperado no servidor")

app.include_router(localizacao_controller.router)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=7070, reload=True)
