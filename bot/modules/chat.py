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
        self._modules['command'].registerCommand('add-sentence', self._addSentence, 'Usage: ' + PREFIX + 'add-sentence <sentence>\nEffect: Add a sentence structure to the sentence list')

    def initialiseData(self):
        with self.getFile('corpus.txt', 'r') as f:
            self._knownSentences = [line.strip('\n') for line in f]

        if len(self._knownSentences) > 0:
            self._markovModel = POSifiedText(' '.join(self._knownSentences), state_size=2)


    def refresh(self):
        self.initialiseData()
        logging.info('ChatModule refreshed!')

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
        reply = await self._modules['util'].sendMessage(message, 'Generating sentence...')
        sentence = self._markovModel.make_short_sentence(140)

        if not sentence:
            await self._modules['util'].editMessage(reply, 'I couldn\'t come up with anything funny :(')
        else:
            await self._modules['util'].sendMessage(reply, sentence)

    async def _listDict(self, message, args):
        with self.getFile('dictionary.txt', 'r') as f:
            f.seek(0)
            await self._modules['util'].sendMessage(message, 'I know these words: {}'.format(f.read()))

    async def _addSentence(self, message, args):
        if len(args) == 1:
            await self._modules['command'].executeCommand(message, ['help', args[0]])
            return

        silent = args[1] == '-s'

        if not silent:
            msg = await self._modules['util'].sendMessage(message, 'Adding sentence...')

        if silent:
            sentence = ' '.join(args[2:])
        else:
            sentence = ' '.join(args[1:])
        if sentence in self._knownSentences:
            if not silent:
                await self._modules['util'].editMessage(msg, 'I already know that sentence!')
        else:
            if not (sentence.endswith('.') or sentence.endswith('?')):
                sentence += '.'

            self._knownSentences.append(sentence)

            with self.getFile('corpus.txt', 'w') as f:
                f.seek(0)
                f.write(' '.join(self._knownSentences))
        if not silent:
            await self._modules['util'].editMessage(msg, 'Sentence added. Refresh module to update markov chain.')