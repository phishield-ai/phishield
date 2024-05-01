from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter

from phishield.packages.fastapi.jsend.response import JSendResponse

from .routers import analyse


router = APIRouter(
    prefix="/email",
    tags=["Email"],
    default_response_class=JSendResponse,
    include_in_schema=True,
    dependencies=[Depends(RateLimiter(times=30, seconds=5))],
)

for app in [analyse]:
    router.include_router(app.router)
