@echo off
cd /d "%~dp0"
echo 通知アプリを起動します...（終了するには Ctrl+C）
echo.
python notifier.py %*
pause
