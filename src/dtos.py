"""App dtos."""

from dataclasses import dataclass
from uuid import UUID

from litestar.dto import DataclassDTO, DTOConfig


@dataclass(slots=True)
class Book:
    """Book dataclass."""

    book_id: UUID
    title: str
    description: str
    author: str


class PartialUpdateBookDTO(DataclassDTO[Book]):
    """Partial update book DTO."""

    config = DTOConfig(exclude={"book_id"}, partial=True)


class UpdateBookDTO(DataclassDTO[Book]):
    """Update book DTO."""

    config = DTOConfig(exclude={"book_id"})
