from typing import Any

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .schemas import JSendResponseModel, Status


class JSendResponse(JSONResponse):
    """JSend response.

    Spec: https://github.com/omniti-labs/jsend
    """

    def __init__(self, data: Any = None, message: str = None, status_code: int = 200, **kwargs):
        if status_code < 400:
            status = Status.SUCCESS
        elif 400 <= status_code < 500:
            status = Status.FAIL
        else:
            status = Status.ERROR

        content = JSendResponseModel(
            status=status,
            data=data if status != "error" else None,
            message=message,
        ).model_dump()

        super().__init__(
            content=jsonable_encoder(content),
            status_code=status_code,
            **kwargs,
        )
