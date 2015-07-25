__module_name__ = 'musicbeeplaying'
__module_version__ = '0.2'
__module_description__ = 'post currently playing song from musicbee'
__author__ = 'kama'

import hexchat
import os

colors = {
    '{white}':  '\x0300',
    '{black}':  '\x0301',
    '{blue}':   '\x0302',
    '{green}':  '\x0303',
    '{red}':    '\x0304',
    '{brown}':  '\x0305',
    '{purple}': '\x0306',
    '{orange}': '\x0307',
    '{yellow}': '\x0308',
    '{lime}':   '\x0309',
    '{teal}':   '\x0310',
    '{cyan}':   '\x0311',
    '{royal}':  '\x0312',
    '{pink}':   '\x0313',
    '{grey}':   '\x0314',
    '{silver}': '\x0315'
}

def colorize(text):
    for color in colors:
        text = text.replace(color, colors[color])
    return text

def get_info(word, word_eol, userdata):
    with open(os.path.join(appdata, 'MusicBee', 'Tags.txt'), 'r', encoding='utf8') as fin:
        playing_info = fin.read()
    if len(playing_info) > 10:
        hexchat.command('say {}'.format(colorize(playing_info)))
    else:
        print("MusicBee is not playing anything.")

def unload_callback(userdata):
	print("{} version {} unloaded.".format(__module_name__, __module_version__))

appdata = os.getenv('APPDATA')
tagsfile = os.path.join(appdata, 'MusicBee', 'Tags.txt')

if os.path.exists(tagsfile):
    hexchat.hook_command("musicbee", get_info, help="/musicbee to post song in current channel")
    hexchat.hook_unload(unload_callback)
    print("{} version {} loaded.".format(__module_name__, __module_version__))
else:
    print(("No currently playing information found. Make sure you installed the plugin: "
           "http://musicbee.wikia.com/wiki/Now_Playing_to_External_Files"))
