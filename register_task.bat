@echo off
setlocal

set "TASK_NAME=Wearable HRV Pipeline"
set "PIPELINE=%~dp0run_pipeline.bat"

if not exist "%PIPELINE%" (
    echo [ERROR] run_pipeline.bat not found.
    exit /b 1
)

schtasks /create ^
    /tn "%TASK_NAME%" ^
    /tr "\"%PIPELINE%\"" ^
    /sc onlogon ^
    /f

if errorlevel 1 (
    echo [ERROR] Failed to register scheduled task.
    exit /b 1
)

echo [INFO] Scheduled task registered successfully.
echo [INFO] Task name: %TASK_NAME%

endlocal
