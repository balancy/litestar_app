"""Main application."""

from litestar import Litestar
from litestar.contrib.sqlalchemy.base import UUIDBase

from controllers import BooksController
from db.connection import sqlalchemy_config, sqlalchemy_plugin


async def on_startup() -> None:
    """App startup event."""
    async with sqlalchemy_config.get_engine().begin() as conn:
        await conn.run_sync(UUIDBase.metadata.create_all)


app = Litestar(
    on_startup=[on_startup],
    plugins=[sqlalchemy_plugin],
    route_handlers=[BooksController],
    debug=True,
)
