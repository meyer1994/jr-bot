import logging

from audiobot.bot import bot

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    bot.polling(none_stop=True)
