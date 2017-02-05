import logging
import nltk
import markovify

from os import path
from random import choice
from nltk.tokenize import TweetTokenizer
from ..consts import *

class ChatModule():
    def __init__(self, client, modules):
        self._client = client
        self._modules = modules
        self._taggedCorpus = []
        self._taggedSentences = []
        self.initialiseChatCommands()
        self.initialiseData()

        logging.info('UtilModule initialised!')

    def initialiseChatCommands(self):
        self._modules['command'].registerCommand('hello', self._hello, 'Usage: ' + PREFIX + 'hello\nEffect: Say hello and mention user')
        self._modules['command'].registerCommand('generate', self._generate, 'Usage: ' + PREFIX + 'generate\nEffect: WIP')
        self._modules['command'].registerCommand('add-words', self._addWords, 'Usage: ' + PREFIX + 'add-words <word1> <word2> <...>\nEffect: Add a list of words to the dictionary')
        self._modules['command'].registerCommand('add-sentence', self._addSentence, 'Usage: ' + PREFIX + 'add-sentence <sentence>\nEffect: Add a sentence structure to the sentence list')
        self._modules['command'].registerCommand('remove-words', self._removeWords, 'Usage: ' + PREFIX + 'add-words <word1> <word2> <...>\nEffect: Remove a list of words from the dictionary', [CREATOR])
        #self._modules['command'].registerCommand('list-corpus', self._listCorpus, 'Usage: ' + PREFIX + 'list-corpus\nEffect: list all known words')
        self._modules['command'].registerCommand('list-dict', self._listDict, 'Usage: ' + PREFIX + 'list-dict\nEffect: list all known words')

    def initialiseData(self):
        with self.getFile('dictionary.txt', 'r') as f:
            self._taggedCorpus = f.read().strip('\n').split()
        
        with self.getFile('sentences.txt', 'r') as f:
            self._taggedSentences = [line.rstrip('\n') for line in f]


    def refresh(self):
        self.initialiseData()
        logging.info('ChatModule refreshed!')

    def getFile(self, filename, mode = 'r'):
        fileDir = path.dirname(path.realpath('__file__'))
        filename = path.join(fileDir, 'bot/data/' + filename)
        return open(filename, mode)

    async def _hello(self, message, args):
        if len(args) == 1:
            await self._client.send_message(message.channel, 'Hi {}'.format(message.author.mention))
        elif len(args) > 1:
            for name in args[1:]:
                await self._client.send_message(message.channel, 'Hi {}'.format(name))

    async def _generate(self, message, args):
        reply = await self._client.send_message(message.channel, 'Generating sentence...')
        taggedTuples = [nltk.tag.str2tuple(x) for x in self._taggedCorpus]
        taggedSentence = choice(self._taggedSentences)
        tupleTags = [x[1] for x in taggedTuples]
        wordDict = {}
        for key in tupleTags:
            wordDict[key] = [x[0] for x in taggedTuples if x[1] == key]

        tags = (taggedSentence).split()
        sentence = []
        for tag in tags:
            sentence.append(choice(wordDict[tag]))

        await self._client.edit_message(reply, ' '.join(sentence))

    async def _listDict(self, message, args):
        with self.getFile('dictionary.txt', 'r') as f:
            f.seek(0)
            await self._client.send_message(message.channel, 'I know these words: {}'.format(f.read()))

    async def _addSentence(self, message, args):
        if len(args) == 1:
            await self._modules['command'].executeCommand(message, ['help', args[0]])
            return

        msg = await self._client.send_message(message.channel, 'Adding sentence...')

        sentence = nltk.pos_tag(nltk.word_tokenize(' '.join(args[1:])))
        sentence = ' '.join([x[1] for x in sentence])

        if sentence in self._taggedSentences:
            await self._client.edit_message(msg, 'I already know that sentence structure')
        else:
            self._taggedSentences.append(sentence)

            with self.getFile('sentences.txt', 'w') as f:
                f.seek(0)
                f.write('\n'.join(self._taggedSentences))

            await self._client.edit_message(msg, 'Sentence structure added')
        await self._modules['command'].executeCommand(message, ['add-words'] + args[1:])

    async def _addWords(self, message, args):
        if len(args) == 1:
            await self._modules['command'].executeCommand(message, ['help', args[0]])
            return

        msg = await self._client.send_message(message.channel, 'Adding words...')

        known = 0
        unknown = 0

        tokenizer = TweetTokenizer()
        sentence = ' '.join(args[1:])
        tokenizedSentence = tokenizer.tokenize(sentence)
        taggedSentence = nltk.pos_tag(tokenizedSentence)

        for arg in taggedSentence:
            arg = nltk.tuple2str(arg)
            if arg in self._taggedCorpus:
                known += 1
            else:
                unknown += 1
                self._taggedCorpus.append(arg)

        with self.getFile('dictionary.txt', 'w') as f:
            f.seek(0)
            f.write(' '.join(self._taggedCorpus).strip())

        knownWords = 'words'
        unknownWords = 'words'
        if known == 1:
            knownWords = 'word'
        if unknown == 1:
            unknownWords = 'word'
        await self._client.edit_message(msg, 'I knew {} {}. Added {} {}.'.format(known, knownWords, unknown, unknownWords))

    async def _removeWords(self, message, args):
        if len(args) == 1:
            await self._modules['command'].executeCommand(message, ['help', args[0]])
            return

        known = 0
        unknown = 0

        msg = await self._client.send_message(message.channel, 'Removing words...')
        for arg in nltk.pos_tag(args[1:]):
            arg = nltk.tuple2str(arg)
            if arg in self._taggedCorpus:
                known += 1
                self._taggedCorpus.remove(arg)

        with self.getFile('dictionary.txt', 'w') as f:
            f.seek(0)
            f.write(' '.join(self._taggedCorpus).strip())

        knownWords = 'words'
        unknownWords = 'words'
        if known == 1:
            knownWords = 'word'
        await self._client.edit_message(msg, 'I knew {} {}. Removed {} {}.'.format(known, knownWords, known, knownWords))