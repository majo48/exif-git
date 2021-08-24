""" MyFile: set file datetime created to metadata.creation_time """
import io, sys, os, filetype, exifread, platform, datetime, shutil

# See https://hachoir.readthedocs.io/en/latest/developer.html
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
# See https://pillow.readthedocs.io/en/stable/
from PIL.PngImagePlugin import PngImageFile, PngInfo

# Constants
HEADER_LEN = 262
CHANGE_TIMESTAMP = False
CHANGE_FILENAME = True
LEAD_IN = 'xfile_'


class MyFile:
    """
        Heavy lifting part of the recreate application.
        For one file only, see iteration in app.
    """

    def __init__(self, file_path):
        """ initialise class variables """
        self.path = file_path
        self.error = None
        self.bytes = self._get_header_bytes(file_path)
        self.mime = self._get_mime(self.bytes)
        self.extension = os.path.splitext(file_path)[1].lower()
        self.tags = self._get_exif_tags(file_path)
        self.created = self._get_datestring(self._get_creation_floating(file_path))

        if (self.mime != None) and (('image/' in self.mime) or ('video/' in self.mime)):
            # set self.originated conditionally
            self.originated = None
            self._set_self_originated(self.mime, self.path, self.tags)

            # set output file attributes
            self.outfile = self._update_file_attributes(self.path, self.originated)
            self.output = {
            'mime': self.mime, 'recorded': self.originated, 'created': self.created, 'outfile': self.outfile
            }
        else:
            # for non-mime types
            self.output = None

    def _update_file_attributes(self, file_path, recorded):
        """ set the file attributes (filename, creation_date) accordingly """
        outfile = file_path # same as input file
        if CHANGE_FILENAME and (LEAD_IN not in outfile):
            # build new output filename
            extension = os.path.splitext(outfile)
            basename = os.path.basename(outfile)
            dirname = os.path.dirname(outfile)
            sortpart = LEAD_IN+recorded.replace(':', '_').replace('-', '_')
            outfile = dirname+'/'+sortpart+'_'+basename
            # make a copy of the media file (data and file permissions)
            shutil.copy(file_path, outfile)

        if CHANGE_TIMESTAMP:
            pass
            # todo: add code here to change creation_date for outfile

        return outfile

    def _set_self_originated(self, mime, file_path, tags):
        """ set (conditionally) the original timestamp from file metadata """
        if mime is None:
            pass

        elif mime == 'image/tiff':
            pass

        elif (mime == 'image/jpeg') or (mime == 'image/heic'):
            if (tags is not None) and ('EXIF DateTimeOriginal' in tags):
                tag = tags['EXIF DateTimeOriginal']
                self.originated = self._get_iso_time(tag.values)

        elif mime == 'image/png':
            self.originated = self._get_EXIF_DateTimeOriginal(file_path)

        elif mime == 'video/quicktime':
            self.originated = self._get_recording_datetime(file_path)

    def _get_EXIF_DateTimeOriginal(self, file_path):
        """ try to get the recording date from the EXIF in PNG file """
        try:
            image = PngImageFile(file_path)
            metadata = PngInfo()
            exif_array = []
            for i in image.text:
                compile = i, str(image.text[i])
                exif_array.append(compile)
            if len(exif_array) > 0:
                header = exif_array[0][0]
                if header.startswith("XML"):
                    xml = exif_array[0][1]
                    for line in xml.splitlines():
                        if 'DateCreated' in line:
                            idx1 = line.find('>')
                            idx2 = line.rfind('<')
                            if (idx1 != -1) and (idx2 != -1):
                                dt = line[idx1+1:idx2]
                                return dt
        except Exception as err:
            pass # returns None
        return None

    def _get_recording_datetime(self, file_path):
        """ try to get the recording date from the QuickTime file """
        parser = createParser(self.path)
        with parser:
            try:
                metadata = extractMetadata(parser).get('creation_date')
                return metadata.strftime('%Y-%m-%dT%H:%M:%S')
            except Exception as err:
                # print("Metadata extraction error: %s" % err)
                return None

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
            header_bytes = f.read(HEADER_LEN)
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
