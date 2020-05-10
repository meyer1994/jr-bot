import telebot

from audiobot.users import Users
from audiobot.controller import Controller
from audiobot.transcripts import Transcripts
from audiobot.settings import TelegramSettings

settings = TelegramSettings()

bot = telebot.AsyncTeleBot(settings.token)
transcripts = Transcripts()
users = Users()

controller = Controller(bot, transcripts, users)


def register(function, **kwargs):
    """ Utility to register handlers to bot """
    handler = {'function': function, 'filters': kwargs}
    return bot.add_message_handler(handler)


register(controller.ping, commands=['ping'])
register(controller.start, commands=['start'])
register(controller.me, commands=['me'])
register(controller.config, commands=['config'])
register(controller.voice, content_types=['voice'])
register(controller.audio, content_types=['audio'])
register(controller.search, func=lambda m: True)


if __name__ == '__main__':
    bot.polling(none_stop=True)
