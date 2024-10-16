"""Router module."""

from litestar import Router

from controllers.author_controller import AuthorsController
from controllers.book_controller import BooksController

api_router = Router(
    path="/api",
    route_handlers=[BooksController, AuthorsController],
)
