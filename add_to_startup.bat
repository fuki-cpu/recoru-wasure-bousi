@echo off
setlocal

set "SRC=%~dp0launcher.vbs"
set "STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"

copy /y "%SRC%" "%STARTUP%\morning_notifier.vbs" >nul

if %errorlevel% == 0 (
    echo [OK] スタートアップへの登録が完了しました。
    echo      次回 Windows 起動時から自動的に通知が有効になります。
    echo      登録先: %STARTUP%\morning_notifier.vbs
) else (
    echo [ERROR] 登録に失敗しました。管理者権限で実行してみてください。
)

endlocal
pause
