from unittest import TestCase
from unittest.mock import patch, PropertyMock

from audiobot.transcripts import Transcripts


@patch('audiobot.transcripts.SearchClient')
class TestTranscripts(TestCase):

    @patch('audiobot.transcripts.AlgoliaSettings')
    def test_constructor(self, settings, algolia):
        """ Creates an algolia client on constructor """
        settings().user = 'user'
        settings().token = 'token'

        Transcripts()
        algolia.create.assert_called_once_with('user', 'token')

    def test_index(self, algolia):
        """ Returns `audio` index """
        transcripts = Transcripts()
        transcripts.index
        algolia.create().init_index.assert_called_with(Transcripts.INDEX)

    @patch.object(Transcripts, 'index', new_callable=PropertyMock)
    def test_save(self, index, algolia):
        """ Saves an item to the index """
        transcripts = Transcripts()
        data = {'some': 'data'}
        transcripts.save('user', data)
        data = {'user': 'user', 'some': 'data'}
        config = {'autoGenerateObjectIDIfNotExist': True}
        index().save_object.assert_called_once_with(data, config)

    @patch.object(Transcripts, 'index', new_callable=PropertyMock)
    def test_search(self, index, algolia):
        """ Searches an item in the index """
        transcripts = Transcripts()
        transcripts.search('user', 'text')
        options = {
            'attributesToHighlight': [],
            'facets': ['user'],
            'filters': 'user:user',
            'hitsPerPage': 1,
        }
        index().search.assert_called_once_with('text', options)
