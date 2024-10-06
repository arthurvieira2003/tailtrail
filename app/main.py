import logging  # Importação do módulo logging
from fastapi import FastAPI
from app.controllers import localizacao_controller
from app.Infra.logging_config import setup_logging  # Importar a configuração de logging

# Configura o logging
setup_logging()

# Cria a aplicação FastAPI
app = FastAPI()

# Inclui o router das rotas
app.include_router(localizacao_controller.router)

# Obter um logger para este módulo
logger = logging.getLogger(__name__)

# Verifica se este script está sendo executado diretamente
if __name__ == "__main__":
    import uvicorn
    # Inicia o servidor Uvicorn, especificando o host e a porta
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)
