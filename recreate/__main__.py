from recreate import app
import sys

if __name__ == '__main__':
    """ handle functional arguments (none, input, input+output)"""
    arg_cnt = len(sys.argv)
    if arg_cnt == 1:
        # no arguments
        app.run()
    if arg_cnt == 2:
        # with input argument
        app.run(sys.argv[1])
    if arg_cnt == 3:
        # with input and output arguments
        app.run(sys.argv[1], sys.argv[2])