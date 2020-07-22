# Os
import os

# Sys
import sys


def isfile(filepath):
    """Check if a file exists

    :param filepath: Path of the file
    """

    return os.path.isfile(filepath)


def get_size_of(object):
    """Get the size of the object

    :param object: Object to will calculate the size
    """
    return sys.getsizeof(object)


def rmfile(path):
    """Delete files from a path

    :param path: Path of the folder with files to will delete
    """
    os.remove(path)
