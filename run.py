from fastapi import FastAPI

# from settings.configuration import settings
from api.endpoints import weather, forecast  # Importe les routes

# from adapters.cache_manager import CacheManager  # Ex. gestionnaire de cache Redis
import uvicorn
from settings.logging_config import logger


def create_app() -> FastAPI:
    app = FastAPI(
        title="Weather API",
        description="API for weather forecasts",
        version="1.0.0",
    )

    # Ajouter les configurations
    # configure_cache(app)
    configure_routes(app)
    # configure_middlewares(app)
    logger.info("Application FastAPI démarrée")  # Log de démarrage

    return app


# def configure_cache(app: FastAPI):
#     # Exemple d'initialisation du cache, supposant une instance Redis ou autre
#     app.state.cache = CacheManager()


def configure_routes(app: FastAPI):
    # Enregistrer les routes depuis le module d'API
    app.include_router(weather.router, prefix="/api/v1/weather")
    app.include_router(forecast.router, prefix="/api/v1/forecast")


# def configure_middlewares(app: FastAPI):
#     # Ajouter les middlewares (exemple: CORS, logger)
#     pass

app = create_app()

# Lancer le serveur avec Uvicorn si le script est exécuté directement
if __name__ == "__main__":
    uvicorn.run("run:app", host="127.0.0.1", port=8000, reload=True)
