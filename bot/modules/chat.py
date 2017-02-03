import logging
import nltk
import markovify

from os import path
from ..consts import *

class ChatModule():
    def __init__(self, client, modules):
        self._client = client
        self._modules = modules
        self._taggedCorpus = []
        self._rawCorpus = ''
        self._customCorpus = ''
        self.initialiseChatCommands()
        self.initialiseCorpus()

        logging.info('UtilModule initialised!')

    def initialiseChatCommands(self):
        self._modules['command'].registerCommand('hello', self._hello, 'Usage: !hello\nEffect: Say hello and mention user', 2)
        self._modules['command'].registerCommand('generate', self._generate, 'Usage: !generate\nEffect: ???', 2)
        self._modules['command'].registerCommand('add-word', self._addWord, 'Usage: !add-word <word>\nEffect: Add a word to the dictionary', 0)
        self._modules['command'].registerCommand('list-corpus', self._listCorpus, 'Usage: !list-corpus\nEffect: list all known words', 2)

    def initialiseCorpus(self):
        self._taggedCorpus = nltk.corpus.brown.tagged_words(tagset='universal')
        self._rawCorpus = nltk.corpus.gutenberg.raw()


    async def _hello(self, message, args):
        await self._client.send_message(message.channel, 'Hi {}'.format(message.author.mention))

    async def _generate(self, message, args):
        reply = await self._client.send_message(message.channel, 'Generating text...')
        # with self.getFile('dictionary.txt', 'r+') as f:
        #     f.seek(0)
        #     self._customCorpus = f.read()
        #     f.seek(0)
        for msg in self._client.messages:
            content = msg.content
            # print(content)
            # if not content.startswith(PREFIX) and msg.author != client.user:
            #     print(content)
            #     if not content.endswith('.'):
            #         '. '.join([self._customCorpus, content])
            #     else:
            #         ' '.join([self._customCorpus, content])

        print(self._customCorpus)
        text = markovify.Text(self._customCorpus)

        await self._client.edit_message(reply, text.make_short_sentence(140))

    async def _listCorpus(self, message, args):
        await self._client.send_message(message.channel, 'I know these words: {}'.format(self._taggedCorpus))

    async def _addWord(self, message, args):
        if len(args) == 1:
            await self._modules['command'].executeCommand(message, ['help', args[0]])
            return

        with self.getFile('dictionary.txt', 'r+') as f:
            f.seek(0)
            content = nltk.word_tokenize(f.read())
            f.seek(0)
            if args[1] in content:
                await self._client.send_message(message.channel, 'I already know `{}`'.format(args[1]))
            else:
                content.append(args[1])
                joinedContent = ' '.join(content)
                f.write(joinedContent)

    def getFile(self, filename, mode = 'r'):
        fileDir = path.dirname(path.realpath('__file__'))
        filename = path.join(fileDir, 'bot/data/' + filename)
        return open(filename, mode)
