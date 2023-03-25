import pytest

from file_storage_service import asgi
from file_storage_service.settings import Config

Config.mode = 'test'


@pytest.fixture
async def rest_client(aiohttp_client):
    app = await asgi()
    return await aiohttp_client(app)


unexpected_params = (
    (
        {"query": {"user_id": ["user_id_num"]}, "extra_param": "extra_data"},
        "got an unexpected keyword argument 'extra_param'"
    ),
    (
        {"qVery": {"user_id": ["user_id_num"]}},
        "got an unexpected keyword argument 'qVery'"
    )
)


@pytest.fixture(params=unexpected_params)
def unexpected_params_query_create_fixture(request):
    yield request.param
