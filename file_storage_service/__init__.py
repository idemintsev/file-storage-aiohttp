from aiohttp import web

from file_storage_service.rest.handlers import upload_file, download_file, delete_file
from file_storage_service.rest.middlewares import auth_middleware


async def asgi() -> 'web.Application':
    app = web.Application(
        middlewares=[auth_middleware]
    )

    app.add_routes([
        web.post('/files', upload_file),
        web.get('/files/{file_name}', download_file),
        web.delete('/files/{file_name}', delete_file),
    ])

    return app
