import io
from unittest import TestCase
from unittest.mock import patch, MagicMock

from audiobot import storage


class TestStorage(TestCase):
    @patch('audiobot.storage._blob')
    def test_download(self, _blob):
        """ Calls GCP client to download blob """
        data = storage.download('key')

        _blob.assert_called_once_with('key')
        _blob().download_to_file.assert_called_once()

    @patch('audiobot.storage._blob')
    def test_upload(self, _blob):
        """ Calls GCP client to upload blob """
        data = io.BytesIO(b'data')

        uri = storage.upload(data, 'key')

        self.assertEqual(uri, 'gs://bucket/key')

        _blob.assert_called_once_with('key')
        _blob().upload_from_file.assert_called_once_with(data)

    @patch('audiobot.storage._blob')
    def test_exists(self, _blob):
        """ Calls GCP client to check if blob exists """
        storage.exists('key')

        _blob.assert_called_once_with('key')
        _blob().exists.assert_called_once_with()
