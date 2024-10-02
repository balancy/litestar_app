"""Base models."""

from pydantic import BaseModel as _BaseModel


class BaseModel(_BaseModel):
    """Base model."""

    model_config = {"from_attributes": True}
