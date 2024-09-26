"""Main application."""

from litestar import Litestar

from controllers import BooksController

app = Litestar(route_handlers=[BooksController])
