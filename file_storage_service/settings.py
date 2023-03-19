import os
from pathlib import Path

from attrs import frozen

Bytes = int
TWO_Mb = 2 * 1024 * 1024


@frozen
class FileStorageConfig:
    """Config for server's file storage."""
    basedir: Path = Path(__file__).absolute().parent
    store_folder_name: str = os.getenv('STORE_FOLDER_NAME', 'store')

    @property
    def upload_folder(self) -> Path:
        return Path.joinpath(self.basedir.parent, self.store_folder_name)


@frozen
class AppConfig:
    """Global app config."""
    host: str = os.getenv('APP_HOST', 'localhost')
    port: int = int(os.getenv('APP_PORT', 8000))
    file_storage: FileStorageConfig = FileStorageConfig()
    chunk_size: Bytes = int(os.getenv('CHUNK_SIZE', TWO_Mb))
    log_level: str = os.getenv('APP_LOG_LEVEL', 'ERROR').upper()


# Initialising VAD config with starting parameters
Config = AppConfig()
