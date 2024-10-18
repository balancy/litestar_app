"""Database fixtures."""

from collections.abc import AsyncGenerator

import pytest
from db_config import TEST_DB_URI, sqlalchemy_config
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy_utils import create_database, database_exists, drop_database

from db.models import Author, Book, UUIDBase


@pytest.fixture(scope="session")
async def test_engine() -> AsyncGenerator[AsyncEngine, None]:
    """Setup test database."""
    if not database_exists(TEST_DB_URI):
        create_database(TEST_DB_URI)

    test_engine = sqlalchemy_config.get_engine()

    async with test_engine.begin() as conn:
        await conn.run_sync(UUIDBase.metadata.create_all)

    yield test_engine

    async with test_engine.begin() as conn:
        await conn.run_sync(UUIDBase.metadata.drop_all)

    drop_database(TEST_DB_URI)


@pytest.fixture(scope="function")
async def db_session(
    test_engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    """Database session fixture."""
    session_maker = sqlalchemy_config.create_session_maker()
    async with test_engine.connect() as conn:
        async with conn.begin():
            async with session_maker() as session:
                yield session


@pytest.fixture(scope="function")
async def created_author(db_session: AsyncGenerator) -> Author:
    """Created author fixture."""
    author = Author(name="Author", dob="2022-01-01")

    db_session.add(author)

    await db_session.commit()
    await db_session.refresh(author)

    return author


@pytest.fixture(scope="function")
async def created_book(
    db_session: AsyncGenerator,
    created_author: Author,
) -> Book:
    """Created book fixture."""
    book = Book(
        title="Book",
        description="Description",
        author_id=created_author.id,
    )

    db_session.add(book)

    await db_session.commit()
    await db_session.refresh(book)

    return book
