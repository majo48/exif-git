"""
    purge all files > MAX_SIZE:
        1. make a list (recursive)
        2. edit the list
        3. purge the list
"""
# packages ====
import os
import io
import exifread

# constants ====
MAX_SIZE = 70 * 1024 * 1024 # 70 MBytes
IMAGE_EXTENSIONS = [ ".pkg", ".ova", ".dmg", ".iso", ".exe" ]
MOVIE_EXTENSIONS = [ ".mp2", ".MP2", ".mp4", ".MP4", ".mov", ".MOV", ".mpg", ".MPG"]
FOLDERS = [
    "/volumes/myArchive/Bilder"
]

def is_movie(file_path):
    """
        check if the file_path represents a movie
    """
    filename, file_extension = os.path.splitext(file_path)
    return file_extension in MOVIE_EXTENSIONS

def get_movie_duration(file_path):
    """
        get the duration of the movie in seconds
    """
    if is_movie(file_path):
        f = io.open(file_path, 'rb')
        tags = exifread.process_file(f)
        f.close()
        pass
    return 0 # not a movie

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

def get_candidates(folders):
    """ get a list with filenames and path """
    candidates = []
    total_size = 0 # MBytes
    for file_path in folders:
        print("Please wait, analyzing", file_path)
        if os.path.isfile(file_path):
            size = os.path.getsize(file_path)
            if size > MAX_SIZE:
                size = round(size/1024/1024,1) # MBytes
                candidates.append((file_path, size))
                total_size += size
            pass
        elif os.path.isdir(file_path):
            for subdir, dirs, files in os.walk(file_path):
                for file in files:
                    size = os.path.getsize(os.path.join(subdir, file))
                    if size > MAX_SIZE:
                        size = round(size / 1024 / 1024, 1)  # MBytes
                        candidates.append((os.path.join(subdir, file), size))
                        total_size += size
                    pass
                pass
            pass
        else:
            print("Invalid path:", file_path)
    return candidates, total_size

def run():
    """ main code """
    candidates, total_size = get_candidates(FOLDERS)

    print("Total size:", round(total_size,1), "MBytes")

    print("List of candidates:")
    for candidate in candidates:
        print(str(candidate[1]), "MBytes", candidate[0])

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