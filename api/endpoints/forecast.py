from fastapi import APIRouter, HTTPException
from services.forecast_service import get_weather_forecast
from api.schema.forecast_schema import WeatherForecastResponse
from settings.logging_config import logger

router = APIRouter()


@router.get("/forecast", response_model=WeatherForecastResponse)
async def weather_forecast(location: str) -> WeatherForecastResponse:
    """API pour récupérer les prévisions des 7 jours d'une ville

    Args:
        location (str): la ville

    Returns:
        WeatherForecastResponse: Un objet contenant les prévisions des 7 jours

    Raises:
        HTTPException: Si une erreur survient lors de la récupération des données
    """
    try:
        forecast_data = await get_weather_forecast(location)
        if not forecast_data:
            logger.error(f"Prévisions météo introuvables pour la ville spécifiée.")
            raise HTTPException(
                status_code=404,
                detail="Prévisions météo introuvables pour la ville spécifiée.",
            )
        return forecast_data
    except Exception as e:
        logger.error(
            f"Erreur lors de la récupération des prévisions météo pour {location}: {e}"
        )
        raise HTTPException(status_code=500, detail="Erreur interne du serveur.")
