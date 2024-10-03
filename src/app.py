"""Main application."""

from litestar import Litestar

from controllers.author_controller import AuthorsController
from controllers.book_controller import BooksController
from db.connection import sqlalchemy_plugin

app = Litestar(
    plugins=[sqlalchemy_plugin],
    route_handlers=[BooksController, AuthorsController],
    debug=True,
)
