__module_name__ = "guesstrivia"
__module_version__ = "0.1"
__module_description__ = "guess year range for trivia bot"
__author__ = 'kama'
import hexchat

def guess(word, word_eol, userdata):
	for year in range(int(word[1]),int(word[2])+1):
		hexchat.command('say %s' % year)

hexchat.hook_command("GUESS", guess, help="/GUESS <STARTYEAR> <ENDYEAR>")
