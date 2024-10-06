import logging
import logging.config
import os

# Configuração básica do logging, pode ser ajustada conforme sua necessidade
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "formatter": "detailed",
            "filename": os.path.join(os.getcwd(), "app_error.log"),  # Arquivo de log
        },
    },
    "loggers": {
        "": {  # Logger raiz
            "level": "DEBUG",
            "handlers": ["console", "file"],
        },
        "uvicorn": {  # Logger do FastAPI/Uvicorn
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

# Função para configurar o logging com base na configuração acima
def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
