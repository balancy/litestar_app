"""DTOs for database models."""

from typing import Annotated

from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO
from litestar.dto import DTOConfig

from db.models import Author, Book

AuthorCreateDTO = SQLAlchemyDTO[Annotated[Author, DTOConfig(exclude={"id"})]]
BookCreateDTO = SQLAlchemyDTO[Annotated[Book, DTOConfig(exclude={"id"})]]

AuthorUpdateDTO = SQLAlchemyDTO[
    Annotated[Author, DTOConfig(exclude={"id"}, partial=True)]
]
BookUpdateDTO = SQLAlchemyDTO[
    Annotated[Book, DTOConfig(exclude={"id"}, partial=True)]
]
