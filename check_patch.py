import json
import os
import urllib.parse
import urllib.request

TOKEN = os.environ["TG_TOKEN"]
CHAT_ID = os.environ["TG_CHAT_ID"]
URL = "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=570&count=5&tags=patchnotes"
STATE = "last_gid.txt"


def send(text):
    data = urllib.parse.urlencode({"chat_id": CHAT_ID, "text": text}).encode()
    urllib.request.urlopen(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage", data=data, timeout=30
    )


with urllib.request.urlopen(URL, timeout=30) as r:
    items = json.load(r)["appnews"]["newsitems"]

if items:
    newest = items[0]
    gid = str(newest["gid"])
    last = open(STATE).read().strip() if os.path.exists(STATE) else ""
    if gid != last:
        send(f"Новый патч Dota 2: {newest['title']}\n{newest['url']}")
        with open(STATE, "w") as f:
            f.write(gid)
        print("Отправлено:", newest["title"])
    else:
        print("Новых патчей нет")
