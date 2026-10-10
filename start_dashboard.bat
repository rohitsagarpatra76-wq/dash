@echo off
title VEYRO Survey Analytics Dashboard
echo =====================================================
echo   Starting VEYRO Survey Analytics Dashboard...
echo =====================================================
echo.
python server.py
if %ERRORLEVEL% NEQ 0 (
    echo Python server launch failed, opening index.html directly...
    start index.html
)
pause
