from unittest import TestCase, mock

from tests.utils import resource

from pydub import AudioSegment

from audiobot.audio import Audio


class TestConverter(TestCase):
    def test_convert(self):
        """ Converts the passed file to mp3 """
        with resource('audio.mp3', 'rb') as file:
            audio = Audio(file)
            result = audio.convert()

        self.assertTrue(result.name.endswith('.mp3'))
        segment = AudioSegment.from_file(result.name)
        self.assertEqual(segment.frame_rate, 48_000)

    @mock.patch('requests.get')
    def test_download(self, mocked):
        """ Downloads a file from google bucket """
        fake_data = [b'1', b'2', b'3']
        mocked().iter_content.return_value = iter(fake_data)

        result = Audio.download('any url here')

        # Assert mocks were called
        mocked.assert_called_with('any url here')
        mocked().iter_content.assert_called()

        # Assert fake data was written to file
        result.temp.seek(0)
        data = result.temp.read()
        self.assertEqual(data, b'123')

    @mock.patch('google.cloud.storage.Client')
    def test_upload(self, mocked):
        """ Uploads to Google's storage bucket """
        with resource('audio.mp3', 'rb') as file:
            audio = Audio(file)
            audio.upload('nice')

        # Assert mocks were called
        mocked.assert_called()
        mocked().bucket.assert_called_with('bucket')
        mocked().bucket().blob.assert_called_with('nice')
        mocked().bucket().blob().upload_from_file.assert_called()

    @mock.patch('google.cloud.speech.SpeechClient')
    def test_recognize(self, mocked):
        """ Gets Google's recognition of audio """
        response = mock.Mock()
        response.results = []
        mocked().recognize.return_value = response

        result = Audio.recognize('uri')

        # No results because we forced to return no results
        self.assertListEqual(result, [])

        # Assert mocks were called
        mocked.assert_called()
        mocked().recognize.assert_called()
