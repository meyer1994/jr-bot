import copy

from algoliasearch.search_client import SearchClient

from audiobot.settings import AlgoliaSettings


class Transcripts(object):
    INDEX = 'audios'

    def __init__(self):
        super(Transcripts, self).__init__()
        settings = AlgoliaSettings()
        self.client = SearchClient.create(settings.user, settings.token)

    @property
    def index(self):
        return self.client.init_index(self.INDEX)

    def save(self, user: str, data: dict):
        data = copy.deepcopy(data)
        data['user'] = user
        config = {'autoGenerateObjectIDIfNotExist': True}
        return self.index.save_object(data, config)

    def search(self, user: str, text: str):
        options = {
            'attributesToHighlight': [],
            'filters': f'user = {user}',
            'hitsPerPage': 1
        }
        return self.index.search(text, options)
