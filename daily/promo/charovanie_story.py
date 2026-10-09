"""Сторис про Чарование 1080x1920 в стиле карточек. Запуск: python3 daily/promo/charovanie_story.py"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from render import CSS, HERE
from playwright.sync_api import sync_playwright
OUT = HERE / "queue" / "stories" / "promo-2026-10-10-charovanie.png"
EXTRA = """
body{height:1920px}
.card{padding:190px 70px 170px;justify-content:flex-start}
.moon{width:300px;height:300px;margin-top:40px}
.big{font-family:GV;font-size:150px;color:var(--gold);line-height:1;margin-top:20px}
.sub{font-family:Cor;font-style:italic;font-size:44px;color:var(--em);margin-top:6px}
.q{font-family:Cor;font-style:italic;font-size:46px;line-height:1.25;color:var(--em);margin-top:46px}
.t{font-size:31px;line-height:1.45;margin-top:30px}
.box{margin-top:40px;text-align:center}
.box p{font-size:31px}
.price{font-size:29px;color:var(--muted);margin-top:14px}
.cta{margin-top:auto;background:var(--em);color:#fff;border-radius:60px;padding:30px 40px;font-size:38px;font-weight:500;width:100%}
.cta small{display:block;font-size:27px;font-weight:400;opacity:.85;margin-top:6px}
.ft{font-size:24px;margin-top:22px;padding-top:0}
"""
MOON = """<svg class="moon" viewBox="0 0 200 200"><circle cx="100" cy="100" r="96" fill="rgba(140,194,154,.14)" stroke="#B48E4A" stroke-width="2"/>
<circle cx="100" cy="100" r="62" fill="#1E5E4B" opacity=".9"/><path d="M100 38 a62 62 0 0 1 0 124 a48 62 0 0 0 0 -124z" fill="#F7F1E6"/></svg>"""
HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}{EXTRA}</style></head><body><div class="card">
<div class="top">ГОРОДСКАЯ МАГИЯ</div>
{MOON}
<div class="big">Чарование</div>
<div class="sub">сегодня новолуние</div>
<div class="q">Помнишь то состояние, когда горят глаза, внутри спокойно и тебе самой нравится, какая&nbsp;ты?</div>
<div class="t">Чарование про то, чтобы вернуть его. Это моя индивидуальная работа по фотографии на твою женскую силу: притяжение, уверенность, энергию.</div>
<div class="box"><p>Провожу два раза в месяц: сегодня, в новолуние, и&nbsp;26&nbsp;октября, в&nbsp;полнолуние.</p>
<div class="price">Одна работа 4&nbsp;000&nbsp;₽<br>Месяц Чарования, обе работы, 7&nbsp;000&nbsp;₽</div></div>
<div class="cta">Напиши мне в директ «ЧАРЫ»<small>расскажу, как всё проходит</small></div>
<div class="ft">@afitciya_magic</div>
</div></body></html>"""
f = HERE / "queue" / "stories" / "_promo.html"; f.write_text(HTML, encoding="utf-8")
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":1080,"height":1920})
    pg.goto(f"file://{f}"); pg.wait_for_timeout(400)
    over = pg.evaluate("(()=>{const c=document.querySelector('.card');return c.scrollHeight-c.clientHeight})()")
    if over > 2: print("не влезает на", over)
    pg.screenshot(path=str(OUT)); b.close()
f.unlink(); print(OUT)
