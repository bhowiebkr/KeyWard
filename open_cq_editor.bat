@echo off

REM Store the current directory in a variable
set "CURRENT_DIR=%CD%"
echo Current directory is: %CURRENT_DIR%

REM Change to the target directory
CD /D C:\ProgramData\cq-editor

@echo off
start /B Scripts\conda.exe run -n base python Scripts\cq-editor-script.py