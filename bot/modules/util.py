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
        self._modules['command'].registerCommand('help', self._help, 'Usage: ' + PREFIX + 'help <command>\nEffect: Show help text for <command>')
        self._modules['command'].registerCommand('whoami', self._whoami, 'Usage: ' + PREFIX + 'whoami \nEffect: Show user and user bot role', ['Bengal#1111'])

    def refresh(self):
        logging.info('UtilModule refreshed!')

    async def _help(self, message, args):
        registeredCommands = self._modules['command'].registeredCommands
        if len(args) == 1:
            await self.sendMessage(message, '`Prefix: {}\nCommands: {}`'.format(PREFIX, ', '.join([x for x in registeredCommands])))
        elif len(args) > 1:
            await self.sendMessage(message, '`{}:\n{}`'.format(args[1], registeredCommands[args[1]].help()))

    async def _whoami(self, message, args):
        serverRoles = ', '.join([str(x.name) for x in message.author.roles])
        await self._client.send_message(message.channel, 'You are {} - {}'.format(str(message.author), serverRoles))

    async def sendMessage(self, message, args):
        return await self._client.send_message(message.channel, args, tts = message.tts)

    async def editMessage(self, message, args):
        return await self._client.edit_message(message, args)

    async def deleteMessage(self, message):
        return await self._client.delete_message(message)