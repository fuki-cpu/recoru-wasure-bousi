@echo off
setlocal

set "TARGET=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\morning_notifier.vbs"

if exist "%TARGET%" (
    del /q "%TARGET%"
    echo [OK] スタートアップから削除しました。
) else (
    echo [INFO] スタートアップに登録されていません。
)

endlocal
pause
