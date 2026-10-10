@echo off
title Deploy VEYRO Survey Dashboard to Netlify
echo =====================================================
echo   Preparing VEYRO Survey Dashboard for Netlify...
echo =====================================================
echo.
python build_netlify_app.py
python deploy_to_netlify.py
pause
