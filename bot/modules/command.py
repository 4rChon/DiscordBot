import asyncio
import nltk
import logging

from ..consts import *

logging.basicConfig(level=logging.INFO)

class Command():
    def __init__(self, action, helpText, users, roles):
        self._action = action
        self._helpText = helpText
        self._users = users
        self._roles = roles

    async def execute(self, message, args):
        await self._action(message, args)

    def help(self):
        if len(self._users) > 0:
            self._helpText += '\nAllowed users: ' + ', '.join(self._users)
        if len(self._roles) > 0:
            self._helpText += '\nAllowed roles: ' + ', '.join(self._roles)
        return self._helpText

    def roles(self):
        return self._roles

    def addRole(self, role):
        self._roles.append(role)

    def users(self):
        return self._users

    def addUser(self, user):
        self._user.append(user)


class CommandModule():
    def __init__(self, client, modules):
        self._client = client
        self._modules = modules
        self.registeredCommands = {}
        logging.info('CommandModule initialised!')

    def registerCommand(self, message, action, helpText, users = [], roles = []):
        self.registeredCommands[message] = Command(action, helpText, users, roles)

    def refresh(self):
        logging.info('CommandModule refreshed!')

    async def executeCommand(self, message, args):
        if len(args) == 0:
            await self._modules['util'].sendMessage(message, 'lol')
            return

        if args[0] in self.registeredCommands:
            command = self.registeredCommands[args[0]]

            if len(command.users()) > 0 and len(command.roles()) > 0 and str(message.author) is not CREATOR:
                if str(message.author) not in command.users() and not any(str(i) in message.author.roles for i in command.roles()):
                    await self._modules['util'].sendMessage(message, 'Izzabbab')
                    return

            await command.execute(message, args)

        else:
            await self._modules['util'].sendMessage(message, 'I don\'t know how to {}'.format(args[0]))
