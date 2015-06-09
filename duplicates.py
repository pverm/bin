import os
import sys
import shutil
import codecs
import hashlib
import argparse

"""
to do:
reformat help message
better filtering (option to ignore subdirs)
more options to compare
permission denied - pagefile.sys
"""

def read_dir(dir=os.getcwd(), absolute=True):
    """Returns a list of all files in dir including subdirectories"""
    filelist = []
    for dirpath, dirnames, filenames in os.walk(dir):
        if '.git' in dirnames:
            dirnames.remove('.git')
        for file in filenames:
            filelist.append(os.path.join(dirpath, file) if absolute else file)
    return filelist

def get_compare_val(file, compare_method):
    """Dispatch method that returns compare value for a given file"""
    if compare_method == "size":
        return get_size(file)
    elif compare_method == "hash":
        return get_hash(file)

def get_hash(file, algorithm='md5', readable=True, chunksize=512*128):
    """Returns hash of file"""
    hash = hashlib.new(algorithm)
    with open(file, 'rb') as fin:
        chunk = fin.read(chunksize)
        while len(chunk) > 0:
            hash.update(chunk)
            chunk = fin.read(chunksize)
    return hash.hexdigest() if readable else hash.digest()

def get_size(file):
    """Returns size of file"""
    return os.stat(file).st_size

def compare_files(filelist, compare_method):
    """Iterates over filelist and returns a dictionary where
        key   -> compare value (computed based on compare_method)
        value -> list of files that have this compare value
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
    """Returns new list that only contains files with specific ext"""
    res = []
    for file in filelist:
        if file.endswith('.'+ext):
            res.append(file)
    return res

def get_duplicates(dir=os.getcwd(), compare_method="hash", ext=False, target="y"):
    """Returns a list of duplicates

    Parameters:
        dir: searches for files in this directory
        compare_method: method used to compute compare value
        ext: only includes files with this extension
    """

    files = read_dir(dir)
    if ext:
        files = filter_by_ext(files, ext)

    print("Found {} files.".format(len(files)))

    comp = compare_files(files, compare_method).items()
    return [Duplicate(val, files, dir, target) for val, files in comp if len(files) > 1]


def action_on_duplicates(dup_list, action, **kwargs):
    """Executes action on all duplicates in dup_list"""
    for dup in dup_list:
        dup.__getattribute__(action)(**kwargs)


class Duplicate:
    """Represents an instance of multiple duplicate files

    Attributes:
        val:        value used to compare the files
        files:      list of duplicate files
        base:       basedirectory of duplicate search
        youngest:   tuple of youngest file and its file creation time
        oldest:     tuple of oldest file and its file creation ctime
        keep:       file not to act on
    """

    def __init__(self, compare_val, files, basedir, target):
        self.val = compare_val
        self.files = files
        self.base = basedir
        self.youngest = (files[0], os.stat(files[0]).st_ctime)
        self.oldest = self.youngest
        for i in range(1, len(files)):
            ctime = os.stat(files[i]).st_ctime
            if ctime > self.youngest[1]:
                self.youngest = (files[i], ctime)
            elif ctime < self.oldest[1]:
                self.oldest = (files[i], ctime)
        if target=="y":
            self.keep = self.oldest[0]
        elif target=="o":
            self.keep = self.youngest[0]
        elif target=="a":
            self.keep = None

    def __str__(self):
        res = str(self.val) + " " + self.files[0]
        for i in range(1,len(self.files)):
            res += "\n " + " " * len(str(self.val)) + self.files[i]
        return res

    def copy(self, dst):
        for file in self.files:
            if file != self.keep:
                path = file.replace(self.base, dst)
                if not os.path.exists(os.path.dirname(path)):
                    os.makedirs(os.path.dirname(path))
                shutil.copy(file, path)
                print("Copied {} [{}]".format(file, self.val))

    def move(self, dst):
        for file in self.files:
            if file != self.keep:
                path = file.replace(self.base, dst)
                if not os.path.exists(os.path.dirname(path)):
                    os.makedirs(os.path.dirname(path))
                shutil.move(file, path)
                print("Moved {} [{}]".format(file, self.val))

    def printout(self, **kwargs):
        print(self)

    def remove(self, **kwargs):
        for file in self.files:
            if file != self.keep:
                try:
                    os.remove(file)
                    print("Removed {} [{}]".format(file, self.val))
                except OSError:
                    print("Failed to remove {}".format(file))


class Logger:
    """Writes to terminal and to file"""

    def __init__(self, filename):
        self.terminal = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        self.encoding = sys.stdout.encoding
        self.log = open(filename, "w", encoding="utf-8")

    def __getattr__(self, attr):
        return getattr(self.terminal, attr)

    def write(self, message):
        self.terminal.write(message)
        self.terminal.flush()
        if not message.startswith('~!'):
            self.log.write(message)


class LoggerAction(argparse.Action):
    """Redirects stdout to Logger object"""

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super(LoggerAction, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)
        sys.stdout = Logger(values)


class DuplicateAction(argparse.Action):
    """Sets flags for action that will be taken on duplicates"""

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, "action", self.dest)
        setattr(namespace, "dst", values)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find duplicate files.')
    parser.add_argument("directory")
    parser.add_argument("-l", "--log", metavar="FILE", action=LoggerAction,
                        help="save output to file")
    parser.add_argument("-m", "--method", choices=["hash", "size"],
                        default="hash", help="method used to compare files")
    parser.add_argument("-f:i", "--filter:include", metavar="EXTENSION", dest="include",
                        help="only include specific filetypes", default="")
    parser.add_argument("-t", "--target", choices=["y", "o", "a"], dest="target", default="y",
                        help="files to act on (y: youngest, o: oldest, a: all) [default: y]")

    action_group = parser.add_mutually_exclusive_group()
    action_group.add_argument("-c", "--copy", metavar="PATH", dest="copy",
                        action=DuplicateAction, help="create copy of duplicates in PATH")
    action_group.add_argument("-mv", "--move", metavar="PATH", dest="move",
                        action=DuplicateAction, help="move duplicates to PATH")
    action_group.add_argument("-rm", "--remove", nargs=0, dest="remove",
                        action=DuplicateAction, help="remove duplicate files")

    args = parser.parse_args()

    duplicates = get_duplicates(args.directory, args.method, args.include, args.target)
    print("Found {} instances of duplicates.".format(len(duplicates)))

    action_on_duplicates(duplicates, "printout")
    if "action" in args:
        action_on_duplicates(duplicates, args.action, dst=args.dst)
