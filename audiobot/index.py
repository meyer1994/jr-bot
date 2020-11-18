from algoliasearch.search_client import SearchClient

from audiobot import settings

ALGOLIA = settings.Algolia()


def _index() -> object:
    client = SearchClient.create(ALGOLIA.user, ALGOLIA.token)
    return client.init_index(ALGOLIA.index)


def save(uri: str, text: str) -> str:
    index = _index()
    data = {'objectID': uri, 'text': text}
    return index.save_object(data)


def search(text: str) -> object:
    index = _index()
    htis = index.search(text)
    return htis['hits']
