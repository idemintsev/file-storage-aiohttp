from aiohttp import web
from aiohttp_swagger import *

from docs.pathes import paths_to_swagger_docs
from file_storage_service.logger import logging
from file_storage_service.rest.utils import upload_file_to_server, find_file_on_server, delete_file_from_server
from file_storage_service.settings import Config

logger = logging.getLogger('rest')


@swagger_path(paths_to_swagger_docs.get('upload'))
async def upload_file(request: 'web.Request') -> 'web.Response':
    """Upload file from client to server by chunks."""
    username = request.username
    logger.debug(f'Uploading file by {username}')
    async for obj in (await request.multipart()):
        if obj.filename is not None:
            if filename := await upload_file_to_server(obj, username):
                logger.info(f'Uploaded file {filename} by {username}')
                return web.Response(text=filename, status=201)
    return web.Response(text='try to upload again', status=400)


@swagger_path(paths_to_swagger_docs.get('download'))
async def download_file(request: 'web.Request') -> 'web.StreamResponse':
    """Send file from server to client by chunks."""
    filename: str = request.url.raw_parts[-1]
    logger.debug(f'Downloading file {filename}')
    if file := await find_file_on_server(filename):
        resp = web.StreamResponse()
        resp.headers.update({'Content-Type': 'application/octet-stream', 'Content-Disposition': 'attachment'})
        resp.enable_chunked_encoding()
        await resp.prepare(request)
        with open(file, 'rb') as f:
            for chunk in iter(lambda: f.read(Config.chunk_size), b""):
                await resp.write(chunk)
        await resp.write_eof()
        logger.info(f'Downloaded file {filename}')
        return resp
    return web.Response(text='file not found', status=404)


@swagger_path(paths_to_swagger_docs.get('delete'))
async def delete_file(request: 'web.Request') -> 'web.Response':
    """Delete file from server."""
    filename = request.url.raw_parts[-1]
    username = request.username
    logger.debug(f'Deleting file {filename} by {username}')
    if res := await delete_file_from_server(username, filename):
        logger.info(f'Deleted file {filename} by {username}')
        return web.Response(text=f'deleted {res}', status=200)
    return web.Response(text='file not found', status=404)
