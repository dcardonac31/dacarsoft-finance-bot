@echo off
echo ===============================================
echo   Dacarsoft Finance Bot - Starting...
echo ===============================================
echo.

REM Activate virtual environment
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo ERROR: Virtual environment not found!
    echo Please run: python -m venv venv
    pause
    exit /b 1
)

REM Check if .env exists
if not exist .env (
    echo ERROR: .env file not found!
    echo Please create a .env file with your configuration.
    echo See example_env.txt for reference.
    pause
    exit /b 1
)

REM Start the bot
python main.py

pause

