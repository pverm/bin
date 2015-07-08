#!python3
import os
import sys
import random
import time
import win32api

def create_desk_ini(path, icon):
    """create new desktop.ini in folder and set relative icon path"""
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

def set_icon(folder):
    """set icon for folder"""
    icon = get_icon(folder)
    if icon:
        desk_ini = os.path.join(folder, 'desktop.ini')
        create_desk_ini(desk_ini, icon)
        win32api.SetFileAttributes(folder, 17) #17 = Read-Only, Directory
        icon_found[folder] = open(desk_ini, 'r')

if __name__ == '__main__':
    rootfolder = sys.argv[1]
    icon_found = {} # key => folder, value => opened desktop.ini file object
    set_icon(rootfolder)
    for dirpath, dirnames, filenames in os.walk(rootfolder):
        for dirname in dirnames:
            set_icon(os.path.join(dirpath, dirname))
    time.sleep(60)
    for folder in icon_found:
        icon_found[folder].close()
        update_folder_content(folder)
    sys.exit(0)
