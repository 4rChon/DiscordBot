import logging
import json

from ..consts import PREFIX
from ..util import get_file
from .module import Module

logging.basicConfig(level=logging.INFO)

class Command(object):
    def __init__(self, action, usage, effect, permissions):
        self._action = action
        self._usage = usage
        self._effect = effect
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

    @property
    def serialized(self):
        return {"usage": self._usage, "effect": self._effect, "permissions": self._permissions}

class CommandModule(Module):
    def __init__(self, client, modules, commands_filename):
        super().__init__(client, modules, commands_filename)

        self.registered_commands = {}

        logging.info('{}: Initialised!'.format(self.__class__.__name__))

    def register_command(self, name, action, props):
        usage = '`{}`'.format(PREFIX + props["usage"])
        effect = '`{}`'.format(props["effect"])
        permissions = props["permissions"]

        self.registered_commands[name] = Command(action, usage, effect, permissions)

    def add_permissions(self, name, auth_group, auth_names):
        auth_group_permissions = self.registered_commands[name].permissions[auth_group]
        auth_group_permissions = list(set().union(auth_group_permissions, auth_names))
        self.registered_commands[name].permissions[auth_group] = auth_group_permissions
        
        for module in self._modules:
            with get_file(self._modules[module].commands_filename, 'r+') as commands_file:
                commands_file.seek(0)
                commands = json.loads(commands_file.read())
                if name in commands:
                    commands_file.seek(0)
                    commands_file.truncate()
                    commands[name]['permissions'] = self.registered_commands[name].permissions
                    json.dump(commands, commands_file)

    def remove_permissions(self, name, auth_group, auth_names):
        auth_group_permissions = self.registered_commands[name].permissions[auth_group]
        auth_group_permissions = list(set(auth_group_permissions) - set(auth_names))
        self.registered_commands[name].permissions[auth_group] = auth_group_permissions
        
        for module in self._modules:
            with get_file(self._modules[module].commands_filename, 'r+') as commands_file:
                commands_file.seek(0)
                commands = json.loads(commands_file.read())
                if name in commands:
                    commands_file.seek(0)
                    commands_file.truncate()
                    commands[name]['permissions'] = self.registered_commands[name].permissions
                    json.dump(commands, commands_file)

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
                    await util.send_message(message, 'Try using your other hand.')
                    return
            await self.registered_commands[cmd].execute(message, args)
        else:
            await util.send_message(message, 'I don\'t know how to {}'.format(cmd))
