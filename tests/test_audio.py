from unittest import TestCase, mock
from unittest.mock import patch, PropertyMock

from tests.utils import resource

from pydub import AudioSegment

from audiobot.audio import Audio


@patch('audiobot.audio.storage')
class TestAudio(TestCase):
    def test_constructor(self, storage):
        """ Creates a storage client on constructor """
        Audio(None)
        storage.Client.assert_called_once()

    def test_bucket(self, storage):
        """ Returns `audios` bucket """
        audio = Audio(None)
        audio.bucket
        storage.Client().bucket.assert_called_once_with('audiosbucket')

    def test_convert(self, storage):
        """ Converts the passed file to mp3 """
        with resource('audio.mp3', 'rb') as file:
            audio = Audio(file)
            result = audio.convert()

        self.assertTrue(result.name.endswith('.mp3'))
        segment = AudioSegment.from_file(result.name)
        self.assertEqual(segment.frame_rate, 48_000)

    @patch('requests.get')
    def test_download(self, response, storage):
        """ Downloads a file from telegram """
        fake_data = [b'1', b'2', b'3']
        response().iter_content.return_value = iter(fake_data)

        result = Audio.download('any url here')

        # Assert mocks were called
        response.assert_called_with('any url here')
        response().iter_content.assert_called_once()

        # Assert fake data was written to file
        result.temp.seek(0)
        data = result.temp.read()
        self.assertEqual(data, b'123')

    @patch.object(Audio, 'bucket', new_callable=PropertyMock)
    def test_upload(self, bucket, storage):
        """ Uploads to Google's storage bucket """
        bucket().name = 'audiosbucket'

        with resource('audio.mp3', 'rb') as file:
            audio = Audio(file)
            uri = audio.upload()

        self.assertTrue(uri.startswith('gs://audiosbucket'))

        # Assert mocks were called
        bucket().blob.assert_called_once()
        bucket().blob().upload_from_file.assert_called_once()

    @mock.patch('audiobot.audio.speech')
    def test_recognize(self, speech, storage):
        """ Gets Google's recognition of audio """
        response = mock.Mock()
        response.results = []
        speech().recognize.return_value = response

        result = Audio.recognize('uri')

        # No results because we forced to return no results
        self.assertListEqual(result, [])

        speech.SpeechClient.assert_called_once_with()
        speech.SpeechClient().recognize.assert_called_once()
