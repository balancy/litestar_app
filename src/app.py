"""Main application."""

from litestar import Litestar

from config import DEBUG
from controllers.author_controller import AuthorsController
from controllers.book_controller import BooksController
from db.connection import sqlalchemy_plugin
from exceptions import EXCEPTION_HANDLERS

app = Litestar(
    plugins=[sqlalchemy_plugin],
    route_handlers=[BooksController, AuthorsController],
    debug=DEBUG,
    exception_handlers=EXCEPTION_HANDLERS,
)
