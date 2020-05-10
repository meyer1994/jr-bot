from unittest import TestCase
from unittest.mock import patch, PropertyMock

from audiobot.users import Users


@patch('audiobot.users.firestore')
class TestUsers(TestCase):
    def test_constructor(self, firestore):
        """ Creates a firestore client on constructor """
        Users()
        firestore.Client.assert_called_once_with()  # Empty

    def test_collection(self, firestore):
        """ Returns `users` collection """
        users = Users()
        users.collection
        firestore.Client().collection.assert_called_once_with('users')

    @patch.object(Users, 'collection', new_callable=PropertyMock)
    def test_get(self, collection, firestore):
        """ Fetches an user from firestore """
        users = Users()
        users.get('user')
        collection().document.assert_called_once_with('user')
        collection().document().get.assert_called_once_with()
        collection().document().get().to_dict.assert_called_once_with()

    @patch.object(Users, 'collection', new_callable=PropertyMock)
    def test_set(self, collection, firestore):
        """ Saves an user to firestore """
        users = Users()
        data = {'nice': 'data'}
        users.set('user', data)
        collection.assert_called_once_with()
        collection().document.assert_called_once_with('user')
        collection().document().set.assert_called_once_with(data)
