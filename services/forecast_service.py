import requests
from settings.configuration import settings
from adapters.cache_redis import redis_cache
from settings.logging_config import logger
from utils.utils import calculate_trend, categorize_wind_speed, evaluate_weather_trend


async def get_weather_forecast(location: str) -> dict:
    """Récupérer les prévisions de 7 jours de la météo pour une ville donné

    Args:
        location (str): Nom de la ville pour laquelle obtenir les données météo.

    Returns:
        dict: Un dictionnaire contenant les informations suivantes :
            - temperature_trend (str): Tendance des températures sur la période ("en hausse", "stable", "en baisse")
            - pressure_trend (str): Tendance de la pression barométrique sur la période
            - wind_speed_category (str): Catégorie moyenne de la vitesse du vent selon l'échelle de Beaufort
            - evolution (str): Évolution générale ("en amélioration", "stable", "en dégradation")
            - forecast_data (list): Liste des prévisions journalières pour les 7 prochains jours, avec chaque élément contenant :
                - date (str): Date de la prévision au format "YYYY-MM-DD".
                - temperature (float): Température prévue pour le jour en question en degrés Celsius.
                - pressure (float): Pression atmosphérique prévue en hPa.
                - wind_speed (float): Vitesse du vent en km/h.

    Raises:
        requests.exceptions.HTTPError: Si une erreur HTTP se produit lors de la requête à l'API.
        Exception: Pour toute autre erreur lors de la récupération ou du traitement des données.
    """

    url = f"https://api.weatherbit.io/v2.0/forecast/daily?city={location}&key={settings.WEATHERBIT_API_KEY}"

    logger.info(f"Demande de prévisions météo pour la ville : {location}")
    # Vérifier le cache Redis
    cached_data = redis_cache.get_from_cache(location, "forecast")
    if cached_data:
        logger.info(f"Cache utilisé pour les prévisions de la ville {location}")
        return cached_data

    # Vérifier si le quota d'appels à l'API WeatherBit est disponible
    if not redis_cache.can_make_api_call():
        logger.warning(
            f"Quota d'appels API atteint pour aujourd'hui. Requête pour {location} non effectuée."
        )
        raise Exception(
            "Quota d'appels API atteint pour aujourd'hui. Veuillez réessayer demain."
        )

    # Si non, appeler l'API pour les prévisions de 7 jours
    try:
        # Effectuer la requête
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Extraire les données des 7 prochains jours
        forecast_data = data["data"][:7]  # Les 7 jours de prévisions

        # Extraire les valeurs de température et de pression pour calculer les tendances
        temperatures = [day["temp"] for day in forecast_data]
        pressures = [day["pres"] for day in forecast_data]
        wind_speeds = [
            day["wind_spd"] * 3.6 for day in forecast_data
        ]  # Conversion en km/h
        precipitation_prob = [
            day["pop"] for day in forecast_data
        ]  # Probabilité de précipitations en %
        cloud_coverage = [day["clouds"] for day in forecast_data]  # Couverture nuageuse
        uv_index = [day["uv"] for day in forecast_data]  # Indice UV

        # Calcul des tendances
        temperature_trend = calculate_trend(temperatures)
        pressure_trend = calculate_trend(pressures)
        wind_speed_avg = sum(wind_speeds) / len(wind_speeds)
        wind_category = categorize_wind_speed(wind_speed_avg)

        # Déterminer l'évolution générale
        evolution = evaluate_weather_trend(
            temperature_trend,
            pressure_trend,
            precipitation_prob,
            cloud_coverage,
            uv_index,
        )

        # les données de réponse
        data_final = {
            "temperature_trend": temperature_trend,
            "pressure_trend": pressure_trend,
            "wind_speed_category": wind_category,
            "evolution": evolution,
            "forecast_data": [
                {
                    "date": day["datetime"],
                    "temperature": day["temp"],
                    "pressure": day["pres"],
                    "wind_speed": day["wind_spd"] * 3.6,  # km/h
                }
                for day in forecast_data
            ],
        }
        # Incrémenter le compteur
        redis_cache.increment_api_call_count()

        # Stocker dans Redis avec un TTL de 24 heures (86400 secondes)
        redis_cache.set_cache(location, data_final, "forecast", ttl=86400)
        logger.info(
            f"API appelée pour les prévisions de la ville {location} et résultat stocké dans le cache"
        )
        return data_final
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"Erreur HTTP pour la ville {location} : {http_err}")
    except Exception as err:
        logger.error(
            f"Erreur lors de la récupération de des prévisions pour {location} : {err}"
        )
