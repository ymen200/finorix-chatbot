@echo off
REM Lancement Django (chemins relatifs au repo)
SET ROOT=%~dp0..
SET PROJECT_PATH=%ROOT%\chatbotBHl\mychatbot
SET WAIT_SCRIPT=%ROOT%\scripts\wait_server.py

if not exist "%PROJECT_PATH%\logs" mkdir "%PROJECT_PATH%\logs"

cd /d "%PROJECT_PATH%"

REM Activer le venv s'il existe à la racine du repo
if exist "%ROOT%\venv\Scripts\activate.bat" (
    call "%ROOT%\venv\Scripts\activate.bat"
)

start "" python manage.py runserver 127.0.0.1:8000 --noreload
python "%WAIT_SCRIPT%"
start "" http://127.0.0.1:8000/
exit
