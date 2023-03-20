from pathlib import Path

from file_storage_service.settings import Config


paths_to_swagger_docs = {
    'upload': str(Path.joinpath(Config.swagger.path_to_docs, 'upload.yaml')),
    'download': str(Path.joinpath(Config.swagger.path_to_docs, 'download.yaml')),
    'delete': str(Path.joinpath(Config.swagger.path_to_docs, 'delete.yaml'))
}
