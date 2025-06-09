FROM python:3.11-slim
LABEL authors="Michkail Piter"

WORKDIR /app

RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    pkgconf \
    pkgconfig \
    curl \
    unzip

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PATH="/app/.venv/bin:$PATH"

COPY . /app/

RUN uv sync
