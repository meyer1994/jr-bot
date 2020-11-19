import logging

from google.cloud import speech

logger = logging.getLogger('speech')
logger.setLevel(logging.INFO)


def _client() -> object:
    return speech.SpeechClient()


def recognize(uri: str) -> str:
    logger.info('Recognizing: %s', uri)
    audio = speech.RecognitionAudio(uri=uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        sample_rate_hertz=48_000,
        language_code='en',
        model='default'
    )

    client = _client()
    result = client.recognize(config=config, audio=audio)
    logger.info('Recognized: %s', uri)
    return result
