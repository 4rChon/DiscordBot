"""This script contains helper functions that do not belong to a particular module."""
import inspect
from os import path

def get_file(filename, mode='r'):
    """Returns an open file with filename from bot/data/.

    Args:
        filename: A filename to be retrieved.
        mode: The read/write mode to be used when opening the file.

    Returns:
        An open file.
    """
    file_dir = path.dirname(path.realpath('__file__'))
    filename = path.join(file_dir, 'bot/data/' + filename)
    return open(filename, mode)

def get_methods(module):
    """Returns a module's methods as a dict with method name as key and
    the method itself as value.

    Args:
        module: The module object for which the methods are to be retrieved.

    Returns:
        A dict mapping method names to functions.
    """
    methods = [x for x in inspect.getmembers(module, inspect.ismethod)]
    method_dict = {}
    for method in methods:
        method_dict[method[0]] = method[1]
    return method_dict
