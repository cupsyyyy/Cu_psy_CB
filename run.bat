@echo off
cd /d "%~dp0src"

:: Vérifie si le venv existe, sinon le crée
if not exist "venv" (
    echo [*] Creating virtual environment...
    python -m venv venv
)

echo [*] Activating virtual environment...
call venv\Scripts\activate

:: Installe les dépendances si nécessaire
echo [*] Installing requirements...
pip install --upgrade pip
pip install -r requirements.txt

echo [*] Starting CUPSY_CB
python main.py
pause
