import pytest

from file_storage_service import asgi


@pytest.fixture
async def rest_client(aiohttp_client):
    app = await asgi()
    return await aiohttp_client(app)
