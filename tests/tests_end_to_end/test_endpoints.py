from fastapi.testclient import TestClient
from run import app
from unittest.mock import patch

client = TestClient(app)


def test_current_weather_endpoint(redis_client):
    response = client.get("/api/v1/weather/current?location=Paris")
    assert response.status_code == 200
    data = response.json()

    # Vérifier les données renvoyées par l'endpoint
    assert "description" in data
    assert "temperature" in data
    assert "wind_speed" in data
    assert "humidity" in data

    # Vérifier que les données sont stockées dans Redis
    cached_data = redis_client.get("current_weather:Paris")
    assert cached_data is not None


def test_forecast_weather_endpoint(redis_client):
    response = client.get("/api/v1/forecast/forecast?location=Paris")
    assert response.status_code == 200
    data = response.json()

    # Vérifier les données renvoyées par l'endpoint
    assert "temperature_trend" in data
    assert "pressure_trend" in data
    assert "wind_speed_category" in data
    assert len(data["forecast_data"]) > 0

    # Vérifier que les données de prévision sont stockées dans Redis
    cached_data = redis_client.get("forecast:Paris")
    assert cached_data is not None
