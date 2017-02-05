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
                command = message.content[1:]
                args = command.split()
                await self._modules['command'].executeCommand(message, args)
            elif message.author.id != self._client.user.id:
                await self._modules['chat'].addSentence(message.content)

    def runClient(self):
        self._client.run(TOKEN)