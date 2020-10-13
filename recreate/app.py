import platform, sys

def run(inputpath='default', outputpath='default'):
    """ replace file created datetime with original data
        arguments:
        none         use defaults for input and output (GUI)
        input        use input path only                 (SCRIPTS)
        input+output use input and output path definitions (SCRIPTS)
    """
    print({'input': inputpath, 'output': outputpath} )


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