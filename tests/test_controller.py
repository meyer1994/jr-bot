from unittest import TestCase
from unittest.mock import Mock, patch, PropertyMock, ANY

from audiobot.controller import Controller


class TestControoler(TestCase):
    def setUp(self):
        """ Sets up all the mocks for tests """
        self.bot = Mock()
        self.users = Mock()
        self.transcripts = Mock()

    def test_ping(self):
        """ Bot replies 'Pong!' """
        message = Mock()
        message.chat.id = 'id'

        controller = Controller(self.bot, self.transcripts, self.users)
        controller.ping(message)

        self.bot.send_message.assert_called_with('id', 'Pong!')

    def test_start(self):
        """ Registers new user """
        message = Mock()
        message.from_user.id = 'id'

        controller = Controller(self.bot, self.transcripts, self.users)
        controller.start(message)

        self.users.set.assert_called_once_with('id', ANY)

    def test_me(self):
        """ Fetches configuration from DB """
        message = Mock()
        message.chat.id = 'chat'
        message.from_user.id = 'user'

        self.users.get.return_value = {'nice': 'data'}

        controller = Controller(self.bot, self.transcripts, self.users)
        controller.me(message)

        self.users.get.assert_called_once_with('user')
        self.bot.send_message.assert_called_once_with('chat', 'Nice: data')

    @patch.object(Controller, 'voice')
    def test_audio(self, voice):
        """ Calls voice handler """
        message = Mock()

        controller = Controller(self.bot, self.transcripts, self.users)
        controller.audio(message)

        voice.assert_called_once_with(message)

    @patch('audiobot.controller.Audio')
    def test_voice(self, audio):
        """ Downloads, converts, uploads, recognizes and index audio """
        result = Mock()
        download = Mock()
        download.upload.return_value = 'any uri'
        audio.download.return_value = download
        audio.recognize.return_value = [result]

        self.users.get.return_value = {'language': 'pt-BR'}
        self.bot.get_file_url.return_value = 'any url'

        message = Mock()
        message.chat.id = 'chat'
        message.from_user.id = 'user'
        message.voice.file_id = 'file'

        controller = Controller(self.bot, self.transcripts, self.users)
        controller.voice(message)

        self.users.get.assert_called_once_with('user')
        self.bot.get_file_url.assert_called_once_with('file')
        audio.download.assert_called_once_with('any url')
        download.convert.assert_called_once_with(fmt='mp3')
        download.upload.assert_called_once_with()
        audio.recognize.assert_called_once_with('any uri', 'pt-BR')
        self.transcripts.save.assert_called_once_with('user', ANY)
        self.bot.reply_to(message, ANY)

    def test_search_no_results(self):
        """ Searches for audios in our index (no results) """
        self.transcripts.search.return_value = {'nbHits': 0}

        message = Mock()
        message.text = 'text'
        message.chat.id = 'chat'
        message.from_user.id = 'user'

        controller = Controller(self.bot, self.transcripts, self.users)
        controller.search(message)

        self.transcripts.search.assert_called_once_with('user', 'text')
        self.bot.send_message.assert_called_once_with('chat', 'No results :(')

    def test_search_with_audio_result(self):
        """ Searches for audios in our index (with audio results) """
        data = {
            'nbHits': 2,
            'hits': [{'file': 'file1', 'type': 'audio'}]
        }
        self.transcripts.search.return_value = data

        message = Mock()
        message.text = 'text'
        message.chat.id = 'chat'
        message.from_user.id = 'user'

        controller = Controller(self.bot, self.transcripts, self.users)
        controller.search(message)

        self.transcripts.search.assert_called_once_with('user', 'text')
        self.bot.send_audio.assert_called_once_with('chat', 'file1')

    def test_search_with_voice_result(self):
        """ Searches for audios in our index (with voice results) """
        data = {
            'nbHits': 2,
            'hits': [{'file': 'file1', 'type': 'voice'}]
        }
        self.transcripts.search.return_value = data

        message = Mock()
        message.text = 'text'
        message.chat.id = 'chat'
        message.from_user.id = 'user'

        controller = Controller(self.bot, self.transcripts, self.users)
        controller.search(message)

        self.transcripts.search.assert_called_once_with('user', 'text')
        self.bot.send_voice.assert_called_once_with('chat', 'file1')
