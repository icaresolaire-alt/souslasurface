"""Commerce maritime : le t-shirt à 5 centimes de transport. Même structure que le pilote."""
import math, sys
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# route stylisée Shanghai -> Rotterdam (via Singapour, Suez)
from worldmap import WorldMap, PORTS, ROUTE_SHANGHAI_ROTTERDAM as ROUTE
MAP = WorldMap(lon=(-15, 130), lat=(-5, 60), x=60, y=600, w=960)
# (port, fraction de route où il est atteint, décalage du libellé, alignement)
STOPS = [('Shanghai', 0.0, -26, 'center'), ('Singapour', 0.27, 40, 'center'), ('Suez', 0.62, 40, 'center'), ('Rotterdam', 1.0, -26, 'center')]

def tshirt(f, x, y, s, col, a=1.0):
    if a <= 0: return
    c = f.c; f.color(col, a)
    P = [(-0.5,-0.6),(-0.18,-0.75),(0,-0.62),(0.18,-0.75),(0.5,-0.6),(0.78,-0.25),(0.5,-0.08),(0.42,-0.3),(0.42,0.75),(-0.42,0.75),(-0.42,-0.3),(-0.5,-0.08),(-0.78,-0.25)]
    c.move_to(x + P[0][0]*s, y + P[0][1]*s)
    for px, py in P[1:]: c.line_to(x + px*s, y + py*s)
    c.close_path(); c.fill()

def container(f, x, y, w, h, col, a=1.0, ribs=True):
    f.rect(x, y, w, h, col, a, 6)
    if ribs:
        n = max(3, int(w / 24))
        for i in range(1, n):
            f.line([(x + i*w/n, y + 8), (x + i*w/n, y + h - 8)], DEEP, a * 0.35, 3)

def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')

    # question persistante
    ha = ease(seg(t, 12.4, 12.9)) * (1 - seg(t, 29.6, 30.0))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Comment si peu cher ?', W/2, 296, 46, SPARK, ha)

    # S1 — accroche (0–4) : vraie carte du monde, le t-shirt suit la route maritime
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        p = ease_io(seg(t, 0.0, 3.6))
        MAP.draw(f, fo)
        MAP.route(f, ROUTE, p, fo, SPARK, 5)
        x, y = MAP.point_on(ROUTE, p)
        tshirt(f, x, y, 56, SPARK, fo)
        words(f, 'Ton t-shirt a fait', 380, 80, 0.15, INK, t_out=o)
        words(f, '20 000 km.', 490, 96, 0.6, INK, t_out=o)
        words(f, 'Le voyage lui a coûté', 1200, 72, 1.5, INK, t_out=o)
        words(f, 'moins de 10 centimes.', 1300, 84, 2.1, SPARK, t_out=o)

    # S2 — le trajet sur la carte (4–12)
    if 4.0 <= t < 12.6:
        ga = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, 12.0, 12.4))
        p = ease_io(seg(t, 4.6, 10.4))
        MAP.draw(f, ga)
        MAP.route(f, ROUTE, p, ga, SPARK, 7)
        for name, frac, dy, al in STOPS:
            col = SPARK if p >= frac else MUTED
            big = name in ('Shanghai', 'Rotterdam')
            MAP.port(f, *PORTS[name], name, ga, col, 12 if big else 8, 34 if big else 28, dy, big)
        x, y = MAP.point_on(ROUTE, p)
        tshirt(f, x, y, 44, INK, ga)
        f.text(fmt_int(19500 * p) + ' km', W/2, 470, 70, INK, ga, MONO)
        words(f, 'Environ un mois en mer.', 1250, 58, 6.8, MUTED, t_out=12.0, bold=False)
        words(f, 'Et pourtant, presque gratuit.', 1340, 58, 9.4, SPARK, t_out=12.0)

    # S3 — la question (12–14.5)
    if 12.2 <= t < 14.9:
        words(f, 'Comment', 840, 120, 12.4, INK, t_out=14.4)
        words(f, 'c’est possible ?', 980, 110, 12.8, SPARK, t_out=14.4)

    # S4 — la preuve : un conteneur (14.5–30)
    if 14.4 <= t < 30.2:
        ga = ease(seg(t, 14.5, 14.9)) * (1 - seg(t, 29.6, 30.0))
        cx0, cy0, cw, chh = 120, 700, 840, 340
        container(f, cx0, cy0, cw, chh, CAPITAL, ga, ribs=False)
        f.text('1 conteneur de 40 pieds', W/2, cy0 - 30, 40, MUTED, ga, bold=False)
        fill = ease_io(seg(t, 15.2, 20.5))
        cols, rows = 20, 8; N = cols * rows
        for i in range(int(N * fill)):
            r, cidx = divmod(i, cols)
            tshirt(f, cx0 + 30 + cidx * (cw - 60) / (cols - 1), cy0 + chh - 40 - r * 40, 30, SPARK, ga)
        f.text('t-shirts', W/2, 470, 44, MUTED, ga, bold=False)
        big_center(f, fmt_int(80000 * fill), 560, 96, SPARK, ga, bump(t, 20.5, 0.15))
        # prix du conteneur puis division
        pa = ease(seg(t, 21.2, 21.6)) * ga
        f.text('Shanghai → Rotterdam', W/2, 1140, 46, MUTED, pa, bold=False)
        big_center(f, '≈ 4 000 $', 1250, 96, INK, pa, bump(t, 21.2))
        da = ease(seg(t, 23.8, 24.2)) * ga
        big_center(f, '4 000 $ ÷ 80 000', 1380, 64, MUTED, da)
        ra = ease(seg(t, 25.6, 26.0)) * ga
        big_center(f, '= 0,05 $', 1500, 110, SPARK, ra, bump(t, 25.6, 0.22))

    # S5 — la réponse (30–36)
    if 29.9 <= t < 36.4:
        a = ease(seg(t, 30.0, 30.3)) * (1 - seg(t, 35.8, 36.2))
        big_center(f, '5 centimes', 860, 170, SPARK, a, bump(t, 30.0, 0.12), DISPLAY)
        words(f, 'par t-shirt.', 990, 72, 30.6, INK, t_out=35.8)
        words(f, 'Sur un t-shirt à 10 €, c’est 0,5 %.', 1150, 52, 31.8, MUTED, t_out=35.8, bold=False)
        f.text('Tarif Drewry de septembre 2026. En 2021, c’était le double.', W/2, 1400, 30, MUTED, ease(seg(t, 32.8, 33.2)) * a, bold=False)

    # S6 — le retournement : la taille (36–48)
    if 36.0 <= t < 48.4:
        words(f, 'Le secret ?', 760, 120, 36.1, INK, t_out=38.1)
        words(f, 'La taille.', 900, 120, 36.7, SPARK, t_out=38.1)
        ga = ease(seg(t, 38.3, 38.8)) * (1 - seg(t, 47.9, 48.3))
        if ga > 0:
            # coque vue de côté
            hx0, hx1, hy = 90, 990, 1180
            c = f.c; f.color(CAPITAL, ga)
            c.move_to(hx0, hy); c.line_to(hx1, hy); c.line_to(hx1 - 50, hy + 150); c.line_to(hx0 + 60, hy + 150); c.close_path(); c.fill()
            f.rect(hx1 - 140, hy - 230, 90, 230, INK, ga * 0.9, 6)   # château
            # piles de conteneurs qui montent
            cols, rows = 14, 10
            pal = [SPARK, EARTH, RED, CAPITAL, MUTED]
            n = int(cols * rows * ease_io(seg(t, 39.0, 44.0)))
            bw = (hx1 - 170 - hx0 - 20) / cols
            for i in range(n):
                r, cidx = divmod(i, cols)
                col = pal[(cidx * 3 + r * 7) % len(pal)]
                f.rect(hx0 + 20 + cidx * bw + 2, hy - (r + 1) * 46 + 3, bw - 4, 40, col, ga * 0.95, 3)
            f.text('conteneurs sur un seul navire', W/2, 470, 42, MUTED, ga, bold=False)
            big_center(f, fmt_int(24000 * ease_io(seg(t, 39.0, 44.0))), 590, 110, SPARK, ga, bump(t, 44.0, 0.18))
            f.text('(en équivalent 20 pieds)', W/2, 650, 30, MUTED, ga, bold=False)
            words(f, 'Pour une vingtaine de marins.', 1440, 54, 44.6, INK, t_out=47.9)
            words(f, 'Le coût se divise à l’infini.', 1520, 54, 45.6, SPARK, t_out=47.9)

    # S7 — l'échelle mondiale (48–56)
    if 48.0 <= t < 56.4:
        out = 1 - seg(t, 55.9, 56.3)
        words(f, 'Environ', 560, 64, 48.2, INK, t_out=55.9)
        v = 0.80 * ease(seg(t, 48.6, 50.0))
        big_center(f, f'{int(round(v*100))} %', 760, 200, SPARK, out * ease(seg(t, 48.5, 48.8)), bump(t, 50.0, 0.12))
        words(f, 'des marchandises du monde', 900, 60, 50.2, INK, t_out=55.9)
        words(f, 'voyagent par la mer.', 980, 60, 50.7, INK, t_out=55.9)
        items = ['ton téléphone', 'ta télé', 'ton café', 'tes baskets']
        for i, s in enumerate(items):
            ia = ease(seg(t, 52.0 + i * 0.6, 52.3 + i * 0.6)) * out
            x = 290 + (i % 2) * 500; y = 1180 + (i // 2) * 110
            f.rect(x - 220, y - 62, 440, 88, OCEAN, ia, 44)
            f.text(s, x, y - 4, 44, INK, ia)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        words(f, 'La mondialisation', 720, 76, 56.3)
        words(f, 'tient dans une boîte en métal.', 830, 64, 57.2, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(110, 1020, 860, 220, OCEAN, a, 28)
        f.text('Abonne-toi.', W/2, 1100, 58, INK, a)
        f.text('Demain : pourquoi tant de navires', W/2, 1166, 38, MUTED, a, bold=False)
        f.text('sont immatriculés au Panama.', W/2, 1214, 38, MUTED, a, bold=False)

def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    for t0, n in ((0.15, 4), (0.6, 2), (1.5, 4), (2.1, 4)):
        for i in range(n): ev.append((t0 + i * 0.11, pop(420 + 40 * i, 0.09)))
    ev += [(x, whoosh(0.5, 0.18)) for x in (3.9, 12.1, 14.4, 29.7, 35.9, 47.9, 55.9)]
    for name_t in (4.6, 6.5, 9.0, 10.4): ev.append((name_t, clink(1700)))
    ev += [(6.8, pop(392)), (9.4, pop(523)), (12.4, pop(330)), (12.8, pop(440))]
    x = 15.2
    while x < 20.5: ev.append((x, tick())); x += 0.09
    ev += [(20.5, ding(880, amp=0.25)), (21.2, pop(392)), (23.8, pop(330)), (25.6, ding(1175, amp=0.3)),
           (30.0, ding(1046, amp=0.3)), (36.1, pop(300, 0.15)), (36.7, pop(450, 0.15))]
    x = 39.0
    while x < 44.0: ev.append((x, clink(900 + (x - 39) * 120))); x += 0.25
    ev += [(44.0, ding(880, amp=0.25)), (48.6, rise(1.4, 300, 1046, 0.1)), (50.0, ding(1046, amp=0.25))]
    for i in range(4): ev.append((52.0 + i * 0.6, pop(500 + i * 60)))
    ev += [(56.3, pop(440)), (57.2, pop(550)), (60.0, ding(784, amp=0.22))]
    return ev

