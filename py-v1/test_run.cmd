@echo off
set SCRIPT_DIR=c:\APP\_script

python heisme_JPG-Resize.py -i ".\test" -r 700 -f -q 85 -v

REM echo %CMDS% 
call %CMDS%


:END
pause