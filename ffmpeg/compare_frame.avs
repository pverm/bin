a=ffvideosource("crf23-film-veryslow.mkv").subtitle("Encode A", align=9)
b=ffvideosource("crf23-none-veryslow.mkv").subtitle("Encode B", align=9)
interleave(a,b)
ffinfo(framenum=true,frametype=true,cfrtime=false,vfrtime=false)