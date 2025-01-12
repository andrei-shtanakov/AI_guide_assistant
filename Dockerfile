FROM python:3.10.15-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Копирование файлов проекта
COPY Pipfile Pipfile.lock ./
COPY src/ ./src/

# Установка pipenv
RUN pip install pipenv

# Установка зависимостей проекта
RUN pipenv install --deploy --system

# Установка переменной окружения PYTHONPATH
ENV PYTHONPATH=/app/src

# Порт для FastAPI (если нужен)
EXPOSE 8000

# Команда запуска (замените на вашу)
CMD ["python", "-m", "src.ai_ga.main"]
