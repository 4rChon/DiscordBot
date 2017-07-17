import logging
import json

from ..consts import PREFIX
from .module import Module

logging.basicConfig(level=logging.INFO)

class Command(object):
    def __init__(self, action, usage, effect, permissions):
        self._action = action
        self._help_text = 'Usage: {} \nEffect: {}'.format(usage, effect)
        self._permissions = permissions

    async def execute(self, message, args):
        await self._action(message, args)

    @property
    def help(self):
        return self._help_text

    @property
    def permissions(self):
        return self._permissions

class CommandModule(Module):
    def __init__(self, client, modules):
        super().__init__(client, modules)

        self.registered_commands = {}

        logging.info('{}: Initialised!'.format(self.__class__.__name__))

    def register_command(self, name, action, props):
        usage = '`{}`'.format(PREFIX + props["usage"])
        effect = '`{}`'.format(props["effect"])
        permissions = props["permissions"]

        self.registered_commands[name] = Command(action, usage, effect, permissions)

    async def execute_command(self, message, args):
        util = self._modules['util']

        if len(args) == 0:
            await util.send_message(message, 'lol')
            return

        cmd = args[0]
        if cmd in self.registered_commands:
            permissions = self.registered_commands[cmd].permissions
            if len(permissions['users']) + len(permissions['roles']) > 0:
                if (str(message.author) not in permissions['users']
                        and not any(str(i) in message.author.roles for i in permissions['roles'])):
                    await util.send_message(message, 'Ghax int ta...')
                    return
            await self.registered_commands[cmd].execute(message, args)
        else:
            await util.send_message(message, 'I don\'t know how to {}'.format(cmd))
