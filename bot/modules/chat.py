"""Contains the ChatModule which defines chatting methods."""
import logging
import nltk
import markovify
import re

from random import choice
from ..consts import PREFIX
from ..util import get_file
from .module import Module

class POSifiedText(markovify.Text):
    """Markovify class to create sentences."""
    def word_split(self, sentence):
        """Splits the words in a sentence and tags them.

        Args:
            sentence: Sentence to be split into words.

        Returns:
            A list of tagged words from sentence.
        """
        words = re.split(self.word_split_pattern, sentence)
        words = ["::".join(tag) for tag in nltk.pos_tag(words)]
        return words

    def word_join(self, words):
        """Joins the words to form a sentence.

        Args:
            words: A list of words to join.

        Returns:
            A sentence formed from the joined words."""
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence

class ChatModule(Module):
    """ChatModule which defines chatting methods."""
    def __init__(self, client, modules, commands_filename):
        super().__init__(client, modules, commands_filename)

        self._known_sentences = []
        self._markov_model = {'english': {}, 'malti': {}, 'chat': {}}

        logging.info('{}: Initialised!'.format(self.__class__.__name__))

    def register_commands(self):
        self._register_commands()

    def refresh(self):
        """Reloads the word dictionary to be used in the markov model."""
        self._load_data()
        logging.info('{}: Refreshed!'.format(self.__class__.__name__))

    def _load_data(self):
        with get_file('corpus.txt', 'r') as corpus:
            self._known_sentences = nltk.tokenize.sent_tokenize(corpus.read())

        with get_file('malti.txt', 'r') as malti:
            self._markov_model['malti'] = POSifiedText(
                ' '.join(nltk.tokenize.sent_tokenize(malti.read())))

        with get_file('english.txt', 'r') as english:
            self._markov_model['english'] = POSifiedText(
                ' '.join(nltk.tokenize.sent_tokenize(english.read())))

        if len(self._known_sentences) > 0:
            self._markov_model['chat'] = POSifiedText(
                ' '.join(self._known_sentences))

    async def add_sentence(self, sentence):
        #TODO: Check with regex if possible
        if not (sentence.endswith('.')
                or sentence.endswith('?')
                or sentence.endswith('!')
                or sentence.endswith('\'')
                or sentence.endswith('"')
                or sentence.endswith('*')):
            sentence += '.'

        if sentence not in self._known_sentences:

            self._known_sentences.append(sentence)

            with get_file('corpus.txt', 'w') as corpus:
                corpus.seek(0)
                corpus.write(' '.join(self._known_sentences))

    async def _hello(self, message, args):
        util = self._modules['util']

        if len(args) == 1:
            await util.send_message(message, 'Hi {}'.format(message.author.mention))
        elif len(args) > 1:
            for name in args[1:]:
                await util.send_message(message, 'Hi {}'.format(name))

    async def _say(self, message, args):
        util = self._modules['util']

        sentence = self._markov_model['chat'].make_short_sentence(100)

        if not sentence:
            await util.send_message(message, 'I couldn\'t come up with anything funny :(')
        else:
            await util.send_message(message, sentence)

    async def _quote(self, message, args):
        util = self._modules['util']
        command = self._modules['command']

        if len(args) == 1:
            await command.execute_command(message, ['help', args[0]])
            return

        sentence = self._markov_model[args[1]].make_short_sentence(100)

        if not sentence:
            await util.send_message(message, 'I couldn\'t come up with anything funny :(')
        else:
            await util.send_message(message, sentence)
