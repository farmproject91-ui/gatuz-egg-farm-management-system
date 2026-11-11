@echo off
setlocal
set "PROJECT_DIR=%~dp0GATUZ_EGG_FARM_MANAGEMENT_SYSTEM\GATUZ_EGG_FARM_MANAGEMENT_SYSTEM"
if not exist "%PROJECT_DIR%\START_GATUZ.bat" (
  echo GATUZ project launcher was not found:
  echo "%PROJECT_DIR%\START_GATUZ.bat"
  pause
  exit /b 1
)
call "%PROJECT_DIR%\START_GATUZ.bat"
exit /b %errorlevel%
