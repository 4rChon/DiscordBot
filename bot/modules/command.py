import asyncio
import nltk
import logging
import json

from ..consts import *
from ..util import *

logging.basicConfig(level=logging.INFO)

class Command():
    def __init__(self, action, helpText):
        self._action = action
        self._helpText = helpText

    async def execute(self, message, args):
        await self._action(message, args)

    def help(self):
        return self._helpText

class CommandModule():
    def __init__(self, client, modules):
        self._client = client
        self._modules = modules
        self.permissions = {}
        self.registeredCommands = {}
        
        logging.info('CommandModule: Initialised!')

    def refresh(self):
        logging.info('CommandModule: Refreshed!')
        self._readPermissions()

    def registerCommand(self, cmd, action, helpText, permissions = {'users': [], 'roles': []}):
        self.permissions[cmd] = permissions
        self.registeredCommands[cmd] = Command(action, helpText)

    def addPermissions(self, cmd, authType, permissables):
        for permissable in permissables:
            permissions = self.permissions[cmd][authType]
            if permissable not in permissions:
                permissions.append(permissable)
        self._writePermissions()

    def removePermissions(self, cmd, authType, unpermissable):
        self.permissions[cmd][authType].remove(unpermissable)
        self._writePermissions()

    def _readPermissions(self):
        with getFile('permissions.json', 'r+') as f:
            f.seek(0)
            self.permissions = json.loads(f.read())

    def _writePermissions(self):
        with getFile('permissions.json', 'w+') as f:
            f.seek(0)
            f.write(json.dumps(self.permissions))

    async def executeCommand(self, message, args):
        util = self._modules['util']

        if len(args) == 0:
            await util.sendMessage(message, 'lol')
            return

        permissions = self.permissions
        cmd = args[0]
        if cmd in permissions:
            if len(permissions[cmd]['users']) + len(permissions[cmd]['roles']) > 0:
                if str(message.author) not in permissions[cmd]['users'] and not any(str(i) in message.author.roles for i in permissions[cmd]['roles']):
                    await util.sendMessage(message, 'Izzabbab')
                    return
            await self.registeredCommands[cmd].execute(message, args)
        else:
            await util.sendMessage(message, 'I don\'t know how to {}'.format(cmd))
