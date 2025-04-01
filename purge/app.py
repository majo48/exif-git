"""
    purge all files > MAX_SIZE:
        1. make a list (recursive)
        2. edit the list
        3. purge the list
"""
# packages ====
import os
from pprint import pprint

# constants ====
MAX_SIZE = 70 * 1024 * 1024 # 70 MBytes
FOLDERS = [
    "/volumes/myArchive/MyDocuments"
]

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
    print("List of candidates:")
    pprint(candidates)
    print("Total size:", round(total_size,1), "MBytes")

if __name__ == '__main__':
    run()
    exit(0)