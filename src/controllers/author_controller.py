"""Author controller."""

from __future__ import annotations

from uuid import UUID

from litestar import Controller, delete, get, patch, post
from litestar.di import Provide

from db.models import AuthorModel
from db.repositories import (
    AuthorRepository,
    provide_author_details_repo,
    provide_authors_repo,
)
from models.author_models import Author, AuthorCreate, AuthorUpdate


class AuthorsController(Controller):
    """Authors controller."""

    path = "/authors"
    dependencies = {"authors_repo": Provide(provide_authors_repo)}
    tags = ["authors"]

    @post(name="post_author", description="Create a new author.")
    async def create_author(
        self,
        authors_repo: AuthorRepository,
        data: AuthorCreate,
    ) -> Author:
        """Create a author."""
        new_row = await authors_repo.add(AuthorModel(**data.model_dump()))
        await authors_repo.session.commit()
        return Author.model_validate(new_row)

    @get(name="get_authors", description="List authors.")
    async def list_authors(
        self, authors_repo: AuthorRepository,
    ) -> list[Author]:
        """List authors."""
        author_rows = await authors_repo.list()
        return [Author.model_validate(_) for _ in author_rows]

    @get(
        path="/{author_id:uuid}",
        name="get_author",
        description="Get a author.",
        dependencies={"authors_repo": Provide(provide_author_details_repo)},
    )
    async def get_author(
        self,
        authors_repo: AuthorRepository,
        author_id: UUID,
    ) -> Author:
        """Get a author."""
        obj = await authors_repo.get(author_id)
        return Author.model_validate(obj)

    @delete(
        path="/{author_id:uuid}",
        name="delete_author",
        description="Delete a author.",
    )
    async def delete_author(
        self,
        authors_repo: AuthorRepository,
        author_id: UUID,
    ) -> None:
        """Delete a author."""
        await authors_repo.delete(author_id)
        await authors_repo.session.commit()

    @patch(
        path="/{author_id:uuid}",
        name="patch_author",
        description="Partially update a author.",
        dependencies={"authors_repo": Provide(provide_author_details_repo)},
    )
    async def update_author(
        self,
        authors_repo: AuthorRepository,
        author_id: UUID,
        data: AuthorUpdate,
    ) -> Author:
        """Update a author."""
        raw_obj = data.model_dump(exclude_unset=True, exclude_none=True)
        raw_obj.update({"id": author_id})
        obj = await authors_repo.update(AuthorModel(**raw_obj))
        await authors_repo.session.commit()
        return Author.model_validate(obj)
