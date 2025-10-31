@echo off
REM Setup and Run Script for PLC Data Mapping Assistant
REM For Windows users

cls
echo ================================================================
echo      PLC Data Mapping Assistant - Setup ^& Run Script
echo ================================================================
echo.

REM Check if Python is installed
echo Checking for Python...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
    echo [OK] Found: %PYTHON_VERSION%
) else (
    echo [ERROR] Python is not installed!
    echo    Please install Python from: https://www.python.org/downloads/
    echo    Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)
echo.

REM Check if requirements are installed
echo Checking dependencies...
python -c "import flask" >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Dependencies already installed
) else (
    echo Installing dependencies...
    pip install -r requirements.txt
    if %errorlevel% equ 0 (
        echo [OK] Dependencies installed successfully
    ) else (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
)
echo.

REM Check for API key
echo Checking for Anthropic API key...
if "%ANTHROPIC_API_KEY%"=="" (
    echo [WARNING] API key not found in environment
    echo.
    echo ================================================================
    echo    IMPORTANT: This application requires PAID API access!
    echo ================================================================
    echo.
    echo To use this application, you must:
    echo   1. Go to: https://console.anthropic.com/
    echo   2. Create an account
    echo   3. Add a payment method (credit card)
    echo   4. Purchase at least $5 in API credits
    echo   5. Create an API key
    echo.
    echo Cost: ~$0.01-0.05 per requirement analyzed
    echo Example: 10 requirements = ~$0.10-0.50
    echo.
    set /p HAS_KEY="Do you have an API key? (y/n): "

    if /i "%HAS_KEY%"=="y" (
        echo.
        set /p API_KEY="Enter your Anthropic API key: "
        set ANTHROPIC_API_KEY=!API_KEY!
        echo [OK] API key set for this session
    ) else (
        echo.
        echo Please get an API key from https://console.anthropic.com/
        echo Then run this script again.
        pause
        exit /b 1
    )
) else (
    echo [OK] API key found
)
echo.

REM Final check
echo ================================================================
echo                    Ready to Launch!
echo ================================================================
echo.
echo Starting the application...
echo.
echo Once started, open your browser to:
echo    http://localhost:5000
echo.
echo Press Ctrl+C to stop the server when done.
echo.
echo ----------------------------------------------------------------
echo.

REM Start the application
python app.py
