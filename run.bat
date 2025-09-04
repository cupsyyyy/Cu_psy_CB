@echo off
cd /d "%~dp0"

:: Vérifie si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo [!] Python isn't installed or not in the PATH
    echo Download and install it there https://www.python.org/downloads/
    pause
    exit /b
)

:: Crée le venv si il n'existe pas
if not exist "venv" (
    echo [*] Creating venv...
    python -m venv venv
)

:: Active le venv
echo [*] Activating venv...
call venv\Scripts\activate

:: Installe les dependances
if exist requirements.txt (
    echo [*] Installing dependencies
    pip install --upgrade pip
    pip install -r requirements.txt
)

:: Lance le script principal
echo [*] Starting CUPSY_CB
python main.py

pause
