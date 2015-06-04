import os
import operator

music_folder = "/home/pascal/musik"
extensions = {}

for dirpath, dirnames, files in os.walk(music_folder):
    for file in files:
        filename, ext = os.path.splitext(file)
        extensions[ext] = extensions.setdefault(ext, 0) + 1

sorted_extensions = sorted(extensions.items(), key=operator.itemgetter(1), reverse=True)

for ext in sorted_extensions:
    print("  %s:   \t%s" % ext)

end = input("\npress enter to exit")
