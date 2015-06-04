import os
import hashlib

"""
to do:
move/remove duplicates
filter
more options to compare
cli options
"""

def get_hash(file, algorithm='md5', readable=False, chunksize=512*128):
    hash = hashlib.new(algorithm)
    with open(file, 'rb') as fin:
        chunk = fin.read(chunksize)
        while len(chunk) > 0:
            hash.update(chunk)
            chunk = fin.read(chunksize)
    return hash.hexdigest() if readable else hash.digest()

def get_size(file):
    return os.stat(file).st_size

"""
MD5_BIN = "md5.exe"
def get_md5(file):
    return subprocess.check_output([MD5_BIN, file]).split()[0]
"""

def read_dir(dir=os.getcwd(), absolute=True):
    res = []
    for dirpath, dirnames, filenames in os.walk(dir):
        for file in filenames:
            res.append(os.path.join(dirpath, file) if absolute else file)
    return res

def get_compareval(filelist, compare):
    d = {}
    for file in filelist:
        if compare == "size":
            d[file] = get_size(file)
        elif compare == "hash":
            d[file] = get_hash(file, 'md5', 'True')
    return d

def filter_by_ext(filelist, ext="txt"):
    res = []
    for file in filelist:
        if file.endswith('.'+ext):
            res.append(file)
    return res

def search_duplicates(d):
    duplicates = {}
    d_temp = {}

    for file, compare_val in d.items():
        if compare_val in d_temp:
            d_temp[compare_val].append(file)
        else:
            d_temp[compare_val] = [file]

    for compare_val, files in d_temp.items():
        if len(d_temp[compare_val]) > 1:
            duplicates[compare_val] = files

    return duplicates

def list_duplicates(d):
    for compare_val, files in d.items():
        for file in files:
            print(compare_val, file)

def remove_duplicates():
    pass

def duplicates(dir=os.getcwd(), compare="hash", ext="jpg", v=False):
    files = read_dir(dir)
    filtered_files = filter_by_ext(files, ext)
    hashed_files = get_compareval(filtered_files, compare)
    duplicate_files = search_duplicates(hashed_files)

    if v:
        list_duplicates(duplicate_files)

    return duplicate_files

duplicates(v=True)
