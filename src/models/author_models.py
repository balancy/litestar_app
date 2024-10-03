"""Author validation models."""

from datetime import date
from uuid import UUID

from models.base_models import BaseModel


class Author(BaseModel):
    """Author validation model."""

    id: UUID
    name: str
    dob: date


class AuthorCreate(BaseModel):
    """Author create validation model."""

    name: str
    dob: date


class AuthorUpdate(BaseModel):
    """Author update validation model."""

    name: str | None = None
    dob: date | None = None
