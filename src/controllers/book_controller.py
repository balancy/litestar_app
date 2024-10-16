"""Book controller."""

from __future__ import annotations

from uuid import UUID

from litestar import Controller, delete, get, patch, post
from litestar.di import Provide

from db.dtos import BookCreateDTO, BookUpdateDTO
from db.models import Book
from db.repositories import BookRepo, provide_books_repo


class BooksController(Controller):
    """Books controller."""

    path = "/books"
    dependencies = {"repo": Provide(provide_books_repo)}
    tags = ["books"]

    @post(
        name="post_book",
        description="Create a new book.",
        dto=BookCreateDTO,
    )
    async def create_book(
        self,
        repo: BookRepo,
        data: Book,
    ) -> Book:
        """Create a book."""
        new_book = await repo.add(data)
        await repo.session.commit()
        return new_book

    @get(name="list_books", description="List books.")
    async def list_books(self, repo: BookRepo) -> list[Book]:
        """List books."""
        return await repo.list()

    @get(path="/{book_id:uuid}", name="get_book", description="Get a book.")
    async def get_book(self, repo: BookRepo, book_id: UUID) -> Book:
        """Get a book."""
        return await repo.get(book_id)

    @delete(
        path="/{book_id:uuid}",
        name="delete_book",
        description="Delete a book.",
    )
    async def delete_book(self, repo: BookRepo, book_id: UUID) -> None:
        """Delete a book."""
        await repo.delete(book_id)
        await repo.session.commit()

    @patch(
        path="/{book_id:uuid}",
        name="patch_book",
        description="Update a book.",
        dto=BookUpdateDTO,
    )
    async def update_book(
        self,
        repo: BookRepo,
        book_id: UUID,
        data: Book,
    ) -> Book:
        """Update a book."""
        data.id = book_id
        book = await repo.update(data)
        await repo.session.commit()
        return book
