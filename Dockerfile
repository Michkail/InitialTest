FROM python:3.11-alpine3.18
LABEL authors="Michkail Piter"

WORKDIR /app

RUN apk add --no-cache --no-check-certificate\
    mariadb-dev \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    pkgconf \
    pkgconfig

RUN apk add --no-cache curl unzip --no-check-certificate

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apk add --no-cache curl unzip --no-check-certificate

ENV PATH="/app/.venv/bin:$PATH"

COPY . /app/

RUN uv sync

