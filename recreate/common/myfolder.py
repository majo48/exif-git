""" MyFolder: set file datetime created to metadata.creation_time in all files in folder """
import io, sys, os
from recreate.common import myfile


class MyFolder:
    """ Recursive part of the recreate application """

    def __init__(self, file_path):
        """ Init class variables """
        self.files = []
        self.error = None
        if os.path.isfile(file_path):
            self.files.append(myfile.MyFile(file_path))
        elif os.path.isdir(file_path):
            for subdir, dirs, files in os.walk(file_path):
                for file in files:
                    self.files.append(myfile.MyFile(os.path.join(subdir, file)))
        else:
            self.error = file_path + 'Invalid path!'


