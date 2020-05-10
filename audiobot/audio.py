import uuid
import logging
import tempfile
import itertools

import requests
from pydub import AudioSegment
from google.cloud import speech
from google.cloud import storage

from audiobot.settings import GoogleSettings


settings = GoogleSettings()


class Audio(object):
    BUCKET = 'audiosbucket'

    logger = logging.getLogger('Audio')

    def __init__(self, temp):
        super(Audio, self).__init__()
        self.temp = temp
        self._storage = storage.Client()

    @property
    def bucket(self):
        return self._storage.bucket(self.BUCKET)

    @staticmethod
    def download(url):
        response = requests.get(url)
        temp = tempfile.NamedTemporaryFile()
        for data in response.iter_content(chunk_size=1024):
            temp.write(data)
        temp.flush()
        temp.seek(0)
        return Audio(temp)

    def convert(self, fmt='mp3', bitrate='48K'):
        audio = AudioSegment.from_file(self.temp.name)
        temp = tempfile.NamedTemporaryFile(suffix=f'.{fmt}')
        audio.export(temp.name, format=fmt, bitrate=bitrate)
        self.temp = temp
        return self.temp

    def upload(self):
        self.temp.flush()
        self.temp.seek(0)
        key = str(uuid.uuid4())
        blob = self.bucket.blob(key)
        blob.upload_from_file(self.temp)
        return f'gs://{self.bucket.name}/{key}'

    @staticmethod
    def recognize(uri, language='pt-BR', hertz=48_000):
        client = speech.SpeechClient()
        audio = speech.types.RecognitionAudio(uri=uri)

        enums = speech.enums.RecognitionConfig.AudioEncoding
        config = speech.types.RecognitionConfig(
            encoding=enums.ENCODING_UNSPECIFIED,
            sample_rate_hertz=hertz,
            language_code=language,
            model='default'
        )

        response = client.recognize(config, audio)
        results = (r.alternatives for r in response.results)
        results = itertools.chain(*results)
        return sorted(results, key=lambda a: a.confidence, reverse=True)
