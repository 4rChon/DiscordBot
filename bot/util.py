from os import path

def getFile(filename, mode = 'r'):
    fileDir = path.dirname(path.realpath('__file__'))
    filename = path.join(fileDir, 'bot/data/' + filename)
    return open(filename, mode)