"""Database repositories."""

from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.models import AuthorModel, BookModel


class BookRepository(SQLAlchemyAsyncRepository[BookModel]):
    """Book repository."""

    model_type = BookModel


class AuthorRepository(SQLAlchemyAsyncRepository[AuthorModel]):
    """Author repository."""

    model_type = AuthorModel


async def provide_books_repo(db_session: AsyncSession) -> BookRepository:
    """Provide the books repository."""
    return BookRepository(session=db_session)


async def provide_authors_repo(db_session: AsyncSession) -> AuthorRepository:
    """Provide the authors repository."""
    return AuthorRepository(session=db_session)


async def provide_author_details_repo(
    db_session: AsyncSession,
) -> AuthorRepository:
    """Provide the authors repository."""
    return AuthorRepository(
        statement=select(AuthorModel).options(selectinload(AuthorModel.books)),
        session=db_session,
    )
