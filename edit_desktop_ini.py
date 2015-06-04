import os
import sys
import re
import stat
import win32api
import win32con
import win32com.shell.shell as shell

def get_desk_ini_content(file):
    content = []
    with open(file, 'r') as desk_ini:
        for line in desk_ini:
            content.append(line)
    return content

def edit_icon_path(content):
    new_content = []
    for line in content:
        if "IconResource" in line:
            find = re.search('IconResource=(.+?),0', line)
            fullpath = find.group(1)
            basename = os.path.basename(fullpath)
            new_content.append('IconResource='+basename+',0\n')
        else:
            new_content.append(line)
    return new_content

def write_new_desk_ini(file, content):
    win32api.SetFileAttributes(file, win32con.FILE_ATTRIBUTE_NORMAL)
    with open(file, 'w') as desk_ini:
        for line in content:
            desk_ini.write(line)
    #38: Archivable, Hidden, System (HSA)
    win32api.SetFileAttributes(file, 38)

def main(folder):

    if 'desktop.ini' not in os.listdir(folder):
        exit()
    desk_ini = os.path.join(folder, 'desktop.ini')
    content = get_desk_ini_content(desk_ini)
    new_content = edit_icon_path(content)
    write_new_desk_ini(desk_ini, new_content)


if __name__ == '__main__':
    main(sys.argv[1])
    """
    if sys.argv[-1] != 'asadmin':
        print('notadmin')
        script = os.path.abspath(sys.argv[0])
        params = ' '.join([script] + sys.argv[1:] + ['asadmin'])
        shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
        sys.exit(0)
    """
