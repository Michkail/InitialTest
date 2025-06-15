# Stage 1 
FROM rust:1.77-slim AS builder

WORKDIR /engine
COPY engine/ /engine/
RUN cargo build --release

# Stage 2
FROM python:3.11-slim
LABEL authors="Michkail Piter"

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libssl-dev \
    curl \
    unzip \
    git \
    nano \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY --from=builder /engine/target/release/engine /usr/local/bin/engine

ENV PATH="/app/.venv/bin:$PATH"

COPY . /app/

RUN uv sync
