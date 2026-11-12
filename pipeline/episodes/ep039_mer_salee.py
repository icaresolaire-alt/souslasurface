"""Pourquoi la mer est salée mais pas les rivières. Même structure que le pilote.

Sources :
- NOAA Ocean Service « Why is the ocean salty? » (oceanservice.noaa.gov/facts/whysalty.html, maj 23/09/2026) :
  « Ocean salt primarily comes from rocks on land and openings in the seafloor » ; « Rainwater that falls on land
  is slightly acidic, so it erodes rocks » ; ions emportés par les rivières vers l'océan ; « The average salinity
  is about 35 parts per thousand » (3,5 % du poids) ; sources hydrothermales et volcans sous-marins ;
  chlorure et sodium ≈ 85 % des ions dissous.
- USGS FAQ « Why is the ocean salty? » et Water Science School : pluie « slightly acidic due to carbonic acid »,
  35 pour mille ; « if the salt in the ocean could be removed and spread evenly over the Earth's land surface it
  would form a layer more than 500 feet (166 meters) thick », comparé à un immeuble de 40 étages (d'après NOAA).
- WHOI « What makes the ocean salty? » : pluie légèrement acide (CO2 → acide carbonique), dissout les roches ;
  la pluie apporte bien plus d'eau douce que de sel aux rivières.
- NOAA « Why is the ocean salty, but rivers flowing into it are not? » (oceanservice.noaa.gov/facts/
  riversnotsalty.html) : « Rain replenishes freshwater in rivers and streams, so they don't taste salty » ;
  l'océan collecte le sel de toutes les rivières ; « rivers carry an estimated four billion tons of dissolved
  salts to the ocean annually » ; à peu près autant se dépose en sédiments, l'océan « probably » n'est plus en
  train de se saler. Concordant : Countryfile, 23 mars 2025 (4 milliards de tonnes par an ; la mer n'a nulle
  part où s'écouler et l'eau douce s'évapore à sa surface).
- Rivières : Britannica « Hydrosphere : River and ocean waters » : salinité moyenne des rivières « about 0.012
  percent, or 120 ppm by weight » (0,12 g/kg) contre 3,5 % pour la mer : rapport ≈ 290 (calcul) ; Countryfile :
  « about two hundred times saltier ». Affiché prudemment : « des centaines de fois plus ».
- Évaporation : Science Notes (A. Helmenstine, maj 6 oct. 2026) « Salts do not evaporate, so they remain trapped
  in the water » ; Countryfile (concordant). Nuance Britannica : la composition de la mer dépend aussi d'autres
  processus chimiques (non affiché, schéma simplifié).
"""
import math
import random
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro (ep038 précédent).
COVER = dict(tag='Science', l1='Pourquoi la mer est salée', l2='mais pas les rivières')

WATER = '#2b6c8f'
WATER2 = '#3f8fb5'
ROCK = '#5b6670'
SALT = '#f4f1e8'


def sea(f, y, a, t, col=WATER, amp=14, x0=0, x1=W, bottom=1560):
    if a <= 0: return
    c = f.c; f.color(col, a)
    c.move_to(x0, bottom)
    for i in range(41):
        x = x0 + (x1 - x0) * i / 40
        c.line_to(x, y + amp * math.sin(x / 70 + t * 2.2))
    c.line_to(x1, bottom); c.close_path(); c.fill()


def grain(f, x, y, s, a):
    if a <= 0: return
    f.rect(x - s / 2, y - s / 2, s, s, SALT, a, s * 0.2)


def drop(f, x, y, s, a, col=WATER2):
    if a <= 0: return
    c = f.c; f.color(col, a)
    c.move_to(x, y - 22 * s)
    c.curve_to(x + 14 * s, y - 4 * s, x + 14 * s, y + 12 * s, x, y + 12 * s)
    c.curve_to(x - 14 * s, y + 12 * s, x - 14 * s, y - 4 * s, x, y - 22 * s)
    c.close_path(); c.fill()


def mountain(f, x, y, w, h, a, col=ROCK):
    if a <= 0: return
    c = f.c; f.color(col, a)
    c.move_to(x - w / 2, y); c.line_to(x - w * 0.1, y - h); c.line_to(x + w * 0.05, y - h * 0.8)
    c.line_to(x + w * 0.2, y - h * 0.95); c.line_to(x + w / 2, y); c.close_path(); c.fill()


def river_path(u):
    """Rivière qui serpente de la montagne (haut gauche) vers la mer (bas droite)."""
    x = 260 + 520 * u + 110 * math.sin(u * 7.5)
    y = 820 + 520 * u
    return x, y


def river(f, a, t, prog=1.0, width=34):
    if a <= 0: return
    n = max(2, int(60 * prog))
    pts = [river_path(i / 60) for i in range(n + 1)]
    f.line(pts, WATER2, a, width)


def jar(f, x, y, a, fill, col, label, val, grains=0, t=0, seed=0):
    """Bocal d'eau (1 kg) avec un tas de sel au fond."""
    if a <= 0: return
    w, h = 300, 380
    f.rect(x - w / 2 - 8, y - h - 8, w + 16, h + 16, LINE, a, 30)
    f.rect(x - w / 2, y - h + h * (1 - fill), w, h * fill, col, a * 0.85, 26)
    r = random.Random(seed)
    for k in range(grains):
        gx = x + r.uniform(-1, 1) * (w / 2 - 30) * (1 - 0.6 * (k / max(grains, 1)))
        gy = y - 18 - r.uniform(0, 1) * 90 * (k / max(grains, 1))
        grain(f, gx, gy, 18, a)
    f.text(label, x, y + 80, 46, INK, a, DISPLAY, True)
    f.text(val, x, y + 150, 56, SPARK, a, MONO, True)


def sun(f, x, y, r, a, t):
    if a <= 0: return
    for k in range(10):
        ang = k * math.pi / 5 + t * 0.4
        f.line([(x + (r + 14) * math.cos(ang), y + (r + 14) * math.sin(ang)),
                (x + (r + 40) * math.cos(ang), y + (r + 40) * math.sin(ang))], SPARK, a * 0.8, 8)
    f.circle(x, y, r, SPARK, a)


def building(f, x, ybase, w, floors, prog, a):
    if a <= 0: return
    fh = 15
    n = int(floors * prog)
    f.rect(x, ybase - n * fh, w, n * fh, CAPITAL, a, 4)
    for k in range(n):
        for j in range(4):
            f.rect(x + 12 + j * (w - 24) / 4, ybase - (k + 1) * fh + 4, (w - 24) / 4 - 8, 7, DEEP, a * 0.7, 2)


def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')
    c = f.c

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.8, 30.2))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('D’où vient le sel ?', W/2, 296, 46, SPARK, ha)

    # S1 — accroche (0–4) : une rivière coule dès la première image
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        words(f, 'Les rivières sont douces.', 460, 80, 0.05, INK, t_out=o)
        words(f, 'Et pourtant, la mer est salée.', 570, 70, 0.9, SPARK, t_out=o)
        mountain(f, 300, 900, 420, 260, fo)
        river(f, fo, t, 0.25 + 0.75 * ease_io(seg(t, 0.0, 2.6)))
        sea(f, 1330, fo, t)
        for k in range(8):
            u = ((t * 0.35 + k / 8) % 1.0)
            x, y = river_path(u)
            drop(f, x, y, 0.7, fo * 0.9, INK)

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.0:
        o1 = 7.4
        g1 = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'Elles s’y jettent', 470, 90, 4.2, INK, t_out=o1)
            words(f, 'depuis toujours.', 580, 90, 4.8, SPARK, t_out=o1)
            sea(f, 1250, g1, t)
            for k in range(3):
                x = 220 + 320 * k
                p = (t * 0.5 + k * 0.3) % 1.0
                f.line([(x, 760), (x + 30 * math.sin(p * 6), 760 + 470 * p)], WATER2, g1 * (1 - p), 26)
                drop(f, x + 30 * math.sin(p * 6), 760 + 470 * p, 1.2, g1)
        o2 = 10.7
        g2 = ease(seg(t, 7.6, 8.0)) * (1 - seg(t, o2, o2 + 0.3))
        if g2 > 0:
            words(f, 'Ton intuition :', 480, 72, 7.7, MUTED, t_out=o2)
            words(f, 'l’eau douce devrait', 600, 80, 8.1, INK, t_out=o2)
            words(f, 'adoucir la mer.', 710, 80, 8.7, SPARK, t_out=o2)
            ab = g2 * ease(seg(t, 8.6, 8.9))
            sea(f, 1180 - 40 * math.sin(t), ab, t, WATER)
            for k in range(6):
                p = (t * 0.6 + k / 6) % 1.0
                drop(f, 200 + 136 * k, 860 + 260 * p, 1.0, ab * (1 - p), INK)

    # S3 — la question (10.9–13.6)
    if 10.9 <= t < 13.6:
        words(f, 'Alors d’où vient', 820, 96, 11.0, INK, t_out=12.5)
        words(f, 'tout ce sel ?', 950, 116, 11.4, SPARK, t_out=12.5)

    # S4 — la preuve (13.5–30)
    if 13.4 <= t < 30.0:
        # A : la pluie ronge les roches (13.6–21.6)
        oa = 21.4
        ga = ease(seg(t, 13.5, 13.9)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'La pluie est', 430, 84, 13.6, INK, t_out=oa)
            words(f, 'légèrement acide.', 540, 84, 14.1, SPARK, t_out=oa)
            # nuage et pluie
            ca = ga * ease(seg(t, 14.4, 14.7))
            for dx, r in ((-90, 70), (0, 95), (95, 75)):
                f.circle(400 + dx, 690, r, MUTED, ca * 0.8)
            for k in range(14):
                p = (t * 1.2 + k * 0.137) % 1.0
                drop(f, 260 + (k * 23) % 290, 760 + 260 * p, 0.6, ca * (1 - p * 0.6))
            # montagne qui s'use et grains qui partent dans la rivière
            mountain(f, 400, 1180, 520, 260 - 30 * seg(t, 15.5, 20.5), ga)
            f.line([(400, 1180), (700, 1250), (980, 1240)], WATER2, ga * ease(seg(t, 15.6, 16.0)), 34)
            for k in range(10):
                q = (t * 0.45 + k / 10) % 1.0
                if t > 16.2:
                    if q < 0.5:
                        gx = 470 + 460 * q; gy = 1110 + 280 * q
                    else:
                        gx = 700 + 560 * (q - 0.5); gy = 1250 - 20 * (q - 0.5)
                    grain(f, gx, gy, 16, ga * ease(seg(t, 16.2, 16.6)))
            words(f, 'Elle ronge les roches', 1380, 52, 16.6, INK, t_out=oa)
            words(f, 'et emporte un peu de sel.', 1450, 52, 17.8, SPARK, t_out=oa)
        # B : comparer 1 kg d'eau (21.6–29.6)
        gb = ease(seg(t, 21.5, 21.9)) * (1 - seg(t, 29.4, 29.8))
        if gb > 0:
            words(f, 'Dans 1 kg d’eau :', 440, 84, 21.6, INK, t_out=29.3)
            p1 = ease(seg(t, 22.6, 25.0))
            jar(f, 300, 1100, gb * ease(seg(t, 22.2, 22.5)), 0.8, WATER2, 'rivière',
                '0,12 g', 1, t, 3)
            jar(f, 780, 1100, gb * ease(seg(t, 23.4, 23.7)), 0.8, WATER, 'mer',
                f'{int(35 * p1)} g', int(40 * p1), t, 7)
            words(f, 'Des centaines de fois', 1390, 60, 26.0, SPARK, t_out=29.3)
            words(f, 'plus salée.', 1460, 60, 26.6, SPARK, t_out=29.3)

    # S5 — la réponse (30–36) : le sel vient bien des rivières
    if 29.9 <= t < 36.0:
        o = 35.6
        a = ease(seg(t, 30.3, 30.6)) * (1 - seg(t, o, o + 0.3))
        words(f, 'Les rivières apportent', 560, 76, 30.0, INK, t_out=o)
        big_center(f, '4', 840, 280, SPARK, a, bump(t, 30.3, 0.18))
        words(f, 'milliards de tonnes', 1020, 76, 31.0, INK, t_out=o)
        words(f, 'de sel par an.', 1120, 76, 31.5, INK, t_out=o)
        words(f, 'estimation NOAA', 1260, 40, 32.5, MUTED, t_out=o, font=MONO, bold=False)

    # S6 — le retournement (36–48.4)
    if 36.0 <= t < 48.4:
        words(f, 'Le secret ?', 900, 150, 36.1, SPARK, t_out=37.9)
        # A : la rivière se renouvelle (38.1–42.6)
        oa = 42.6
        ga = ease(seg(t, 38.1, 38.5)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'La rivière', 440, 90, 38.2, INK, t_out=oa)
            words(f, 'ne fait que passer.', 550, 84, 38.7, SPARK, t_out=oa)
            for dx, r in ((-90, 60), (0, 80), (90, 60)):
                f.circle(330 + dx, 720, r, MUTED, ga * 0.8)
            for k in range(10):
                p = (t * 1.2 + k * 0.17) % 1.0
                drop(f, 220 + (k * 29) % 230, 780 + 200 * p, 0.6, ga * (1 - p * 0.6))
            mountain(f, 330, 1080, 380, 200, ga)
            f.line([(330, 1080), (600, 1180), (980, 1200)], WATER2, ga, 40)
            for k in range(7):
                q = (t * 0.6 + k / 7) % 1.0
                drop(f, 360 + 640 * q, 1080 + 110 * min(q * 2, 1), 0.8, ga, INK)
            f.text('pluie neuve, eau neuve', W/2, 1400, 44, MUTED, ga * ease(seg(t, 39.8, 40.1)), MONO, False)
        # B : la mer garde le sel (42.9–47.9)
        ob = 47.9
        gb = ease(seg(t, 42.8, 43.2)) * (1 - seg(t, ob, ob + 0.3))
        if gb > 0:
            words(f, 'La mer, elle,', 440, 84, 42.9, INK, t_out=ob)
            words(f, 'n’a pas de sortie.', 550, 84, 43.4, RED, t_out=ob)
            sun(f, 850, 720, 60, gb, t)
            sea(f, 1180, gb, t)
            # l'eau s'évapore (gouttes qui montent), le sel reste
            for k in range(7):
                p = (t * 0.5 + k / 7) % 1.0
                drop(f, 180 + 110 * k, 1150 - 380 * p, 0.8, gb * ease(seg(t, 44.0, 44.3)) * (1 - p), INK)
            r = random.Random(11)
            ng = int(40 * ease(seg(t, 44.6, 47.0)))
            for k in range(ng):
                grain(f, r.uniform(90, 990), r.uniform(1330, 1530), 16, gb)
            f.text('l’eau s’évapore', 330, 860, 40, INK, gb * ease(seg(t, 44.2, 44.5)), MONO, True)
            f.text('le sel reste', W/2, 1280, 48, SPARK, gb * ease(seg(t, 45.4, 45.7)), MONO, True)

    # S7 — l'escalade (48–56.4) : tout ce sel étalé sur les continents
    if 48.0 <= t < 56.4:
        o = 55.9
        ga = ease(seg(t, 48.1, 48.4)) * (1 - seg(t, o, o + 0.3))
        if ga > 0:
            words(f, 'Tout ce sel,', 430, 84, 48.1, INK, t_out=o)
            words(f, 'étalé sur les continents :', 540, 64, 48.7, MUTED, t_out=o)
            base = 1300
            prog = ease_io(seg(t, 49.6, 52.6))
            # couche de sel qui monte à côté d'un immeuble de 40 étages
            f.rect(100, base, 880, 10, LINE, ga, 4)
            hh = 40 * 15 * prog
            f.rect(130, base - hh, 400, hh, SALT, ga * 0.92, 6)
            building(f, 640, base, 220, 40, prog, ga)
            aa = ga * ease(seg(t, 52.6, 52.9))
            c.save(); c.translate(330, base - hh - 40); s = bump(t, 52.6, 0.15); c.scale(s, s)
            f.text('+ de 160 m', 0, 0, 64, SPARK, aa, MONO, True); c.restore()
            f.text('40 étages', 750, base - hh - 40, 44, INK, aa, MONO, True)
            f.text('estimation, d’après la NOAA et l’USGS', W/2, base + 80, 32, MUTED,
                   ga * ease(seg(t, 53.2, 53.5)), MONO, False)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        a = ease(seg(t, 56.1, 56.4))
        sea(f, 700 + 10 * math.sin(t), a, t, WATER, 12, 140, 940, 780)
        r = random.Random(5)
        for k in range(14):
            grain(f, r.uniform(170, 910), r.uniform(735, 770), 12, a)
        words(f, 'La rivière ne fait que passer.', 900, 60, 56.3, INK)
        words(f, 'La mer, elle, garde tout.', 1010, 74, 57.6, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(240, 1160, 600, 150, OCEAN, a, 28)
        pa = 0.5 + 0.5 * math.sin((t - 60) * 3)
        f.rect(240, 1160, 600, 150, SPARK, a * 0.25 * pa, 28)
        f.text('Abonne-toi.', W/2, 1255, 62, INK, a)


def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    ev += [(0.15, rise(1.2, 300, 900, 0.07))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (12.5, 29.6, 47.9, 55.9)]
    ev += [(11.0, pop(520))]
    ev += [(23.4, ding(784, amp=0.18))]
    ev += [(30.3, ding(1046, amp=0.28)), (36.1, pop(300, 0.15))]
    ev += [(52.6, ding(784, amp=0.18))]
    ev += [(56.3, pop(440)), (60.0, ding(784, amp=0.22))]
    return ev
