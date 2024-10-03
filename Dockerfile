FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock alembic.ini ./

RUN uv sync --frozen

ENV PATH="/app/.venv/bin:$PATH"

COPY src/ /app/src