# Audio bot
This bot indexes all audio that you send to it and make it searchable by text.

[![Build Status](https://travis-ci.org/meyer1994/jr-bot.svg?branch=dev)](https://travis-ci.org/meyer1994/jr-bot)
[![codecov](https://codecov.io/gh/meyer1994/jr-bot/branch/master/graph/badge.svg)](https://codecov.io/gh/meyer1994/jr-bot)


## Commands

### `/ping`
Will make it answer "Pong!". Mostly used to check if the service is up when developing.

## `/start`
Will create an entry to our database containing user configuration. It is automatically called by telegram when first interacting with the bot. Currently, the only information stored is the language. Defaults to `pt-BR`.

### `/me`
Will return the stored user configuration.

### Audio/voice
Every audio you send to this bot will trigger the recognition pipeline. You will receive some messages telling you which step of the pipeline we are currently at.

### `{TEXT}`
If you type any message that is not a command or audio/voice files, it will return the first matching result that the user has. Only audios from the user can be returned.


## Development
We use Algolia to perform the text search. The bot is deployed in Google Cloud. To start developing:

```bash
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Test
To run the tests, simply execute:

```bash
$ python -m unittest discover -vb tests/
```

## Google Cloud
This bot is currently deployed in Google Compute Engine preemptible instance. Because it is crazy cheap.
