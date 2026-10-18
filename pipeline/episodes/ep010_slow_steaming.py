"""Slow steaming : pourquoi les navires ralentissent exprès. Même structure que le pilote."""
import math
from lib import *
from kinetic import words, bump, big_center
from worldmap import WorldMap, PORTS, ROUTE_SHANGHAI_ROTTERDAM as ROUTE

TOTAL = 66.0
MAP = WorldMap(lon=(-15, 130), lat=(-5, 60), x=60, y=560, w=960)

NM = 10500                     # Shanghai -> Rotterdam via Suez, milles nautiques (≈ 19 500 km)
D_FAST = NM / 24 / 24          # ≈ 18,2 jours à 24 nœuds
D_SLOW = NM / 18 / 24          # ≈ 24,3 jours à 18 nœuds
FUEL_SLOW = (18 / 24) ** 2     # loi du cube : carburant par trajet ∝ v² -> 0,5625

def fr(x, d=1): return f'{x:.{d}f}'.replace('.', ',')

def ship(f, x, y, s, col, a=1.0, ang=0.0):
    """Petit porte-conteneurs vu de côté (orientable)."""
    if a <= 0: return
    c = f.c; c.save(); c.translate(x, y); c.rotate(ang); f.color(col, a)
    c.move_to(-1.0*s, -0.1*s); c.line_to(1.0*s, -0.1*s); c.line_to(0.75*s, 0.35*s); c.line_to(-0.85*s, 0.35*s); c.close_path(); c.fill()
    for i in range(4): f.rect(-0.8*s + i*0.36*s, -0.42*s, 0.3*s, 0.3*s, col, a, 2)
    f.rect(0.62*s, -0.62*s, 0.22*s, 0.52*s, col, a, 2)
    c.restore()

def heading(p):
    x0, y0 = MAP.point_on(ROUTE, max(0, p - 0.01)); x1, y1 = MAP.point_on(ROUTE, min(1, p + 0.01))
    a = math.atan2(y1 - y0, x1 - x0)
    if abs(a) > math.pi / 2: a = a - math.pi if a > 0 else a + math.pi   # jamais à l'envers
    return a

def wake(f, p, col, a, n=5):
    for i in range(1, n + 1):
        q = p - i * 0.008
        if q <= 0: break
        x, y = MAP.point_on(ROUTE, q); f.circle(x, y, 6 - i, col, a * (1 - i / (n + 1)) * 0.7)

def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')

    # question persistante
    ha = ease(seg(t, 12.4, 12.9)) * (1 - seg(t, 29.6, 30.0))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Pourquoi ralentir ?', W/2, 296, 46, SPARK, ha)

    # S1 — accroche (0–4) : deux navires partent de Shanghai, l'un file, l'autre traîne
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        MAP.draw(f, fo)
        pf = 0.30 * ease_io(seg(t, 0.0, 3.8)); ps = 0.30 * 0.75 * ease_io(seg(t, 0.0, 3.8))
        MAP.route(f, ROUTE, pf, fo, RED, 4)
        for p, col in ((pf, RED), (ps, SPARK)):
            wake(f, p, col, fo); x, y = MAP.point_on(ROUTE, p); ship(f, x, y - 18, 30, col, fo, heading(p))
        words(f, 'Les cargos', 380, 90, 0.15, INK, t_out=o)
        words(f, 'ralentissent exprès.', 490, 90, 0.5, SPARK, t_out=o)
        words(f, 'Et c’est plus rentable.', 1200, 72, 1.6, INK, t_out=o)

    # S2 — enjeu (4–12)
    if 4.0 <= t < 12.6:
        ga = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, 12.0, 12.4))
        a1 = ease(seg(t, 4.2, 4.6)) * (1 - seg(t, 7.3, 7.6)) * ga
        if a1 > 0:
            f.text('Avant 2008, les gros cargos filaient à', W/2, 600, 46, MUTED, a1, bold=False)
            v = 24 * ease(seg(t, 4.4, 5.6))
            big_center(f, f'{int(round(v))} nœuds', 790, 140, INK, a1, bump(t, 5.6, 0.15))
            f.text(f'≈ {int(round(v * 1.852))} km/h', W/2, 900, 56, MUTED, a1, MONO)
            # jauge de vitesse qui tremble
            sh = 2 * math.sin(t * 40) * seg(t, 5.6, 6.0)
            f.rect(190, 1000, 700, 26, OCEAN, a1, 13)
            f.rect(190, 1000, 700 * v / 26 + sh, 26, RED, a1, 13)
        a2 = ease(seg(t, 7.6, 7.9)) * ga
        if a2 > 0:
            f.text('Vers 2009, Maersk passe à', W/2, 600, 50, MUTED, a2, bold=False)
            v = 24 - 6 * ease(seg(t, 7.9, 9.4))
            big_center(f, f'{int(round(v))} nœuds', 790, 140, SPARK, a2, bump(t, 9.4, 0.15))
            f.rect(190, 1000, 700, 26, OCEAN, a2, 13)
            f.rect(190, 1000, 700 * v / 26, 26, SPARK, a2, 13)
        words(f, 'Le temps, c’est de l’argent…', 1240, 58, 9.8, MUTED, t_out=12.0, bold=False)
        words(f, 'Alors pourquoi ?', 1340, 68, 10.8, SPARK, t_out=12.0)

    # S3 — la question (12–14.5)
    if 12.2 <= t < 14.9:
        words(f, 'Pourquoi', 840, 130, 12.4, INK, t_out=14.4)
        words(f, 'ralentir ?', 990, 130, 12.8, SPARK, t_out=14.4)

    # S4 — la preuve : la course sur la vraie route (14.5–30)
    if 14.4 <= t < 30.2:
        ga = ease(seg(t, 14.5, 14.9)) * (1 - seg(t, 29.6, 30.0))
        MAP.draw(f, ga)
        days = D_SLOW * ease_io(seg(t, 15.4, 26.6))
        pf = min(1.0, days / D_FAST); ps = days / D_SLOW
        MAP.route(f, ROUTE, pf, ga, RED, 4)
        MAP.port(f, *PORTS['Shanghai'], 'Shanghai', ga, MUTED, 10, 32, -26)
        MAP.port(f, *PORTS['Rotterdam'], 'Rotterdam', ga, MUTED, 10, 32, 52)
        for p, col in ((ps, SPARK), (pf, RED)):
            wake(f, p, col, ga); x, y = MAP.point_on(ROUTE, p); ship(f, x, y - 18, 28, col, ga, heading(p))
        f.text('Shanghai → Rotterdam', W/2, 430, 44, MUTED, ga, bold=False)
        f.text(f'jour {int(days)}', W/2, 515, 58, INK, ga, MONO)
        rows = [(RED, '24 nœuds', pf, D_FAST, 1.0), (SPARK, '18 nœuds', ps, D_SLOW, FUEL_SLOW)]
        for i, (col, lab, p, dd, fu) in enumerate(rows):
            y = 1110 + i * 200
            ship(f, 150, y - 16, 26, col, ga)
            f.text(lab, 200, y, 46, INK, ga, DISPLAY, True, 'left')
            arrived = p >= 1.0
            f.text(f'arrivé en {int(round(dd))} j' if arrived else 'en route', 940, y, 40, col if arrived else MUTED, ga, DISPLAY, arrived, 'right')
            f.text('carburant', 150, y + 62, 30, MUTED, ga, DISPLAY, False, 'left')
            f.rect(320, y + 40, 620, 28, OCEAN, ga, 14)
            f.rect(320, y + 40, 620 * fu * p, 28, col, ga, 14)
            if arrived:
                f.text(f'{int(round(fu * 100 * p))}', 940, y + 115, 40, col, ga, MONO, True, 'right')
        f.text('carburant brûlé (rapide = 100)', W/2, 1520, 30, MUTED, ga * seg(t, 22.0, 22.4), bold=False)

    # S5 — la réponse (30–36)
    if 29.9 <= t < 36.4:
        a = ease(seg(t, 30.0, 30.3)) * (1 - seg(t, 35.8, 36.2))
        v = 44 * ease(seg(t, 30.2, 31.4))
        big_center(f, f'−{int(round(v))} %', 860, 200, SPARK, a, bump(t, 31.4, 0.12))
        words(f, 'de carburant.', 990, 72, 31.5, INK, t_out=35.8)
        words(f, 'Pour 6 jours de mer en plus.', 1110, 56, 32.4, MUTED, t_out=35.8, bold=False)
        sa = ease(seg(t, 33.2, 33.6)) * a
        f.text('Ordre de grandeur théorique : 24 → 18 nœuds,', W/2, 1360, 30, MUTED, sa, bold=False)
        f.text('même route d’environ 10 500 milles.', W/2, 1402, 30, MUTED, sa, bold=False)

    # S6 — le retournement : l'eau résiste au cube (35–48)
    if 35.0 <= t < 48.4:
        words(f, 'Le secret ?', 760, 120, 35.1, INK, t_out=37.1)
        words(f, 'L’eau.', 900, 120, 35.7, SPARK, t_out=37.1)
        ga = ease(seg(t, 37.3, 37.8)) * (1 - seg(t, 47.9, 48.3))
        if ga > 0:
            words(f, 'Puissance moteur nécessaire', 450, 52, 37.4, MUTED, t_out=47.9, bold=False)
            speeds = [12, 15, 18, 21, 24]
            bx0, base, bw, hmax = 150, 1200, 140, 560
            for i, s in enumerate(speeds):
                ti = 38.2 + i * 0.8
                gp = ease(seg(t, ti, ti + 0.6)) * ga
                pw = (s / 24) ** 3
                x = bx0 + i * 180
                col = RED if s == 24 else (SPARK if s == 18 else CAPITAL)
                f.rect(x, base - hmax * pw * gp, bw, hmax * pw * gp, col, ga, 8)
                f.text(f'{int(round(pw * 100 * gp))}', x + bw / 2, base - hmax * pw * gp - 16, 34, INK, gp, MONO)
                f.text(f'{s} nd', x + bw / 2, base + 50, 34, MUTED, ga, MONO, False)
            words(f, 'Vitesse × 2 = puissance × 8.', 1380, 56, 42.6, INK, t_out=47.9)
            words(f, 'La résistance explose avec la vitesse.', 1470, 44, 44.2, SPARK, t_out=47.9)

    # S7 — l'escalade : la règle de l'OMI (48–56)
    if 48.0 <= t < 56.4:
        out = 1 - seg(t, 55.9, 56.3)
        words(f, 'Juste 10 % plus lent :', 520, 70, 48.2, INK, t_out=55.9)
        rows = [(49.4, 'puissance moteur', 27), (51.0, 'carburant sur le trajet', 19)]
        for i, (t0, lab, pct) in enumerate(rows):
            a = ease(seg(t, t0, t0 + 0.3)) * out
            y = 720 + i * 260
            v = pct * ease(seg(t, t0 + 0.1, t0 + 1.1))
            f.text(lab, 140, y, 48, MUTED, a, DISPLAY, False, 'left')
            f.text(f'−{int(round(v))} %', 940, y + 100, 90, SPARK, a, MONO, True, 'right')
            f.rect(140, y + 40, 420, 26, OCEAN, a, 13)
            f.rect(140, y + 40, 420 * (1 - v / 100), 26, EARTH, a, 13)
        sa = ease(seg(t, 52.6, 53.0)) * out
        words(f, 'Moins de carburant, moins de CO2.', 1300, 54, 52.8, INK, t_out=55.9)
        f.text('Ordres de grandeur : OMI (GreenVoyage2050) et ICCT.', W/2, 1440, 30, MUTED, sa, bold=False)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        words(f, 'En mer, la vitesse', 740, 76, 56.3, INK)
        words(f, 'se paie au cube.', 850, 76, 57.2, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(240, 1010, 600, 150, OCEAN, a, 28)
        f.rect(300, 1130, 480 * ease_io(seg(t, 60.4, 65.5)), 5, SPARK, a * 0.8, 3)
        c = f.c; c.save(); s = 1 + 0.03 * math.sin((t - 60.0) * 3) if t > 60.4 else bump(t, 60.0, 0.12); c.translate(W/2, 1085); c.scale(s, s)
        f.text('Abonne-toi.', 0, 21, 62, INK, a); c.restore()
        # un petit navire lent traverse en bas
        ship(f, lerp(-80, W + 80, seg(t, 56.0, 66.0)), 1420, 34, SPARK, 0.6 * ease(seg(t, 56.5, 57.5)))

def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    for t0, n in ((0.15, 2), (0.5, 2), (1.6, 4)):
        for i in range(n): ev.append((t0 + i * 0.11, pop(420 + 40 * i, 0.09)))
    ev += [(x, whoosh(0.5, 0.18)) for x in (3.9, 12.1, 14.4, 29.7, 34.9, 47.9, 55.9)]
    ev += [(4.4, rise(1.2, 300, 900, 0.08)), (5.6, ding(660, amp=0.2)), (7.9, rise(1.4, 900, 400, 0.08)),
           (9.4, ding(784, amp=0.2)), (9.8, pop(330)), (10.8, pop(440)), (12.4, pop(330)), (12.8, pop(440))]
    x = 15.4
    while x < 26.6: ev.append((x, tick())); x += 0.25
    tf = 22.95   # arrivée du rapide (ease_io = 0,75)
    ev += [(tf, ding(880, amp=0.22)), (26.6, ding(1175, amp=0.28)), (30.2, rise(1.2, 300, 1046, 0.1)),
           (31.4, ding(1046, amp=0.3)), (32.4, pop(392)), (35.1, pop(300, 0.15)), (35.7, pop(450, 0.15))]
    for i in range(5): ev.append((38.2 + i * 0.8, clink(900 + i * 250)))
    ev += [(42.6, ding(880, amp=0.25)), (44.2, pop(440))]
    for t0 in (49.4, 51.0): ev += [(t0, pop(500)), (t0 + 1.1, clink(1900))]
    ev += [(52.8, pop(392)), (56.3, pop(440)), (57.2, pop(550)), (60.0, ding(784, amp=0.22))]
    return ev
