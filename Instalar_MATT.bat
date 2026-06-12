@echo off
title Instalador de MATT AI

net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Solicitando permisos de administrador...
    powershell -Command "Start-Process -Verb RunAs -FilePath '%~f0'"
    exit /b
)

cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" install.py
    exit
)

if exist "%LocalAppData%\Programs\Python\Python312\python.exe" (
    "%LocalAppData%\Programs\Python\Python312\python.exe" install.py
    exit
)
if exist "%LocalAppData%\Programs\Python\Python313\python.exe" (
    "%LocalAppData%\Programs\Python\Python313\python.exe" install.py
    exit
)
if exist "%LocalAppData%\Programs\Python\Python311\python.exe" (
    "%LocalAppData%\Programs\Python\Python311\python.exe" install.py
    exit
)

where python >nul 2>&1
if %errorlevel% equ 0 (
    python install.py
    exit
)

if exist "%ProgramFiles%\Python312\python.exe" (
    "%ProgramFiles%\Python312\python.exe" install.py
    exit
)
if exist "%ProgramFiles%\Python313\python.exe" (
    "%ProgramFiles%\Python313\python.exe" install.py
    exit
)

echo.
echo [ERROR] No se pudo encontrar una instalacion de Python valida.
echo Instala Python 3.12 o 3.13 con "Add Python to PATH".
echo.
pause
exit
