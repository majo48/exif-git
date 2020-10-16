""" MyFile: set file datetime created to metadata.creation_time """
import io, sys, os


class MyFile:
    """ set file datetime created to metadata.creation_time """

    def __init__(self, file_path):
        """ initialise class variables """
        self.path = file_path
        self.error_msg = None
        self.has_metadata = False
        self.is_writeable = False
        # open file
        try:
            f = io.open( self.path, "wb")
            self.is_writeable = f.writable()
            self.extension = os.path.splitext(file_path)[1].lower()
            self.check_metadata(f)
            f.close()
        except:
            self.error_msg = repr(sys.exc_info()[1])
        finally:
            pass
        # finish
        self.info = 'Work in progress...'

    def check_metadata(self, f):
        """" check the file for metadata """
        pass