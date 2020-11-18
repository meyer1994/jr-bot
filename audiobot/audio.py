import io
import hashlib
import functools
from typing import IO

import httpx
from pydub import AudioSegment


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
        data = io.BytesIO()
        response = httpx.get(url)
        for chunk in response.iter_bytes():
            data.write(chunk)
        return Audio(data)

    def sha256(self) -> str:
        sha256 = hashlib.new('sha256')
        reader = functools.partial(self.data.read, 1024)
        for chunk in iter(reader, b''):
            sha256.update(chunk)
        return sha256.hexdigest()

    def to_mp3(self) -> 'Audio':
        segment = AudioSegment.from_file(self.data, frame_rate=48_000)
        data = io.BytesIO()
        segment.export(data, format='mp3')
        return Audio(data)
