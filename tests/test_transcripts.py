from unittest import TestCase
from unittest.mock import patch, PropertyMock

from audiobot.transcripts import Transcripts


@patch('audiobot.transcripts.SearchClient')
class TestTranscripts(TestCase):
    def test_constructor(self, algolia):
        """ Creates an algolia client on constructor """
        Transcripts()
        # We do not use `with` here because the settings are taken from
        # environment and may change frequently
        algolia.create.assert_called_once()

    def test_index(self, algolia):
        """ Returns `audio` index """
        transcripts = Transcripts()
        transcripts.index
        algolia.create().init_index.assert_called_once_with('audios')

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
            'filters': 'user = user',
            'hitsPerPage': 1
        }
        index().search.assert_called_once_with('text', options)
