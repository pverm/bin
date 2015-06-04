@echo off
move D:\btsync\xdcc\* D:\downloads
for /D %%d IN (D:\btsync\xdcc\*) DO move "%%d" D:\downloads
