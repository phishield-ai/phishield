from fastapi import APIRouter


router = APIRouter(
    tags=["API Healthchecks"],
    include_in_schema=False,
)


@router.get("/healthz")
async def liveness():
    return {"status": "OK"}
