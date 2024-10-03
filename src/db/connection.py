"""Database connection configuration."""

from litestar.contrib.sqlalchemy.plugins import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyPlugin,
)

from config import DB_URI

session_config = AsyncSessionConfig(expire_on_commit=False)
sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string=DB_URI,
    session_config=session_config,
)
sqlalchemy_plugin = SQLAlchemyPlugin(config=sqlalchemy_config)
