"""Contains the AdminModule which defines administrative methods."""
import asyncio
import logging
import sys
import os

from .module import Module

logging.basicConfig(level=logging.INFO)

class AdminModule(Module):
    """AdminModule which defines administrative methods."""
    def __init__(self, client, modules):
        super().__init__(client, modules)

        self._initialise_commands()

        logging.info('%: Initialised!', self.__class__.__name__)

    def _initialise_commands(self):
        command = self._modules['command']

        command.register_commands(self, 'admin_commands.json')

    #TODO
    async def _sleep(self, message, args):
        print('..')

    async def _kill(self, message, args):
        util = self._modules['util']
        client = self._client

        if len(args) > 1:
            await asyncio.sleep(int(args[1]))

        await util.send_message(message, 'You typed `kill`. It is super effective :(')
        await client.logout()

    async def _restart(self, message, args):
        util = self._modules['util']
        client = self._client

        seconds = 0
        if len(args) > 1:
            seconds = int(args[1])

        output = await util.send_message(message, 'Restarting in... {}'.format(seconds))

        while seconds > 0:
            await asyncio.sleep(1)
            seconds -= 1
            await util.edit_message(output, 'Restarting in... {}.'.format(seconds))

        await util.delete_message(output)
        await client.logout()

        os.system('"' + sys.path[0] + '/start.bat"')

    async def _exec(self, message, args):
        util = self._modules['util']
        command = self._modules['command']

        if len(args) == 1:
            await util.send_message(message, 'Invalid script.')
            await command.execute_command(message, ['help', args[1]])
        elif len(args) > 1:
            exec(' '.join(args[1:]))
            await util.send_message(message, 'Executing script... (Check your console)')

    async def _eval(self, message, args):
        util = self._modules['util']
        command = self._modules['command']

        if len(args) == 1:
            await util.send_message(message, 'Invalid expression.')
            await command.execute_command(message, ['help', args[1]])
        elif len(args) > 1:
            result = eval(' '.join(args[1:]))
            msg = await util.send_message(message, 'Evaluating...')
            await util.edit_message(msg, result)

    async def _auth(self, message, args):
        command = self._modules['command']

        cmd = args[0]

        if len(args) <= 3:
            await command.execute_command(message, ['help', cmd])
        elif len(args) == 4:
            if args[2] == 'users' or args[2] == 'roles':
                command.addPermissions(args[1], args[2], args[3:])
            else:
                await command.execute_command(message, ['help', cmd])

    async def _refresh(self, message, args):
        util = self._modules['util']

        if len(args) == 1:
            for module in self._modules:
                self._modules[module].refresh()
                await util.send_message(message, '`{}` module refreshed'.format(module))
        elif len(args) > 1:
            for arg in args[1:]:
                if arg in self._modules:
                    self._modules[arg].refresh()
                    await util.send_message(message, '`{}` module refreshed'.format(arg))
                else:
                    await util.send_message(message, ' `{}` module does not exist'.format(arg))
