FROM python:3.13.0-slim

# Устанавливаем зависимости системы и Poetry
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY backend/sender-service/pyproject.toml .

RUN pip install poetry
RUN poetry install --no-root 
RUN poetry update 
RUN poetry lock

WORKDIR /app
COPY backend/sender-service .

CMD poetry run python main.py || true && tail -f /dev/null 