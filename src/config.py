"""App configuration module."""

from environs import Env

COOKIES_MAX_AGE = 60 * 60 * 24 * 7
GZIP_COMPRESS_LEVEL = 9

env = Env()
env.read_env()

DB_URI = env.str(
    "DB_URI",
    "postgresql+psycopg://postgres:postgres@postgres:5432/db",
)
DEBUG = env.bool("DEBUG", False)
ALLOW_ORIGINS = env.list("ALLOW_ORIGINS", ["localhost", "127.0.0.1"])
