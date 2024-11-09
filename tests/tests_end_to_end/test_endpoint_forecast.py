import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from run import app

client = TestClient(app)


# Fixture pour mocker la fonction `get_weather_forecast()`
@pytest.fixture
def mock_get_weather_forecast():
    """Fixture pour mocker la fonction get_weather_forecast."""
    with patch("api.endpoints.forecast.get_weather_forecast") as mock:
        yield mock


# Simuler des données prévisionnels
mock_data = {
    "temperature_trend": "en hausse",
    "pressure_trend": "stable",
    "wind_speed_category": "Légère brise",
    "evolution": "stable",
    "forecast_data": [
        {
            "date": "2024-11-05",
            "temperature": 15.5,
            "pressure": 1015,
            "wind_speed": 12.3,
        },
        {
            "date": "2024-11-06",
            "temperature": 16.0,
            "pressure": 1013,
            "wind_speed": 14.0,
        },
    ],
}


# Test pour un appel valide
def test_weather_forecast_valid(mock_get_weather_forecast):
    """Test pour vérifier que l'API retourne des données valides."""
    mock_get_weather_forecast.return_value = mock_data

    response = client.get("/api/v1/forecast/forecast?location=Paris")
    assert response.status_code == 200
    data = response.json()
    assert data == mock_data


# Test pour un cas où les données ne sont pas trouvées
# def test_weather_forecast_not_found(mock_get_weather_forecast):
#     mock_get_weather_forecast.return_value = None

#     response = client.get("/api/v1/forecast/forecast?location=VilleInconnue")
#     assert response.status_code == 404
#     assert response.json() == {"detail": "Prévisions météo introuvables pour la ville spécifiée."}


# Test pour une erreur interne
def test_weather_forecast_internal_error(mock_get_weather_forecast):
    """Test pour vérifier que l'API retourne une erreur 500 en cas d'échec."""
    mock_get_weather_forecast.side_effect = Exception("Erreur inattendue")

    response = client.get("/api/v1/forecast/forecast?location=Paris")
    assert response.status_code == 500
    assert response.json() == {"detail": "Erreur interne du serveur."}
