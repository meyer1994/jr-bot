
import audiobot.audio


class Controller(object):
    def __init__(self, bot, algolia, firestore):
        super(Controller, self).__init__()
        self.bot = bot
        self.algolia = algolia
        self.firestore = firestore

    def ping(self, message):
        chat = message.chat.id
        self.bot.send_message(chat, 'Pong!')

    def start(self, message):
        user = str(message.from_user.id)
        collection = self.firestore.collection('users')
        document = collection.document(user)
        data = {'language': 'pt-BR'}
        document.set(data)

    def audio(self, message):
        message.voice = message.audio
        return self.voice(message)

    def voice(self, message):
        user = str(message.from_user.id)
        file = message.voice.file_id

        collection = self.firestore.collection('users')
        document = collection.document(user)
        snapshot = document.get(['language'])
        data = snapshot.to_dict()

        lang = data.pop('language')

        # Process
        url = self.bot.get_file_url(file)
        temp = audiobot.audio.download(url)
        temp = audiobot.audio.convert(temp)
        uri = audiobot.audio.upload(temp, file)
        results = audiobot.audio.recognize(uri, lang)

        # Index
        result = results[0]
        data = {
            'file': file,
            'text': result.transcript,
            'type': message.content_type,
            'user': message.from_user.id,
            'language': lang,
            'confidence': result.confidence
        }
        config = {'autoGenerateObjectIDIfNotExist': True}
        index = self.algolia.init_index('audio')
        result = index.save_object(data, config)

    def search(self, message):
        """ Searches Algolia's index. Returns objects """
        user = message.from_user.id
        options = {
            'attributesToHighlight': [],
            'filters': f'user = {user}',
            'hitsPerPage': 1
        }
        index = self.algolia.init_index('audio')
        result = index.search(message.text, options)

        chat = message.chat.id

        if result['nbHits'] < 1:
            return self.bot.send_message(chat, 'No results :(')

        hit = result['hits'][0]
        file = hit['file']

        if hit['type'] == 'audio':
            self.bot.send_audio(chat, file)
        elif hit['type'] == 'voice':
            self.bot.send_voice(chat, file)
