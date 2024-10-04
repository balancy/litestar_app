"""Database repositories."""

from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.models import Author, Book


class BookRepo(SQLAlchemyAsyncRepository[Book]):
    """Book repository."""

    model_type = Book


class AuthorRepo(SQLAlchemyAsyncRepository[Author]):
    """Author repository."""

    model_type = Author


async def provide_books_repo(db_session: AsyncSession) -> BookRepo:
    """Provide the books repository."""
    return BookRepo(session=db_session)


async def provide_authors_repo(db_session: AsyncSession) -> AuthorRepo:
    """Provide the authors repository."""
    return AuthorRepo(session=db_session)


async def provide_author_details_repo(db_session: AsyncSession) -> AuthorRepo:
    """Provide the authors repository."""
    return AuthorRepo(
        statement=select(Author).options(selectinload(Author.books)),
        session=db_session,
    )
