import io
import hashlib
import logging
import functools
from typing import IO

import httpx
from pydub import AudioSegment

logger = logging.getLogger('Audio')
logger.setLevel(logging.INFO)


class Audio(object):
    def __init__(self, data: IO):
        super(Audio, self).__init__()
        self._data = data

    @property
    def data(self):
        self._data.seek(0)
        return self._data

    @staticmethod
    def from_url(url: str) -> 'Audio':
        logger.info('Loading from url: %s', url)
        data = io.BytesIO()
        response = httpx.get(url)
        for chunk in response.iter_bytes():
            data.write(chunk)
        logger.info('Loaded from url: %s', url)
        return Audio(data)

    def sha256(self) -> str:
        logger.info('Calculating sha256')
        sha256 = hashlib.new('sha256')
        reader = functools.partial(self.data.read, 1024)
        for chunk in iter(reader, b''):
            sha256.update(chunk)
        result = sha256.hexdigest()
        logger.info('Calculated sha256')
        return result

    def to_mp3(self) -> 'Audio':
        logger.info('Converting to mp3')
        segment = AudioSegment.from_file(self.data, frame_rate=48_000)
        data = io.BytesIO()
        segment.export(data, format='mp3')
        logger.info('Converted to mp3')
        return Audio(data)
