import logging

from ..consts import *

logging.basicConfig(level=logging.INFO)

class UtilModule():
    def __init__(self, client, modules):
        self._client = client
        self._modules = modules
        self._initialiseUtilCommands()

        logging.info('UtilModule: Initialised!')

    def refresh(self):
        logging.info('UtilModule: Nothing to refresh!')

    def _initialiseUtilCommands(self):
        command = self._modules['command']

        command.registerCommand('help', self._help, 'Usage: `' + PREFIX + 'help <command>`\nEffect: `Show help text for <command>`')
        command.registerCommand('whoami', self._whoami, 'Usage: `' + PREFIX + 'whoami`\nEffect: `Show user and user bot role`')

    async def _help(self, message, args):
        command = self._modules['command']

        registeredCommands = command.registeredCommands
        if len(args) == 1:
            await self.sendMessage(message, '`Prefix: {}\nCommands: {}`'.format(PREFIX, ', '.join([x for x in registeredCommands])))
        elif len(args) > 1:
            authText = ''
            permissions = command.permissions[args[1]]
            if len(permissions['users']) > 0:
                authText += '\nAllowed users: `{}`'.format(', '.join(permissions['users']))
            if len(permissions['roles']) > 0:
                authText += '\nAllowed roles: `{}`'.format(', '.join(permissions['roles']))
            await self.sendMessage(message, '{}:\n{}{}'.format(args[1], registeredCommands[args[1]].help(), authText))

    async def _whoami(self, message, args):
        serverRoles = ', '.join([str(x.name) for x in message.author.roles[1:]])
        await self._client.send_message(message.channel, 'You are `{}` \n\nUser: `{}` \nRoles: `{}`'.format(message.author.display_name, str(message.author), serverRoles))

    async def sendMessage(self, message, args):
        return await self._client.send_message(message.channel, args, tts = message.tts)

    async def editMessage(self, message, args):
        return await self._client.edit_message(message, args)

    async def deleteMessage(self, message):
        return await self._client.delete_message(message)