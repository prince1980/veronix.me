@echo off
:: Enable ANSI colors for the terminal
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1
cls
:: Set sleek terminal size
mode con: cols=90 lines=24
:: Default dark gray/black theme (no flashbangs)
color 0F

python generate_seo_free.py

if %errorlevel% neq 0 (
    echo.
    echo  [31mError: Automation failed. Please check the network or try again. [0m
)

pause >nul
