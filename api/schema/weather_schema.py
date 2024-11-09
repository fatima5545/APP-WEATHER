from pydantic import BaseModel, PositiveInt, PositiveFloat


class WeatherResponse(BaseModel):
    description: str  # Brief description de la météo
    wind_speed: PositiveFloat  # Vitesse du vent en km/h
    humidity: PositiveInt  # Humidité relative en %
    temperature: PositiveFloat  # Température en °C

    class Config:
        json_schema_extra = {
            "example": {
                "description": "Ensoleillé",
                "wind_speed": 45,
                "humidity": 80,
                "temperature": 26,
            }
        }
