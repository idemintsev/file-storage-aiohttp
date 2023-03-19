import os
import subprocess
import asyncclick as click
import uvloop

from file_storage_service import asgi  # noqa


@click.group
def cli():
    pass


@cli.command()
def appserver():
    app_env = os.environ.copy()
    click.echo('Run file storage service')
    subprocess.run("gunicorn gateway:asgi -c ./deploy/gunicorn.ini".split(' '), env=app_env)


if __name__ == '__main__':
    uvloop.install()
    cli(_anyio_backend='asyncio')
