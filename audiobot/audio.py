import os
import logging
import tempfile
import itertools

import requests
from pydub import AudioSegment
from google.cloud import speech
from google.cloud import storage


GOOGLE_STORAGE_BUCKET = os.environ['GOOGLE_STORAGE_BUCKET']

client = storage.Client()
bucket = client.bucket(GOOGLE_STORAGE_BUCKET)

logger = logging.getLogger('Audio')
logger.setLevel(logging.INFO)


def download(url):
    """ Downloads file from url using requests """
    logger.info('Downloading %s', url)
    req = requests.get(url)
    temp = tempfile.NamedTemporaryFile()
    for data in req.iter_content(chunk_size=1024):
        temp.write(data)
    temp.flush()
    temp.seek(0)
    logger.info('Downloaded %s', url)
    return temp


def upload(file, key):
    """ Uploads file to bucket with the passed key """
    logger.info('Uploading %s', key)
    file.seek(0)
    file.flush()
    blob = bucket.blob(key)
    blob.upload_from_file(file)
    logger.info('Uploaded %s', key)
    return f'gs://{GOOGLE_STORAGE_BUCKET}/{key}'


def convert(file):
    """ Converts file to .mp3 returning a temporary file """
    logger.info('Converting %s', file.name)
    audio = AudioSegment.from_file(file.name)
    temp = tempfile.NamedTemporaryFile(suffix='.mp3')
    audio.export(temp.name, format='mp3', bitrate='48K')
    logger.info('Converted %s', file.name)
    return temp


def recognize(uri, language='en-US'):
    """ Extract text from audio using Google """
    logger.info('Recognizing %s', uri)
    client = speech.SpeechClient()
    audio = speech.types.RecognitionAudio(uri=uri)

    enums = speech.enums.RecognitionConfig.AudioEncoding
    config = speech.types.RecognitionConfig(
        encoding=enums.ENCODING_UNSPECIFIED,
        sample_rate_hertz=48_000,
        language_code=language,
        model='default'
    )

    response = client.recognize(config, audio)

    results = (r.alternatives for r in response.results)
    results = itertools.chain(*results)
    result = sorted(results, key=lambda a: a.confidence, reverse=True)

    logger.info('Recognized %s', uri)
    return result
