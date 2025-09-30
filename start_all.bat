@echo off
echo ===================================
echo    🍳 FlavorGraph Full Stack
echo    Starting Backend and Frontend
echo ===================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed! Please install Python 3.8+
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed! Please install Node.js 16+
    pause
    exit /b 1
)

echo 📋 Prerequisites Check: ✅ Python and Node.js found
echo.

REM Start backend in a new window
echo 🚀 Starting Backend Server...
start "FlavorGraph Backend" cmd /k "cd backend && python run.py"

REM Wait for backend to start
echo ⏳ Waiting for backend to initialize...
timeout /t 5 /nobreak >nul

REM Start frontend in a new window
echo 🚀 Starting Frontend Server...
start "FlavorGraph Frontend" cmd /k "npm run dev"

echo.
echo ===================================
echo    ✅ SERVERS STARTED!
echo ===================================
echo.
echo 🌐 Frontend: http://localhost:3000
echo 📚 Backend API: http://localhost:8000/api/docs
echo.
echo 🎯 Open http://localhost:3000 in your browser
echo.
echo Press any key to exit (servers will keep running)...
pause >nul
