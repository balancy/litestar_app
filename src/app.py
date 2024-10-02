"""Main application."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import psycopg
from litestar import Litestar

from config import DB_URI
from controllers import BooksController


@asynccontextmanager
async def db_connection(app: Litestar) -> AsyncGenerator[None, None]:
    """Create and dispose of the database connection."""
    connection = getattr(app.state, "db_connection", None)
    if connection is None:
        connection = await psycopg.AsyncConnection.connect(DB_URI)
        app.state.db_connection = connection

    try:
        yield
    finally:
        await connection.close()


app = Litestar(
    lifespan=[db_connection],
    route_handlers=[BooksController],
)
