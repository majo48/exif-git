""" scripting part of the recreate app

    functions:
        run(input_path, output_path): handles scripting interface
"""
from recreate.common import constants, myfolder
import io, sys


def run(input_path, output_path):
    """ handle scripting interface """
    print('SCRIPTING is active...')
    myf = myfolder.MyFolder(input_path)
    if (output_path == 'stdout' or output_path == 'default'):
        if myf.error is not None:
            print({'path': input_path, 'error': myf.error})
        else:
            print('[')
            for myfile in myf.files:
                if myfile.error is not None:
                    print(myfile.error)
                elif myfile.mime is not None:
                    print(myfile.output)
            print(']')
    else:
        try:
            f = io.open( output_path, "w", encoding="utf-8")
            f.write('['+"\n")
            for myfile in myf.files:
                if myfile.error is not None:
                    f.write(str(myfile.error)+"\n")
                elif myfile.mime is not None:
                    f.write(str(myfile.output)+"\n")
                else:
                    f.write(str("error in "+myfile.path)+"\n")
                    break  # escape for loop
            f.write(']' + "\n")
            f.close()
            print('Wrote', len(myf.files), 'lines to', output_path)
        except IOError:
            print({'path': output_path, 'error': repr(sys.exc_info()[1])})
        finally:
            pass

if __name__ == '__main__':
    """ handle functional arguments """
    run(constants.mydocuments(), 'stdout')