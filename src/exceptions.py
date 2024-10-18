"""Exception halndlers."""

from advanced_alchemy.exceptions import NotFoundError
from litestar import MediaType, Request, Response
from litestar.exceptions import HTTPException
from litestar.exceptions.http_exceptions import NoRouteMatchFoundException
from litestar.status_codes import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from litestar.types import ExceptionHandlersMap
from sqlalchemy.exc import DatabaseError, IntegrityError


def http_exception_handler(_: Request, exc: HTTPException) -> Response:
    """Handle http exceptions."""
    return Response(
        media_type=MediaType.TEXT,
        content=str(exc),
        status_code=exc.status_code,
    )


def no_route_match_found_exception_handler(
    _: Request,
    exc: NoRouteMatchFoundException,
) -> Response:
    """Handle no route match found exceptions."""
    return Response(
        media_type=MediaType.TEXT,
        content=str(exc),
        status_code=HTTP_400_BAD_REQUEST,
    )


def db_integrity_exception_handler(
    _: Request,
    exc: IntegrityError,
) -> Response:
    """Handle database integrity exceptions."""
    return Response(
        media_type=MediaType.TEXT,
        content=str(exc),
        status_code=HTTP_409_CONFLICT,
    )


def db_not_found_exception_handler(_: Request, exc: NotFoundError) -> Response:
    """Handle database 'not found' exceptions."""
    return Response(
        media_type=MediaType.TEXT,
        content=str(exc),
        status_code=HTTP_404_NOT_FOUND,
    )


def db_exception_handler(_: Request, exc: DatabaseError) -> Response:
    """Handle database exceptions."""
    return Response(
        media_type=MediaType.TEXT,
        content=str(exc),
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )


def unhandled_exception_handler(_: Request, exc: Exception) -> Response:
    """Handle unhandled exceptions."""
    return Response(
        media_type=MediaType.TEXT,
        content=str(exc),
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )


exception_handlers: ExceptionHandlersMap = {
    HTTPException: http_exception_handler,
    NoRouteMatchFoundException: no_route_match_found_exception_handler,
    IntegrityError: db_integrity_exception_handler,
    DatabaseError: db_exception_handler,
    NotFoundError: db_not_found_exception_handler,
    Exception: unhandled_exception_handler,
}
