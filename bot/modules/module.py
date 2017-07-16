import logging

class Module(object):
    def __init__(self, client, modules):
        self._client = client
        self._modules = modules

    def refresh(self):
        logging.info('{}: Nothing to Refresh!'.format(self.__class__.__name__))
