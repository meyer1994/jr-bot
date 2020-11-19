import logging
import itertools

from google.cloud import speech

logger = logging.getLogger('speech')
logger.setLevel(logging.INFO)


def _client() -> object:
    return speech.SpeechClient()


def _pick_best(response: object) -> str:
    alternatives = (r.alternatives for r in response.results)
    alternatives = itertools.chain(*alternatives)
    alternatives = sorted(alternatives, key=lambda a: a.confidence)
    return alternatives[-1].transcript if len(alternatives) > 0 else ''


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
    response = client.recognize(config=config, audio=audio)
    logger.info('Recognized: %s', uri)
    return _pick_best(response)
