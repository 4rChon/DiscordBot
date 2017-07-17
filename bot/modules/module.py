import logging
import json

from ..util import get_file, get_methods

class Module(object):
    def __init__(self, client, modules):
        self._client = client
        self._modules = modules

    def register_commands(self):
        logging.info('{}: No commands to register!'.format(self.__class__.__name__))
        return

    def _register_commands(self, commands_filename):
        command = self._modules['command']

        with get_file(commands_filename, 'r+') as commands_file:
            commands_file.seek(0)
            self.commands = json.loads(commands_file.read())

        module_methods = get_methods(self)

        for cmd_name in self.commands:
            cmd = self.commands[cmd_name]
            command.register_command(
                cmd_name,
                module_methods['_' + cmd_name],
                cmd)

    def refresh(self):
        logging.info('{}: Nothing to Refresh!'.format(self.__class__.__name__))
