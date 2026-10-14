"""Карусель «Шепоток на Покров» в фирменном стиле (бумага + маркер + рукописные пометки).
Запуск: python3 carousel/pokrov_shepotok.py  → carousel/out/pokrov/01.png … 04.png (1080x1350)"""
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
F = ROOT / "daily" / "fonts"
P = ROOT / "brand" / "photos"
OUT = ROOT / "carousel" / "out" / "pokrov"; OUT.mkdir(parents=True, exist_ok=True)

def ph(name): return f"file://{P}/{name}.jpg"

CSS = f"""
@font-face{{font-family:Osw;src:url('file://{F}/Oswald.ttf')}}
@font-face{{font-family:Man;src:url('file://{F}/Manrope.ttf')}}
@font-face{{font-family:Hand;src:url('file://{F}/Caveat.ttf')}}
@font-face{{font-family:Cor;src:url('file://{F}/Cormorant-Italic.ttf')}}
:root{{--paper:#F6F0E4;--ink:#24302C;--gold:#E2B84E;--goldd:#B48E4A;--em:#1E5E4B;--muted:#5E6B66}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;overflow:hidden;background:var(--paper);color:var(--ink);font-family:Man;position:relative}}
body:before{{content:"";position:absolute;inset:0;opacity:.35;filter:url(#grain);background:#fff;mix-blend-mode:multiply}}
.top,.bot{{position:absolute;left:64px;right:64px;display:flex;align-items:center;gap:22px;font:600 19px Man;letter-spacing:.3em;color:var(--muted)}}
.top{{top:52px}} .bot{{bottom:46px}}
.top i,.bot i{{flex:1;height:1.5px;background:var(--muted);opacity:.5}}
.h{{font-family:Osw;font-weight:700;text-transform:uppercase;line-height:.98;letter-spacing:-.005em;color:var(--ink)}}
.mk{{position:relative;display:inline-block;padding:0 .12em;z-index:0}}
.mk:before{{content:"";position:absolute;left:-.06em;right:-.06em;top:.12em;bottom:.02em;background:var(--gold);z-index:-1;filter:url(#rough);border-radius:6px;transform:rotate(-1deg)}}
.ul{{position:relative;display:inline-block}}
.ul:after{{content:"";position:absolute;left:0;right:0;bottom:-.08em;height:.12em;background:var(--gold);filter:url(#rough);border-radius:4px}}
.hand{{font-family:Hand;font-weight:500;color:var(--ink);line-height:1.05}}
.em{{color:var(--em)}}
.photo{{position:absolute;background:#fff;padding:16px 16px 54px;box-shadow:0 18px 40px rgba(36,48,44,.22)}}
.photo img{{display:block;width:100%;height:100%;object-fit:cover}}
.photo .cap{{position:absolute;left:0;right:0;bottom:8px;text-align:center;font:500 34px Hand;color:var(--muted)}}
.tape{{position:absolute;width:150px;height:42px;background:rgba(226,184,78,.55);top:-20px;left:50%;margin-left:-75px;transform:rotate(-4deg);filter:url(#rough)}}
.card{{background:rgba(255,255,255,.72);border:1.5px solid rgba(36,48,44,.18);border-radius:22px;padding:26px 30px}}
.li{{display:flex;gap:20px;align-items:flex-start;font-size:31px;line-height:1.32;margin:0 0 22px}}
.li b{{font-weight:700}}
.num{{flex:none;width:76px;height:76px;border-radius:50%;background:var(--gold);display:flex;align-items:center;justify-content:center;font:700 46px Osw;filter:url(#roughs)}}
svg.a{{position:absolute;overflow:visible}}
svg.a path{{fill:none;stroke:var(--ink);stroke-width:3.2;stroke-linecap:round;stroke-linejoin:round}}
.round{{border-radius:50%;object-fit:cover;border:8px solid #fff;box-shadow:0 12px 30px rgba(36,48,44,.25);position:absolute}}
.verse{{font-family:Cor;font-style:italic;font-size:40px;line-height:1.5;color:var(--ink)}}
.verse b{{font-weight:600;color:var(--em)}}
"""

DEFS = """<svg width="0" height="0" style="position:absolute"><defs>
<filter id="rough"><feTurbulence type="fractalNoise" baseFrequency="0.035 0.6" numOctaves="2" seed="4"/><feDisplacementMap in="SourceGraphic" scale="14"/></filter>
<filter id="roughs"><feTurbulence type="fractalNoise" baseFrequency="0.05" numOctaves="2" seed="7"/><feDisplacementMap in="SourceGraphic" scale="6"/></filter>
<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 .55  0 0 0 0 .5  0 0 0 0 .42  0 0 0 .5 0"/></filter>
</defs></svg>"""

TICK = '<svg class="tick" viewBox="0 0 40 40" width="40" height="40"><path d="M6 21 L16 31 L35 7" fill="none" stroke="#B48E4A" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def arrow(x, y, w, h, d, head):
    return f'<svg class="a" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px" viewBox="0 0 {w} {h}"><path d="{d}"/><path d="{head}"/></svg>'

def frame(n, body):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{DEFS}
<div class="top"><span>ГОРОДСКАЯ МАГИЯ</span><i></i><span>ШЕПОТОК НА ПОКРОВ</span></div>
{body}
<div class="bot"><span>0{n} / 04</span><i></i><span>@AFITCIYA_MAGIC</span></div></body></html>"""

S = []

# 1. Обложка
S.append(frame(1, f"""
<div class="h" style="position:absolute;left:64px;top:140px;font-size:128px;width:950px">Шепоток<br><span class="mk">на Покров</span></div>
<div class="hand" style="position:absolute;left:64px;top:462px;font-size:44px;width:640px;line-height:1.2">«Покров-батюшка,<br>покрой землю снежком,<br>а меня, молоду, <span class="em">женишком</span>»</div>
<div class="photo" style="left:420px;top:620px;width:560px;height:600px;transform:rotate(3deg)"><div class="tape"></div><img src="{ph('portret-stena-1')}" style="object-position:50% 35%"><div class="cap">на рассвете, перед окном</div></div>
<div class="hand" style="position:absolute;left:70px;top:770px;font-size:38px;width:310px;transform:rotate(-5deg)">так шептали у окна наши бабушки. я шепчу иначе ♡</div>
{arrow(150, 940, 240, 160, "M10 10 C 40 90, 130 130, 230 110", "M208 90 L232 111 L206 130")}
<div class="hand" style="position:absolute;left:70px;top:1150px;font-size:40px;color:var(--muted)">листай →</div>
"""))

# 2. Как делать
steps = [
    ("1", "Подойди к окну", "открой его или просто посмотри на небо"),
    ("2", "Положи правую ладонь", "на сердце"),
    ("3", "Трижды произнеси шепоток", "текст на следующем слайде"),
    ("4", "Закрой глаза на пару секунд", "и почувствуй, как в жизнь приходит тепло"),
]
rows = "".join(
    f'<div class="li" style="align-items:center;margin-bottom:34px"><div class="num">{n}</div>'
    f'<div><b style="font-size:37px">{t}</b><br><span style="color:var(--muted);font-size:29px">{s}</span></div></div>'
    for n, t, s in steps
)
S.append(frame(2, f"""
<div class="h" style="position:absolute;left:64px;top:130px;font-size:104px">Как <span class="ul">делать</span></div>
<div style="position:absolute;left:64px;right:64px;top:360px">{rows}</div>
<div class="hand em" style="position:absolute;left:64px;top:1130px;font-size:44px;width:950px">никаких сложных ритуалов, пять минут у окна</div>
"""))

# 3. Текст шепотка
VERSE = (
    "Покров-батюшка, укрой моё сердце<br>"
    "от одиночества, как землю снегом.<br><br>"
    "Не чужого прошу, а <b>своего</b>,<br>"
    "кто мне по судьбе.<br><br>"
    "Пусть наши дороги пересекутся,<br>"
    "без обмана, по-честному.<br><br>"
    "Как сказано, так и будет."
)
S.append(frame(3, f"""
<div class="h" style="position:absolute;left:64px;top:110px;font-size:92px">Текст <span class="mk">шепотка</span></div>
<div class="card" style="position:absolute;left:64px;right:64px;top:290px;padding:56px 54px;text-align:center">
<div class="verse">{VERSE}</div>
</div>
<div class="hand" style="position:absolute;right:80px;top:1150px;font-size:42px;transform:rotate(-3deg)">можно своими словами, суть важнее точности</div>
"""))

# 4. Если уже в паре + мягкий переход в канал
S.append(frame(4, f"""
<img class="round" src="{ph('portret-tsss-sekret')}" style="left:700px;top:120px;width:300px;height:300px;object-position:50% 25%">
<div class="hand" style="position:absolute;left:460px;top:420px;font-size:42px;transform:rotate(-6deg)">если ты уже в паре ♡</div>
<div class="h" style="position:absolute;left:64px;top:140px;font-size:72px;width:620px">Если ты<br>уже в<br>отношениях</div>
<div class="card" style="position:absolute;left:64px;right:64px;top:540px;padding:34px 34px 30px">
 <div style="font-size:30px;line-height:1.45;color:var(--muted);margin-bottom:16px">замени две строки:</div>
 <div class="verse" style="font-size:33px">«Пусть между нами тепло не угасает,<br>любовь и доверие день ото дня возрастают.<br>Пусть дороги наши вместе идут,<br>а сердца <b>согласие</b> берегут.»</div>
</div>
<div style="position:absolute;left:64px;right:64px;top:970px;text-align:center">
 <div style="font-size:30px;color:var(--muted);line-height:1.4;width:880px;margin:0 auto">шепоток про дорогу к любви, а в чём твоя сила притяжения, уже знаешь?</div>
 <div style="font-size:34px;margin-top:18px">бесплатный тест ждёт по слову</div>
 <div class="h" style="font-size:140px;margin:6px 0"><span class="mk">ЧАРЫ</span></div>
 <div class="hand" style="font-size:34px;color:var(--muted)">напиши в личку ♡</div>
</div>
"""))

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1350})
    for i, html in enumerate(S, 1):
        f = OUT / f"{i:02d}.html"; f.write_text(html, encoding="utf-8")
        pg.goto(f"file://{f}"); pg.wait_for_timeout(400)
        pg.screenshot(path=str(OUT / f"{i:02d}.png")); f.unlink()
    b.close()
print("готово:", OUT)
