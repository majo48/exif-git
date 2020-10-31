""" MyFile: set file datetime created to metadata.creation_time """
import io, sys, os, filetype, exifread

HEADERLEN = 262


class MyFile:
    """ Heavy lifting part of the recreate application """

    def __init__(self, file_path):
        """ initialise class variables """
        self.path = file_path
        self.error = None
        self.bytes = self._get_header_bytes(file_path)
        self.mime = self._get_mime(self.bytes)
        self.extension = os.path.splitext(file_path)[1].lower()
        self.tags = self._get_exif_tags(file_path)
        # finish
        self.output = {'path': self.path, 'mime': self.mime, 'DateTimeOriginal': self._get_iso_time(self.tags['EXIF DateTimeOriginal'])}
        pass

    def _get_iso_time(self, exif_time):
        """ get (convert) to ISO 8601 time format """
        xtime = exif_time.values
        year = xtime[0:4]
        month = xtime[5:7]
        day = xtime[8:10]
        hour = xtime[11:13]
        minute = xtime[14:16]
        second = xtime[17:19]
        return year+'-'+month+'-'+day+'T'+hour+':'+minute+':'+second

    def _get_exif_tags(self, file_path):
        """ open file, read exif meta data """
        tags = None
        try:
            f = io.open( file_path, 'rb')
            tags = exifread.process_file(f)
            f.close()
        except IOError:
            self.error = {'path': file_path, 'error': repr(sys.exc_info()[1])}
        finally:
            return tags

    def _get_header_bytes(self, file_path):
        """ open file, read header bytes, close file """
        header_bytes = None
        try:
            f = io.open( file_path, 'rb')
            header_bytes = f.read(HEADERLEN)
            f.close()
        except IOError:
            self.error = {'path': file_path, 'error': repr(sys.exc_info()[1])}
        finally:
            return header_bytes

    def _get_mime(self, inp):
        """" get the file mime type """
        kind = filetype.guess(inp)
        if kind is None:
            self.error = {'path': self.path, 'error': 'Cannot guess file type'}
            return None
        return kind.mime

