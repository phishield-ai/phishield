from enum import Enum

from pydantic import BaseModel


class Analysis(BaseModel):
    malicious: int
    suspicious: int
    undetected: int
    harmless: int


class URLAnalysis(Analysis):
    pass


class FileAnalysis(Analysis):
    failure: int
    type_insupported: int


class AnalysisStatus(Enum):
    COMPLETED = "completed"
    QUEUED = "queued"
    IN_PROGRESS = "in-progress"
