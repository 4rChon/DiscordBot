import asyncio
import nltk
import logging
import json

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
        helpText = self._helpText
        if len(self._users) > 0:
            helpText += '\nAllowed users: ' + ', '.join(self._users)
        if len(self._roles) > 0:
            helpText += '\nAllowed roles: ' + ', '.join(self._roles)
        return helpText

    def roles(self):
        return self._roles

    def addRole(self, role):
        self._roles.append(role)
        print(self._roles)

    def users(self):
        return self._users

    def addUser(self, user):
        self._users.append(user)
        print(self._users)


class CommandModule():
    def __init__(self, client, modules):
        self._client = client
        self._modules = modules
        self._permissions = {}
        self.registeredCommands = {}
        logging.info('CommandModule initialised!')

    def registerCommand(self, name, action, helpText, users = [], roles = []):
        self._permissions[name] = {'users': users, 'roles': roles}
        #print(self._permissions)
        self.registeredCommands[name] = Command(action, helpText, users, roles)

    def refresh(self):
        logging.info('CommandModule refreshed!')

    async def executeCommand(self, message, args):
        util = self._modules['util']

        if len(args) == 0:
            await util.sendMessage(message, 'lol')
            return

        if args[0] in self.registeredCommands:
            command = self.registeredCommands[args[0]]

            if len(command.users()) + len(command.roles()) > 0:
                if str(message.author) not in command.users() and not any(str(i) in message.author.roles for i in command.roles()):
                    await util.sendMessage(message, 'Izzabbab')
                    return

            await command.execute(message, args)

        else:
            await util.sendMessage(message, 'I don\'t know how to {}'.format(args[0]))
