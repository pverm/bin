import os
import json

if __name__ == '__main__':
    music_dir = 'MUSIC'
    outfile = 'find_incompatible.json'
    allowed_extensions = ['.flac', '.mp3']
    deletable = ['.jpg', '.png', '.gif', '.db', '.ini', '.tmp', '.txt']
    log = { 'deleted': [], 'incompatible': [] }

    for dirpath, dirnames, filenames in os.walk(music_dir):
        for file in filenames:
            ext = os.path.splitext(file)[1].lower()

            if ext in deletable:
                os.remove(os.path.join(dirpath, file))
                log['deleted'].append(os.path.join(dirpath, file))

            elif ext not in allowed_extensions:
                log['incompatible'].append(os.path.join(dirpath, file))

    with open(outfile, 'w') as fout:
        json.dump(log, fout)
