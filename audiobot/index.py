from algoliasearch.search_client import SearchClient

from audiobot import settings

ALGOLIA = settings.Algolia()


def index(uri: str, text: str) -> str:
    client = SearchClient.create(ALGOLIA.user, ALGOLIA.token)
    index = client.init_index(ALGOLIA.index)

    data = {'objectID': key, 'text': transcription}
    result = index.save_object(data, config)

    return uri


def search(text: str) -> object:
    client = SearchClient.create(ALGOLIA.user, ALGOLIA.token)
    index = client.init_index(ALGOLIA.index)

    config = {'hitPerPage': 1}
    search = index.search(text, config)

    return search
