import logging
import os

from ..consts import *

logging.basicConfig(level=logging.INFO)

class AdminModule():
    def __init__(self, client, modules):
        self._client = client
        self._modules = modules
        self.initialiseAdminCommands()

        logging.info('AdminModule initialised!')

    def initialiseAdminCommands(self):
        self._modules['command'].registerCommand('kill', self._shutdown, 'Usage: ' + PREFIX + 'kill\nEffect: Shutdown bot', [CREATOR])
        self._modules['command'].registerCommand('restart', self._restart, 'Usage: ' + PREFIX + 'restart <seconds = 0>\nEffect: Restart bot after <seconds>', [CREATOR])
        self._modules['command'].registerCommand('exec', self._exec, 'Usage: ' + PREFIX + 'exec <code>\nEffect: Execute <code>', [CREATOR])
        self._modules['command'].registerCommand('eval', self._eval, 'Usage: ' + PREFIX + 'eval <expression>\nEffect: Evaluate <expression>', [CREATOR])
        self._modules['command'].registerCommand('refresh', self._refresh, 'Usage: ' + PREFIX + 'refresh <module = all>\nEffect: Refresh <module>', [CREATOR])
        #self._modules['command'].registerCommand('auth', self._auth, 'Usage: ' + PREFIX + 'auth <command> [user <username> | role <rolename>]\nEffect: Allow <username>/<rolename> to use <command>', [CREATOR])

    def refresh(self):
        logging.info('AdminModule refreshed!')

    async def _shutdown(self, message, args):
        await self._modules['util'].sendMessage(message, 'You typed `kill`. It is super effective :(')
        await self._client.logout()

    async def _restart(self, message, args):
        util = self._modules['util']

        seconds = 0

        if len(args) > 1:
            seconds = int(args[1])

        output = await util.sendMessage(message, 'Restarting in... {}'.format(seconds))

        while seconds > 0:
            await asyncio.sleep(1)
            seconds -= 1
            await util.editMessage(output, 'Restarting in... {}.'.format(seconds))

        await util.deleteMessage(output)

        await self._client.logout()
        os.system("C:/Users/Alarak/Desktop/DiscordBot/start.bat")

    async def _exec(self, message, args):
        util = self._modules['util']
        command = self._modules['command']

        if len(args) == 1:
            await util.sendMessage(message, 'Invalid script.')
            await command.executeCommand(message, ['help', args[1]])
        elif len(args) > 1:
            exec(' '.join(args[1:]))
            print(args)
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

        if len(args) <= 3:
            await command.executeCommand(message, ['help', args[0]])
        elif len(args) == 4:
            if args[2] == 'user':
                print(args[1])
                command.registeredCommands[args[1]].addUser(args[3])
            elif args[2] == 'role':
                command.registeredCommands[args[1]].addRole(' '.join(args[3:]))
            else:
                command.executeCommand(message, ['help', args[0]])

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
