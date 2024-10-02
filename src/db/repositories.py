"""Database repositories."""

from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import BookModel


class BookRepository(SQLAlchemyAsyncRepository[BookModel]):
    """Book repository."""

    model_type = BookModel


async def provide_books_repo(db_session: AsyncSession) -> BookRepository:
    """Provide the books repository."""
    return BookRepository(session=db_session)
