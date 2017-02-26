from os import path

def get_file(filename, mode='r'):
    file_dir = path.dirname(path.realpath('__file__'))
    filename = path.join(file_dir, 'bot/data/' + filename)
    return open(filename, mode)
