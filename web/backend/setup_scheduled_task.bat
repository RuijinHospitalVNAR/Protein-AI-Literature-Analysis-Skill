@echo off

REM Setup scheduled task for weekly literature update

set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%..\.."
set "UPDATE_SCRIPT=%SCRIPT_DIR%update_script.py"
set "LOG_FILE=%SCRIPT_DIR%update.log"

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Create log directory
if not exist "%SCRIPT_DIR%logs" (
    mkdir "%SCRIPT_DIR%logs"
)

REM Setup scheduled task
SCHTASKS /CREATE /TN "Protein AI Literature Update" /TR "python \"%UPDATE_SCRIPT%\"" /SC WEEKLY /D SUN /ST 00:00 /F /RL HIGHEST

if %errorlevel% eq 0 (
    echo Scheduled task created successfully!
    echo Task will run every Sunday at 00:00
    echo Logs will be saved to: %LOG_FILE%
) else (
    echo Failed to create scheduled task
    echo Please run this script as administrator
    pause
    exit /b 1
)

REM Test the update script
 echo Testing update script...
python "%UPDATE_SCRIPT%"

if %errorlevel% eq 0 (
    echo Test completed successfully!
) else (
    echo Test failed. Please check the logs.
)

pause
