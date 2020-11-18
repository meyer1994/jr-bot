import io
from typing import IO

from google.cloud import speech


def transcribe(key: str) -> str:
    audio = speech.types.RecognitionAudio(uri=key)
    enums = speech.enums.RecognitionConfig.AudioEncoding

    config = speech.types.RecognitionConfig(
        encoding=enums.ENCODING_UNSPECIFIED,
        sample_rate_hertz=48_000,
        language_code='en',
        model='default'
    )

    client = speech.SpeechClient()
    return client.recognize(config, audio)
