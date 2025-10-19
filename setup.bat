@echo off
echo 🚀 Orange Sage Setup
echo ====================

echo.
echo Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found!
    echo Please install Python from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
) else (
    echo ✅ Python found
)

echo.
echo Checking Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js not found!
    echo Please install Node.js from https://nodejs.org
    pause
    exit /b 1
) else (
    echo ✅ Node.js found
)

echo.
echo Installing backend dependencies...
cd backend
pip install -r requirements_local.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install backend dependencies
    pause
    exit /b 1
)
echo ✅ Backend dependencies installed

echo.
echo Installing frontend dependencies...
cd ..\frontend
npm install
if %errorlevel% neq 0 (
    echo ❌ Failed to install frontend dependencies
    pause
    exit /b 1
)
echo ✅ Frontend dependencies installed

echo.
echo ====================
echo 🎉 Setup Complete!
echo ====================
echo.
echo To start Orange Sage:
echo 1. Backend: cd backend && python -m uvicorn app.main_local:app --reload
echo 2. Frontend: cd frontend && npm run dev
echo.
echo Then visit: http://localhost:5173
echo.
pause