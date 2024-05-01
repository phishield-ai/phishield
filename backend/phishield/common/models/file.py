from pydantic import BaseModel


class HashValues(BaseModel):
    md5: str
    sha1: str
    sha256: str
    sha512: str
