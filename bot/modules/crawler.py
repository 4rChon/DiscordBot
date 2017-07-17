import logging

from .module import Module

class CrawlerModule(Module):
    def __init__(self, client, modules):
        super().__init__(client, modules)

        logging.info('{}: Initialised!'.format(self.__class__.__name__))