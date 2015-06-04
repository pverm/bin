@echo off
echo ICON CACHE LOESCHEN? (n zum abbrechen)
set /p start=
if "%start%" == "n" goto END
taskkill /F /IM explorer.exe
attrib -h "%userprofile%\AppData\Local\IconCache.db"
copy "%userprofile%\AppData\Local\IconCache.db" "%userprofile%\AppData\Local\BackupIconCache.db"
del "%userprofile%\AppData\Local\IconCache.db"
start explorer
echo icon cache geloescht, taste druecken zum beenden
pause > nul
:END
