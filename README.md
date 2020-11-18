# Audio bot
This bot indexes all audio that you send to it and make it searchable by text.

[![Build Status](https://travis-ci.org/meyer1994/jr-bot.svg?branch=dev)](https://travis-ci.org/meyer1994/jr-bot)
[![codecov](https://codecov.io/gh/meyer1994/jr-bot/branch/dev/graph/badge.svg)](https://codecov.io/gh/meyer1994/jr-bot)


## Commands

### `/ping`
Will make it answer "Pong!". Mostly used to check if the service is up when developing.

### Audio/voice
Every audio you send to this bot will trigger the recognition pipeline. You will receive some messages telling you which step of the pipeline we are currently at.

### `{TEXT}`
If you type any message that is not a command or audio/voice files, it will return the first matching result that is indexed.


## Development
We use Algolia to perform the text search. The bot is deployed on Heroku. To start developing:

```bash
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ pip install -r requirements-dev.txt
```

## Tests
To run the tests, simply execute:

```bash
$ python -m unittest discover -vb tests/
```
