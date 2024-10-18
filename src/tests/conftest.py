"""Testing fixtures."""

from collections.abc import AsyncGenerator, AsyncIterator

import pytest
from litestar import Litestar
from litestar.contrib.sqlalchemy.plugins import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyPlugin,
)
from litestar.testing import AsyncTestClient
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy_utils import create_database, database_exists, drop_database
from advanced_alchemy import AsyncTestClient

from db.models import Author, UUIDBase
from logger import structlog_plugin
from routers import api_router

TEST_DB_URI = "postgresql+psycopg://postgres:postgres@postgres:5432/db_test"

sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string=TEST_DB_URI,
    session_config=AsyncSessionConfig(expire_on_commit=False),
)
sqlalchemy_plugin = SQLAlchemyPlugin(config=sqlalchemy_config)


@pytest.fixture(scope="session")
def test_app() -> Litestar:
    """Create and configure the test app."""
    return Litestar(
        route_handlers=[api_router],
        plugins=[sqlalchemy_plugin, structlog_plugin],
    )


@pytest.fixture(scope="session")
async def test_engine() -> AsyncGenerator[AsyncEngine, None]:
    """Setup test database."""
    if not database_exists(TEST_DB_URI):
        create_database(TEST_DB_URI)

    test_engine = sqlalchemy_config.get_engine()

    async with test_engine.begin() as conn:
        await conn.run_sync(UUIDBase.metadata.create_all)

    yield test_engine

    async with test_engine.begin() as conn:
        await conn.run_sync(UUIDBase.metadata.drop_all)

    drop_database(TEST_DB_URI)


@pytest.fixture(scope="function")
async def db_session(
    test_engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    """Database session fixture."""
    session_maker = sqlalchemy_config.create_session_maker()
    async with test_engine.connect() as conn:
        async with conn.begin():
            async with session_maker() as session:
                yield session


@pytest.fixture(scope="function")
async def test_client(
    test_app: Litestar,
    test_engine: AsyncEngine,
) -> AsyncIterator[AsyncTestClient[Litestar]]:
    """Test client fixture."""
    async with AsyncTestClient(app=test_app) as client:
        yield client


@pytest.fixture(scope="function")
async def created_author(db_session: AsyncGenerator) -> Author:
    """Created author fixture."""
    author = Author(name="Author", dob="2022-01-01")

    db_session.add(author)

    await db_session.commit()
    await db_session.refresh(author)

    return author
