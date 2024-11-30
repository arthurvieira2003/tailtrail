import logging  
import uvicorn
from fastapi import FastAPI
from app.controllers import localizacao_controller
from app.Infra.logging_config import setup_logging  

setup_logging()

app = FastAPI()

app.include_router(localizacao_controller.router)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)
