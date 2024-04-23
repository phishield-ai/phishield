from typing import Generic, List, TypeVar

from pydantic import BaseModel

from .overwrites import Page


T = TypeVar("T")


class Content(BaseModel, Generic[T]):
    content: T


class ContentList(BaseModel, Generic[T]):
    content: List[T]


class ContentPagination(Page):
    content: List[T]
