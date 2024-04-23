from fastapi import HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from .response import JSendResponse


async def uncatched_exception_handler(request: Request, exc: Exception):
    return JSendResponse(
        status_code=500,
        message="Internal server error",
    )


async def starlette_http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSendResponse(
        status_code=exc.status_code,
        message=exc.detail,
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    return JSendResponse(
        status_code=exc.status_code,
        message=exc.detail,
    )


async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSendResponse(
        status_code=422,
        message="Validation error",
        data=jsonable_encoder(exc.errors()),
    )


StarletteHTTPExceptionHandler = (StarletteHTTPException, starlette_http_exception_handler)
HTTPExceptionHandler = (HTTPException, http_exception_handler)
RequestValidationExceptionHandler = (RequestValidationError, request_validation_exception_handler)
UncatchedExceptionHandler = (Exception, uncatched_exception_handler)
