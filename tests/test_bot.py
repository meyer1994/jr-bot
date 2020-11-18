import io
from unittest import TestCase
from unittest.mock import patch, MagicMock

from audiobot import bot as audiobot


class TestBot(TestCase):
    @patch('audiobot.bot.bot')
    def test_ping(self, bot):
        """ Sends a 'pong' response """
        message = MagicMock()
        message.chat.id = 'chat'

        audiobot.ping(message)

        bot.send_message.assert_called_once_with('chat', 'pong')

    @patch('audiobot.bot.index')
    @patch('audiobot.bot.storage')
    @patch('audiobot.bot.speech')
    @patch('audiobot.bot.Audio')
    @patch('audiobot.bot.bot')
    def test_voice(self, bot, Audio, speech, storage, index):
        """ Processes an audio message """
        message = MagicMock()
        message.chat.id = 'chat'
        message.voice.file_id = 'file'

        audiobot.voice(message)

        bot.get_file_url.assert_called_once_with('file')
        self.assertEqual(bot.send_message.call_count, 2)

        Audio.from_url.assert_called_once()
        Audio.from_url().to_mp3.assert_called_once_with()
        Audio.from_url().to_mp3().sha256.assert_called_once_with()

        storage.upload.assert_called_once()

        speech.recognize.assert_called_once()

        index.save.assert_called_once()

    @patch('audiobot.bot.voice')
    def test_audio(self, voice):
        """ Calls the voice method """
        message = MagicMock()

        audiobot.audio(message)

        voice.assert_called_once_with(message)

    @patch('audiobot.bot.index')
    def test_search(self, index):
        """ Searches the index """
        message = MagicMock()
        message.text = 'text'

        audiobot.search(message)

        index.search.assert_called_once_with('text')
