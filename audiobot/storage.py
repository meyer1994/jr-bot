import io
from typing import IO

import httpx
from google.cloud import storage

from audiobot import settings

GOOGLE = settings.Google()


def download(key: str) -> IO:
    data = io.BytesIO()
    storage.Client()\
        .bucket(GOOGLE.bucket)\
        .blob(key)\
        .download_to_file(data)
    data.seek(0)
    return data


def upload(data: IO, key: str) -> str:
    data.seek(0)
    storage.Client()\
        .bucket(GOOGLE.bucket)\
        .blob(key)\
        .upload_from_file(data)
    data.seek(0)
    return f'gs://{GOOGLE.bucket}/{key}'


def exists(key: str) -> bool:
    return storage.Client()\
        .bucket(GOOGLE.bucket)\
        .blob(key)\
        .exists()
