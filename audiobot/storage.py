import io
import logging
from typing import IO

from google.cloud import storage

from audiobot import settings

GOOGLE = settings.Google()

logger = logging.getLogger('storage')
logger.setLevel(logging.INFO)


def _blob(key: str) -> object:
    return storage.Client()\
        .bucket(GOOGLE.bucket)\
        .blob(key)


def download(key: str) -> IO:
    logger.info('Downloading: %s', key)
    data = io.BytesIO()
    _blob(key).download_to_file(data)
    data.seek(0)
    logger.info('Downloaded: %s', key)
    return data


def upload(data: IO, key: str) -> str:
    logger.info('Uploading: %s', key)
    data.seek(0)
    _blob(key).upload_from_file(data)
    data.seek(0)
    logger.info('Uploaded: %s', key)
    return f'gs://{GOOGLE.bucket}/{key}'


def exists(key: str) -> bool:
    logger.info('Checking for: %s', key)
    result = _blob(key).exists()
    logger.info('Checking for: %s', key)
    return result
