from enum import Enum
from typing import Any, Dict, Generic, Optional, Type, TypeVar

from pydantic import BaseModel, Field
from typing_extensions import Annotated


class Status(str, Enum):
    SUCCESS = "success"
    FAIL = "fail"
    ERROR = "error"


T = TypeVar("T")


StatusAnnotation = Annotated[
    str,
    Field(
        title="Response Status",
    ),
]

DataAnnotation = Annotated[
    Optional[Any],
    Field(
        title="Response Data",
    ),
]

TDataAnnotation = Annotated[
    T,
    Field(
        title="Response Data",
    ),
]

MesageAnnotation = Annotated[
    Optional[str],
    Field(
        title="Response Message",
    ),
]


class JSendResponseModel(BaseModel, Generic[T]):
    status: StatusAnnotation
    data: Optional[TDataAnnotation] = None
    message: MesageAnnotation = None


class SuccesJSendResponse(JSendResponseModel[T]):
    status: StatusAnnotation = Status.SUCCESS
    data: TDataAnnotation


class FailResponse(JSendResponseModel):
    status: StatusAnnotation = Status.FAIL


class ErrorResponse(JSendResponseModel):
    status: StatusAnnotation = Status.ERROR


def response_documentation(model: Type[T]) -> Dict[int | str, Dict[str, Any]]:
    return {
        200: {"model": SuccesJSendResponse[model] if model is not None else JSendResponseModel},
        404: {"model": FailResponse},
        422: {"model": FailResponse},
        500: {"model": ErrorResponse},
    }
