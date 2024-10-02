"""Validation models."""

from uuid import UUID

from pydantic import BaseModel as _BaseModel


class BaseModel(_BaseModel):
    """Base model."""

    model_config = {"from_attributes": True}


class Book(BaseModel):
    """Book validation model."""

    id: UUID
    title: str
    description: str


class BookCreate(BaseModel):
    """Book create validation model."""

    title: str
    description: str


class BookUpdate(BaseModel):
    """Book update validation model."""

    title: str | None = None
    description: str | None = None
