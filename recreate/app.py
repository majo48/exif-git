""" top-level recreate app

    functions:
        run(input_path, output_path): defers to gui, scripting packages
"""
import sys


def run(input_path='default', output_path='default'):
    """ replace file created datetime with original data
        arguments:
        none         use defaults for input and output (GUI)
        input        use input path only                 (SCRIPTS)
        input+output use input and output path definitions (SCRIPTS)
    """
    if input_path == 'default' and output_path == 'default':
        from recreate.gui import app
        app.run(input_path, output_path)
    else:
        from recreate.scripting import app
        app.run(input_path, output_path)


if __name__ == '__main__':
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