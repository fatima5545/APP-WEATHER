from fastapi import APIRouter, HTTPException
from services.weather_service import get_current_weather
from api.schema.weather_schema import WeatherResponse
from settings.logging_config import logger

router = APIRouter()


@router.get("/current", response_model=WeatherResponse)
async def current_weather(location: str) -> WeatherResponse:
    """API pour récupérer les informations météorologiques actuelles d'une ville

    Args:
        location (str): la ville

    Returns:
        WeatherResponse: Un objet contenant les informations météorologiques actuelles

    Raises:
        HTTPException: Si une erreur survient lors de la récupération des données
    """
    try:
        weather_data = await get_current_weather(location)
        if not weather_data:
            logger.error(f"Données météo introuvables pour la ville spécifiée")
            raise HTTPException(
                status_code=404,
                detail="Données météo introuvables pour la ville spécifiée",
            )
        return weather_data
    except Exception as e:
        logger.error(
            f"Erreur lors de la récupération des données météo pour {location}: {e}"
        )
        raise HTTPException(status_code=500, detail="Erreur interne du serveur.")
