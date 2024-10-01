"""Main application."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from litestar import Litestar
from sqlalchemy.ext.asyncio import create_async_engine

from config import DB_URI
from controllers import BooksController


@asynccontextmanager
async def db_connection(app: Litestar) -> AsyncGenerator[None, None]:
    """Create and dispose of the database connection."""
    engine = getattr(app.state, "engine", None)
    if engine is None:
        engine = create_async_engine(DB_URI)
        app.state.engine = engine

    try:
        yield
    finally:
        await engine.dispose()


app = Litestar(
    lifespan=[db_connection],
    route_handlers=[BooksController],
)
