import os
import logging

from algoliasearch.search_client import SearchClient

ALGOLIA_USER = os.environ['ALGOLIA_USER']
ALGOLIA_TOKEN = os.environ['ALGOLIA_TOKEN']
ALGOLIA_INDEX = 'audio'

logger = logging.getLogger('Algolia')
logger.setLevel(logging.INFO)

client = SearchClient.create(ALGOLIA_USER, ALGOLIA_TOKEN)
index = client.init_index(ALGOLIA_INDEX)


def save(data):
    """ Saves itself to Algolia's index """
    logger.info('Saving')
    config = {'autoGenerateObjectIDIfNotExist': True}
    results = index.save_object(data, config)
    _id = results[0]['objectIDs'][0]
    logger.info('Saved %s', _id)
    return _id


def search(text):
    """ Searches Algolia's index. Returns objects """
    logger.info('Searching %s', text)
    options = {'attributesToHighlight': []}
    result = index.search(text, options)
    hits = result['hits']
    logger.info('Searched %d', len(hits))
    return hits


def get(item):
    """ Gets item by id """
    logger.info('Getting %s', item)
    result = index.get_object(item)
    logger.info('Got %s', item)
    return result
