from os import path, makedirs


def myoPath():
    rootPath = path.expanduser('~')
    try:
        makedirs(rootPath + r'\pyMyo')
        addrPyMyo = rootPath + r'\pyMyo'
    except:
        addrPyMyo = rootPath + r'\pyMyo'

    return addrPyMyo
