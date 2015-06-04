from __future__ import print_function

__module_name__ = 'figlet'
__module_version__ = '0.3'
__module_description__ = 'print words in ascii art using pyfiglet'
__author__ = 'kama'

import hexchat
from random import randint
try:
    from pyfiglet import Figlet, FigletFont
    figlet_loaded = True
except ImportError:
    print("Unable to load pyfiglet module. Please make sure you installed it.")
    figlet_loaded = False


def pyfig_say(word, font='standard'):
    fig = Figlet(font=font)
    lines = fig.renderText(word).split('\n')[:-1]
    for line in lines:
        if line != '':
            hexchat.command('say %s' % line)

def pyfig(word, word_eol, userdata):
    if len(word) == 1:
        print('figlet usage:  /figlet <word> [<font>|random]')
        print('See http://pastebin.com/raw.php?i=5EA5KvEP for available fonts')
    elif len(word) == 2:
        pyfig_say(word[1])
    elif len(word) >= 3:
        if word[2] in AVAILABLE_FONTS:
            pyfig_say(word[1], word[2])
        elif word[2] == "random":
            font = AVAILABLE_FONTS[randint(0,len(AVAILABLE_FONTS)-1)]
            print('figlet: using', font)
            pyfig_say(word[1], font)
        else:
            print(word[2]+': invalid font')


def unload_callback(userdata):
	print("%s version %s unloaded." % (__module_name__, __module_version__))


if figlet_loaded:
    AVAILABLE_FONTS = FigletFont.getFonts()
    hexchat.hook_command("figlet", pyfig, help="/figlet <word> [<font>]")
    hexchat.hook_unload(unload_callback)
    print("%s version %s loaded." % (__module_name__, __module_version__))
