import requests
from settings.configuration import settings
from adapters.cache_redis import (
    get_from_cache,
    set_cache,
    can_make_api_call,
    increment_api_call_count,
)
from settings.logging_config import logger


async def get_current_weather(location: str) -> dict:
    """Récupérer la météo pour une ville donné

    Args:
        location (str): Nom de la ville pour laquelle obtenir les données météo.

    Returns:
        dict: Un dictionnaire contenant les informations météorologiques suivantes :
            - description (str): Une brève description de la météo
            - temperature (float): Température actuelle en degrés Celsius.
            - wind_speed (float): Vitesse du vent en km/h.
            - humidity (int): Humidité relative en pourcentage.
    Raises:
        requests.exceptions.HTTPError: Si une erreur HTTP se produit lors de la requête à l'API weather
        Exception: Pour toute autre erreur lors de la récupération ou du traitement des données
    """
    url = f"https://api.weatherbit.io/v2.0/current?city={location}&key={settings.WEATHERBIT_API_KEY}"

    logger.info(f"Demande de météo actuelle pour la ville : {location}")
    # Vérifier si les données sont déjà dans le cache Redis
    cached_data = get_from_cache(location, "current_weather")
    if cached_data:
        logger.info(f"Cache utilisé pour la météo de {location}")
        return cached_data

    # Vérifier si le quota d'appels à l'API WeatherBit est disponible
    if not can_make_api_call():
        logger.warning(
            f"Quota d'appels API atteint pour aujourd'hui. Requête pour {location} non effectuée."
        )
        raise Exception(
            "Quota d'appels API atteint pour aujourd'hui. Veuillez réessayer demain."
        )

    # Si les données ne sont pas en cache et le quota est disponible, faire un appel à l'API
    try:
        response = requests.get(url)
        response.raise_for_status()  # déclenche erreur pour codes HTTP 4xx 5xx
        data = response.json()
        weather_data = {
            "description": data["data"][0]["weather"]["description"],
            "temperature": data["data"][0]["temp"],
            "wind_speed": data["data"][0]["wind_spd"] * 3.6,  # Convertir m/s en km/h
            "humidity": data["data"][0]["rh"],
        }
        # Incrémenter le compteur seulement après un appel réussi
        increment_api_call_count()

        set_cache(
            location, weather_data, "current_weather", ttl=3600
        )  # Expiration de 1 heure
        logger.info(
            f"API appelée pour la météo de {location} et résultat stocké dans le cache"
        )
        return weather_data
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"Erreur HTTP pour la ville {location} : {http_err}")
    except Exception as err:
        logger.error(
            f"Erreur lors de la récupération de la météo pour {location} : {err}"
        )
