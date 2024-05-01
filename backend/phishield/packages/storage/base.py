from io import BytesIO
from typing import Optional

import aioboto3
from loguru import logger

from phishield.conf import environment

from .schemas import MinioObjectStorageSettings


class StorageConnector:
    def __init__(self, settings: Optional[MinioObjectStorageSettings] = None) -> None:
        self.session = aioboto3.Session()
        if not settings:
            self.settings = MinioObjectStorageSettings(
                endpoint_url=f"http://{environment.MINIO_STORAGE_URI}",
                bucket=environment.MINIO_STORAGE_BUCKET,
                user=environment.MINIO_ROOT_USER,
                password=environment.MINIO_ROOT_PASSWORD,
            )

    async def upload(self, bytes: BytesIO, key: str, bucket: str) -> str:
        bucket_url = self.get_bucket_url(bucket)

        if not self.client:
            logger.trace(f"Not uploading data to {key}")

        logger.trace(f"Uploading data to {key}")
        await self.client.upload_fileobj(bytes, bucket, key)
        return f"{bucket_url}/{key}"

    async def download(self, key: str, bucket: str) -> BytesIO:
        if not self.client:
            logger.trace(f"Not downloading data from {key}")
            return BytesIO()

        logger.trace(f"Downloading data from {key}")
        obj = BytesIO()
        await self.client.download_fileobj(bucket, key, obj)
        return obj

    def get_bucket_url(self, bucket: str) -> str:
        return f"{self.settings.endpoint_url}/{bucket}"

    async def __aenter__(self):
        client = self.session.client("s3", use_ssl=False, **self.get_boto_client_args())
        self.client = await client.__aenter__()
        return self

    def get_boto_client_args(self):
        return {
            "endpoint_url": self.settings.endpoint_url,
            "aws_access_key_id": self.settings.user,
            "aws_secret_access_key": self.settings.password,
        }

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.client.__aexit__(exc_type, exc_value, traceback)
        del self.client
