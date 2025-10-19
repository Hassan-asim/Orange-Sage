@echo off
echo 🚀 Orange Sage Setup
echo ====================

echo.
echo Checking Python...
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found with 'py' command
    echo Trying 'python'...
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ Python not found with 'python' command
        echo Trying 'python3'...
        python3 --version >nul 2>&1
        if %errorlevel% neq 0 (
            echo ❌ Python not found!
            echo.
            echo Please install Python from https://python.org
            echo Make sure to check "Add Python to PATH" during installation
            pause
            exit /b 1
        ) else (
            echo ✅ Python found with 'python3' command
            set PYTHON_CMD=python3
        )
    ) else (
        echo ✅ Python found with 'python' command
        set PYTHON_CMD=python
    )
) else (
    echo ✅ Python found with 'py' command
    set PYTHON_CMD=py
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
%PYTHON_CMD% -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install backend dependencies
    echo Trying with --user flag...
    %PYTHON_CMD% -m pip install --user -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Still failed to install backend dependencies
        echo Please check your Python installation and try again
        pause
        exit /b 1
    )
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
echo 1. Backend: cd backend && %PYTHON_CMD% -m uvicorn app.main_local:app --reload
echo 2. Frontend: cd frontend && npm run dev
echo.
echo Then visit: http://localhost:5173
echo.
echo Note: Use '%PYTHON_CMD%' instead of 'python' if needed
echo.
pause