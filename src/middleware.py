"""Middleware module."""

from pathlib import Path

from litestar.config.compression import CompressionConfig
from litestar.config.cors import CORSConfig
from litestar.middleware.rate_limit import RateLimitConfig
from litestar.middleware.session.server_side import ServerSideSessionConfig
from litestar.stores.base import Store
from litestar.stores.file import FileStore

from config import ALLOW_ORIGINS, COOKIES_MAX_AGE, GZIP_COMPRESS_LEVEL

cors_config = CORSConfig(allow_origins=ALLOW_ORIGINS)
compression_config = CompressionConfig(
    "gzip",
    gzip_compress_level=GZIP_COMPRESS_LEVEL,
)
rate_limit_config = RateLimitConfig(rate_limit=("second", 1))
session_config = ServerSideSessionConfig(
    httponly=True,
    max_age=COOKIES_MAX_AGE,
)
stores: dict[str, Store] = {"sessions": FileStore(path=Path("session_data"))}
