"""Database models."""

from __future__ import annotations

from litestar.contrib.sqlalchemy.base import UUIDBase
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class BookModel(UUIDBase):
    """Book model."""

    __tablename__ = "book"

    title: Mapped[str]
    description: Mapped[str]


    # author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("author.id"))
    # author: Mapped[AuthorModel] = relationship(
    #     lazy="joined", innerjoin=True, viewonly=True
    # )


# class AuthorModel(UUIDBase):
#     """Author model."""

#     __tablename__ = "author"

#     name: Mapped[str]
#     books: Mapped[list[BookModel]] = relationship(
#         back_populates="author", lazy="selectin"
#     )
