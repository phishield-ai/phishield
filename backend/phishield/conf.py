from loguru import logger
from pydantic_settings import BaseSettings


class Environment(BaseSettings):
    PRODUCTION: bool = False

    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    MINIO_STORAGE_BUCKET: str
    MINIO_STORAGE_URI: str

    CACHE_HOST: str
    CACHE_PORT: str
    CACHE_DB: int

    GOOGLE_API_KEY: str
    GOOGLE_AI_MODEL: str

    VIRUS_TOTAL_API_KEY: str

    @property
    def DATABASE_URI(self):
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def CACHE_URI(self):
        return f"redis://{self.CACHE_HOST}:{self.CACHE_PORT}/{self.CACHE_DB}"

    @classmethod
    def from_env(cls):
        return cls.model_validate({})


logger.debug("Loading environment variables")
environment = Environment.from_env()
