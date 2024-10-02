"""Book validation models."""

from uuid import UUID

from models.base_models import BaseModel


class Book(BaseModel):
    """Book validation model."""

    id: UUID
    title: str
    description: str
    author_id: UUID


class BookCreate(BaseModel):
    """Book create validation model."""

    title: str
    description: str
    author_id: UUID


class BookUpdate(BaseModel):
    """Book update validation model."""

    title: str | None = None
    description: str | None = None
    author_id: UUID | None = None
