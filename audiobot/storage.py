import io
from typing import IO

from google.cloud import storage

from audiobot import settings

GOOGLE = settings.Google()


def _blob(key: str) -> object:
    return storage.Client()\
        .bucket(GOOGLE.bucket)\
        .blob(key)


def download(key: str) -> IO:
    data = io.BytesIO()
    _blob(key).download_to_file(data)
    data.seek(0)
    return data


def upload(data: IO, key: str) -> str:
    data.seek(0)
    _blob(key).upload_from_file(data)
    data.seek(0)
    return f'gs://{GOOGLE.bucket}/{key}'


def exists(key: str) -> bool:
    return _blob(key).exists()
