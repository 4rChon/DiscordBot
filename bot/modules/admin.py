import logging
import os

from ..consts import *

logging.basicConfig(level=logging.INFO)

class AdminModule():
    def __init__(self, client, modules):
        self._client = client
        self._modules = modules
        self._initialiseAdminCommands()

        logging.info('AdminModule initialised!')

    def refresh(self):
        logging.info('AdminModule refreshed!')

    def _initialiseAdminCommands(self):
        command = self._modules['command']

        command.registerCommand('kill', self._shutdown, 'Usage: `' + PREFIX + 'kill`\nEffect: `Shutdown bot`')
        command.registerCommand('restart', self._restart, 'Usage: `' + PREFIX + 'restart <seconds = 0>`\nEffect: `Restart bot after <seconds>`')
        command.registerCommand('exec', self._exec, 'Usage: `' + PREFIX + 'exec <code>`\nEffect: `Execute <code>`')
        command.registerCommand('eval', self._eval, 'Usage: `' + PREFIX + 'eval <expression>`\nEffect: `Evaluate <expression>`')
        command.registerCommand('refresh', self._refresh, 'Usage: `' + PREFIX + 'refresh <module = all>`\nEffect: `Refresh <module>`')
        command.registerCommand('auth', self._auth, 'Usage: `' + PREFIX + 'auth <command> [user <username1> <username2> <...> | role <rolename1> <rolename2> <...>]`\nEffect: `Allow <usernames>/<rolenames> to use <command>`')
        command.registerCommand('sleep', self._sleep, 'Usage: `' + PREFIX + 'sleep`\nEffect: `Ignore commands unless invoked by ' + CREATOR + '`')

    #TODO
    async def _sleep(self, message, args):
        print('..')
        

    async def _shutdown(self, message, args):
        util = self._modules['util']
        client = self._client

        await util.sendMessage(message, 'You typed `kill`. It is super effective :(')
        await client.logout()

    async def _restart(self, message, args):
        util = self._modules['util']
        client = self._client

        seconds = 0

        if len(args) > 1:
            seconds = int(args[1])

        output = await util.sendMessage(message, 'Restarting in... {}'.format(seconds))

        while seconds > 0:
            await asyncio.sleep(1)
            seconds -= 1
            await util.editMessage(output, 'Restarting in... {}.'.format(seconds))

        await util.deleteMessage(output)
        await client.logout()

        os.system("C:/Users/Alarak/Desktop/DiscordBot/start.bat")

    async def _exec(self, message, args):
        util = self._modules['util']
        command = self._modules['command']

        if len(args) == 1:
            await util.sendMessage(message, 'Invalid script.')
            await command.executeCommand(message, ['help', args[1]])
        elif len(args) > 1:
            exec(' '.join(args[1:]))
            await util.sendMessage(message, 'Executing script... (Check your console)')

    async def _eval(self, message, args):
        util = self._modules['util']
        command = self._modules['command']

        if len(args) == 1:
            await util.sendMessage(message, 'Invalid expression.')
            await command.executeCommand(message, ['help', args[1]])
        elif len(args) > 1:
            result = eval(' '.join(args[1:]))
            msg = await util.sendMessage(message, 'Evaluating...')
            await util.editMessage(msg, result)

    async def _auth(self, message, args):
        util = self._modules['util']
        command = self._modules['command']

        cmd = args[0]

        if len(args) <= 3:
            await command.executeCommand(message, ['help', cmd])
        elif len(args) == 4:
            if args[2] == 'users' or args[2] == 'roles':
                command.addPermissions(args[1], args[2], args[3:])
            else:
                await command.executeCommand(message, ['help', cmd])

    async def _refresh(self, message, args):
        util = self._modules['util']

        if len(args) == 1:
            for module in self._modules:
                self._modules[module].refresh()
                await util.sendMessage(message, '`{}` module refreshed'.format(module))
        elif len(args) > 1:
            for arg in args[1:]:
                if arg in self._modules:
                    self._modules[arg].refresh()
                    await util.sendMessage(message, '`{}` module refreshed'.format(arg))
                else:
                    await util.sendMessage(message, ' `{}` module does not exist'.format(arg))
