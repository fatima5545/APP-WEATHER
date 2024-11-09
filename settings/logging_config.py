import logging
import os

# Crée le répertoire logs
log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Configuration de base des logs
logger = logging.getLogger("weather_app")
logger.setLevel(logging.INFO)

# Format des messages de logs
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

# Handler pour la console
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Handler pour le fichier de logs
file_handler = logging.FileHandler(os.path.join(log_directory, "app.log"))
file_handler.setFormatter(formatter)

# Ajouter les handlers au logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
