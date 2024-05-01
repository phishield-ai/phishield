from typing import Optional

from pydantic import BaseModel

from phishield.common.models.file import HashValues
from phishield.common.models.virustotal import Analysis


class EmailLink(BaseModel):
    url: str
    status: int


class EmailAttachment(BaseModel):
    filename: str
    extension: str
    size: int
    content_type: Optional[list[str]] = None
    analysis: Optional[Analysis] = None
    hashes: HashValues


class EmailServer(BaseModel):
    results: Optional[str] = None
    spf_status: Optional[str] = None
    dkim_status: Optional[str] = None
    dmarc_status: Optional[str] = None


class EmailHeader(BaseModel):
    subject: Optional[str] = None
    languages: Optional[list[str]] = None
    date: str


class EmailSummary(BaseModel):
    server: Optional[EmailServer] = None
    header: Optional[EmailHeader] = None
    body: Optional[list[str]] = None
    links: Optional[list[EmailLink]] = []
    attachments: Optional[list[EmailAttachment]] = []
