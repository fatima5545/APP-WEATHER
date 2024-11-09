from pydantic import BaseModel
from typing import List


class DailyForecast(BaseModel):
    date: str  # La date de la prévision
    temperature: float  # Température pour la journée en °C
    pressure: float  # Pression en hPa
    wind_speed: float  # Vitesse du vent en km/h


class WeatherForecastResponse(BaseModel):
    evolution: str  # Evolution générale
    temperature_trend: (
        str  # Tendance des températures ("en hausse", "stable", "en baisse")
    )
    pressure_trend: str  # Tendance de la pression ("en forte hausse", "en hausse", "stable", "en baisse", "en forte baisse")
    wind_speed_category: str  # Catégorie de vitesse de vent selon l'échelle de Beaufort (ex: "Petite brise")
    forecast_data: List[DailyForecast]  # Liste des prévisions pour chaque jour

    class Config:
        json_schema_extra = {
            "example": {
                "temperature_trend": "en hausse",
                "pressure_trend": "en hausse",
                "wind_speed_category": "Petite brise",
                "evolution": "en amélioration",
                "forecast_data": [
                    {
                        "date": "2024-12-01",
                        "temperature": 18.5,
                        "pressure": 1015,
                        "wind_speed": 10.8,
                    },
                    {
                        "date": "2024-12-02",
                        "temperature": 19.0,
                        "pressure": 1013,
                        "wind_speed": 12.6,
                    },
                ],
            }
        }
