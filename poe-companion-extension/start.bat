@echo off
echo ============================================
echo PoE Companion Extension Launcher
echo ============================================
echo.
echo Starting Flask Backend...
echo.

REM Start Flask backend in a new window
start "PoE Backend" cmd /k "cd ..\poe-build-guide && python app.py"

REM Wait a bit for backend to start
timeout /t 3 /nobreak > nul

echo.
echo Starting Companion Overlay...
echo.

REM Start Electron app
npm start

echo.
echo Companion closed. Press any key to exit...
pause > nul
