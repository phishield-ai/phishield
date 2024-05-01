import io
import re
from typing import List, Optional

import eml_parser
import requests
from html2text import html2text

from phishield.apps.email.models.email import EmailAttachment, EmailLink, EmailServer, EmailSummary
from phishield.common.models.virustotal import Analysis
from phishield.common.utils.file import FileProcessor


class EmailProcessor:
    def __init__(self, contents: bytes):
        self.contents = contents
        self.parser = eml_parser.EmlParser(
            include_attachment_data=True,
            include_raw_body=True,
            parse_attachments=True,
            include_href=True,
            include_www=True,
        )
        self.eml = self.parser.decode_email_bytes(contents)

    def _text(self, payload: bytes) -> str:
        decoded = payload.decode("utf-8")
        text = html2text(decoded).strip()
        return text

    def body(self) -> Optional[list[str]]:
        body = []
        if "body" in self.eml:
            for item in self.eml["body"]:
                if "content" in item and item["content_type"] == "text/plain":
                    body.append(self._text(item["content"].encode("utf-8")))
        return body

    async def attachments(self) -> List[EmailAttachment]:
        attachments = []

        if "attachment" in self.eml:
            for attachment in self.eml["attachment"]:
                file = FileProcessor()
                analysis = await file.scan(io.BytesIO(attachment["raw"]))

                attachments.append(
                    EmailAttachment(
                        filename=attachment["filename"],
                        size=attachment["size"],
                        extension=attachment["extension"],
                        hashes=attachment["hash"],
                        content_type=attachment["content_header"]["content-type"] or None,
                        analysis=Analysis(**analysis) or None,  # type: ignore
                    )
                )

        return attachments

    def links(self) -> List[EmailLink]:
        links = []
        visited = set()

        if "body" in self.eml:
            for item in self.eml["body"]:
                if "uri" in item:
                    for url in item["uri"]:
                        if url not in visited:
                            try:
                                response = requests.head(url, allow_redirects=True)
                                links.append(EmailLink(url=response.url, status=response.status_code))
                                visited.add(url)
                            except requests.RequestException:
                                continue

        return links

    def server(self) -> EmailServer:
        data = self.eml["header"]["header"]["authentication-results"]
        spf_status = re.search(r"spf=(\w+)", data[0])
        dkim_status = re.search(r"dkim=(\w+)", data[0])
        dmarc_status = re.search(r"dmarc=(\w+)", data[0])

        return EmailServer(
            results=data[0] or None,
            spf_status=spf_status.group(1) if spf_status else None,
            dkim_status=dkim_status.group(1) if dkim_status else None,
            dmarc_status=dmarc_status.group(1) if dmarc_status else None,
        )

    async def summary(self) -> EmailSummary:
        return EmailSummary(
            server=self.server(),
            subject=self.eml["header"]["subject"],  # type: ignore
            attachments=await self.attachments(),
            links=self.links(),
            body=self.body(),
        )
