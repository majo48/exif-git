import sys, os

def run(inputpath, outputpath):
    """ gui for recreating original creation datetime """
    print('SCRIPTING is active...')
    print(inputpath)
    print(outputpath)

if __name__ == '__main__':
    """ handle functional arguments """
    os.path.expanduser('~/documents')
    run(os.path.expanduser('~/documents'), 'stdout')