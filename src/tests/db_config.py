"""Database configuration for tests."""

from litestar.contrib.sqlalchemy.plugins import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyPlugin,
)

TEST_DB_URI = "postgresql+psycopg://postgres:postgres@postgres:5432/db_test"

sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string=TEST_DB_URI,
    session_config=AsyncSessionConfig(expire_on_commit=False),
)
sqlalchemy_plugin = SQLAlchemyPlugin(config=sqlalchemy_config)
