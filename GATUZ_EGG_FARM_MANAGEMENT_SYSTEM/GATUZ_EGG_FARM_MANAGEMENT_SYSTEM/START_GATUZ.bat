@echo off
setlocal
cd /d "%~dp0"
echo ==========================================
echo   GATUZ EGG FARM MANAGEMENT SYSTEM
echo ==========================================
where py >nul 2>nul
if %errorlevel%==0 (set PY=py) else (set PY=python)
%PY% -c "import sys; print(sys.version_info)" 
if errorlevel 1 (
  echo Python 3.12 or newer is required. Install it from https://www.python.org/
  pause
  exit /b 1
)
%PY% -m pip install --upgrade pip
%PY% -m pip install -r requirements.txt
if errorlevel 1 (
  echo Dependency installation failed. Check your internet connection and Python installation.
  pause
  exit /b 1
)
%PY% app.py
if errorlevel 1 pause
