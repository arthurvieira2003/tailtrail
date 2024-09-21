# main.py
from fastapi import FastAPI
from app.controllers import localizacao_controller

app = FastAPI()

# Inclui o router do controller
app.include_router(localizacao_controller.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="148.113.172.140", port=8080, reload=True)
