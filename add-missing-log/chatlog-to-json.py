import re
import json
import sys

# JSON structure:
#  [{"time":"hh:mm:ss","nick":"user","msg":"bla"}]

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print("Transform chatlog to JSON")
		print("  python chatlog-to-json.py <chat.log> <out.json>")
		sys.exit(0)
	
	log = []
	with open(sys.argv[1], 'r', encoding="utf-8",  errors="ignore") as fin:
		for line in fin:
			mt = re.search(' ([0-9:]*)]', line)
			mn = re.search('<[@#+~&]?([a-zA-Z0-9]*)>', line)
			mm = re.search('>(.*)', line)
			if mt and mn and mm:
				time = mt.group(1)
				nick = mn.group(1)
				msg = mm.group(1).lstrip()
				log.append({"time":time,"nick":nick,"msg":msg})
				
	with open(sys.argv[2], 'w', encoding="utf-8") as fout:
		json.dump(log, fout, indent=2)
