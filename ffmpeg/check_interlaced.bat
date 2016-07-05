@echo off
set /p file=Input file: 
ffmpeg -filter:v idet -frames:v 100 -an -f rawvideo -y NUL -i %file%