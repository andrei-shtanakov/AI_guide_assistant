FROM python:3.10.15-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY Pipfile Pipfile.lock ./
COPY src/ ./src/
COPY entrypoint.sh ./

RUN pip install pipenv

RUN pipenv install --deploy --system

ENV PYTHONPATH=/app/src

RUN chmod 777 entrypoint.sh

EXPOSE 8000

ENTRYPOINT bash entrypoint.sh
