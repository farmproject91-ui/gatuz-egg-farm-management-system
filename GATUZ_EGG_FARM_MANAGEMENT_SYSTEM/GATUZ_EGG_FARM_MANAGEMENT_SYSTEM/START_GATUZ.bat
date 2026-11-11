@echo off
setlocal
cd /d "%~dp0"
echo ==========================================
echo   GATUZ EGG FARM MANAGEMENT SYSTEM
echo ==========================================
where py >nul 2>nul
if not errorlevel 1 (
  set "PY=py -3"
) else (
  where python >nul 2>nul
  if errorlevel 1 (
    echo Python 3.12 or newer is required. Install it from https://www.python.org/
    pause
    exit /b 1
  )
  set "PY=python"
)
%PY% -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 12) else 1)"
if errorlevel 1 (
  echo Python 3.12 or newer is required. Check your Python installation.
  pause
  exit /b 1
)
%PY% -m pip install -r requirements.txt
if errorlevel 1 (
  echo Dependency installation failed. Check your internet connection and Python installation.
  pause
  exit /b 1
)
%PY% app.py
if errorlevel 1 pause
