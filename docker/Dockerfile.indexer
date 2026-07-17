FROM python:3.13-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y git \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./

RUN pip install uv \
    && uv sync --group indexer

ENV PATH="/app/.venv/bin:$PATH"

COPY . .