@echo off
setlocal enabledelayedexpansion

:: Place disksys.rom in the same folder as this script

for %%f in (add\*.fds add\*.nes) do (
    set "file=%%f"
    set "name=%%~nf"

    call :remove_bracket "!name!" out
    if exist "add\!name!.cfg" (
        call hvca_compile.py "!file!" "add\!name!.cfg" -x "bin\flash_ez4_ezo.sub" -o "add\!out!.gba" -pat
    ) else (
        call hvca_compile.py "!file!" -x "bin\flash_ez4_ezo.sub" -o "add\!out!.gba" -pat
    )
)

goto :eof

:remove_bracket
set "str=%~1"
set "result=%str: (=&rem.%"
for /f "delims=& tokens=1,*" %%a in ("%result%") do set "%2=%%a"
goto :eof
