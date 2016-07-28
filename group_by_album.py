import os
import shutil
import sys

def move_to_album(file_name, album_name):
    if not os.path.exists(album_name):
        os.mkdir(album_name)
    shutil.move(file_name, album_name)
    
def get_album_name(file_name):
    return file_name.rsplit('_', 1)[0].strip('.jpg').strip('.png')

if __name__ == '__main__':
    if not input("Enter 'y' to group files by album and put in folders: ").lower() == 'y':
        sys.exit()
    for file in [f for f in os.listdir() if os.path.isfile(f) and f != os.path.basename(__file__)]:
        move_to_album(file, get_album_name(file))
