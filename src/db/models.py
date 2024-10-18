"""Database models."""

from __future__ import annotations

import uuid
from datetime import date

from litestar.contrib.sqlalchemy.base import UUIDBase
from litestar.dto import dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Book(UUIDBase):
    """Book model."""

    __tablename__ = "book"

    title: Mapped[str]
    description: Mapped[str]

    author_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("author.id", ondelete="CASCADE"),
        info=dto_field("write-only"),
    )
    author: Mapped[Author] = relationship(
        lazy="joined",
        innerjoin=True,
        viewonly=True,
        info=dto_field("read-only"),
    )


class Author(UUIDBase):
    """Author model."""

    __tablename__ = "author"

    name: Mapped[str]
    dob: Mapped[date]
    books: Mapped[list[Book]] = relationship(
        back_populates="author",
        lazy="selectin",
        info=dto_field("read-only"),
    )
