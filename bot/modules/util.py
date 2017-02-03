import logging

from ..consts import *

logging.basicConfig(level=logging.INFO)

class UtilModule():
    def __init__(self, client, modules):
        self._client = client
        self._modules = modules
        self.initialiseUtilCommands()

        logging.info('UtilModule initialised!')

    def initialiseUtilCommands(self):
        self._modules['command'].registerCommand('help', self._help, 'Usage: help <command>\nEffect: Show help text for <command>', 2)
        self._modules['command'].registerCommand('whoami', self._whoami, 'Usage: whoami \nEffect: Show user and user bot role', 2)

    

    async def _help(self, message, args):
        registeredCommands = self._modules['command'].registeredCommands
        if len(args) == 1:
            await self._client.send_message(message.channel, '`Prefix: {}\nCommands: {}`'.format(PREFIX, ', '.join([x for x in registeredCommands])))
        elif len(args) > 1:
            await self._client.send_message(message.channel, '`{}:\n{}`'.format(args[1], registeredCommands[args[1]].help()))

    async def _whoami(self, message, args):
        serverRoles = [x.name for x in message.author.roles]
        role = 'Noob'
        if str(message.author) == CREATOR:
            role = 'Creator'
        elif 'a47members' in serverRoles or 'Guilty Motherfuckers' in serverRoles:
            role = 'User'
        await self._client.send_message(message.channel, 'You are {} - {}'.format(str(message.author), role))