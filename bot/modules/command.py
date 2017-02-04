import asyncio
import nltk
import logging

from ..consts import *

logging.basicConfig(level=logging.INFO)

class Command():
    def __init__(self, action, helpText, auth):
        self.action = action
        self.helpText = helpText
        self.auth = auth

    async def execute(self, message, args):
        await self.action(message, args)

    def help(self):
        if self.auth == 0:
            self.helpText += '\nAuth: ArChon#7601'
        elif self.auth == 1:
            self.helpText += '\nAuth: a47members'
        elif self.auth == 2:
            self.helpText += '\nAuth: Everyone'
        return self.helpText

    def auth(self):
        return self.auth

class CommandModule():
    def __init__(self, client, modules):
        self.client = client
        self._modules = modules
        self.registeredCommands = {}
        logging.info('CommandModule initialised!')

    def registerCommand(self, message, action, helpText, auth):
        self.registeredCommands[message] = Command(action, helpText, auth)

    def refresh(self):
        logging.info('CommandModule refreshed!')

    async def executeCommand(self, message, args):
        if len(args) == 0:
            await self.client.send_message(message.channel, 'lol')
            return

        if args[0] in self.registeredCommands:
            command = self.registeredCommands[args[0]]

            if command.auth == 0:
                if str(message.author) != CREATOR:
                    await self.client.send_message(message.channel, 'Izzabbab')
                    return

            await command.execute(message, args)
        else:
            await self.client.send_message(message.channel, 'I don\'t know how to {}'.format(args[0]))
    # async def _sentence(self, message, args):
    #     await 