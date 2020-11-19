import logging

from algoliasearch.search_client import SearchClient

from audiobot import settings

ALGOLIA = settings.Algolia()

logger = logging.getLogger('index')
logger.setLevel(logging.INFO)


def _index() -> object:
    client = SearchClient.create(ALGOLIA.app, ALGOLIA.token)
    return client.init_index(ALGOLIA.index)


def save(uri: str, text: str) -> str:
    logger.info('Saving: %s', uri)
    index = _index()
    data = {'objectID': uri, 'text': text}
    result = index.save_object(data)
    logger.info('Saved: %s', uri)
    return result


def search(text: str) -> object:
    logger.info('Searching: %s', text)
    index = _index()
    hits = index.search(text)
    logger.info('Searched: %s', text)
    return hits
