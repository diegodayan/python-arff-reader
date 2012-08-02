__author__ = "Diego Dayan"
__version__ = "0.1"

def fileExists(filename):
    try:
        open(filename)
        return True
    except IOError:
        pass
    return False