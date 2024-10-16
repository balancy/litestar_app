"""Main application."""

from litestar import Litestar

from config import DEBUG
from db.connection import sqlalchemy_plugin
from exceptions import exception_handlers
from logger import structlog_plugin
from middleware import (
    compression_config,
    cors_config,
    rate_limit_config,
    session_config,
    stores,
)
from routers import api_router

app = Litestar(
    plugins=[sqlalchemy_plugin, structlog_plugin],
    route_handlers=[api_router],
    debug=DEBUG,
    exception_handlers=exception_handlers,
    cors_config=cors_config,
    compression_config=compression_config,
    middleware=[rate_limit_config.middleware, session_config.middleware],
    stores=stores,
)
