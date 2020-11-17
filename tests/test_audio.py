import io
from unittest import TestCase
from unittest.mock import patch, MagicMock

from audiobot import audio

class TestAudio(TestCase):
    @patch('audiobot.audio.httpx')
    def test_download(self, httpx):
        """ Downloads data to stream """
        response = MagicMock()
        response.iter_bytes.return_value = b'abc'.split()
        httpx.get.return_value = response

        url = 'https://example.org'
        data = audio.download(url)

        httpx.get.assert_called_once_with(url)
        response.iter_bytes.assert_called_once_with()

    def test_upload(self):
        """ Uploads data to GCP bucket """
        self.fail()

    def test_sha256(self):
        """ Calculates sha256 of data """
        data = io.BytesIO(b'nice')
        sha256 = audio.sha256(data)

        # Value got using:
        #   $ echo -n 'nice' | sha256sum
        r = 'e186022d0931afe9fe0690857e32f85e50165e7fbe0966d49609ef1981f920c6'
        self.assertEqual(sha256, r)
        self.assertEqual(data.tell(), 0)

    @patch('audiobot.audio.AudioSegment')
    def test_convert(self, AudioSegment):
        """ Calls MP3 converter """
        data = io.BytesIO(b'data')
        result = audio.convert(data)
        AudioSegment.from_file.assert_called_once_with(data, frame_rate=48_000)
        AudioSegment.from_file().export.assert_called_once()
        self.assertEqual(data.tell(), 0)
        self.assertEqual(result.tell(), 0)

    def test_index(self):
        self.fail()
