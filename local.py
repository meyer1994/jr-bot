import os
import logging

import telebot

import audiobot

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Handler')
logger.setLevel(logging.INFO)

bot = telebot.AsyncTeleBot(TELEGRAM_TOKEN)
telebot.logger.setLevel(logging.INFO)


@bot.message_handler(commands=['ping'])
def ping(message):
    """ Simply answers this command with 'Pong!' """
    logger.info('Handling /ping')
    chat = message.chat.id
    bot.send_message(chat, 'Pong!')
    logger.info('Handled /ping')


@bot.message_handler(content_types=['voice'])
def voice(message):
    """
    Receives the voice/audio messages from Telegram and uploads it to our
    indexing bucket
    """
    logger.info('Handling %s', message.content_type)
    if message.content_type == 'audio':
        file = message.audio.file_id
    else:
        file = message.voice.file_id

    # Process
    url = bot.get_file_url(file)
    temp = audiobot.audio.download(url)
    temp = audiobot.audio.convert(temp)
    uri = audiobot.audio.upload(temp, file)
    results = audiobot.audio.recognize(uri)

    # Index
    result = results[0]
    data = {
        'file': file,
        'text': result.transcript,
        'type': message.content_type,
        'confidence': result.confidence
    }
    response = audiobot.algolia.save(data)

    # Reply
    chat = message.chat.id
    bot.send_message(chat, f"Indexed: {response}")
    logger.info('Handled %s', message.content_type)


@bot.message_handler(commands=['search'])
def search(message):
    """ Searches our database """
    logger.info('Handling /search')

    text = message.text[7:].strip()  # Remove `/search`
    hits = audiobot.algolia.search(text)

    # No results
    if len(hits) < 1:
        chat = message.chat.id
        bot.send_message(chat, 'No results :(')
        logger.info('Handled /search')
        return

    # Results
    file = hits[0]['file']
    chat = message.chat.id
    logger.info('Sending: %s', file)
    bot.send_voice(chat, file)
    logger.info('Sent: %s', file)

    logger.info('Handled /search')


if __name__ == '__main__':
    bot.polling(none_stop=True)
