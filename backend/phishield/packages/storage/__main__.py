import asyncio

import click

from .base import StorageConnector
from .schemas import MinioObjectStorageSettings
from .utils import minio_setup_bucket


async def upload(file, filename, settings):
    async with StorageConnector(settings) as connector:
        await connector.upload(bytes=file, key=filename)


def base_options(f):
    f = click.option("-f", "--file", type=click.File("rb"), required=True)(f)
    f = click.option("-n", "--filename", type=str, required=True)(f)
    f = click.option("-b", "--bucket", type=str, required=True, default="raws")(f)
    return f


@click.group()
def cli():
    pass


@click.command(help="Upload file to Minio storage")
@click.option("-u", "--user", type=str, required=True)
@click.option("-p", "--password", type=str, required=True)
@base_options
def minio(
    file: click.File,
    filename: str,
    endpoint_url: str,
    user: str,
    password: str,
    domain: str,
    bucket: str,
):
    settings = MinioObjectStorageSettings(
        endpoint_url=endpoint_url,
        user=user,
        password=password,
        bucket=bucket,
        domain=domain,
    )
    minio_setup_bucket(domain, user, password, bucket, False)
    click.echo("Starting upload...")
    asyncio.run(upload(file, filename, settings))
    click.echo("Upload finished!")


cli.add_command(minio)

if __name__ == "__main__":
    cli()
