import sys
import time

import click
from dramatiq import cli as dramatiq
from loguru import logger

from phishield.packages.redis.utils import get_cache


def base_options(f):
    f = click.option(
        "--dev",
        is_flag=True,
        default=False,
        help="Enable dev mode.",
    )(f)
    return f


@click.group()
def cli():
    """Command line interface for phishield."""
    pass


@click.command(help="Run API.")
@base_options
def api(dev):
    import uvicorn

    if dev:
        import debugpy

        from phishield.conf import environment
        from phishield.packages.storage.utils import minio_health_check, minio_setup_bucket

        debugpy.listen(7999)

        while not get_cache().ping():
            logger.info("Waiting for Redis to be up...")
            time.sleep(2)

        while not minio_health_check(
            endpoint_url=environment.MINIO_STORAGE_URI,
            user=environment.MINIO_ROOT_USER,
            password=environment.MINIO_ROOT_PASSWORD,
            secure=False,
        ):
            logger.info("Waiting for MinIO to be up...")
            time.sleep(2)

        minio_setup_bucket(
            endpoint_url=environment.MINIO_STORAGE_URI,
            bucket=environment.MINIO_STORAGE_BUCKET,
            user=environment.MINIO_ROOT_USER,
            password=environment.MINIO_ROOT_PASSWORD,
            secure=False,
        )

    uvicorn.run(
        "phishield:api",
        host="0.0.0.0",
        port=8000,
        proxy_headers=True,
        forwarded_allow_ips="*",
        reload=True if dev else False,
        log_level="debug" if dev else "info",
    )


@click.command(help="Run Worker.")
@base_options
def worker(dev):
    sys.argv.pop(0)
    if dev:
        sys.argv.pop(0)

    sys.argv += [
        "phishield.worker.tasks:broker",
    ]

    if dev:
        sys.argv += [
            "--processes=1",
            "--threads=1",
            "--watch=phishield/",
        ]
    dramatiq.main()


@cli.group(help="Setup commands")
def setup():
    pass


cli.add_command(api)
cli.add_command(worker)
