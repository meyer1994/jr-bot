import io
from typing import IO

from google.cloud import speech


def _client() -> object:
    return speech.SpeechClient()


def recognize(uri: str) -> str:
    audio = speech.RecognitionAudio(uri=uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        sample_rate_hertz=48_000,
        language_code='en',
        model='default'
    )

    return _client().recognize(config, audio)
