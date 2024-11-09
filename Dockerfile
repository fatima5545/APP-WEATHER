FROM python:3.10-slim

WORKDIR /app

# Copier seulement requirements.txt d'abord pour optimiser le cache Docker
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste de l'application
COPY . /app

# Lancer l'application
CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8000"]
