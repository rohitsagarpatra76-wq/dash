@echo off
title Push VEYRO Dashboard to GitHub
echo =====================================================
echo   Pushing to https://github.com/rohitsagarpatra76-wq/dash.git
echo =====================================================
echo.
echo If prompted, enter your GitHub Username and Personal Access Token (or password).
echo.
"C:\Users\ROHIT SAGAR PATRA\.gemini\mingit\cmd\git.exe" push -u origin main
echo.
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Repository pushed to GitHub!
    echo Next step: Connect this repository to Netlify at https://app.netlify.com
) else (
    echo [NOTE] Push failed. If authentication failed, use a Personal Access Token:
    echo https://github.com/settings/tokens
)
pause
