""" MyFile: set file datetime created to metadata.creation_time """
import io, sys, os, filetype, exifread, platform, datetime

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
        self.created = self._get_datestring(self._get_creation_floating(file_path))
        self.originated = None
        # conditional
        if self.mime is None:
            pass

        elif self.mime == 'image/tiff':
            pass

        elif (self.mime == 'image/jpeg') or (self.mime == 'image/png'):
            if (self.tags is not None) and ('EXIF DateTimeOriginal' in self.tags):
                tag = self.tags['EXIF DateTimeOriginal']
                self.originated = self._get_iso_time(tag.values)

        elif self.mime == 'image/heic':
            if (self.tags is not None) and ('EXIF DateTimeOriginal' in self.tags):
                tag = self.tags['EXIF DateTimeOriginal']
                self.originated = self._get_iso_time(tag.values)

        elif self.mime == 'video/quicktime':
            pass

        else:
            pass
        # finish
        self.output = {'path': self.path, 'mime': self.mime, 'originated': self.originated, 'created': self.created}
        pass

    def _get_creation_floating(self, file_path):
        """ try to get creation date SO#237079 """
        if platform.system() == 'Windows':
            return os.path.getctime(file_path)
        else:
            stat = os.stat(file_path)
            try:
                return stat.st_birthtime
            except AttributeError:
                # We're probably on Linux. No easy way to get creation dates here,
                # so we'll settle for when its content was last modified.
                return stat.st_mtime

    def _get_datestring(self, floatingnumber):
        """ convert floating date to ISO 8601 string """
        t = datetime.datetime.fromtimestamp(floatingnumber)
        return t.strftime('%Y-%m-%dT%H:%M:%S')

    def _get_iso_time(self, timestring):
        """ get (convert) to ISO 8601 time format """
        year = timestring[0:4]
        month = timestring[5:7]
        day = timestring[8:10]
        hour = timestring[11:13]
        minute = timestring[14:16]
        second = timestring[17:19]
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
            return None
        return kind.mime
