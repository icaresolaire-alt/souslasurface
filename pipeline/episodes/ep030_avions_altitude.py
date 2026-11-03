"""Pourquoi les avions de ligne volent vers 10 000 mètres. Même structure que le pilote.

Sources :
- Altitude de croisière : Flight Deck Friend « How High Do Passenger Planes Fly? »
  (« Most commercial passenger jets typically cruise at an altitude of 30,000 to 42,000 feet », soit 9 à 13 km) ;
  Military & Aerospace Electronics, 21 août 2026, « Why commercial aircraft cruise around 35,000 feet »
  (35 000 pieds = 10 700 m, « a compromise between aerodynamic efficiency and engine performance »).
- Air plus rare : Wikipedia « International Standard Atmosphere » (niveau de la mer : 15 °C, 1,225 kg/m³ ;
  11 000 m : −56,5 °C, 22 632 Pa, 0,3639 kg/m³). Calcul : 0,3639 / 1,225 = 29,7 % -> « 30 % », 3,4 fois moins.
- Moins de traînée, plus de distance pour le carburant brûlé : Military & Aerospace Electronics 2026
  (« The air gets thinner with altitude, which lessens aerodynamic drag and can help an aircraft cover more
  distance for the fuel it burns »). Limites : « fewer air molecules are available to produce the aerodynamic
  forces that keep the aircraft aloft » ; « Engines face their own limits as atmospheric pressure and density
  decrease ».
- Météo : Britannica « Troposphere » (« contains most of Earth's clouds and is the location where weather
  primarily occurs ») ; formulation prudente « au-dessus de la plupart des nuages ».
- Concorde : Flight Deck Friend (« cruise at about 60,000 feet or 18,000 meters ») ; British Airways
  « Celebrating Concorde » et Migflug « Mach 2, 60,000 Feet » (Mach 2).
- Everest : 8 848,86 m (Népal et Chine, 8 déc. 2020 : Kathmandu Post, Al Jazeera).
"""
import math, random
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro (ep029 précédent).
COVER = dict(tag='Science', l1='Pourquoi ton avion vole', l2='à 10 000 mètres')

rnd = random.Random(30)
DOTS = [(rnd.random(), rnd.random(), rnd.random() * 6.28) for _ in range(120)]


def plane(f, x, y, a, s=1.0, ang=0.0):
    """Avion de ligne de profil, nez à droite."""
    if a <= 0: return
    c = f.c; c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    f.color(INK, a)
    c.new_sub_path(); c.move_to(-120, -10); c.line_to(95, -14)
    c.curve_to(125, -14, 135, 0, 135, 2); c.curve_to(130, 12, 110, 14, 95, 14)
    c.line_to(-110, 12); c.close_path(); c.fill()
    # dérive
    c.move_to(-120, -10); c.line_to(-140, -62); c.line_to(-112, -62); c.line_to(-80, -10); c.close_path(); c.fill()
    # aile
    f.color(MUTED, a)
    c.move_to(-10, 4); c.line_to(-60, 54); c.line_to(-38, 54); c.line_to(40, 4); c.close_path(); c.fill()
    # hublots
    f.color(OCEAN, a)
    for k in range(7):
        c.new_sub_path(); c.arc(-60 + k * 22, -2, 4, 0, 6.29); c.fill()
    c.restore()


def air_box(f, x, y, w, h, n, a, t, col=MUTED):
    f.rect(x, y, w, h, OCEAN, a * 0.9, 18)
    for i in range(n):
        u, v, ph = DOTS[i]
        px = x + 20 + (w - 40) * u + 8 * math.sin(t * 2.2 + ph)
        py = y + 20 + (h - 40) * v + 8 * math.cos(t * 1.9 + ph)
        f.circle(px, py, 9, col, a * 0.85)


def cloud(f, x, y, s, a, col=CAPITAL):
    for dx, dy, r in ((-60, 10, 40), (-15, -12, 55), (40, 0, 45), (80, 14, 32)):
        f.circle(x + dx * s, y + dy * s, r * s, col, a)
    f.rect(x - 95 * s, y + 10 * s, 205 * s, 40 * s, col, a, 18 * s)


def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.8, 30.2))
    f.rect(120, 236, 840, 92, OCEAN, ha * 0.9, 46)
    f.text('Pourquoi voler si haut ?', W/2, 296, 44, SPARK, ha)

    # S1 — accroche (0–4) : l'avion décolle, l'altimètre grimpe
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        p = ease_io(seg(t, 0.0, 3.6))
        x0, y0, x1, y1 = 140, 1380, 900, 760
        f.line([(x0, y0), (lerp(x0, x1, p), lerp(y0, y1, p))], SPARK, fo * 0.5, 4, [10, 14])
        plane(f, lerp(x0, x1, p), lerp(y0, y1, p), fo, 0.9, -0.55 * (1 - p) - 0.1)
        f.rect(60, 1400, 960, 10, EARTH, fo, 5)
        words(f, 'Ton avion de ligne', 470, 74, 0.05, INK, t_out=o)
        words(f, 'vole à 10 000 mètres.', 580, 74, 0.6, SPARK, t_out=o)
        f.text(fmt_int(10000 * p) + ' m', W/2, 1520, 64, INK, fo * ease(seg(t, 0.1, 0.4)), MONO, True)

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.0:
        o1 = 7.4
        g1 = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'Pourtant, monter', 470, 76, 4.2, INK, t_out=o1)
            words(f, 'coûte du carburant.', 580, 76, 4.7, SPARK, t_out=o1)
            # jauge qui baisse
            lvl = 1 - 0.35 * ease_io(seg(t, 5.0, 7.0))
            f.rect(400, 760, 280, 560, LINE, g1, 28)
            f.rect(420, 780 + 520 * (1 - lvl), 240, 520 * lvl, SPARK, g1 * 0.85, 18)
            f.text('carburant', W/2, 1400, 44, MUTED, g1, MONO, False)
        o2 = 10.7
        g2 = ease(seg(t, 7.6, 8.0)) * (1 - seg(t, o2, o2 + 0.3))
        if g2 > 0:
            words(f, 'Et là-haut, dehors :', 470, 72, 7.7, MUTED, t_out=o2)
            temp = lerp(15, -56.5, ease_io(seg(t, 8.2, 10.0)))
            s = f'{temp:+.1f}'.replace('.', ',').replace('-', '−') + ' °C'
            big_center(f, s, 900, 170, INK if temp > 0 else '#9fd3ff', g2)
            # thermomètre
            f.rect(500, 1000, 80, 400, LINE, g2, 40)
            hgt = 360 * (temp + 60) / 75
            f.rect(515, 1385 - hgt, 50, hgt, RED if temp > 0 else '#9fd3ff', g2, 25)
            f.circle(540, 1400, 60, RED if temp > 0 else '#9fd3ff', g2)

    # S3 — la question (10.9–13.6)
    if 10.9 <= t < 13.6:
        words(f, 'Alors pourquoi', 820, 96, 11.0, INK, t_out=12.5)
        words(f, 'monter si haut ?', 950, 96, 11.4, SPARK, t_out=12.5)

    # S4 — la preuve (13.5–30)
    if 13.4 <= t < 30.0:
        # A : on monte avec lui, l'Everest passe dessous (13.6–21)
        oa = 21.0
        ga = ease(seg(t, 13.5, 13.9)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Montons avec lui.', 440, 76, 13.6, INK, t_out=oa)
            yb, ytop = 1450, 650            # 0 m en bas, 12 000 m en haut
            ym = lambda m: yb - (yb - ytop) * m / 12000
            # axe gradué
            f.line([(150, yb), (150, ytop)], LINE, ga, 4)
            for m in range(0, 12001, 2000):
                f.line([(140, ym(m)), (165, ym(m))], LINE, ga, 3)
                f.text(f'{m // 1000} km', 130, ym(m) + 10, 28, MUTED, ga, MONO, False, 'right')
            # Everest
            ev = ym(8849)
            c = f.c; f.color(CAPITAL, ga)
            c.move_to(220, yb); c.line_to(470, ev); c.line_to(720, yb); c.close_path(); c.fill()
            f.color(INK, ga * 0.9)
            c.move_to(420, ev + 70); c.line_to(470, ev); c.line_to(520, ev + 70); c.close_path(); c.fill()
            f.text('Everest 8 849 m', 470, ev - 26, 36, MUTED, ga * ease(seg(t, 14.2, 14.5)), MONO, False)
            f.rect(160, yb, 860, 10, EARTH, ga, 5)
            # avion qui grimpe
            p = ease_io(seg(t, 14.6, 19.4))
            alt = 11000 * p
            plane(f, 820, ym(alt) - 10, ga, 0.75)
            f.text(fmt_int(alt) + ' m', 820, ym(alt) + 80, 52, SPARK, ga, MONO, True)
            f.text('Plus haut que l’Everest.', W/2, 560, 56, SPARK, ga * ease(seg(t, 18.0, 18.4)))
        # B : un mètre cube d'air au sol et en haut (21.3–29.6)
        gb = ease(seg(t, 21.2, 21.6)) * (1 - seg(t, 29.4, 29.8))
        if gb > 0:
            words(f, 'Pèse 1 m³ d’air', 440, 76, 21.3, INK, t_out=29.4)
            words(f, 'en bas, puis en haut.', 550, 76, 21.8, SPARK, t_out=29.4)
            nb = int(120 * ease(seg(t, 22.4, 23.4)))
            air_box(f, 80, 700, 440, 560, nb, gb, t)
            f.text('Au sol', 300, 1330, 46, INK, gb)
            f.text(f'{1.225 * ease(seg(t, 22.4, 23.4)):.3f}'.replace('.', ',') + ' kg', 300, 1400, 44, MUTED, gb, MONO, True)
            nh = int(36 * ease(seg(t, 24.6, 25.6)))
            g2 = ease(seg(t, 24.4, 24.8))
            air_box(f, 560, 700, 440, 560, nh, gb * g2, t, SPARK)
            f.text('À 11 000 m', 780, 1330, 46, SPARK, gb * g2)
            f.text(f'{0.364 * ease(seg(t, 24.6, 25.6)):.3f}'.replace('.', ',') + ' kg', 780, 1400, 44, MUTED, gb * g2, MONO, True)
            f.text('Atmosphère type OACI', W/2, 1490, 30, MUTED, gb * ease(seg(t, 26.0, 26.3)), MONO, False)

    # S5 — la réponse (30–36)
    if 29.9 <= t < 36.0:
        o = 35.6
        a = ease(seg(t, 30.3, 30.6)) * (1 - seg(t, o, o + 0.3))
        big_center(f, '30 %', 820, 240, SPARK, a, bump(t, 30.3, 0.18))
        words(f, 'Là-haut, il ne reste que', 1000, 66, 31.0, INK, t_out=o)
        words(f, '30 % de l’air du sol.', 1100, 66, 31.6, INK, t_out=o)
        f.text('Plus de 3 fois moins dense', W/2, 1300, 38, MUTED, ease(seg(t, 32.6, 33.0)) * a, MONO, False)

    # S6 — le retournement (36–48.4)
    if 36.0 <= t < 48.4:
        words(f, 'Le secret ?', 900, 130, 36.1, INK, t_out=37.9)
        # A : l'air freine (38.1–42.6)
        oa = 42.6
        ga = ease(seg(t, 38.1, 38.5)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'L’air freine l’avion.', 440, 76, 38.2, INK, t_out=oa)
            words(f, 'Moins d’air, moins de frein.', 550, 70, 38.8, SPARK, t_out=oa)
            k = ease_io(seg(t, 39.6, 41.0))           # 0 = au sol, 1 = en haut
            n = int(lerp(110, 33, k))
            for i in range(n):
                u, v, ph = DOTS[i]
                px = 1040 - ((u * 1000 + t * 420) % 1000)
                py = 740 + 520 * v
                f.circle(px, py, 8, MUTED, ga * 0.8)
            plane(f, 560, 1000, ga, 1.1)
            L = lerp(320, 110, k)                      # flèche de traînée
            f.line([(380, 1000), (380 - L, 1000)], RED, ga, 12)
            c = f.c; f.color(RED, ga)
            c.move_to(380 - L - 30, 1000); c.line_to(380 - L + 6, 978); c.line_to(380 - L + 6, 1022); c.close_path(); c.fill()
            f.text('frein', 380 - L / 2, 960, 36, RED, ga, MONO, True)
            f.text('Même carburant,', W/2, 1380, 50, INK, ga * ease(seg(t, 40.8, 41.1)))
            f.text('plus de distance.', W/2, 1450, 50, SPARK, ga * ease(seg(t, 40.8, 41.1)))
        # B : au-dessus de la météo (42.9–48)
        ob = 47.9
        gb = ease(seg(t, 42.8, 43.2)) * (1 - seg(t, ob, ob + 0.3))
        if gb > 0:
            words(f, 'Bonus : il passe au-dessus', 440, 68, 42.9, INK, t_out=ob)
            words(f, 'de la plupart des nuages.', 550, 68, 43.4, SPARK, t_out=ob)
            drift = (t - 43) * 30
            for i, (cx, cy, s) in enumerate(((200, 1150, 1.2), (560, 1230, 1.5), (900, 1140, 1.1), (380, 1330, 1.0), (760, 1360, 1.2))):
                cloud(f, (cx - drift) % 1200 - 60, cy, s, gb * 0.9)
            if 0.5 < (t * 1.3) % 2 < 0.62:
                f.line([(560, 1290), (530, 1360), (570, 1360), (540, 1440)], SPARK, gb, 6)
            plane(f, 540, 800 + 6 * math.sin(t * 2), gb, 0.9)
            f.text('La plupart des nuages restent plus bas.', W/2, 1520, 36, MUTED, gb * ease(seg(t, 45.0, 45.3)), MONO, False)

    # S7 — l'escalade (48–56.4) : pourquoi pas plus haut ?
    if 48.0 <= t < 56.4:
        oa = 51.6
        ga = ease(seg(t, 48.1, 48.4)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Alors pourquoi', 440, 80, 48.1, INK, t_out=oa)
            words(f, 'pas plus haut ?', 550, 80, 48.5, SPARK, t_out=oa)
            wob = math.sin(t * 7) * 0.06 * seg(t, 49.2, 49.8)
            for i in range(12):
                u, v, ph = DOTS[i]
                f.circle(100 + 880 * u, 760 + 440 * v + 6 * math.sin(t * 2 + ph), 8, MUTED, ga * 0.7)
            plane(f, W/2, 980, ga, 1.1, wob)
            f.text('Trop peu d’air pour porter les ailes', W/2, 1340, 44, INK, ga * ease(seg(t, 49.2, 49.5)))
            f.text('et nourrir les réacteurs.', W/2, 1405, 44, INK, ga * ease(seg(t, 49.2, 49.5)))
        o = 55.9
        gb = ease(seg(t, 51.8, 52.1)) * (1 - seg(t, o, o + 0.3))
        if gb > 0:
            words(f, 'Le Concorde, lui,', 440, 76, 51.9, INK, t_out=o)
            words(f, 'montait à 18 000 m.', 550, 76, 52.4, SPARK, t_out=o)
            yb = 1380; sc = 560 / 18000
            h1 = 11000 * sc * ease_io(seg(t, 52.4, 53.2))
            h2 = 18000 * sc * ease_io(seg(t, 52.8, 54.0))
            f.rect(240, yb - h1, 220, h1, CAPITAL, gb, 14)
            f.rect(620, yb - h2, 220, h2, SPARK, gb, 14)
            f.text('avion de ligne', 350, yb + 50, 34, MUTED, gb, MONO, False)
            f.text('Concorde', 730, yb + 50, 34, SPARK, gb, MONO, True)
            f.text('11 000 m', 350, yb - h1 - 20, 40, INK, gb * (h1 > 10), MONO, True)
            f.text('18 000 m', 730, yb - h2 - 20, 40, INK, gb * (h2 > 10), MONO, True)
            f.text('Mais à 2 fois la vitesse du son.', W/2, 1520, 44, MUTED, gb * ease(seg(t, 54.0, 54.3)))

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        words(f, 'Ton avion ne monte pas pour la vue.', 760, 58, 56.3, INK)
        words(f, 'Il monte pour fuir l’air.', 870, 72, 57.6, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(240, 1160, 600, 150, OCEAN, a, 28)
        pa = 0.5 + 0.5 * math.sin((t - 60) * 3)
        f.rect(240, 1160, 600, 150, SPARK, a * 0.25 * pa, 28)
        f.text('Abonne-toi.', W/2, 1255, 62, INK, a)


def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    ev += [(0.15, pop(440, 0.09)), (0.6, rise(3.0, 300, 800, 0.06))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (12.5, 29.6, 47.9, 55.9)]
    ev += [(11.0, pop(520))]
    ev += [(18.0, clink(1500))]
    ev += [(24.6, ding(784, amp=0.2))]
    ev += [(30.3, ding(1046, amp=0.28)), (36.1, pop(300, 0.15))]
    ev += [(40.8, ding(784, amp=0.18))]
    ev += [(49.2, pop(360, 0.12)), (53.8, ding(880, amp=0.18))]
    ev += [(56.3, pop(440)), (60.0, ding(784, amp=0.22))]
    return ev
