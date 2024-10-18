"""Client-related fixtures."""

from typing import AsyncIterator

import pytest
from db_config import sqlalchemy_plugin
from litestar import Litestar
from litestar.testing import AsyncTestClient
from sqlalchemy.ext.asyncio import AsyncEngine

from exceptions import exception_handlers
from routers import api_router


@pytest.fixture(scope="session")
def test_app() -> Litestar:
    """Create and configure the test app."""
    return Litestar(
        route_handlers=[api_router],
        plugins=[sqlalchemy_plugin],
        exception_handlers=exception_handlers,
    )


@pytest.fixture(scope="function")
async def test_client(
    test_app: Litestar,
    test_engine: AsyncEngine,
) -> AsyncIterator[AsyncTestClient[Litestar]]:
    """Test client fixture."""
    async with AsyncTestClient(app=test_app) as client:
        yield client
