import logging

from google.cloud import firestore


class Users(object):
    COLLECTION = 'users'

    logger = logging.getLogger('Users')

    def __init__(self):
        super(Users, self).__init__()
        self.client = firestore.Client()

    @property
    def collection(self: str):
        """ Returns `users` collection """
        return self.client.collection(self.COLLECTION)

    def get(self, user: str):
        """ Gets user data """
        document = self.collection.document(user)
        snapshot = document.get()
        return snapshot.to_dict()

    def set(self, user: str, data: dict):
        """ Sets user data """
        document = self.collection.document(user)
        return document.set(data)
