import asyncio
import nltk
import logging
import json

from ..consts import *
from ..util import *

logging.basicConfig(level=logging.INFO)

class Command():
    def __init__(self, action, helpText, users, roles):
        self._action = action
        self._helpText = helpText
        self._permissions = {'users': users, 'roles': roles}

    async def execute(self, message, args):
        await self._action(message, args)

    def help(self):
        helpText = self._helpText
        if len(self._users) > 0:
            helpText += '\nAllowed users: ' + ', '.join(self._permissions['users'])
        if len(self._roles) > 0:
            helpText += '\nAllowed roles: ' + ', '.join(self._permissions['roles'])
        return helpText

    def roles(self):
        return self._permissions['roles']

    def users(self):
        return self._permissions['users']

    def permissions(self):
        return self._permissions

    def addRole(self, role):
        self._permissions['roles'].append(role)

    def addUser(self, user):
        self._permissions['users'].append(user)


class CommandModule():
    def __init__(self, client, modules):
        self._client = client
        self._modules = modules
        self._permissions = {}
        self.registeredCommands = {}
        logging.info('CommandModule initialised!')

    def registerCommand(self, name, action, helpText, users = [], roles = []):
        self._permissions[name] = {'users': users, 'roles': roles}
        self.registeredCommands[name] = Command(action, helpText, users, roles)

    def readPermissions(self):
        with getFile('permissions.json', 'r+') as f:
            f.seek(0)
            self._permissions = json.loads(f.read())

    def writePermissions(self):
        with getFile('permissions.json', 'w+') as f:
            f.seek(0)
            f.write(json.dumps(self._permissions))

    def mergePermissions(self):
        print(self._permissions)
        dump = json.dumps(self._permissions)
        print(dump)
        load = json.loads(dump)
        print(load)

        with getFile('permissions.json', 'w+') as f:
            f.seek(0)
            self._permissions = {**json.loads(f.read()), **self._permissions}
            f.seek(0)
            f.write(json.dumps(self._permissions))


    def refresh(self):
        logging.info('CommandModule refreshed!')
        self.mergePermissions()

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
