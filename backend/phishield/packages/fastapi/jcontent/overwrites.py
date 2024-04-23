from abc import ABC
from math import ceil
from typing import (
    Any,
    Generic,
    Optional,
    Sequence,
    TypeVar,
)

from fastapi_pagination import Params
from fastapi_pagination.bases import AbstractPage, AbstractParams
from fastapi_pagination.types import GreaterEqualOne, GreaterEqualZero
from fastapi_pagination.utils import create_pydantic_model


T = TypeVar("T")


class BasePage(AbstractPage[T], Generic[T], ABC):
    content: Sequence[T]
    total: Optional[GreaterEqualZero]


class Page(BasePage[T], Generic[T]):
    page: Optional[GreaterEqualOne]
    size: Optional[GreaterEqualOne]
    pages: Optional[GreaterEqualZero] = None

    __params_type__ = Params

    @classmethod
    def create(
        cls,
        items: Any,
        params: AbstractParams,
        **kwargs: Any,
    ) -> BasePage[T]:
        total = kwargs.pop("total")

        if not isinstance(params, Params):
            raise TypeError("Page should be used with Params")

        size = params.size if params.size is not None else total
        page = params.page if params.page is not None else 1

        if size == 0:
            pages = 0
        elif total is not None:
            pages = ceil(total / size)
        else:
            pages = None

        return create_pydantic_model(
            cls,
            total=total,
            content=items,
            page=page,
            size=size,
            pages=pages,
            **kwargs,
        )
