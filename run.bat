@echo off
set "FILENAME=all.txt"
:loop
echo.
echo [Step 1] Attempting to delete %FILENAME%...
if exist "%FILENAME%" (
    del /Q "%FILENAME%"
    echo Success: %FILENAME% deleted.
) else (
    echo Notice: %FILENAME% does not exist or was already deleted.
)
echo.
echo [Step 2] Running Python script for the first time...
python main.py
echo.
echo [Step 3] Running Python script again to ensure correct formatting...
python main.py
echo.
echo Process complete. Press any key to repeat the process or close this window to exit.
pause > nul
echo.
goto loop
