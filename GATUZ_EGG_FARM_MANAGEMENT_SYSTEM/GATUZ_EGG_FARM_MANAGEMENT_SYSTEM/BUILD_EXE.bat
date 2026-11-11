@echo off
setlocal
cd /d "%~dp0"
py -m pip install -r requirements.txt pyinstaller
py -m PyInstaller --noconfirm --clean --windowed --onedir --name GATUZ_EGG_FARM app.py
echo.
echo EXE build output: dist\GATUZ_EGG_FARM\
pause
