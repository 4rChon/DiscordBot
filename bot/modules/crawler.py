import logging

from .module import Module

class CrawlerModule(Module):
    def __init__(self, client, modules, commands_filename):
        super().__init__(client, modules, commands_filename)

        logging.info('{}: Initialised!'.format(self.__class__.__name__))