from contextlib import asynccontextmanager

import redis.asyncio as redis
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from phishield.conf import environment


@asynccontextmanager
async def api_lifespan(app: FastAPI):
    await api_startup(app)
    yield
    await api_shutdown(app)


def get_db():
    engine = create_engine(environment.DATABASE_URI)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def api_startup(app: FastAPI):
    logger.info("Starting up FastAPI")

    await FastAPILimiter.init(
        redis=redis.from_url(
            environment.CACHE_URI,
            encoding="utf-8",
            decode_responses=True,
        )
    )


async def api_shutdown(app: FastAPI):
    logger.debug("Shutting down FastAPI")
