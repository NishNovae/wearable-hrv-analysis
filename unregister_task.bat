@echo off
setlocal

set "TASK_NAME=Wearable HRV Pipeline"

schtasks /delete ^
    /tn "%TASK_NAME%" ^
    /f

if errorlevel 1 (
    echo [ERROR] Failed to remove scheduled task.
    exit /b 1
)

echo [INFO] Scheduled task removed successfully.

endlocal
