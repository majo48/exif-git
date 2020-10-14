""" GUI part of the recreate app

    functions:
        run(input_path, output_path): handles graphic user interface
"""
from recreate.common import constants


def run(input_path, output_path):
    """ gui for recreating original creation datetime """
    input = constants.mydocuments()
    print('GUI is active in folder '+input)


if __name__ == '__main__':
    """ handle functional arguments """
    run('default', 'default')