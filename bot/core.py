import logging

from .modules.command import CommandModule
from .modules.admin import AdminModule
from .modules.util import UtilModule
from .modules.chat import ChatModule
from .consts import TOKEN, PREFIX

logging.basicConfig(level=logging.INFO)

class Core(object):
    def __init__(self, client):
        self._client = client
        self._modules = {}

        self._initialise_modules(
            {
                'command': CommandModule,
                'admin': AdminModule,
                'util': UtilModule,
                'chat': ChatModule
            })
        self._initialise_events()

    def _register_module(self, name, module):
        self._modules[name] = module(self._client, self._modules)

    def _initialise_modules(self, modules):
        for module in modules:
            self._register_module(module, modules[module])

        for module in self._modules:
            self._modules[module].refresh()

        logging.info('\nModules: \n\t{}'.format('\n\t'.join([x for x in self._modules])))

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
