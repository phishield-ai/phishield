import sys

import click
import uvicorn
from dramatiq import cli as dramatiq


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
