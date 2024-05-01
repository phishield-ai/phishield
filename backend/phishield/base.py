from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from starlette.middleware import Middleware
from starlette_context import plugins
from starlette_context.middleware import RawContextMiddleware

from phishield import lifespan
from phishield.apps import email
from phishield.packages.fastapi import healthcheks
from phishield.packages.fastapi.jsend.exceptions import (
    HTTPExceptionHandler,
    RequestValidationExceptionHandler,
    StarletteHTTPExceptionHandler,
    UncatchedExceptionHandler,
)


api = FastAPI(
    title="phishield",
    description="phishield",
    docs_url="/debug",
    redoc_url="/docs",
    middleware=[
        Middleware(
            RawContextMiddleware,
            plugins=(
                plugins.RequestIdPlugin(),  # type: ignore
                plugins.CorrelationIdPlugin(),  # type: ignore
            ),
        )
    ],
    lifespan=lifespan.api_lifespan,
)


api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api.add_exception_handler(*StarletteHTTPExceptionHandler)  # type: ignore
api.add_exception_handler(*HTTPExceptionHandler)  # type: ignore
api.add_exception_handler(*RequestValidationExceptionHandler)  # type: ignore
api.add_exception_handler(*UncatchedExceptionHandler)

api.include_router(healthcheks.routes.router)

for app in [email]:
    api.include_router(app.router)

add_pagination(api)
