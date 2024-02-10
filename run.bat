@echo off
set "FILENAME=all.txt"
:loop
echo Deleting %FILENAME%...
del /Q "%FILENAME%"
echo Running Python script...
python main.py
echo Press any key to run again or close this window to exit.
pause > nul
goto loop
