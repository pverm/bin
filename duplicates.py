import os
import sys
import hashlib
import argparse

"""
to do:
move/remove duplicates
better filtering (option to ignore subdirs)
more options to compare
permission denied - pagefile.sys
"""

def read_dir(dir=os.getcwd(), absolute=True):
    """returns a list of all files in dir including subdirectories"""
    filelist = []
    for dirpath, dirnames, filenames in os.walk(dir):
        if '.git' in dirnames:
            dirnames.remove('.git')
        for file in filenames:
            filelist.append(os.path.join(dirpath, file) if absolute else file)
    return filelist

def get_compare_val(file, compare_method):
    """dispatch method that returns compare value for a given file"""
    if compare_method == "size":
        return get_size(file)
    elif compare_method == "hash":
        return get_hash(file)

def get_hash(file, algorithm='md5', readable=True, chunksize=512*128):
    """returns hash of given file"""
    hash = hashlib.new(algorithm)
    with open(file, 'rb') as fin:
        chunk = fin.read(chunksize)
        while len(chunk) > 0:
            hash.update(chunk)
            chunk = fin.read(chunksize)
    return hash.hexdigest() if readable else hash.digest()

def get_size(file):
    """returns size of given file"""
    return os.stat(file).st_size
    
def compare_files(filelist, compare_method):
    """Iterates over filelist and returns a dictionary where
        key   -> compare value (computed based on compare_method)
        alue -> list of files that have this compare value
    """
    d = {}
    count, total = 1, len(filelist)
    for file in filelist:
        skip = "~!" if count < total else ""
        print("{}\rProcessing file {}/{}\r".format(skip, count, total), end="")
        compare_val = get_compare_val(file, compare_method)
        d.setdefault(compare_val, []).append(file)
        count += 1
    print("")
    return d

def filter_by_ext(filelist, ext):
    """returns new list that only contains files with specific ext"""
    res = []
    for file in filelist:
        if file.endswith('.'+ext):
            res.append(file)
    return res

def list_duplicates(dup_list):
    """prints all duplicates in list"""
    for dup in dup_list:
        print(dup)

def get_duplicates(dir=os.getcwd(), compare_method="hash", ext=False):
    """Returns a list of duplicates
    
    Attributes:
        dir: searches for files in this directory
        compare_method: method used to compute compare value
        ext: only includes files with this extension
    """
    
    files = read_dir(dir)
    if ext:
        files = filter_by_ext(files, ext)
        
    print("Found {} files.".format(len(files)))
        
    comp = compare_files(files, compare_method).items()
    return [Duplicate(val, files) for val, files in comp if len(files) > 1]
    
    
class Duplicate(object):

    def __init__(self, compare_val, files):
        self.val = compare_val
        self.files = files
        
    def __str__(self):
        str = self.val + " " + self.files[0]
        for i in range(1,len(self.files)):
            str += "\n " + " " * len(self.val) + self.files[i] 
        return str
        
    def copy(self, dst):
        pass
        
    def move(self, dst):
        pass
        
    def delete(self):
        pass
        
    
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
    parser.add_argument("-f:i", "--filter:include", metavar="EXTENSION", dest="include",
                        help="only include specific filetypes", default="")
    args = parser.parse_args()
    
    dup = get_duplicates(args.directory, args.method, args.include)
    print("Found {} instances of duplicates.".format(len(dup)))
    list_duplicates(dup)
