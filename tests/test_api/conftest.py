"""API test fixtures."""

from typing import AsyncGenerator

import pytest

from db.models import Author, Book


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
