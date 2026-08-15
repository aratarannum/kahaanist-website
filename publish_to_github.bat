@echo off
echo === Kahaanist Website Publisher ===
echo.
echo This script will save a version of your website and publish it to the live server.
echo (You can always revert to older versions later if needed).
echo.

set /p desc="Enter a short label for this version (e.g., 'Added Medusa Ring'): "

echo.
echo Saving and publishing...
git add .
git commit -m "%desc%"
git push origin main
echo.
echo Successfully published! Cloudflare will update your live site in ~60 seconds.
pause
