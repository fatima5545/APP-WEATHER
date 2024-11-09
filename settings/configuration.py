from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    WEATHERBIT_API_KEY: str = os.getenv(
        "WEATHERBIT_API_KEY"
    )  # Priorise la variable d'env
    REDIS_HOST: str = os.getenv(
        "REDIS_HOST", "redis"
    )  # Valeur par défaut pour Redis en local
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB: int = int(os.getenv("REDIS_DB", 0))

    class Config:
        env_file = ".env"  # Utilise le fichier .env si les variables d'environnement ne sont pas définies


settings = Settings()
