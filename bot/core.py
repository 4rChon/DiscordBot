import discord
import asyncio
import logging

from .modules.command import CommandModule
from .modules.admin import AdminModule
from .modules.util import UtilModule
from .modules.chat import ChatModule
from .consts import *

logging.basicConfig(level=logging.INFO)

class Core():
    def __init__(self, client):
        self._client = client
        self._modules = {}

        self.initialiseModules()
        self.initialiseEvents()

        self.runClient()

    def registerModule(self, name, module):
        self._modules[name] = module(self._client, self._modules)

    def initialiseModules(self):
        self.registerModule('command', CommandModule)
        self.registerModule('admin', AdminModule)
        self.registerModule('util', UtilModule)
        self.registerModule('chat', ChatModule)

        logging.info('Modules: \n\t{}'.format('\n\t'.join([x for x in self._modules])))

    def initialiseEvents(self):
        command = self._modules['command']
        chat = self._modules['chat']

        @self._client.event
        async def on_ready():
            print('Logged in as')
            print(self._client.user.name)
            print(self._client.user.id)
            print('------')

        @self._client.event
        async def on_message(message):
            message.content = message.content.strip()
            if message.content.startswith(PREFIX):
                args = message.content[1:].split()
                await command.executeCommand(message, args)
            elif not message.author.bot:
                await chat.addSentence(message.content)

    def runClient(self):
        self._client.run(TOKEN)