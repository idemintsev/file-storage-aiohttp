import hashlib
import os
import aiofiles
from pathlib import Path
import shutil

from file_storage_service.settings import Config


async def upload_file_to_server(obj, username) -> str:
    hash_object = hashlib.new('sha256')
    try:
        async with aiofiles.tempfile.NamedTemporaryFile(
                'wb+', dir=Config.file_storage.upload_folder, delete=False
        ) as tmp_f:
            while True:
                if chunk := await obj.read_chunk(Config.chunk_size):
                    await tmp_f.write(chunk)
                    hash_object.update(chunk)
                else:
                    break
            filename = hash_object.hexdigest()
            path = Path.joinpath(Config.file_storage.upload_folder, filename[0:2])
            path.mkdir(parents=True, exist_ok=True)
            os.replace(tmp_f.name, f'{path}/{filename}.{username}')
        return filename
    except Exception as exc:
        return ''


async def reader_generator(path):
    async with aiofiles.open(path, 'rb') as f:
        while True:
            _data = await f.read(Config.chunk_size)
            if not _data:
                break
            yield _data


def find_file_on_server(file_name: str) -> str:
    path_to_file = Path.joinpath(Config.file_storage.upload_folder, file_name[0:2], file_name)
    if path_to_file.parent.is_dir():
        files = [f for f in path_to_file.parent.iterdir() if f.is_file()]
        if file := [f for f in files if f.name.startswith(file_name)]:
            return file[0]
        return ''


def delete_file_from_server(username: str, file_name: str) -> str:
    result = ''
    path_to_file = Path.joinpath(Config.file_storage.upload_folder, file_name[0:2], f'{file_name}.{username}')
    if path_to_file.is_file():
        try:
            files_quantity = sum(1 for f in path_to_file.parent.iterdir() if f.is_file())
            if files_quantity > 1:
                path_to_file.unlink(path_to_file)
            else:
                shutil.rmtree(path_to_file.parent)
            result = file_name
        except FileNotFoundError as exc:
            pass
    return result