"""Астрологические данные на день (тропический зодиак, геоцентрически).
Считается на 06:00 по Москве (03:00 UTC). Использует astronomy-engine."""
import sys, json, datetime as dt
import astronomy as A

SIGNS = ["Овен","Телец","Близнецы","Рак","Лев","Дева","Весы","Скорпион","Стрелец","Козерог","Водолей","Рыбы"]
SIGNS_IN = ["в Овне","в Тельце","в Близнецах","в Раке","во Льве","в Деве","в Весах","в Скорпионе","в Стрельце","в Козероге","в Водолее","в Рыбах"]
BODIES = [("Солнце",A.Body.Sun),("Луна",A.Body.Moon),("Меркурий",A.Body.Mercury),("Венера",A.Body.Venus),
          ("Марс",A.Body.Mars),("Юпитер",A.Body.Jupiter),("Сатурн",A.Body.Saturn)]
WEEKDAY = [("понедельник","Луна"),("вторник","Марс"),("среда","Меркурий"),("четверг","Юпитер"),
           ("пятница","Венера"),("суббота","Сатурн"),("воскресенье","Солнце")]
ASPECTS = [(0,"соединение"),(60,"секстиль"),(90,"квадрат"),(120,"трин"),(180,"оппозиция")]

def lon(body, t):
    if body == A.Body.Moon:
        return A.EclipticGeoMoon(t).lon % 360
    return A.Ecliptic(A.GeoVector(body, t, True)).elon % 360

def phase_name(a):
    if a < 10 or a >= 350: return "новолуние"
    if a < 80: return "растущая Луна"
    if a < 100: return "первая четверть, растущая Луна"
    if a < 170: return "растущая Луна"
    if a < 190: return "полнолуние"
    if a < 260: return "убывающая Луна"
    if a < 280: return "последняя четверть, убывающая Луна"
    return "убывающая Луна, перед новолунием"

def day(date):
    utc = dt.datetime(date.year, date.month, date.day, 3, 0)
    t = A.Time.Make(utc.year, utc.month, utc.day, utc.hour, 0, 0)
    t1 = t.AddDays(1); tm = t.AddDays(-1)
    out = {"date": date.isoformat(), "weekday": WEEKDAY[date.weekday()][0],
           "day_ruler": WEEKDAY[date.weekday()][1], "planets": {}, "aspects": [], "events": []}
    L = {}
    for name, b in BODIES:
        l0, l1, lm = lon(b, t), lon(b, t1), lon(b, tm)
        L[name] = l0
        d = ((l1 - l0 + 180) % 360) - 180
        dm = ((l0 - lm + 180) % 360) - 180
        retro = d < 0
        p = {"sign": SIGNS[int(l0 // 30)], "deg": round(l0 % 30, 1), "retro": retro}
        out["planets"][name] = p
        if name not in ("Солнце", "Луна") and (dm < 0) != (d < 0):
            out["events"].append(f"{name} разворачивается {'назад (начало ретроградности)' if d < 0 else 'в прямое движение'}")
        if int(l0 // 30) != int(l1 // 30) and name != "Луна":
            out["events"].append(f"{name} переходит {SIGNS_IN[int(l1 // 30)]}")
    ph = A.MoonPhase(t)
    out["moon_phase_angle"] = round(ph, 1)
    out["moon_phase"] = phase_name(ph)
    out["moon_sign"] = out["planets"]["Луна"]["sign"]
    # фазы в ближайшие сутки
    for ang, nm in [(0, "Новолуние"), (90, "Первая четверть"), (180, "Полнолуние"), (270, "Последняя четверть")]:
        q = A.SearchMoonPhase(ang, t, 1.0)
        if q:
            u = q.Utc() + dt.timedelta(hours=3)
            out["events"].append(f"{nm}: {u.strftime('%d.%m %H:%M')} МСК")
    # ближайшие развороты Меркурия и Венеры (на 30 дней вперёд), чтобы предупреждать заранее
    out["upcoming"] = []
    for name, b in BODIES[2:4]:
        prev = None
        for k in range(0, 31):
            tk = t.AddDays(k)
            d = ((lon(b, tk.AddDays(1)) - lon(b, tk) + 180) % 360) - 180
            if prev is not None and (prev < 0) != (d < 0):
                u = tk.Utc() + dt.timedelta(hours=3)
                out["upcoming"].append(f"{name} {'становится ретроградным' if d < 0 else 'выходит из ретроградности'} около {u.strftime('%d.%m')}")
                break
            prev = d
    names = [n for n, _ in BODIES]
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            diff = abs(((L[a] - L[b] + 180) % 360) - 180)
            orb = 6 if "Луна" in (a, b) else 3
            for ang, nm in ASPECTS:
                if abs(diff - ang) <= orb:
                    out["aspects"].append(f"{a} {nm} {b} (орб {abs(diff-ang):.1f}°)")
    return out

if __name__ == "__main__":
    start = dt.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else dt.date.today()
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    print(json.dumps([day(start + dt.timedelta(days=k)) for k in range(n)], ensure_ascii=False, indent=1))
