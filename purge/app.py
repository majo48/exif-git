"""
    purge all files > MAX_SIZE:
        1. make a list (recursive)
        2. edit the list
        3. purge the list
"""
# packages ====
import os
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata

# constants ====
MAX_SIZE = 70 * 1024 * 1024 # 70 MBytes
IMAGE_EXTENSIONS = [ ".pkg", ".ova", ".dmg", ".iso", ".exe" ]
MOVIE_EXTENSIONS = [ ".mp2", ".MP2", ".mp4", ".MP4", ".mov", ".MOV", ".mpg", ".MPG"]
FOLDERS = [
    'C:\\Users\\mart\\Pictures\\2019'
] # /volumes/myArchive/Bilder
DURATION = '- Duration: '
LEN_DURATION = len(DURATION)

def is_movie(file_path):
    """
        check if the file_path represents a movie
    """
    filename, file_extension = os.path.splitext(file_path)
    return file_extension in MOVIE_EXTENSIONS

def get_movie_duration(file_path):
    """
        get the duration of the movie in seconds
        two methodes are feasible:
        1. use hachoir package
        2. use ExifTool with subprocess
    """
    parser = createParser(file_path)
    if parser:
        with parser:
            try:
                metadata = extractMetadata(parser)
            except Exception as error:
                metadata = 'metadata extraction error (1)'
        pass
        for line in metadata.exportPlaintext():
            if DURATION in line:
                return line[LEN_DURATION:]
            pass
        pass
        metadata = 'metadata extraction error (2)'
    else:
        metadata = 'unable to parse file'
    #
    return metadata

def is_software_image(file_path):
    """
        check if the file_path contains a software image extension
    """
    filename, file_extension = os.path.splitext(file_path)
    if file_extension in IMAGE_EXTENSIONS:
        return True
    elif (file_extension == ".zip") and ("vmware" in filename):
        return True
    else:
        return False

def get_duration(file_path):
    """
        get duration (of movie)
    """
    if is_movie(file_path):
        return get_movie_duration(file_path)
    else:
        return None

def get_candidates(folders):
    """ get a list with filenames and path """
    try:
        candidates = []
        total_size = 0 # MBytes
        file_path = ""
        for folder in folders:
            print("Please wait, analyzing", folder)
            if os.path.isfile(folder):
                size = os.path.getsize(folder)
                if size > MAX_SIZE:
                    size = round(size/1024/1024,1) # MBytes
                    candidates.append((folder, size, get_duration(folder)))
                    total_size += size
                pass
            elif os.path.isdir(folder):
                for subdir, dirs, files in os.walk(folder):
                    for file in files:
                        file_path = os.path.join(subdir, file)
                        size = os.path.getsize(file_path)
                        if size > MAX_SIZE:
                            size = round(size / 1024 / 1024, 1)  # MBytes
                            candidates.append((file_path, size, get_duration(file_path)))
                            total_size += size
                        pass
                    pass
                pass
            else:
                print("Invalid path:", file_path)
        return candidates, total_size
    except Exception as error:
        print("Exception occured:", error)
    pass

def run():
    """ main code """
    candidates, total_size = get_candidates(FOLDERS)

    print("Total size:", round(total_size,1), "MBytes")

    print("List of candidates:")
    for candidate in candidates:
        print(str(candidate[1]), "MBytes -", candidate[0], "- duration", candidate[2])

    image_size = 0.0
    print("List of Software Images:")
    for candidate in candidates:
        if is_software_image(candidate[0]):
            image_size += candidate[1]
            print(str(candidate[1]), "MBytes", candidate[0])
        pass
    print("Images size:", round(image_size, 1), "MBytes")

if __name__ == '__main__':
    run()
    exit(0)