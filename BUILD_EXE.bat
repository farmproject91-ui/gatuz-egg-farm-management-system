@echo off
setlocal
set "PROJECT_DIR=%~dp0GATUZ_EGG_FARM_MANAGEMENT_SYSTEM\GATUZ_EGG_FARM_MANAGEMENT_SYSTEM"
if not exist "%PROJECT_DIR%\BUILD_EXE.bat" (
  echo GATUZ build script was not found:
  echo "%PROJECT_DIR%\BUILD_EXE.bat"
  pause
  exit /b 1
)
call "%PROJECT_DIR%\BUILD_EXE.bat"
exit /b %errorlevel%
