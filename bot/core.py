"""Core module of the discord bot.

Calls initialisers for all modules and sets up event handlers.
"""
import logging

from .modules.command import CommandModule
from .modules.admin import AdminModule
from .modules.util import UtilModule
from .modules.chat import ChatModule
from .modules.crawler import CrawlerModule
from .consts import TOKEN, PREFIX

logging.basicConfig(level=logging.INFO)

class Core(object):
    """Core class containing the core components of the discord bot."""
    def __init__(self, client):
        self._client = client
        self._modules = {}

        self._initialise_modules(
            {
                'command': CommandModule,
                'admin': AdminModule,
                'util': UtilModule,
                'chat': ChatModule,
                'crawler': CrawlerModule
            })

        self._initialise_events()

    def _initialise_modules(self, modules):
        for name, module in modules.items():
            self._modules[name] = module(self._client, self._modules)

        for _, module in self._modules.items():
            module.register_commands()

        for _, module in self._modules.items():
            module.refresh()

    def _initialise_events(self):
        command = self._modules['command']
        chat = self._modules['chat']

        #################
        # Event actions #
        #################
        @self._client.event
        async def on_ready():
            login_message = '\nLogged in as\n\t{}\n\t{}\n------------------------------'
            logging.info(login_message.format(self._client.user.name, self._client.user.id))

        @self._client.event
        async def on_message(message):
            message.content = message.content.strip()
            if message.content.startswith(PREFIX):
                args = message.content[1:].split()
                await command.execute_command(message, args)
            elif not message.author.bot:
                await chat.add_sentence(message.content)
        ########################
        # End of Event actions #
        ########################


    def run_client(self):
        self._client.run(TOKEN)
