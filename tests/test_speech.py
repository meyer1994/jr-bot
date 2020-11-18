import io
from unittest import TestCase
from unittest.mock import patch, MagicMock

from audiobot import speech


class TestSpeech(TestCase):
    @patch('audiobot.speech._client')
    def test_transcribe(self, _client):
        """ Calls GCP client to recognize audio """
        speech.recognize('uri')

        _client.assert_called_once_with()
        _client().recognize.assert_called_once()
