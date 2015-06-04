from __future__ import print_function

__module_name__ = "box"
__module_version__ = "0.3"
__module_description__ = "print out box/rotated box"
__author__ = 'kama'

import xchat

def box(word, word_eol, userdata):
    for n in range(int(word[1])): xchat.command("say %s" % ((int(word[1]))*"# " if n==0 or n==int(word[1])-1 else "# "+"  "*(int(word[1])-2)+"#"))

def rbox(word, word_eol, userdata):
    for i in list(range(int(word[1])-1,0,-1))+list(range(int(word[1]))): xchat.command("say %s" % ("  "*i+"# "+((int(word[1])-1-i)*2-1)*"  "+"# "*((int(word[1])-1-i)*2-1 > 0)))

def unload_callback(userdata):
	print("%s version %s unloaded." % (__module_name__, __module_version__))


xchat.hook_command("box", box, help="/box <size>")
xchat.hook_command("rbox", rbox, help="/rbox <size>")
xchat.hook_unload(unload_callback)

print("%s version %s loaded." % (__module_name__, __module_version__))
