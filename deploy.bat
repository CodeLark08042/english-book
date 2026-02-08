@echo off
echo ========================================
echo       Updating Word Flashcards (Gitee Only)
echo ========================================

echo.
echo 1. Updating words from Excel...
python convert_to_json.py

echo.
echo 2. Committing changes to Git...
git add .
set /p commit_msg="Enter commit message (default: Update words): "
if "%commit_msg%"=="" set commit_msg=Update words
git commit -m "%commit_msg%"

echo.
echo 3. Pushing to Gitee...
echo (Attempting to bypass proxy for Gitee...)
git -c http.proxy= -c https.proxy= push gitee master

echo.
echo ========================================
echo       Deployment Complete!
echo ========================================
echo Gitee:  https://happy-08042.gitee.io/english-book/
echo.
pause
