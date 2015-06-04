@echo off
echo ####CONVERT VIDEO TO IMAGES####
echo.
set /p video=Enter videofile:
set /p fps=Take x frames per second, 0=all frames:

set file=%video:~0,-4%
mkdir "%file%

if "%fps%" == "0" goto ALL

ffmpeg -i "%video%" -vsync 1 -qscale:v 2 -r %fps% "%file%\%file% img%%3d.jpg"
echo press any key to exit
pause > nul
exit

:ALL
ffmpeg -i "%video%" -vsync 1 -qscale:v 2 "%file%\%file% img%%3d.jpg"
echo press any key to exit
pause > nul
exit

rem ffmpeg -i "%video%" -y -ss %seconds% -an -qscale 0 -f image2 -r 1/5 %folder%\%file%%%3d.jpg
