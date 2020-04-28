import os
import logging

import telebot
from google.cloud import firestore
from algoliasearch.search_client import SearchClient

from audiobot.controller import Controller

ALGOLIA_INDEX = 'audio'
ALGOLIA_TOKEN = os.environ['ALGOLIA_TOKEN']
ALGOLIA_USER = os.environ['ALGOLIA_USER']
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']


bot = telebot.AsyncTeleBot(TELEGRAM_TOKEN)
fireclient = firestore.Client()
algoclient = SearchClient.create(ALGOLIA_USER, ALGOLIA_TOKEN)

controller = Controller(bot, algoclient, fireclient)


def register(function, **kwargs):
    handler = {'function': function, 'filters': kwargs}
    return bot.add_message_handler(handler)


register(controller.ping, commands=['ping'])
register(controller.start, commands=['start'])
register(controller.voice, content_types=['voice'])
register(controller.audio, content_types=['audio'])
register(controller.search, func=lambda m: True)










# @bot.message_handler(commands=['ping'])
# def ping(bot, message):
#     """ Simply answers this command with 'Pong!' """
#     logger.info('Handling /ping')
#     chat = message.chat.id
#     bot.send_message(chat, 'Pong!')
#     logger.info('Handled /ping')


# register(ping, commands=['ping'])

# @bot.message_handler(commands=['start'])
# def start(message):
#     logger.info('Handling /start')
#     user = str(message.from_user.id)
#     audiobot.firestore.register(user)
#     logger.info('Handled /start')


# @bot.message_handler(content_types=['voice', 'audio'])
# def voice(message):
#     """
#     Receives the voice/audio messages from Telegram and uploads it to our
#     indexing bucket
#     """
#     logger.info('Handling %s', message.content_type)
#     if message.content_type == 'audio':
#         file = message.audio.file_id
#     else:
#         file = message.voice.file_id

#     # Process
#     url = bot.get_file_url(file)
#     temp = audiobot.audio.download(url)
#     temp = audiobot.audio.convert(temp)
#     uri = audiobot.audio.upload(temp, file)
#     results = audiobot.audio.recognize(uri)

#     # Index
#     result = results[0]
#     data = {
#         'file': file,
#         'text': result.transcript,
#         'type': message.content_type,
#         'confidence': result.confidence
#     }
#     response = audiobot.algolia.save(data)

#     # Reply
#     chat = message.chat.id
#     bot.send_message(chat, f"Indexed: {response}")
#     logger.info('Handled %s', message.content_type)


# @bot.message_handler(commands=['search'])
# def search(message):
#     """ Searches our database """
#     logger.info('Handling /search')

#     text = message.text[7:].strip()  # Remove `/search`
#     hits = audiobot.algolia.search(text)

#     # No results
#     if len(hits) < 1:
#         chat = message.chat.id
#         bot.send_message(chat, 'No results :(')
#         logger.info('Handled /search')
#         return

#     # Results
#     hit = hits[0]
#     file = hit['file']
#     chat = message.chat.id
#     logger.info('Sending %s: %s', hit['type'], file)
#     if hit['type'] == 'audio':
#         bot.send_audio(chat, file)
#     else:
#         bot.send_voice(chat, file)
#     logger.info('Sent: %s', file)

#     logger.info('Handled /search')


# @bot.message_handler(commands=['get'])
# def get(message):
#     logger.info('Handling /get')
#     item = message.text[4:].strip()
#     item = audiobot.algolia.get(item)

#     chat = message.chat.id
#     if item['type'] == 'audio':
#         bot.send_audio(chat, item['file'])
#     else:
#         bot.send_voice(chat, item['file'])

#     logger.info('Handled /get')


if __name__ == '__main__':
    bot.polling(none_stop=True)
