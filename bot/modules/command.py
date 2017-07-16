import logging
import json

from ..consts import PREFIX
from ..util import get_file, get_methods
from .module import Module

logging.basicConfig(level=logging.INFO)

class Command(object):
    def __init__(self, action, usage, effect):
        self._action = action
        self._help_text = 'Usage: ' + usage + '\n' + 'Effect: ' + effect

    async def execute(self, message, args):
        await self._action(message, args)

    def help(self):
        return self._help_text

class CommandModule(Module):
    def __init__(self, client, modules):
        super().__init__(client, modules)

        self.permissions = {}
        self.registered_commands = {}

        logging.info('CommandModule: Initialised!')

    def refresh(self):
        self._read_permissions()
        logging.info('CommandModule: Refreshed!')

    def register_commands(self, module, commands_filename):
        with get_file(commands_filename, 'r+') as commands_file:
            commands_file.seek(0)
            module.commands = json.loads(commands_file.read())

        module_methods = get_methods(module)

        for cmd_name in module.commands:
            cmd = module.commands[cmd_name]

            self.register_command(
                cmd         = cmd_name,
                action      = module_methods['_' + cmd_name], 
                usage       = '`' + PREFIX + cmd["usage"] + '`', 
                effect      = '`' + cmd["effect"] + '`', 
                permissions = cmd["permissions"]
            )

    def register_command(self, cmd, action, usage="Undocumented", effect="Undocumented", permissions=None):
        if permissions is None:
            permissions = {'users':[], 'roles':[]}

        self.permissions[cmd] = permissions
        self.registered_commands[cmd] = Command(action, usage, effect)       

    def add_permissions(self, cmd, auth_type, permissables):
        for permissable in permissables:
            permissions = self.permissions[cmd][auth_type]
            if permissable not in permissions:
                permissions.append(permissable)
        self._write_permissions()

    def remove_permissions(self, cmd, auth_type, unpermissable):
        self.permissions[cmd][auth_type].remove(unpermissable)
        self._write_permissions()

    def _read_permissions(self):
        with get_file('permissions.json', 'r+') as permissions_file:
            permissions_file.seek(0)
            self.permissions = json.loads(permissions_file.read())

    def _write_permissions(self):
        with get_file('permissions.json', 'w+') as permissions_file:
            permissions_file.seek(0)
            permissions_file.write(json.dumps(self.permissions))


    async def execute_command(self, message, args):
        util = self._modules['util']

        if len(args) == 0:
            await util.send_message(message, 'lol')
            return

        permissions = self.permissions
        cmd = args[0]
        if cmd in permissions:
            if len(permissions[cmd]['users']) + len(permissions[cmd]['roles']) > 0:
                if (str(message.author) not in permissions[cmd]['users']
                        and not any(str(i) in message.author.roles for i in permissions[cmd]['roles'])):
                    await util.send_message(message, 'Ghax int ta...')
                    return
            await self.registered_commands[cmd].execute(message, args)
        else:
            await util.send_message(message, 'I don\'t know how to {}'.format(cmd))
