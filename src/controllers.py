"""App controllers."""

from __future__ import annotations

from uuid import UUID

from litestar import Controller, delete, get, patch, post
from litestar.di import Provide

from db.models import BookModel
from db.repositories import BookRepository, provide_books_repo
from models import Book, BookCreate, BookUpdate


class BooksController(Controller):
    """Books controller."""

    path = "/books"
    dependencies = {"books_repo": Provide(provide_books_repo)}

    @post(name="post_book", description="Create a new book.")
    async def create_book(self, books_repo: BookRepository, data: BookCreate) -> Book:
        """Create a book."""
        new_row = await books_repo.add(BookModel(**data.model_dump()))
        await books_repo.session.commit()
        return Book.model_validate(new_row)

    @get(name="get_books", description="List books.")
    async def list_books(self, books_repo: BookRepository) -> list[Book]:
        """List books."""
        book_rows = await books_repo.list()
        return [Book.model_validate(_) for _ in book_rows]

    @get(path="/{book_id:uuid}", name="get_book", description="Get a book.")
    async def get_book(self, books_repo: BookRepository, book_id: UUID) -> Book:
        """Get a book."""
        obj = await books_repo.get(book_id)
        return Book.model_validate(obj)

    @delete(path="/{book_id:uuid}", name="delete_book", description="Delete a book.")
    async def delete_book(self, books_repo: BookRepository, book_id: UUID) -> None:
        """Delete a book."""
        await books_repo.delete(book_id)
        await books_repo.session.commit()

    @patch(
        path="/{book_id:uuid}",
        name="patch_book",
        description="Partially update a book.",
    )
    async def partial_update_book(
        self,
        books_repo: BookRepository,
        book_id: UUID,
        data: BookUpdate,
    ) -> Book:
        """Partial update a book."""
        raw_obj = data.model_dump(exclude_unset=True, exclude_none=True)
        raw_obj.update({"id": book_id})
        obj = await books_repo.update(BookModel(**raw_obj))
        await books_repo.session.commit()
        return Book.model_validate(obj)
