import os

outfile = "C:\\Users\\Pascal\\Downloads\\naming.txt"

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
    f.close()

filename = ""

lenv = file_len("video.txt")
lena = file_len("audio.txt")

metav = open("video.txt", "r")
i = 1
while i < lenv:
    curline = metav.readline()
    if "width" in curline:
        filename += "("+curline[-5:-2]+"x"
    if "height" in curline:
        filename += curline[-5:-2]+")"
    i+=1
metav.close()

metaa = open("audio.txt", "r")
i = 1
while i < lena:
    curline = metaa.readline()
    if "codec_name" in curline:
        filename += "("+curline[-6:-3]+"-"
    if "language" in curline:
        filename += curline[-6:-3]+")"
    i+=1
metaa.close()

fp = os.getcwd()
path,fn = os.path.split(fp)

with open(outfile, "a") as fout:
    fout.write(fn + " " + filename)
