@echo off
move /Y D:\btsync\new\logs\* D:\documents\pastes\chatlogs\laptopchatlogs
for /F %%i in ('dir /b "D:\btsync\new\logs\*.*"') do goto notempty
rmdir D:\btsync\new\logs
:notempty
move D:\btsync\new\* D:\downloads
for /D %%d IN (D:\btsync\new\*) DO move "%%d" D:\downloads
