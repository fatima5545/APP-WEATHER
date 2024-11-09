import redis
from settings.configuration import settings
import json
from datetime import timedelta
from settings.logging_config import logger

# Nombre max d'appels API par jour
MAX_API_CALLS_PER_DAY = 50


class RedisCache:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisCache, cls).__new__(cls)
            cls._instance._initialize_client()
        return cls._instance

    def _initialize_client(self):
        """
        Initialise le client Redis avec les paramètres de configuration définis.
        Effectue un test de connexion pour vérifier l'accessibilité de Redis.
        """
        try:
            self.client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
            )
            # Test de connexion
            self.client.ping()
            logger.info("Connexion Redis réussie")
        except ConnectionError as e:
            logger.error(f"Échec de connexion à Redis: {e}")
            raise SystemExit(
                "Impossible de se connecter à Redis. Vérifiez la configuration."
            )

    def get_from_cache(self, city: str, cache_type: str):
        """Récupère les données en cache pour une ville donnée.

        Args:
            city (str): Le nom de la ville pour laquelle récupérer les données en cache.
            cache_type (str): Le type de cache (par exemple, "current_weather" ou "forecast")

        Returns:
            dict | None: Les données en cache sous forme de dictionnaire si elles existent, sinon None.
        """
        key = f"{cache_type}:{city}"
        data = self.client.get(key)
        if data:
            logger.info(f"Données sont récupérées du cache pour {city} ({cache_type})")
            return json.loads(data)
        logger.info(f"Aucune données en cache pour {city} ({cache_type})")
        return None

    def set_cache(self, city: str, data, cache_type: str, ttl: int = 3600):
        """Stocke les données dans le cache avec une durée d'expiration.

        Args:
            city (str): Le nom de la ville.
            data (dict): Les données à mettre en cache.
            cache_type (str): Le type de cache (ex: "current_weather", "forecast").
            ttl (int): Durée de vie des données en cache en secondes (par défaut 3600).
        """
        key = f"{cache_type}:{city}"
        self.client.setex(
            key, ttl, json.dumps(data)
        )  # Stocker les données en JSON avec expiration
        logger.info(
            f"Données sont mises en cache pour {city} ({cache_type}) avec TTL de {ttl} secondes"
        )

    def increment_api_call_count(self):
        """Incrémente le count d'appels API avec expiration de 24H.

        Returns:
            int: Nombre actuel d'appels API après incrémentation.
        """
        if not self.client.exists("weatherbit_api_call_count"):
            self.client.set("weatherbit_api_call_count", 0, ex=timedelta(days=1))
        count = self.client.incr("weatherbit_api_call_count")
        logger.info(f"Compteur d'appels API incrémenté : {count}")
        return count

    def get_api_call_count(self):
        """Retourne le nombre d'appels API effectués aujourd'hui.

        Returns:
            int: Nombre actuel d'appels API pour la journée.
        """
        count = self.client.get("weatherbit_api_call_count")
        final_count = int(count) if count else 0
        logger.info(f"Nombre d'appels API effectués aujourd'hui : {final_count}")
        return final_count

    def can_make_api_call(self):
        """Vérifie si le quota d'appels API n'est pas dépassé.

        Returns:
            bool: True si le quota n'est pas dépassé, False sinon.
        """
        return self.get_api_call_count() < MAX_API_CALLS_PER_DAY


# Instance unique de RedisCache
redis_cache = RedisCache()
