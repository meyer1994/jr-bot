import io
from unittest import TestCase
from unittest.mock import patch, MagicMock

from audiobot.audio import Audio


class TestAudio(TestCase):
    def test_sha256(self):
        """ Calculates sha256 of data """
        data = io.BytesIO(b'nice')
        audio = Audio(data)

        sha256 = audio.sha256()

        # Value got using:
        #   $ echo -n 'nice' | sha256sum
        r = 'e186022d0931afe9fe0690857e32f85e50165e7fbe0966d49609ef1981f920c6'
        self.assertEqual(sha256, r)

    @patch('audiobot.audio.AudioSegment')
    def test_to_mp3(self, AudioSegment):
        """ Calls PyDub to convert audio to MP3 """
        data = io.BytesIO(b'data')
        audio = Audio(data)

        audio = audio.to_mp3()

        AudioSegment.from_file.assert_called_once_with(data, frame_rate=48_000)
        AudioSegment.from_file().export\
            .assert_called_once_with(audio.data, format='mp3')

    @patch('audiobot.audio.httpx.get')
    def test_from_url(self, get):
        """ Calls httpx to download data """
        Audio.from_url('url')

        get.assert_called_once_with('url')
        get().iter_bytes.assert_called_once_with()
