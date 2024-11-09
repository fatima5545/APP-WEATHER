from pydantic_settings import BaseSettings
import os

from settings.logging_config import logger


class Settings(BaseSettings):
    WEATHERBIT_API_KEY: str = os.getenv(
        "WEATHERBIT_API_KEY"
    )  # Priorise la variable d'env
    REDIS_HOST: str = os.getenv(
        "REDIS_HOST", "redis"
    )  # Valeur par défaut pour Redis en local
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB: int = int(os.getenv("REDIS_DB", 0))
    WEATHERBIT_API_BASE_URL: str = "https://api.weatherbit.io/v2.0/"

    class Config:
        env_file = ".env"  # Utilise le fichier .env si les variables d'environnement ne sont pas définies

    def check_missing_variables(self):
        """Vérifie si des variables d'environnement sont manquantes et les loggue."""
        missing_vars = []

        if not self.WEATHERBIT_API_KEY:
            missing_vars.append("WEATHERBIT_API_KEY")
        if not self.REDIS_HOST:
            missing_vars.append("REDIS_HOST")
        if not self.REDIS_PORT:
            missing_vars.append("REDIS_PORT")
        if not self.REDIS_DB:
            missing_vars.append("REDIS_DB")

        if missing_vars:
            logger.error(
                f"Les variables d'environnement suivantes sont manquantes : {', '.join(missing_vars)}. "
                "Veuillez vérifier votre fichier .env ou vos variables d'environnement système."
            )


# Initialiser les paramètres et vérifier les variables manquantes
settings = Settings()
settings.check_missing_variables()
