from pydantic import BaseModel


class WeatherResponse(BaseModel):
    description: str  # Brief description de la météo
    wind_speed: float  # Vitesse du vent en km/h
    humidity: int  # Humidité relative en %
    temperature: float  # Température en °C

    class Config:
        json_schema_extra = {
            "example": {
                "description": "Ensoleillé",
                "wind_speed": 45,
                "humidity": 80,
                "temperature": 26,
            }
        }
