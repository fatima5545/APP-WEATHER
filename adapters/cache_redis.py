import redis
from settings.configuration import settings
import json
from datetime import timedelta
from settings.logging_config import logger

# Nombre max d'appels API par jour
MAX_API_CALLS_PER_DAY = 50


def get_redis_client():
    """
    Initialise et retourne un client Redis connecté avec les paramètres de configuration définis.
    Effectue un test de connexion pour vérifier l'accessibilité de Redis.

    Returns:
        redis.Redis: Instance de client Redis connectée.

    Raises:
        SystemExit: Si la connexion à Redis échoue.
    """
    try:
        client = redis.Redis(
            host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
        )
        # Test de la connexion Redis & leve une exception s'il n'est pas accessible
        client.ping()
        logger.info("Connexion Redis réussie")
        return client
    except ConnectionError as e:
        logger.error(f"Échec de connexion à Redis: {e}")
        raise SystemExit(
            "Impossible de se connecter à Redis. Veuillez vérifier la configuration."
        )


# Initialisation du client Redis
redis_client = get_redis_client()


def get_from_cache(city: str, cache_type: str):
    """Récupère les données en cache pour une ville donnée

    Args:
        city (str): Le nom de la ville pour laquelle récupérer les données en cache.
        cache_type (str): Le type de cache (par exemple, "current_weather" ou "forecast")

    Returns:
        dict | None: Les données en cache sous forme de dictionnaire si elles existent,
        sinon None
    """
    key = f"{cache_type}:{city}"
    data = redis_client.get(key)
    if data:
        logger.info(f"Données récupérées du cache pour {city} ({cache_type})")
        return json.loads(data)
    logger.info(f"Aucune donnée en cache pour {city} ({cache_type})")
    return None


def set_cache(city: str, data, cache_type: str, ttl: int = 3600):
    """Stocke les données dans le cache pour une ville donnée et un type de cache spécifique, avec une durée d'expiration.

    Args:
        city (str): Le nom de la ville.
        data (dict): Les données à mettre en cache.
        cache_type (str): Le type de cache (par exemple, "current_weather" ou "forecast").
        ttl (int): La durée de vie en secondes des données en cache. Par défaut à 3600 secondes (1 heure).
    """
    key = f"{cache_type}:{city}"
    redis_client.setex(
        key, ttl, json.dumps(data)
    )  # Stocker les données en JSON avec expiration
    logger.info(
        f"Données mises en cache pour {city} ({cache_type}) avec une durée de {ttl} secondes"
    )


def increment_api_call_count():
    """
    Incrémente le count d'appels API pour la journée en cours dans Redis, avec expiration de 24H.

    Returns:
        int: Nombre actuel d'appels après incrémentation.
    """
    if not redis_client.exists("weatherbit_api_call_count"):
        redis_client.set("weatherbit_api_call_count", 0, ex=timedelta(days=1))
    count = redis_client.incr("weatherbit_api_call_count")
    logger.info(f"Compteur d'appels API incrémenté : {count}")
    return count


def get_api_call_count():
    """
    Retourne le nombre d'appels API effectués aujourd'hui.

    Returns:
        int: Nombre actuel d'appels API pour la journée.
    """
    count = redis_client.get("weatherbit_api_call_count")
    final_count = int(count) if count else 0
    logger.info(f"Nombre d'appel actuel effectué pour aujourd'hui : {final_count}")
    return final_count


def can_make_api_call():
    """
    Vérifie si le nombre maximal d'appels API n'est pas encore atteint.

    Returns:
        bool: True si le quota n'est pas dépassé sinon si c dépassé False.
    """
    return get_api_call_count() < MAX_API_CALLS_PER_DAY
