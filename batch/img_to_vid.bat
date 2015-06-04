ffmpeg -framerate 30 -start-number 76 -i %d.png -c:v libvpx -vf "fps=30" out.webm
rem -c:v libx264 out.mp4
rem -s 480x360
