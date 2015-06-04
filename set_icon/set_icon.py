#!python3
import os
import sys
import random
import time
import win32api

def create_desk_ini(path, icon):
    """create new desktop.ini in folder and set icon"""
    content = ( '[.ShellClassInfo]\n'
                'IconResource='+icon+',0\n'
                '[ViewState]\n'
                'Mode=\n'
                'Vid=\n'
                'FolderType=Generic\n' )
    if os.path.exists(path):
        win32api.SetFileAttributes(path, 128) #128 = win32con.FILE_ATTRIBUTE_NORMAL
    with open(path, 'w') as desk_ini:
        desk_ini.write(content)
    win32api.SetFileAttributes(path, 38) #38 = Hidden, System, Archive

def get_icon(folder):
    """return first icon found in folder"""
    foldercontent = os.listdir(folder)
    for item in foldercontent:
        if item.endswith('.ico'):
            return item
    return None

def update_folder_content(folder):
    """create temporary file in folder and delete it"""
    exists = True
    while exists:
        fn = 'temp' + ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(10))
        temp_path = os.path.join(folder, fn)
        exists = True if os.path.exists(temp_path) else False
    temp_file = open(temp_path, 'w')
    temp_file.close()
    os.remove(temp_path)


if __name__ == '__main__':
    folder = sys.argv[1]
    desk_ini = os.path.join(folder, 'desktop.ini')
    icon = get_icon(folder)
    if icon:
        create_desk_ini(desk_ini, icon)
        win32api.SetFileAttributes(folder, 17) #17 = Read-Only, Directory
        #lock desktop.ini and wait 60 seconds before updating folder content
        flock = open(desk_ini, 'r')
        time.sleep(60)
        flock.close()
        update_folder_content(folder)
    sys.exit(0)
