""" common part of the recreate app

    functions:
        mydocuments(): the fully qualified path to the MyDocuments folder
"""
import os


def mydocuments():
    """ get the path to the MyDocuments folder """
    return os.path.expanduser('~/documents')