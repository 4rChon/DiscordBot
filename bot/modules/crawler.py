import logging

from .module import Module

class CrawlerModule(Module):
    def __init__(self, client, modules):
        super().__init__(client, modules)

        logging.info('CrawlerModule: Initialised!')

    def refresh(self):
        logging.info('CrawlerModule: Refreshed!')

    def _initialise_commands(self):
        command = self._modules['command']