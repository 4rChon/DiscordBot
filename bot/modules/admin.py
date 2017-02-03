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
        self._modules['command'].registerCommand('kill', self._shutdown, 'Usage: !kill\nEffect: Shutdown bot', 0)
        self._modules['command'].registerCommand('restart', self._restart, 'Usage: !restart <seconds>\nEffect: Restart bot after <seconds>', 0)

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