"""Author controller."""

from __future__ import annotations

from uuid import UUID

from litestar import Controller, delete, get, patch, post
from litestar.di import Provide

from db.dtos import AuthorCreateDTO, AuthorUpdateDTO
from db.models import Author
from db.repositories import (
    AuthorRepo,
    provide_author_details_repo,
    provide_authors_repo,
)


class AuthorsController(Controller):
    """Authors controller."""

    path = "/authors"
    dependencies = {"repo": Provide(provide_authors_repo)}
    tags = ["authors"]

    @post(
        name="post_author",
        description="Create a new author.",
        dto=AuthorCreateDTO,
    )
    async def create_author(self, repo: AuthorRepo, data: Author) -> Author:
        """Create a new author."""
        new_author = await repo.add(data)
        await repo.session.commit()
        return new_author

    @get(name="get_authors", description="List authors.")
    async def list_authors(self, repo: AuthorRepo) -> list[Author]:
        """List authors."""
        return await repo.list()

    @get(
        path="/{author_id:uuid}",
        name="get_author",
        description="Get an author.",
        dependencies={"repo": Provide(provide_author_details_repo)},
    )
    async def get_author(self, repo: AuthorRepo, author_id: UUID) -> Author:
        """Get a author."""
        return await repo.get(author_id)

    @delete(
        path="/{author_id:uuid}",
        name="delete_author",
        description="Delete an author.",
    )
    async def delete_author(self, repo: AuthorRepo, author_id: UUID) -> None:
        """Delete an author."""
        await repo.delete(author_id)
        await repo.session.commit()

    @patch(
        path="/{author_id:uuid}",
        name="patch_author",
        description="Update an author.",
        dependencies={"repo": Provide(provide_author_details_repo)},
        dto=AuthorUpdateDTO,
    )
    async def update_author(
        self,
        repo: AuthorRepo,
        author_id: UUID,
        data: Author,
    ) -> Author:
        """Update an author."""
        data.id = author_id
        author = await repo.update(data)
        await repo.session.commit()
        return author
