# Audio bot
This bot indexes all audio that you send to it and make it searchable by text.

## Commands

### `/ping`
This will make it answer "Pong!". Mostly used to check if the service is up.

### `/search [text]`
Will return the best match of the already indexed audios.

### `/audio [audio_id]` TODO
Will return the audio that is represented by the ID passed.

### Audio/voice
Every audio you send to this bot will trigger the recognition pipeline. You will receive some messages telling you which step of the pipeline we are currently at.

## Development
We use Algolia to perform the text search. The bot is deployed in Google Cloud. To start developing:

```bash
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Tests TODO (broken)
To run the tests, simply execute:

```bash
$ python -m unittest discover -vb tests/
```

## Google Cloud TODO
