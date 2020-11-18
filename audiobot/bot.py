import io
import logging

import httpx
import telebot

from audiobot import storage, speech, index, settings
from audiobot.audio import Audio

logger = logging.getLogger('bot')
logger.setLevel(logging.INFO)

telegram = settings.Telegram()
bot = telebot.AsyncTeleBot(telegram.token)


@bot.message_handler(commands=['ping'])
def ping(message):
    logger.info('Start ping')
    bot.send_message(message.chat.id, 'pong')
    logger.info('End ping')


@bot.message_handler(content_types=['voice'])
def voice(message):
    logger.info('Start voice')
    url = bot.get_file_url(message.voice.file_id)

    audio = Audio.from_url(url)
    audio = audio.convert()
    sha256 = audio.sha256()

    uri = storage.upload(data, sha256)
    text = speech.transcribe(uri)

    saved = index.save(uri, text)

    bot.send_message(message.chat.id, sha256)
    bot.send_message(message.chat.id, text)
    logger.info('End voice')


@bot.message_handler(content_types=['audio'])
def audio(message):
    logger.info('Start audio')
    message.voice = message.audio
    voice(messsage)
    logger.info('End audio')


@bot.message_handler(func=lambda m: True)
def search(message):
    logger.info('Start search')
    result = index.search(message.text)
    print(result)
    logger.info('End search')

