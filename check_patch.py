import json
import os
import urllib.parse
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

TOKEN = os.environ["TG_TOKEN"]
CHAT_ID = os.environ["TG_CHAT_ID"]
URL = "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=570&count=5&tags=patchnotes"
STATE = "last_gid.txt"
HEARTBEAT = "last_heartbeat.txt"
TZ = ZoneInfo("Europe/Chisinau")
HEARTBEAT_HOUR = 13  # во сколько (по Кишинёву) слать отчёт "я в порядке"


def read(path):
    return open(path).read().strip() if os.path.exists(path) else ""


def write(path, value):
    with open(path, "w") as f:
        f.write(value)


def send(text):
    data = urllib.parse.urlencode({"chat_id": CHAT_ID, "text": text}).encode()
    urllib.request.urlopen(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage", data=data, timeout=30
    )


with urllib.request.urlopen(URL, timeout=30) as r:
    items = json.load(r)["appnews"]["newsitems"]

newest = items[0] if items else None

# 1. Новый патч
if newest:
    gid = str(newest["gid"])
    if gid != read(STATE):
        send(f"Новый патч Dota 2: {newest['title']}\n{newest['url']} ПОБЕДА!??! НАЛИВАЙ!!!")
        write(STATE, gid)
        print("Отправлено:", newest["title"])
    else:
        print("Новых патчей нет")

# 2. Ежедневный отчёт "я работаю"
now = datetime.now(TZ)
today = now.strftime("%Y-%m-%d")
if now.hour >= HEARTBEAT_HOUR and read(HEARTBEAT) != today:
    last = f"\nПоследний патч: {newest['title']}" if newest else ""
    send(f"Бот работает, всё в порядке. Новых патчей нет.{last}")
    write(HEARTBEAT, today)
    print("Отчёт отправлен")
