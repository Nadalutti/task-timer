@echo off
title Task Timer
cd /d "%~dp0"

python task-timer.py status
echo.
set /p risposta=Vuoi avviare un task ora? (s/n):

if /i "%risposta%"=="s" (
    python task-timer.py start
) else (
    echo Ok, nessun task avviato.
)

echo.
echo ------------------------------------------
echo Comandi rapidi (da questa cartella): tt start / tt stop / tt status
echo ------------------------------------------
pause
