from base64 import b64decode
from typing import Callable

from aiohttp.web import middleware, Response, Request

from file_storage_service.rest.auth import check_user


@middleware
async def auth_middleware(request: Request, handler: Callable) -> Response:
    if str(request.rel_url).startswith('/api/doc'):
        return await handler(request)

    if credentials := request.headers.get('Authorization', ''):
        username, password = b64decode(credentials.split(' ')[-1]).decode('utf-8').split(':')
        if await check_user(username, password):
            request.username = username
            return await handler(request)
    return Response(text='Unauthorized', status=401)
