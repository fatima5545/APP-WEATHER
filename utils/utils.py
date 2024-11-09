def calculate_trend(values) -> str:
    """Détermine la tendance d'une série de valeurs numériques (ça peut être les températures, les pressions ...)

    Args:
        values (list of float): Liste de valeurs numériques représentant les mesures successives d'un indicateur.
    Returns:
        str: La tendance de la série
    """

    if values[-1] > values[0]:
        return "en hausse"
    elif values[-1] < values[0]:
        return "en baisse"
    else:
        return "stable"


def categorize_wind_speed(speed) -> str:
    """catégoriser la vitesse moyenne du vent selon l'échelle de Beaufort

    Args:
        speed (float): avg de vitesse
    Returns:
        str: description de la vitesse du vent
    """

    if speed < 1:
        return "Calme"
    elif speed <= 5:
        return "Légère brise"
    elif speed <= 11:
        return "Petite brise"
    elif speed <= 19:
        return "Jolie brise"
    elif speed <= 28:
        return "Bonne brise"
    elif speed <= 38:
        return "Vent frais"
    elif speed <= 49:
        return "Grand vent"
    elif speed <= 61:
        return "Coup de vent"
    else:
        return "Tempête"


def evaluate_weather_trend(
    temperature_trend: str,
    pressure_trend: str,
    precipitation_prob: list,
    cloud_coverage: list,
    uv_index: list,
) -> str:
    """
    Évalue l'évolution générale des conditions météorologiques en fonction de plusieurs indicateurs.

    Args:
        temperature_trend (str): Tendance de la température
        pressure_trend (str): Tendance de la pression atmosphérique
        precipitation_prob (list of float): Liste des probabilités de précipitations pour chaque jour (%).
        cloud_coverage (list of float): Liste des couvertures nuageuses pour chaque jour (%).
        uv_index (list of float): Liste des indices UV pour chaque jour.

    Returns:
        str: Une description de l'évolution générale des conditions météorologiques :
             - "en amélioration"
             - "en dégradation"
             - "stable"
    """
    # Vérifier si la tendance est en amélioration
    if (
        temperature_trend == "en hausse"
        and pressure_trend == "en hausse"
        and max(precipitation_prob) < 30
        and max(cloud_coverage) < 50
        and max(uv_index) > 5
    ):
        return "en amélioration"

    # Vérifier si la tendance est en dégradation
    elif (
        temperature_trend == "en baisse"
        or pressure_trend == "en baisse"
        or max(precipitation_prob) > 60
        or max(cloud_coverage) > 70
        or min(uv_index) < 3
    ):
        return "en dégradation"

    # Sinon, la tendance est considérée comme stable
    else:
        return "stable"
