from pydantic import BaseModel


class MinioObjectStorageSettings(BaseModel):
    endpoint_url: str
    user: str
    password: str
    bucket: str
