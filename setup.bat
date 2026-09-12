@echo off
REM Minecraft Battery HUD - Quick Setup for Windows

echo.
echo ===================================
echo  🎮 Minecraft Battery HUD Setup 🎮
echo ===================================
echo.

REM Check for Node.js
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Node.js not found! Download from: https://nodejs.org
    pause
    exit /b 1
)
echo ✅ Node.js found

REM Check for Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python not found! Download from: https://python.org
    pause
    exit /b 1
)
echo ✅ Python found

REM Install Node dependencies
echo.
echo 📦 Installing Node.js dependencies...
call npm install
if %errorlevel% neq 0 (
    echo ❌ Failed to install Node dependencies
    pause
    exit /b 1
)
echo ✅ Node dependencies installed

REM Install Python dependencies
echo.
echo 🐍 Installing Python dependencies...
call python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install Python dependencies
    pause
    exit /b 1
)
echo ✅ Python dependencies installed

REM Optional: Install advanced features
echo.
echo.
echo 🎵 Optional: Advanced Features
echo   - Text-to-Speech: pyttsx3
echo   - Desktop Notifications: plyer
echo   - Battery Monitoring: psutil
echo.
set /p install_optional="Install advanced features? (y/n): "
if /i "%install_optional%"=="y" (
    echo Installing advanced features...
    call python -m pip install psutil pyttsx3 plyer
    echo ✅ Advanced features installed
)

REM Create .env.local
if not exist .env.local (
    echo.
    echo 📝 Creating .env.local...
    copy .env.example .env.local >nul
    echo ✅ .env.local created
)

REM Summary
echo.
echo ===================================
echo   ✅ Setup Complete!
echo ===================================
echo.
echo 🚀 To start the development server:
echo    npm run dev
echo.
echo 📖 Then open: http://localhost:3000
echo.
echo 📚 For deployment guide, see: DEPLOYMENT.md
echo 📘 For more info, see: README.md
echo.
echo ===================================
echo.
pause
