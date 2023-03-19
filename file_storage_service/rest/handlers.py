from aiohttp import web

from file_storage_service.rest.utils import upload_file_to_server, reader_generator, find_file_on_server, \
    delete_file_from_server


async def upload_file(request: 'web.Request') -> 'web.Response':
    """Upload file from client to server by chunks."""
    username = request.username
    async for obj in (await request.multipart()):
        if obj.filename is not None:
            if filename := await upload_file_to_server(obj, username):
                return web.Response(text=filename, status=201)
    return web.Response(text='try to upload again', status=400)


async def download_file(request: 'web.Request') -> 'web.StreamResponse':
    """Send file from server to client by chunks."""
    file_name: str = request.url.raw_parts[-1]
    if file := await find_file_on_server(file_name):
        return web.Response(body=reader_generator(file), status=200)
    return web.Response(text='file not found', status=404)


async def delete_file(request: 'web.Request') -> 'web.Response':
    """Delete file from server."""
    file_name = request.url.raw_parts[-1]
    username = request.username
    if res := await delete_file_from_server(username, file_name):
        return web.Response(text=f'deleted {res}', status=200)
    return web.Response(text='file not found', status=404)

