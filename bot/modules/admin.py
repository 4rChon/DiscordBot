import asyncio
import logging
import os

from ..consts import PREFIX, CREATOR
from .module import Module

logging.basicConfig(level=logging.INFO)

class AdminModule(Module):
    def __init__(self, client, modules):
        super().__init__(client, modules)

        self._initialise_commands()

        logging.info('AdminModule: Initialised!')

    def _initialise_commands(self):
        command = self._modules['command']

        command.register_command(
            'kill', self._shutdown,
            '`' + PREFIX + 'kill`',
            '`Shutdown bot`')
        command.register_command(
            'restart', self._restart,
            '`' + PREFIX + 'restart <seconds = 0>`',
            '`Restart bot after <seconds>`')
        command.register_command(
            'exec', self._exec,
            '`' + PREFIX + 'exec <code>`',
            '`Execute <code>`')
        command.register_command(
            'eval', self._eval,
            '`' + PREFIX + 'eval <expression>`',
            '`Evaluate <expression>`')
        command.register_command(
            'refresh', self._refresh,
            '`' + PREFIX + 'refresh <module = all>`',
            '`Refresh <module>`')
        command.register_command(
            'auth', self._auth,
            """`' + PREFIX + 'auth <command> [user <username1> <username2> <...> | role <rolename1>
             <rolename2> <...>]`""",
            '`Allow <usernames>/<rolenames> to use <command>`')
        command.register_command(
            'sleep', self._sleep,
            '`' + PREFIX + 'sleep`',
            '`Ignore commands unless invoked by ' + CREATOR + ' (NYI)`')

    #TODO
    async def _sleep(self, message, args):
        print('..')

    async def _shutdown(self, message, args):
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

        os.system("C:/Users/Alarak/Desktop/DiscordBot/start.bat")

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
