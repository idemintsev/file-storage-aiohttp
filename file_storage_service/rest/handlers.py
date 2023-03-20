from aiohttp import web
from aiohttp_swagger import *

from file_storage_service.logger import logging
from file_storage_service.rest.utils import upload_file_to_server, find_file_on_server, delete_file_from_server
from docs.pathes import paths_to_swagger_docs

logger = logging.getLogger('rest')


@swagger_path(paths_to_swagger_docs.get('upload'))
async def upload_file(request: 'web.Request') -> 'web.Response':
    """Upload file from client to server by chunks."""
    username = request.username
    logger.debug(f'Uploading file by {username}')
    async for obj in (await request.multipart()):
        if obj.filename is not None:
            if filename := await upload_file_to_server(obj, username):
                return web.Response(text=filename, status=201)
    return web.Response(text='try to upload again', status=400)


@swagger_path(paths_to_swagger_docs.get('download'))
async def download_file(request: 'web.Request') -> 'web.StreamResponse':
    """Send file from server to client by chunks."""
    file_name: str = request.url.raw_parts[-1]
    logger.debug(f'Downloading file {file_name}')
    if file := await find_file_on_server(file_name):
        resp = web.StreamResponse()
        resp.headers.update({'Content-Type': 'application/octet-stream', 'Content-Disposition': 'attachment'})
        resp.enable_chunked_encoding()
        await resp.prepare(request)
        with open(file, 'rb') as f:
            for chunk in iter(lambda: f.read(1024), b""):
                await resp.write(chunk)
        await resp.write_eof()
        return resp
    return web.Response(text='file not found', status=404)


@swagger_path(paths_to_swagger_docs.get('delete'))
async def delete_file(request: 'web.Request') -> 'web.Response':
    """Delete file from server."""
    file_name = request.url.raw_parts[-1]
    username = request.username
    logger.debug(f'Deleting file {file_name} by {username}')
    if res := await delete_file_from_server(username, file_name):
        return web.Response(text=f'deleted {res}', status=200)
    return web.Response(text='file not found', status=404)
