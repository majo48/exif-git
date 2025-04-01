""" top-level rename script
    Copyright (c) 2021 Martin Jonasse
"""
import sys
from rename.scripting import app


def run(input_path='default', output_path='default'):
    """ replace file attibutes with original creation datetime
        arguments:
        input        use input path only                 (SCRIPTS)
        input+output use input and output path definitions (SCRIPTS)
    """
    app.run(input_path, output_path)

def manage_arguments():
    """ handle functional arguments (none, input, input+output)"""
    arg_cnt = len(sys.argv)
    if arg_cnt == 1:
        # no arguments
        run()
    if arg_cnt == 2:
        # with input argument
        run(sys.argv[1])
    if arg_cnt == 3:
        # with input and output arguments
        run(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    manage_arguments()