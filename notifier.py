#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
平日朝 9:28 通知アプリ  (Windows 11, JST)
外部ライブラリ不要 ─ Python 標準ライブラリのみ使用

使い方:
  python notifier.py          # 通常起動
  python notifier.py --test   # 今すぐテスト通知を送信
"""

import datetime
import time
import subprocess
import sys
from typing import Optional

# ── 設定 ──────────────────────────────────────────────────────────────────────
NOTIFY_HOUR    = 9
NOTIFY_MINUTE  = 28
NOTIFY_TITLE   = "おはようございます"
NOTIFY_BODY    = "平日 9:28 のお知らせです。今日も一日よろしくお願いします！"
CHECK_INTERVAL = 20          # 秒ごとに時刻チェック
APP_ID         = "MorningNotifier"
JST            = datetime.timezone(datetime.timedelta(hours=9))
WEEKDAY_NAMES  = ["月", "火", "水", "木", "金", "土", "日"]
# ──────────────────────────────────────────────────────────────────────────────

_notified_today: Optional[datetime.date] = None


def get_jst_now() -> datetime.datetime:
    """JST の現在時刻を返す（システム時計が UTC でも正しく動作する）"""
    return datetime.datetime.now(JST)


def _escape_ps(text: str) -> str:
    """PowerShell 文字列内の特殊文字をエスケープ"""
    return text.replace("\\", "\\\\").replace('"', '`"').replace("'", "`'")


def show_toast(title: str, body: str) -> bool:
    """Windows ネイティブのトースト通知を表示（外部モジュール不要）"""
    ps = f"""
$ErrorActionPreference = 'Stop'
[void][Windows.UI.Notifications.ToastNotificationManager,
       Windows.UI.Notifications, ContentType = WindowsRuntime]

$tpl = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent(
    [Windows.UI.Notifications.ToastTemplateType]::ToastText02)
$xml = [xml]$tpl.GetXml()
$t   = $xml.GetElementsByTagName('text')
[void]$t[0].AppendChild($xml.CreateTextNode("{_escape_ps(title)}"))
[void]$t[1].AppendChild($xml.CreateTextNode("{_escape_ps(body)}"))

$doc = New-Object Windows.Data.Xml.Dom.XmlDocument
$doc.LoadXml($xml.OuterXml)

[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier(
    "{APP_ID}").Show(
        [Windows.UI.Notifications.ToastNotification]::new($doc))
"""
    try:
        result = subprocess.run(
            ["powershell", "-NonInteractive", "-WindowStyle", "Hidden", "-Command", ps],
            capture_output=True,
            timeout=15,
            creationflags=0x08000000,   # CREATE_NO_WINDOW
        )
        return result.returncode == 0
    except Exception as e:
        print(f"[WARN] トースト通知エラー: {e}", file=sys.stderr)
        return False


def play_sound() -> None:
    """通知音を鳴らす（Windows 標準ビープ）"""
    try:
        import winsound  # type: ignore
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
    except Exception:
        pass


def fire_notification() -> None:
    now = get_jst_now()
    print(f"[{now.strftime('%H:%M:%S')}] 通知を送信します...")
    ok = show_toast(NOTIFY_TITLE, NOTIFY_BODY)
    play_sound()
    status = "送信完了" if ok else "送信失敗（PowerShell ログを確認してください）"
    print(f"[{now.strftime('%H:%M:%S')}] {status}")


def main() -> None:
    global _notified_today

    # ── テストモード ───────────────────────────────────────────────────────────
    if "--test" in sys.argv or "-t" in sys.argv:
        print("テスト通知を送信します...")
        fire_notification()
        return

    # ── 通常起動 ───────────────────────────────────────────────────────────────
    print("=" * 54)
    print("  平日朝 9:28 通知アプリ  -  起動しました")
    print("=" * 54)
    now = get_jst_now()
    print(f"  現在時刻 (JST) : {now.strftime('%Y-%m-%d %H:%M:%S')} "
          f"({WEEKDAY_NAMES[now.weekday()]}曜日)")
    print(f"  通知スケジュール: 平日 {NOTIFY_HOUR:02d}:{NOTIFY_MINUTE:02d} JST")
    print(f"  終了           : Ctrl+C")
    print("=" * 54)

    try:
        while True:
            now   = get_jst_now()
            today = now.date()

            is_target  = (now.hour == NOTIFY_HOUR and now.minute == NOTIFY_MINUTE)
            is_weekday = (now.weekday() < 5)          # 0=月 〜 4=金
            not_done   = (_notified_today != today)

            if is_target and is_weekday and not_done:
                fire_notification()
                _notified_today = today
                time.sleep(61)      # 同分内の重複発火を防ぐ
            else:
                time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        print("\n  停止しました。お疲れさまでした。")


if __name__ == "__main__":
    main()
