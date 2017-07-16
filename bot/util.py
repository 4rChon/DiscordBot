import inspect
from os import path

def get_file(filename, mode='r'):
    file_dir = path.dirname(path.realpath('__file__'))
    filename = path.join(file_dir, 'bot/data/' + filename)
    return open(filename, mode)

def get_methods(module):
    methods = [x for x in inspect.getmembers(module, inspect.ismethod)]
    method_dict = {}
    for method in methods:
        method_dict[method[0]] = method[1]
    return method_dict