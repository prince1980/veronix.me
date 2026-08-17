@echo off
title Veronix Reddit Automation Engine
color 05

echo.
echo ===================================================
echo     VERONIX REDDIT AUTOMATION ENGINE (PROFILE)
echo ===================================================
echo.

:: Check for .env file
if not exist ".env" (
    setlocal enabledelayedexpansion
    echo [SETUP REQUIRED] First-time setup detected.
    echo Please provide your Reddit API credentials. 
    echo If you don't have them, read the walkthrough guide!
    echo.
    set /p client_id="Enter Reddit Client ID: "
    set /p client_secret="Enter Reddit Client Secret: "
    set /p username="Enter Reddit Username: "
    set /p password="Enter Reddit Password: "
    
    echo REDDIT_CLIENT_ID=!client_id!> .env
    echo REDDIT_CLIENT_SECRET=!client_secret!>> .env
    echo REDDIT_USERNAME=!username!>> .env
    echo REDDIT_PASSWORD=!password!>> .env
    echo.
    echo Credentials saved to .env file!
    endlocal
)

:: Install missing python packages silently
echo ^> Verifying required AI and Reddit dependencies...
pip install -q praw python-dotenv g4f >nul 2>&1

:: Run the python engine
python generate_reddit_free.py

echo.
echo ===================================================
echo                    DONE
echo ===================================================
pause
