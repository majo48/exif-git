""" scripting part of the recreate app

    functions:
        run(input_path, output_path): handles scripting interface
"""
from recreate.common import constants, myfile

def run(input_path, output_path):
    """ gui for recreating original creation datetime """
    print('SCRIPTING is active...')
    print(input_path)
    print(output_path)
    myf = myfile.MyFile(input_path)
    print(myf.info)

if __name__ == '__main__':
    """ handle functional arguments """
    run(constants.mydocuments(), 'stdout')