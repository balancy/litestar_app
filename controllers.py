"""App controllers."""

from __future__ import annotations

from typing import ClassVar
from uuid import UUID

from litestar import Controller, delete, get, patch, post, put
from litestar.dto import DTOData

from dtos import Book, PartialUpdateBookDTO, UpdateBookDTO


class BooksController(Controller):
    """Books controller."""

    path = "/books"
    books: ClassVar[dict[UUID, Book]] = {}

    @post()
    async def create_book(self, data: Book) -> Book:
        """Create a book."""
        book = data
        self.books[book.book_id] = book
        return book

    @get()
    async def list_books(self) -> list[Book]:
        """List books."""
        return list(self.books.values())

    @patch(path="/{book_id:uuid}", dto=PartialUpdateBookDTO)
    async def partial_update_book(
        self,
        book_id: UUID,
        data: DTOData[Book],
    ) -> Book:
        """Partial update a book."""
        book = self.books[book_id]
        for key, value in data.as_builtins().items():
            setattr(book, key, value)

        return self.books[book_id]

    @put(path="/{book_id:uuid}", dto=UpdateBookDTO)
    async def update_book(self, book_id: UUID, data: DTOData[Book]) -> Book:
        """Update a book."""
        book = self.books[book_id]
        for key, value in data.as_builtins().items():
            setattr(book, key, value)

        return self.books[book_id]

    @get(path="/{book_id:uuid}")
    async def get_book(self, book_id: UUID) -> Book:
        """Get a book."""
        return self.books[book_id]

    @delete(path="/{book_id:uuid}")
    async def delete_book(self, book_id: UUID) -> None:
        """Delete a book."""
        del self.books[book_id]
