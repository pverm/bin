import os
import sys
import hashlib
import argparse

"""
to do:
move/remove duplicates
filter
more options to compare
add shit to parser
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
            
    print("Found {} files.".format(len(res)))
    return res

def get_compareval(filelist, compare):
    d = {}
    total = len(filelist)
    count = 1
    for file in filelist:
        skip = "~!" if count < total else ""
        print("{}\rProcessing file {}/{}\r".format(skip, count, total), end="")
        if compare == "size":
            d[file] = get_size(file)
        elif compare == "hash":
            d[file] = get_hash(file, 'md5', 'True')
        count += 1
    print("")
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

def get_duplicates(dir=os.getcwd(), compare_method="hash", ext=False, v=False):
    files = read_dir(dir)
    if ext:
        files = filter_by_ext(files, ext)
    hashed_files = get_compareval(files, compare_method)
    duplicate_files = search_duplicates(hashed_files)

    if v:
        list_duplicates(duplicate_files)

    return duplicate_files
    
    
class Logger(object):

    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w")
        
    def __getattr__(self, attr):
        return getattr(self.terminal, attr)

    def write(self, message):
        self.terminal.write(message)
        if not message.startswith('~!'):
            self.log.write(message)
    
    
class LoggerAction(argparse.Action):

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super(LoggerAction, self).__init__(option_strings, dest, **kwargs)
        
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)
        sys.stdout = Logger(values)
        

        
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Find duplicate files.')
    parser.add_argument("directory")
    parser.add_argument("-l", "--log", metavar="file", action=LoggerAction,
                        help="save output to file")
    parser.add_argument("-m", "--method", choices=["hash", "size"],
                        default="hash", help="method used to compare files")
    args = parser.parse_args()
    
    dup = get_duplicates(args.directory, args.method)
    list_duplicates(dup)
