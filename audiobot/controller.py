from audiobot.audio import Audio


class Controller(object):
    def __init__(self, bot, transcripts, users):
        super(Controller, self).__init__()
        self.bot = bot
        self.transcripts = transcripts
        self.users = users

    def ping(self, message):
        chat = message.chat.id
        self.bot.send_message(chat, 'Pong!')

    def start(self, message):
        user = str(message.from_user.id)
        data = {'language': 'pt-BR'}
        self.users.set(user, data)

    def me(self, message):
        user = str(message.from_user.id)
        data = self.users.get(user)
        response = (f'{k.title()}: {v}' for k, v in data.items())
        response = '\n'.join(response)
        chat = message.chat.id
        self.bot.send_message(chat, response)

    def audio(self, message):
        message.voice = message.audio
        return self.voice(message)

    def voice(self, message):
        file = message.voice.file_id

        # Get configuration
        user = str(message.from_user.id)
        config = self.users.get(user)
        language = config.pop('language')

        # Process
        url = self.bot.get_file_url(file)
        audio = Audio.download(url)
        audio.convert(fmt='mp3')
        uri = audio.upload()
        results = Audio.recognize(uri, language)

        # Save to algolia
        result = results[0]
        data = {
            'file': file,
            'text': result.transcript,
            'type': message.content_type,
            'language': language,
            'confidence': result.confidence
        }
        self.transcripts.save(user, data)

        text = f'Audio indexed:\n{result.transcript}'
        self.bot.reply_to(message, text)

    def search(self, message):
        """ Searches Algolia's index. Returns objects """
        user = message.from_user.id
        result = self.transcripts.search(user, message.text)

        chat = message.chat.id

        # No results
        if result['nbHits'] < 1:
            return self.bot.send_message(chat, 'No results :(')

        hit = result['hits'][0]
        file = hit['file']

        if hit['type'] == 'audio':
            self.bot.send_audio(chat, file)
        elif hit['type'] == 'voice':
            self.bot.send_voice(chat, file)
