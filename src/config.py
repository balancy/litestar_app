"""App configuration module."""

from environs import Env

env = Env()
env.read_env()

DB_URI = env.str(
    "DB_URI",
    "postgresql+asyncpg://postgres:postgres@postgres:5432/db",
)
