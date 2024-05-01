from pydantic import BaseModel


class APIResponseAnalysis(BaseModel):
    score: int
    suspicious_elements: str
