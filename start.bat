@echo off
REM Startup script for Wine Recommendation System (Windows)

echo ================================
echo Wine Recommendation System
echo ================================
echo.

REM Check if .env exists
if not exist .env (
    echo WARNING: .env file not found!
    echo Please create .env file with PERPLEXITY_API_KEY
    echo.
)

echo Starting Backend API (Python)...
echo.
start cmd /k "title Backend API && python api.py"

timeout /t 3 /nobreak > nul

echo Starting Frontend (Next.js)...
echo.
start cmd /k "title Frontend && npm run dev"

echo.
echo ================================
echo Both servers are starting...
echo ================================
echo.
echo Backend API: http://localhost:8000
echo Frontend:    http://localhost:3000
echo.
echo Press any key to open browser...
pause > nul

start http://localhost:3000

echo.
echo Servers are running!
echo Close both terminal windows to stop.
