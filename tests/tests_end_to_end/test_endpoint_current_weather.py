from fastapi.testclient import TestClient
from run import app
from unittest.mock import patch
import pytest

client = TestClient(app)

# Simuler des données météo pour les tests
mock_weather_data = {
    "description": "Ciel dégagé",
    "temperature": 25.5,
    "wind_speed": 10.0,
    "humidity": 50,
}


@pytest.fixture
def mock_get_current_weather():
    """Fixture pour mocker la fonction get_current_weather."""
    with patch("api.endpoints.weather.get_current_weather") as mock:
        yield mock


def test_current_weather_success(mock_get_current_weather):
    """Test pour vérifier que l'API retourne des données valides."""
    # Configurer le mock pour retourner des données simulées
    mock_get_current_weather.return_value = mock_weather_data

    response = client.get("/api/v1/weather/current?location=Paris")
    assert response.status_code == 200
    data = response.json()
    # Vérifier le contenu de la réponse
    assert mock_weather_data == data


# def test_current_weather_not_found(mock_get_current_weather):
#     """Test pour vérifier que l'API retourne une erreur 404 si les données sont introuvables."""
#     # Configurer le mock pour retourner None (données non trouvées)
#     mock_get_current_weather.return_value = None

#     response = client.get("/api/v1/weather/current?location=Inconnue")
#     assert response.status_code == 404
#     assert response.json()["detail"] == "Données météo introuvables pour la ville spécifiée"


def test_current_weather_internal_error(mock_get_current_weather):
    """Test pour vérifier que l'API retourne une erreur 500 en cas d'échec."""
    # Configurer le mock pour lever une exception
    mock_get_current_weather.side_effect = Exception("Erreur interne")

    response = client.get("/api/v1/weather/current?location=Paris")
    assert response.status_code == 500
    assert response.json()["detail"] == "Erreur interne du serveur."
