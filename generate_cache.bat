@echo off
echo ========================================
echo KATAKANA CACHE GENERATOR
echo ========================================
echo.
echo This script will generate a JSON cache
echo of ~2000+ Katakana to English translations
echo using Google Translate API.
echo.
echo Estimated time: 5-10 minutes
echo ========================================
echo.

python generate_katakana_cache.py

echo.
echo ========================================
echo DONE! Check katakana_cache.json
echo ========================================
pause
