"""Рисует карточки «Знак дня» из week.json в queue/ДАТА.png + queue/ДАТА.txt (подпись к посту).
Запуск: python3 render.py week.json"""
import sys, json, html, pathlib, datetime as dt
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
Q = HERE / "queue"; Q.mkdir(exist_ok=True)
MONTHS = ["января","февраля","марта","апреля","мая","июня","июля","августа","сентября","октября","ноября","декабря"]

# Руны Старшего футарка, линии в поле 100x160
RUNES = {
 "fehu":    [(35,10,35,150),(35,62,78,26),(35,98,78,62)],
 "berkana": [(35,10,35,150),(35,10,72,45),(72,45,35,80),(35,80,72,115),(72,115,35,150)],
 "sowilo":  [(66,12,34,62),(34,62,66,98),(66,98,34,148)],
 "laguz":   [(40,10,40,150),(40,10,76,46)],
 "ansuz":   [(35,10,35,150),(35,10,76,46),(35,52,76,88)],
 "jera":    [(46,22,14,60),(14,60,46,98),(54,62,86,100),(86,100,54,138)],
 "wunjo":   [(35,10,35,150),(35,10,72,40),(72,40,35,70)],
 "gebo":    [(18,30,82,130),(82,30,18,130)],
 "uruz":    [(30,150,30,12),(30,12,72,46),(72,46,72,150)],
 "kenaz":   [(70,20,30,80),(30,80,70,140)],
 "othala":  [(50,10,20,50),(50,10,80,50),(20,50,85,137),(80,50,15,137)],
 "teiwaz":  [(50,10,50,150),(50,10,20,45),(50,10,80,45)],
 "inguz":   [(50,20,80,80),(80,80,50,140),(50,140,20,80),(20,80,50,20)],
 "dagaz":   [(15,25,15,135),(85,25,85,135),(15,25,85,135),(85,25,15,135)],
}

def rune_svg(key, size=330):
    lines = "".join(f'<line x1="{a}" y1="{b}" x2="{c}" y2="{d}"/>' for a,b,c,d in RUNES[key])
    return (f'<svg viewBox="-10 -5 120 170" width="{size*0.72:.0f}" height="{size}" '
            f'stroke="var(--em)" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" fill="none">{lines}</svg>')

CSS = f"""
@font-face{{font-family:Cor;src:url('file://{HERE}/fonts/Cormorant.ttf')}}
@font-face{{font-family:Cor;font-style:italic;src:url('file://{HERE}/fonts/Cormorant-Italic.ttf')}}
@font-face{{font-family:Jost;src:url('file://{HERE}/fonts/Jost.ttf')}}
@font-face{{font-family:GV;src:url('file://{HERE}/fonts/GreatVibes.ttf')}}
:root{{--cream:#F7F1E6;--paper:#FBF7EF;--em:#1E5E4B;--gold:#B48E4A;--fresh:#8CC29A;--ink:#2E3A36;--muted:#5E6B66}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-variant-numeric:lining-nums;width:1080px;height:1350px;background:var(--cream);font-family:Jost;color:var(--ink);overflow:hidden}}
.card{{position:absolute;inset:34px;border:2px solid var(--gold);border-radius:28px;background:
 radial-gradient(circle at 50% 33%, rgba(140,194,154,.32) 0, rgba(140,194,154,0) 34%), var(--paper);
 padding:56px 70px 40px;display:flex;flex-direction:column;align-items:center;text-align:center}}
.top{{font-size:21px;letter-spacing:.32em;color:var(--gold);font-weight:500}}
.date{{font-family:Cor;font-weight:600;font-size:62px;color:var(--em);margin-top:14px;line-height:1}}
.wd{{font-family:Cor;font-style:italic;font-size:34px;color:var(--muted);margin-top:4px}}
.sky{{margin-top:20px;font-size:23px;color:var(--em);background:rgba(140,194,154,.22);padding:10px 24px;border-radius:40px;font-weight:500}}
.ring{{margin-top:26px;width:330px;height:330px;border-radius:50%;border:2px solid var(--gold);display:flex;align-items:center;justify-content:center;
 box-shadow:0 0 0 12px rgba(180,142,74,.08) inset}}
.name{{font-family:GV;font-size:76px;color:var(--gold);line-height:1;margin-top:14px}}
.mean{{font-family:Cor;font-style:italic;font-size:33px;color:var(--em);margin-top:2px}}
.txt{{font-size:25px;line-height:1.45;color:var(--ink);margin-top:20px;max-width:880px}}
.how{{margin-top:22px;width:100%;text-align:left;background:#fff;border:1.5px solid rgba(180,142,74,.45);border-radius:20px;padding:20px 28px}}
.how b{{display:block;font-size:19px;letter-spacing:.2em;color:var(--gold);font-weight:600;margin-bottom:6px}}
.how p{{font-size:24px;line-height:1.42}}
.ph{{font-family:Cor;font-style:italic;font-size:33px;color:var(--em);margin-top:auto;line-height:1.2}}
.ft{{margin-top:16px;font-size:19px;letter-spacing:.18em;color:var(--muted)}}
"""

def page(d):
    date = dt.date.fromisoformat(d["date"])
    e = html.escape
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="card">
<div class="top">ГОРОДСКАЯ МАГИЯ · ЗНАК ДНЯ</div>
<div class="date">{date.day} {MONTHS[date.month-1]}</div><div class="wd">{e(d['weekday'])}</div>
<div class="sky">{e(d['sky'])}</div>
<div class="ring">{rune_svg(d['rune'], 250)}</div>
<div class="name">{e(d['rune_name'])}</div><div class="mean">{e(d['rune_meaning'])}</div>
<div class="txt">{e(d['about'])}</div>
<div class="how"><b>КАК ПРИМЕНИТЬ</b><p>{e(d['how'])}</p></div>
<div class="ph">«{e(d['phrase'])}»</div>
<div class="ft">t.me/afitciy</div>
</div></body></html>"""

def main(path):
    days = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width":1080,"height":1350})
        for d in days:
            f = Q / f"{d['date']}.html"; f.write_text(page(d), encoding="utf-8")
            pg.goto(f"file://{f}"); pg.wait_for_timeout(300)
            over = pg.evaluate("(()=>{const c=document.querySelector('.card');return c.scrollHeight-c.clientHeight})()")
            if over > 2: print(f"ВНИМАНИЕ {d['date']}: текст не влезает на {over}px")
            pg.screenshot(path=str(Q / f"{d['date']}.png")); f.unlink()
            cap = d["caption"].strip()
            if len(cap) > 1024: print(f"ВНИМАНИЕ {d['date']}: подпись {len(cap)} символов, больше 1024")
            (Q / f"{d['date']}.txt").write_text(cap + "\n", encoding="utf-8")
            print("готово", d["date"])
        b.close()

if __name__ == "__main__":
    main(sys.argv[1])
