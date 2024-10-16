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
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from db.models import Author, UUIDBase
from logger import structlog_plugin
from routers import api_router

TEST_DB_URI = (
    "postgresql+psycopg://postgres:postgres@postgres_test:5432/db_test"
)


@pytest.fixture(scope="function")
def test_app() -> Litestar:
    """Create and configure the test app."""
    sqlalchemy_plugin = SQLAlchemyPlugin(
        config=SQLAlchemyAsyncConfig(
            connection_string=TEST_DB_URI,
            session_config=AsyncSessionConfig(expire_on_commit=False),
        ),
    )

    return Litestar(
        route_handlers=[api_router],
        plugins=[sqlalchemy_plugin, structlog_plugin],
        debug=True,
        # exception_handlers=exception_handlers,
    )


@pytest.fixture(scope="function")
async def test_client(
    test_app: Litestar,
    setup_test_db: AsyncGenerator,
) -> AsyncIterator[AsyncTestClient[Litestar]]:
    """Test client fixture."""
    async with AsyncTestClient(app=test_app) as client:
        yield client


test_engine = create_async_engine(TEST_DB_URI, echo=False)
session_local = async_sessionmaker(
    test_engine,
    autocommit=False,
    autoflush=False,
)


@pytest.fixture(scope="function")
async def setup_test_db() -> AsyncGenerator:
    """Setup test database."""
    async with test_engine.begin() as conn:
        await conn.run_sync(UUIDBase.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(UUIDBase.metadata.drop_all)


@pytest.fixture(scope="function")
async def db_session(
    setup_test_db: AsyncGenerator,
) -> AsyncGenerator:
    """Database session fixture."""
    async with session_local() as session:
        yield session
        await session.rollback()


@pytest.fixture(scope="function")
async def created_author(db_session: AsyncGenerator) -> Author:
    """Created author fixture."""
    author = Author(name="Author", dob="2022-01-01")

    db_session.add(author)

    await db_session.commit()
    await db_session.refresh(author)

    return author
