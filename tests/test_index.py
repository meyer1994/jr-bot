from unittest import TestCase
from unittest.mock import patch

from audiobot import index


class TestIndex(TestCase):
    @patch('audiobot.index._index')
    def test_save(self, _index):
        """ Calls Algolia client to save entry """
        response = {'objectID': 'uri'}
        _index().save_object.return_value = response

        saved = index.save('uri', 'text')
        self.assertDictEqual(saved, response)

        payload = {'objectID': 'uri', 'text': 'text'}
        _index().save_object.assert_called_once_with(payload)

    @patch('audiobot.index._index')
    def test_search(self, _index):
        """ Calls Algolia client to search for entry """
        response = {'hits': [{'objectID': 'uri', 'text': 'text'}]}
        _index().search.return_value = response

        searched = index.search('text')
        self.assertDictEqual(searched, response)
