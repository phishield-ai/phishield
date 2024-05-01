from fastapi import APIRouter
from pydantic import BaseModel



class APIStatus(BaseModel):
    status: str

router = APIRouter(
    tags=["API Healthchecks"],
    include_in_schema=True
)

@router.get(
    "/healthz",
    summary="Health",
    response_model=APIStatus,
)
async def liveness():
    """
    Endpoint for checking the liveness of the API.
    
    Returns:
        APIStatus: An instance of APIStatus containing the status of the API.
    """
    return APIStatus(status="OK")
