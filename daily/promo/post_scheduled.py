"""Публикует в Telegram согласованные разовые посты из daily/promo/scheduled/<папка>/.

В каждой папке meta.json с полями telegram_at и telegram_until (ISO с часовым поясом),
telegram_image и telegram_text. Пост уходит только если сейчас между telegram_at и
telegram_until и папки ещё нет в daily/promo/posted.log. Раньше времени ничего не публикует,
поэтому запускать workflow можно в любой момент. Карточку «Знак дня» не трогает.

Переменные окружения: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID (как у post.py).
PROMO_NOW (ISO) подменяет текущее время для проверки, PROMO_DRY=1 ничего не отправляет."""
import os, sys, json, pathlib, datetime as dt

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import post  # noqa: E402  (fmt, call, TOKEN, CHAT из основного скрипта)

QUEUE = HERE / "scheduled"
LOG = HERE / "posted.log"


def now():
    v = os.environ.get("PROMO_NOW", "").strip()
    return dt.datetime.fromisoformat(v) if v else dt.datetime.now(dt.timezone.utc)


def main():
    t = now()
    dry = os.environ.get("PROMO_DRY") == "1"
    done = LOG.read_text().split() if LOG.exists() else []
    missed = []
    for d in sorted(p for p in QUEUE.iterdir() if p.is_dir()) if QUEUE.exists() else []:
        meta = json.loads((d / "meta.json").read_text(encoding="utf-8"))
        name = d.name
        if name in done:
            print("Уже опубликовано:", name); continue
        at = dt.datetime.fromisoformat(meta["telegram_at"])
        until = dt.datetime.fromisoformat(meta["telegram_until"])
        if t < at:
            print("Ещё рано:", name, "время публикации", meta["telegram_at"]); continue
        if t > until:
            print("ПРОПУЩЕНО окно публикации:", name, meta["telegram_at"], "–", meta["telegram_until"])
            missed.append(name); continue
        img = d / meta["telegram_image"]
        text = post.fmt((d / meta["telegram_text"]).read_text(encoding="utf-8").strip())
        if dry:
            print("DRY: опубликовала бы", name, "| символов в подписи:", len(text)); continue
        if not post.TOKEN:
            sys.exit("Не задан TELEGRAM_BOT_TOKEN")
        post.call("sendPhoto", {"chat_id": post.CHAT, "caption": text, "parse_mode": "HTML"}, img)
        with LOG.open("a") as f:
            f.write(name + "\n")
        print("Опубликовано:", name)
    if missed:
        sys.exit("Не опубликовано, окно прошло: " + ", ".join(missed))


if __name__ == "__main__":
    main()
