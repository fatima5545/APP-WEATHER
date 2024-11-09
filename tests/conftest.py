import pytest
import os
import sys
from redis import Redis

# Ajouter le répertoire racine du projet au PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from settings.configuration import (
    settings,
)  # Modifier l'import pour correspondre au bon chemin


@pytest.fixture(scope="session")
def redis_client():
    client = Redis(
        host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
    )
    yield client
    client.flushdb()  # Nettoyer la DB après les tests
