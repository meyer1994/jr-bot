from unittest import TestCase

from tests.utils import resource

from pydub import AudioSegment

from audiobot import audio


class TestConverter(TestCase):
    def test_convert_to_mp3(self):
        """ Converts the passed file to mp3 """
        with resource('audio.mp3', 'rb') as file:
            result = audio.convert(file)
            self.assertTrue(result.name.endswith('.mp3'))

    def test_convert_to_48k(self):
        """ Converts the passed file to mp3 with 48k bitrate """
        with resource('audio.mp3', 'rb') as file:
            result = audio.convert(file)
            segment = AudioSegment.from_file(result.name)
            self.assertEqual(segment.frame_rate, 48_000)
