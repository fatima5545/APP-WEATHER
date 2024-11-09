from services.forecast_service import (
    calculate_trend,
    categorize_wind_speed,
    evaluate_weather_trend,
)


def test_calculate_trend_increasing():
    values = [10, 12, 15, 18]  # Valeurs croissantes
    result = calculate_trend(values)
    assert result == "en hausse"


def test_calculate_trend_decreasing():
    values = [20, 18, 15, 12]  # Valeurs décroissantes
    result = calculate_trend(values)
    assert result == "en baisse"


def test_calculate_trend_stable():
    values = [10, 10, 10, 10]  # Valeurs constantes
    result = calculate_trend(values)
    assert result == "stable"


def test_calculate_trend_edge_case_two_values_increasing():
    values = [10, 20]  # Deux valeurs croissantes
    result = calculate_trend(values)
    assert result == "en hausse"


def test_calculate_trend_edge_case_two_values_decreasing():
    values = [20, 10]  # Deux valeurs décroissantes
    result = calculate_trend(values)
    assert result == "en baisse"


def test_calculate_trend_edge_case_mixed_values():
    values = [10, 15, 12, 18]  # Série mixte
    result = calculate_trend(values)
    # Avec la logique actuelle, on ne prend que la première et dernière valeur
    assert result == "en hausse"


def test_calculate_trend_single_value():
    values = [10]  # Cas limite avec une seule valeur
    result = calculate_trend(values)
    assert result == "stable"  # Une seule valeur est interprétée comme "stable"


def test_categorize_wind_speed():
    # Calme
    assert categorize_wind_speed(0) == "Calme"
    assert categorize_wind_speed(0.5) == "Calme"

    # Légère brise
    assert categorize_wind_speed(1) == "Légère brise"
    assert categorize_wind_speed(5) == "Légère brise"

    # Petite brise
    assert categorize_wind_speed(5.1) == "Petite brise"
    assert categorize_wind_speed(11) == "Petite brise"

    # Jolie brise
    assert categorize_wind_speed(11.1) == "Jolie brise"
    assert categorize_wind_speed(19) == "Jolie brise"

    # Bonne brise
    assert categorize_wind_speed(19.1) == "Bonne brise"
    assert categorize_wind_speed(28) == "Bonne brise"

    # Vent frais
    assert categorize_wind_speed(28.1) == "Vent frais"
    assert categorize_wind_speed(38) == "Vent frais"

    # Grand vent
    assert categorize_wind_speed(38.1) == "Grand vent"
    assert categorize_wind_speed(49) == "Grand vent"

    # Coup de vent
    assert categorize_wind_speed(49.1) == "Coup de vent"
    assert categorize_wind_speed(61) == "Coup de vent"

    # Tempête
    assert categorize_wind_speed(61.1) == "Tempête"
    assert categorize_wind_speed(70) == "Tempête"


def test_evaluate_weather_trend_improving():
    # Cas où la météo s'améliore
    result = evaluate_weather_trend(
        temperature_trend="en hausse",
        pressure_trend="en hausse",
        precipitation_prob=[10, 15, 20],
        cloud_coverage=[20, 30, 40],
        uv_index=[6, 7, 8],
    )
    assert result == "en amélioration"


def test_evaluate_weather_trend_deteriorating():
    # Cas où la météo se dégrade
    result = evaluate_weather_trend(
        temperature_trend="en baisse",
        pressure_trend="en baisse",
        precipitation_prob=[70, 65, 80],
        cloud_coverage=[80, 85, 90],
        uv_index=[2, 2.5, 3],
    )
    assert result == "en dégradation"


def test_evaluate_weather_trend_stable():
    # Cas où la météo est stable
    result = evaluate_weather_trend(
        temperature_trend="stable",
        pressure_trend="stable",
        precipitation_prob=[20, 25, 30],
        cloud_coverage=[40, 50, 45],
        uv_index=[4, 5, 4.5],
    )
    assert result == "stable"
