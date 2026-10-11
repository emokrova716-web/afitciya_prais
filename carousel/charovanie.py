"""Карусель «Чарование» в стиле «бумага + маркер + рукописные пометки».
Запуск: python3 carousel/charovanie.py  → carousel/out/charovanie/01.png … 06.png (1080x1350)"""
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
F = ROOT / "daily" / "fonts"
P = ROOT / "brand" / "photos"
OUT = ROOT / "carousel" / "out" / "charovanie"; OUT.mkdir(parents=True, exist_ok=True)

def ph(name): return f"file://{P}/{name}.jpg"

CSS = f"""
@font-face{{font-family:Osw;src:url('file://{F}/Oswald.ttf')}}
@font-face{{font-family:Man;src:url('file://{F}/Manrope.ttf')}}
@font-face{{font-family:Hand;src:url('file://{F}/Caveat.ttf')}}
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
.tick{{flex:none;width:40px;height:40px;margin-top:2px}}
.num{{flex:none;width:76px;height:76px;border-radius:50%;background:var(--gold);display:flex;align-items:center;justify-content:center;font:700 46px Osw;filter:url(#roughs)}}
svg.a{{position:absolute;overflow:visible}}
svg.a path{{fill:none;stroke:var(--ink);stroke-width:3.2;stroke-linecap:round;stroke-linejoin:round}}
.round{{border-radius:50%;object-fit:cover;border:8px solid #fff;box-shadow:0 12px 30px rgba(36,48,44,.25);position:absolute}}
"""

DEFS = """<svg width="0" height="0" style="position:absolute"><defs>
<filter id="rough"><feTurbulence type="fractalNoise" baseFrequency="0.035 0.6" numOctaves="2" seed="4"/><feDisplacementMap in="SourceGraphic" scale="14"/></filter>
<filter id="roughs"><feTurbulence type="fractalNoise" baseFrequency="0.05" numOctaves="2" seed="7"/><feDisplacementMap in="SourceGraphic" scale="6"/></filter>
<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 .55  0 0 0 0 .5  0 0 0 0 .42  0 0 0 .5 0"/></filter>
</defs></svg>"""

TICK = '<svg class="tick" viewBox="0 0 40 40"><path d="M6 21 L16 31 L35 7" fill="none" stroke="#B48E4A" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CROSS = '<svg class="tick" viewBox="0 0 40 40"><path d="M9 9 L31 31 M31 9 L9 31" fill="none" stroke="#24302C" stroke-width="4.5" stroke-linecap="round"/></svg>'

def arrow(x, y, w, h, d, head):
    return f'<svg class="a" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px" viewBox="0 0 {w} {h}"><path d="{d}"/><path d="{head}"/></svg>'

def frame(n, body):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{DEFS}
<div class="top"><span>ГОРОДСКАЯ МАГИЯ</span><i></i><span>ЧАРОВАНИЕ</span></div>
{body}
<div class="bot"><span>0{n} / 06</span><i></i><span>@AFITCIYA_MAGIC</span></div></body></html>"""

S = []

# 1. Обложка
S.append(frame(1, f"""
<div class="h" style="position:absolute;left:64px;top:120px;font-size:132px;width:960px">Чарование<br><span class="mk">не кнопка</span><br><span style="font-size:96px">«стать неотразимой»</span></div>
<div class="photo" style="left:430px;top:600px;width:560px;height:640px;transform:rotate(3deg)"><div class="tape"></div><img src="{ph('altar-vzglyad')}" style="object-position:50% 30%"><div class="cap">у алтаря, перед работой</div></div>
<div class="hand" style="position:absolute;left:70px;top:700px;font-size:50px;width:330px;transform:rotate(-5deg)">а что тогда?<br>рассказываю<br>честно ♡</div>
{arrow(150, 900, 260, 200, "M10 10 C 40 120, 140 170, 245 150", "M222 130 L247 151 L220 170")}
<div class="hand" style="position:absolute;left:70px;top:1130px;font-size:40px;color:var(--muted)">листай →</div>
"""))

# 2. Чего не делает
S.append(frame(2, f"""
<div class="h" style="position:absolute;left:64px;top:130px;font-size:104px;width:950px">Чего Чарование<br><span class="ul">не сделает</span></div>
<div class="hand" style="position:absolute;right:80px;top:330px;font-size:44px;transform:rotate(-3deg)">лучше сказать на берегу ♡</div>
<div class="card" style="position:absolute;left:64px;right:64px;top:430px;padding:34px 34px 30px">
 <div class="li" style="font-size:34px;margin-bottom:34px">{CROSS}<div>Не заставит <b>конкретного человека</b> влюбиться. Чарование работает с тобой и твоим состоянием.</div></div>
 <div class="li" style="font-size:34px;margin-bottom:34px">{CROSS}<div>Не решит всё <b>за один вечер</b>. Состояние возвращается постепенно, и у каждой в своём темпе.</div></div>
 <div class="li" style="font-size:34px;margin-bottom:34px">{CROSS}<div>Не отменит <b>сон, отдых и заботу о себе</b>. Это остаётся на тебе, и это нормально.</div></div>
 <div class="li" style="margin:0">{CROSS}<div>Не даёт <b>гарантий</b>. Я честно делаю свою часть работы.</div></div>
</div>
<div class="hand em" style="position:absolute;left:64px;top:1150px;font-size:46px">а вот что делает, на следующем слайде</div>
"""))

# 3. Что делает
S.append(frame(3, f"""
<div class="h" style="position:absolute;left:64px;top:130px;font-size:110px;width:600px">А что<br><span class="mk">делает</span></div>
<div class="photo" style="left:610px;top:120px;width:410px;height:520px;transform:rotate(-3deg)"><div class="tape"></div><img src="{ph('portret-stena-2')}" style="object-position:50% 40%"><div class="cap">то самое состояние</div></div>
<div style="position:absolute;left:64px;top:440px;width:520px;font-size:33px;line-height:1.38">Работает с твоей женской силой: привлекательностью, уверенностью, энергией. Чтобы вернулось состояние, когда:</div>
<div class="card" style="position:absolute;left:64px;right:64px;top:720px">
 <div class="li" style="font-size:34px;margin-bottom:34px">{TICK}<div><b>горят глаза</b> и хочется наряжаться для себя</div></div>
 <div class="li" style="font-size:34px;margin-bottom:34px">{TICK}<div>внутри <b>спокойно и уверенно</b>, без вечного «а вдруг я не такая»</div></div>
 <div class="li" style="margin:0">{TICK}<div>тебе самой <b>нравится, какая ты</b>, и это видно со стороны</div></div>
</div>
<div class="hand" style="position:absolute;right:70px;top:1150px;font-size:42px;transform:rotate(-3deg)">И это состояние, когда хочется жить ♡</div>
"""))

# 4. Как проходит
steps = [("1","Пишешь мне","кодовое слово ЧАРЫ"),("2","Присылаешь фото","работа идёт по фотографии"),
         ("3","Я провожу работу","в полнолуние или новолуние, у алтаря"),("4","Ты наблюдаешь","за своим состоянием в следующие дни")]
rows = "".join(f'<div class="li" style="align-items:center;margin-bottom:30px"><div class="num">{n}</div><div><b style="font-size:36px">{t}</b><br><span style="color:var(--muted)">{s}</span></div></div>' for n,t,s in steps)
S.append(frame(4, f"""
<div class="h" style="position:absolute;left:64px;top:130px;font-size:110px">Как <span class="ul">проходит</span></div>
<div style="position:absolute;left:64px;top:330px;width:560px">{rows}</div>
<div class="photo" style="left:650px;top:380px;width:370px;height:560px;transform:rotate(4deg)"><div class="tape"></div><img src="{ph('altar-piony-krasnye-svechi')}" style="object-position:50% 45%"><div class="cap">мой алтарь</div></div>
<div class="hand" style="position:absolute;left:64px;top:1060px;font-size:46px;width:900px;transform:rotate(-2deg)">ничего делать по шагам не нужно,<br>всю работу у свечей делаю я</div>
"""))

# 5. Когда и сколько
S.append(frame(5, f"""
<div class="h" style="position:absolute;left:64px;top:130px;font-size:110px">Когда <span class="em">и</span> сколько</div>
<div class="card" style="position:absolute;left:64px;width:600px;top:330px;text-align:center;padding:34px 20px">
 <div class="hand" style="font-size:44px;color:var(--muted)">ближайшее полнолуние</div>
 <div class="h" style="font-size:112px;margin-top:10px"><span class="mk">26 октября</span></div>
</div>
<div class="hand" style="position:absolute;left:700px;top:360px;font-size:44px;width:330px;transform:rotate(5deg)">Чарование проходит<br>2 раза в месяц,<br>по Луне</div>
{arrow(690, 520, 140, 110, "M120 10 C 110 60, 80 90, 20 92", "M44 74 L18 93 L46 108")}
<div style="position:absolute;left:64px;right:64px;top:760px;display:flex;gap:28px">
 <div class="card" style="flex:1"><div class="h" style="font-size:40px">Персональное</div><div style="font-size:28px;color:var(--muted);margin:10px 0 18px">одна работа</div><div class="h" style="font-size:84px">4 000 ₽</div></div>
 <div class="card" style="flex:1;border:3px solid var(--gold)"><div class="h" style="font-size:40px">Месяц Чарования</div><div style="font-size:28px;color:var(--muted);margin:10px 0 18px">две работы, новолуние и полнолуние</div><div class="h" style="font-size:84px">7 000 ₽</div></div>
</div>
<div class="hand em" style="position:absolute;right:80px;top:1130px;font-size:44px;transform:rotate(-3deg)">вместо 8 000 ₽ по отдельности</div>
"""))

# 6. Призыв
S.append(frame(6, f"""
<img class="round" src="{ph('portret-tsss-sekret')}" style="left:700px;top:130px;width:310px;height:310px;object-position:50% 30%">
<div class="hand" style="position:absolute;left:470px;top:440px;font-size:42px;transform:rotate(-6deg)">это я, Елена ♡</div>
<div class="h" style="position:absolute;left:64px;top:150px;font-size:100px;width:620px">Хочешь<br>начать<br>с себя?</div>
<div style="position:absolute;left:64px;right:64px;top:580px;text-align:center">
 <div style="font-size:40px">Напиши в директ</div>
 <div class="h" style="font-size:230px;margin:10px 0"><span class="mk">ЧАРЫ</span></div>
</div>
<div class="card" style="position:absolute;left:64px;right:64px;top:920px;font-size:31px;line-height:1.45">
 <div class="li" style="margin-bottom:12px">{TICK}<div>пришлю мини-тест <b>«В чём твоя сила притяжения?»</b></div></div>
 <div class="li" style="margin:0">{TICK}<div>и всё про Чарование: как записаться к <b>26 октября</b></div></div>
</div>
"""))

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width":1080,"height":1350})
    for i, html in enumerate(S, 1):
        f = OUT / f"{i:02d}.html"; f.write_text(html, encoding="utf-8")
        pg.goto(f"file://{f}"); pg.wait_for_timeout(400)
        pg.screenshot(path=str(OUT / f"{i:02d}.png")); f.unlink()
    b.close()
print("готово:", OUT)
