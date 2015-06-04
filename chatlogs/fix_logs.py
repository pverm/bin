import os

LOGDIR = "/home/pascal/sync/media/logs/"

def fix_files(src):
    for dirpath, dirnames, filenames in os.walk(LOGDIR):
        for f in filenames:
            if '\r' in f:
                newname = os.path.join(dirpath, f.replace('\r', ''))
                os.rename(os.path.join(dirpath, f), newname)

def fix_dir(path):
    os.rename(path, path.replace('\r', ''))

def get_invalid_dir(src):
    for dirpath, dirnames, filenames in os.walk(src):
        for d in dirnames:
            if d.endswith('\r'):
                return os.path.join(dirpath, d)
    return None

if __name__ == "__main__":
    if os.path.exists(LOGDIR):
        fix_files(LOGDIR)
        invalid = get_invalid_dir(LOGDIR)
        while invalid:
            fix_dir(invalid)
            invalid = get_invalid_dir(LOGDIR)
