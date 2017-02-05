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
        self._modules['command'].registerCommand('auth', self._auth, 'Usage: ' + PREFIX + 'auth <command> [user <username> | role <rolename>]\nEffect: Allow <username>/<rolename> to use <command>', [CREATOR])

    def refresh(self):
        logging.info('AdminModule refreshed!')

    async def _shutdown(self, message, args):
        await self._client.send_message(message.channel, 'You typed `kill`. It is super effective :(')
        await self._client.logout()

    async def _restart(self, message, args):
        seconds = 0

        if len(args) > 1:
            seconds = int(args[1])

        output = await self._client.send_message(message.channel, 'Restarting in... {}'.format(seconds))

        while seconds > 0:
            await asyncio.sleep(1)
            seconds -= 1
            await self._client.edit_message(output, 'Restarting in... {}.'.format(seconds))

        await self._client.delete_message(output)

        await self._client.logout()
        os.system("C:/Users/Alarak/Desktop/DiscordBot/start.bat")

    async def _exec(self, message, args):
        if len(args) == 1:
            await self._client.send_message(message.channel, 'Invalid script.')
            await self._modules['command'].executeCommand(message, ['help', args[1]])
        elif len(args) > 1:
            exec(' '.join(args[1:]))
            print(args)
            await self._client.send_message(message.channel, 'Executing script... (Check your console)')

    async def _eval(self, message, args):
        if len(args) == 1:
            await self._client.send_message(message.channel, 'Invalid expression.')
            await self._modules['command'].executeCommand(message, ['help', args[1]])
        elif len(args) > 1:
            result = eval(' '.join(args[1:]))
            msg = await self._client.send_message(message.channel, 'Evaluating...')
            await self._client.edit_message(msg, result)

    async def _auth(self, message, args):
        if len(args) <= 2:
            await self._modules['command'].executeCommand(message, ['help', args[0]])
        elif len(args) > 2:
            if args[2] == 'user':
                self._modules['command'].registeredCommands[args[1]].addUser(args[3])
            elif args[2] == 'role':
                self._modules['command'].registeredCommands[args[1]].addRole(args[3])
            else:
                await self._modules['command'].executeCommand(message, ['help', args[0]])

    async def _refresh(self, message, args):
        if len(args) == 1:
            for module in self._modules:
                self._modules[module].refresh()
                await self._client.send_message(message.channel, '`{}` module refreshed'.format(module))
        elif len(args) > 1:
            for arg in args[1:]:
                if arg in self._modules:
                    self._modules[arg].refresh()
                    await self._client.send_message(message.channel, '`{}` module refreshed'.format(arg))
                else:
                    await self._client.send_message(message.channel, ' `{}` module does not exist'.format(arg))
