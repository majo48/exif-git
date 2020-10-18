""" MyFile: set file datetime created to metadata.creation_time """
import io, sys, os, filetype


class MyFile:
    """ set file datetime created to metadata.creation_time """

    def __init__(self, file_path):
        """ initialise class variables """
        self.path = file_path
        self.error_msg = None
        self.mime = self._get_mime(file_path)
        self.extension = os.path.splitext(file_path)[1].lower()
        self.info = self._get_exif(file_path)
        # finished

    def _get_mime(self, file_path):
        """" get the file minme type """
        kind = filetype.guess(file_path)
        if kind is None:
            self.error_msg = 'Cannot guess file type'
            return
        return kind.mime

    def _get_exif(self, file_path):
        # open file
        try:
            self.f = io.open( file_path, 'rb')
            self.bytes = self.f.read(262)
            self.f.close()
        except:
            self.error_msg = repr(sys.exc_info()[1])
        finally:
            return 'Work in progress...'
