# Base builder stage
FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock alembic.ini ./

# Development stage
FROM builder AS dev

RUN uv sync --frozen --extra dev

ENV PATH="/app/.venv/bin:$PATH"

COPY src/ /app/src

COPY tests/ /app/src/tests

# Production stage
FROM builder AS prod

RUN uv sync --frozen

ENV PATH="/app/.venv/bin:$PATH"

COPY src/ /app/src
