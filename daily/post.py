"""Публикует карточку на сегодня (по Москве) в Telegram-канал.
Нужны переменные окружения TELEGRAM_BOT_TOKEN и TELEGRAM_CHAT_ID (например @afitciy)."""
import os, re, sys, json, html, pathlib, datetime as dt, urllib.request, uuid

HERE = pathlib.Path(__file__).resolve().parent
LOG = HERE / "posted.log"
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
CHAT = os.environ.get("TELEGRAM_CHAT_ID", "").strip() or "@afitciy"

def fmt(text):
    t = html.escape(text, quote=False)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)

def call(method, fields, file=None):
    url = f"https://api.telegram.org/bot{TOKEN}/{method}"
    if file is None:
        req = urllib.request.Request(url, data=json.dumps(fields).encode(), headers={"Content-Type": "application/json"})
    else:
        b = uuid.uuid4().hex; body = b""
        for k, v in fields.items():
            body += f"--{b}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
        body += (f"--{b}\r\nContent-Disposition: form-data; name=\"photo\"; filename=\"{file.name}\"\r\n"
                 f"Content-Type: image/png\r\n\r\n").encode() + file.read_bytes() + f"\r\n--{b}--\r\n".encode()
        req = urllib.request.Request(url, data=body, headers={"Content-Type": f"multipart/form-data; boundary={b}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        res = json.load(r)
    if not res.get("ok"):
        sys.exit(f"Telegram ответил ошибкой: {res}")

def main():
    today = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=3)).date().isoformat()
    if len(sys.argv) > 1: today = sys.argv[1]
    done = LOG.read_text().split() if LOG.exists() else []
    if today in done:
        print("Уже опубликовано:", today); return
    img, cap = HERE / "queue" / f"{today}.png", HERE / "queue" / f"{today}.txt"
    if not img.exists():
        print("Нет карточки на", today); return
    if not TOKEN:
        sys.exit("Не задан TELEGRAM_BOT_TOKEN")
    text = fmt(cap.read_text(encoding="utf-8").strip()) if cap.exists() else ""
    if len(text) <= 1024:
        call("sendPhoto", {"chat_id": CHAT, "caption": text, "parse_mode": "HTML"}, img)
    else:
        call("sendPhoto", {"chat_id": CHAT}, img)
        call("sendMessage", {"chat_id": CHAT, "text": text, "parse_mode": "HTML"})
    with LOG.open("a") as f: f.write(today + "\n")
    print("Опубликовано:", today)

if __name__ == "__main__":
    main()
