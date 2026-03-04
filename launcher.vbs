' 平日朝 9:28 通知アプリ ランチャー
' コンソールウィンドウを表示せずにバックグラウンドで起動します

Option Explicit

Dim oShell, sDir, sCmd

Set oShell = CreateObject("WScript.Shell")

' このVBSファイルと同じフォルダのパスを取得
sDir = Left(WScript.ScriptFullName, InStrRev(WScript.ScriptFullName, "\"))

' pythonw を使用（コンソールウィンドウが開かない）
sCmd = "pythonw """ & sDir & "notifier.py"""

' 第2引数 0 = ウィンドウ非表示, 第3引数 False = 非同期実行
oShell.Run sCmd, 0, False

Set oShell = Nothing
