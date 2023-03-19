from aiohttp import web

from file_storage_service.rest.handlers import upload_file, download_file, delete_file


async def asgi() -> 'web.Application':
    app = web.Application()

    app.add_routes([
        web.post('/files', upload_file),
        web.get('/files/{file_name}', download_file),
        web.delete('/files/{file_name}', delete_file),
    ])

    return app
