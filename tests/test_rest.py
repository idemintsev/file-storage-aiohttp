from aiohttp import BasicAuth
import trafaret as t
from unittest.mock import mock_open


# negative cases
async def test_upload_file_unauthorized_user(rest_client):
    payload = {
        "file": b"anyfile",
    }

    res = await rest_client.post('/files', data=payload)
    assert res.status == 401


async def test_download_file_unauthorized_user(rest_client):
    res = await rest_client.get('/files/qwerty')
    assert res.status == 401


async def test_delete_file_unauthorized_user(rest_client):
    res = await rest_client.delete('/files/qwerty/')
    assert res.status == 401


# positive cases
async def test_upload_file_authorized_user(rest_client, mocker):
    mock_upload = mocker.patch(
        'file_storage_service.rest.handlers.upload_file_to_server',
        return_value='98fd8d7d7e551b6bc13d2bc67c08fd0e7b1aff1e8bb07ba0c82984aa5c39900e'
    )
    res = await rest_client.post('/files', auth=BasicAuth('user', 'password'), data={"file": b"anyfile"})
    res_trafaret = t.Atom('98fd8d7d7e551b6bc13d2bc67c08fd0e7b1aff1e8bb07ba0c82984aa5c39900e')

    assert mock_upload.call_count == 1
    assert res.status == 201
    res_trafaret.check(await res.text())


async def test_download_file_authorized_user(rest_client, mocker):
    mock_upload = mocker.patch(
        'file_storage_service.rest.handlers.find_file_on_server'
    )
    mocked_open = mocker.patch('file_storage_service.rest.handlers.open', mock_open(read_data=b"anyfile"))
    res = await rest_client.get('/files/file_hash', auth=BasicAuth('user', 'password'))
    res_trafaret = t.Bytes(b"anyfile")

    assert mock_upload.call_count == 1
    assert mocked_open.call_count == 1
    assert res.status == 200
    results = [data async for data in res.content.iter_chunked(1024)]
    res_trafaret.check(*results)
