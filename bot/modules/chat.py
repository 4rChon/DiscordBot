import logging
import nltk
import markovify
import re

from os import path
from random import choice
from nltk.tokenize import TweetTokenizer
from ..consts import *

class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = [ "::".join(tag) for tag in nltk.pos_tag(words)]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence

class ChatModule():
    def __init__(self, client, modules):
        self._client = client
        self._modules = modules
        self._knownSentences = []
        self._markovModel = {}

        self.initialiseChatCommands()
        self.initialiseData()

        logging.info('UtilModule initialised!')

    def initialiseChatCommands(self):
        self._modules['command'].registerCommand('hello', self._hello, 'Usage: ' + PREFIX + 'hello\nEffect: Say hello and mention user')
        self._modules['command'].registerCommand('say', self._say, 'Usage: ' + PREFIX + 'say\nEffect: WIP')

    def initialiseData(self):
        with self.getFile('corpus.txt', 'r') as f:
            self._knownSentences = [line.strip('\n') for line in f]

        if len(self._knownSentences) > 0:
            self._markovModel = POSifiedText(' '.join(self._knownSentences), state_size=2)


    def refresh(self):
        self.initialiseData()
        logging.info('ChatModule refreshed!')

    async def addSentence(self, sentence):
        if not (sentence.endswith('.') or sentence.endswith('?') or sentence.endswith('!')):
            sentence += '.'

        if sentence not in self._knownSentences:

            self._knownSentences.append(sentence)

            with self.getFile('corpus.txt', 'w') as f:
                f.seek(0)
                f.write(' '.join(self._knownSentences))

    def getFile(self, filename, mode = 'r'):
        fileDir = path.dirname(path.realpath('__file__'))
        filename = path.join(fileDir, 'bot/data/' + filename)
        return open(filename, mode)

    async def _hello(self, message, args):
        if len(args) == 1:
            await self._modules['util'].sendMessage(message, 'Hi {}'.format(message.author.mention))
        elif len(args) > 1:
            for name in args[1:]:
                await self._modules['util'].sendMessage(message, 'Hi {}'.format(name))

    async def _say(self, message, args):
        sentence = self._markovModel.make_short_sentence(140)

        if not sentence:
            await self._modules['util'].sendMessage(message, 'I couldn\'t come up with anything funny :(')
        else:
            await self._modules['util'].sendMessage(message, sentence)