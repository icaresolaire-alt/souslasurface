"""L'Ever Given bloque le canal de Suez (mars 2021). Même structure que ep002, vraie carte du monde."""
import math
import numpy as np
from lib import *
from kinetic import words, bump, big_center
from worldmap import WorldMap, PORTS, ROUTE_SHANGHAI_ROTTERDAM as ROUTE

TOTAL = 66.0
COVER = dict(tag='Mer', l1='Un seul navire', l2='a bloqué le monde', big='6 jours')

# cadrages : monde (Asie -> Europe, Afrique entière) et zoom sur le canal
WORLD = dict(lon=(-25, 125), lat=(-40, 60), x=60, y=600, w=960)        # y 600 -> 1240
ZOOM = dict(lon=(30.6, 34.4), lat=(28.9, 31.9), x=60, y=600, w=960)     # y 600 -> 1358
MW = WorldMap(**WORLD); MZ = WorldMap(**ZOOM)

def map_between(p):
    """Carte interpolée (zoom continu) entre le monde (p=0) et le canal (p=1)."""
    if p <= 0: return MW
    if p >= 1: return MZ
    q = ease_io(p)
    def L(a, b): return a + (b - a) * q
    span0, span1 = WORLD['lon'][1] - WORLD['lon'][0], ZOOM['lon'][1] - ZOOM['lon'][0]
    span = span0 * (span1 / span0) ** q
    u = (span0 - span) / (span0 - span1)          # centre suit le zoom (pas de dérive)
    cl = lerp(sum(WORLD['lon']) / 2, sum(ZOOM['lon']) / 2, u)
    cy = lerp(sum(WORLD['lat']) / 2, sum(ZOOM['lat']) / 2, u)
    hl = span * 640 / 960 / 2 * (1 + 0.1875 * q)   # garde le ratio (monde 640 px, zoom 758 px)
    return WorldMap(lon=(cl - span / 2, cl + span / 2), lat=(cy - hl, cy + hl), x=60, y=600, w=960)

# canal de Suez (lon, lat) : Port-Saïd -> Ismaïlia -> Grand Lac Amer -> Suez
CANAL = [(32.31, 31.27), (32.32, 30.9), (32.30, 30.62), (32.35, 30.45), (32.45, 30.3), (32.55, 30.12), (32.57, 30.0), (32.56, 29.93)]
STUCK = (32.58, 30.02)                    # lieu de l'échouement, près de l'entrée sud

# route du détour : Shanghai -> Malacca -> sud de Madagascar -> Cap -> côte ouest-africaine -> Rotterdam
ROUTE_CAPE = ROUTE[:10] + [
    (80.0, 2.0), (65.0, -12.0), (52.0, -30.0), (40.0, -36.5), (25.0, -37.5), (18.5, -35.6), (12.0, -30.0),
    (8.0, -15.0), (3.0, -1.0), (-12.0, 4.0), (-20.0, 15.0), (-19.0, 26.0), (-14.0, 33.0), (-11.0, 40.0),
    (-10.0, 43.0), (-6.0, 48.3), (-2.0, 49.9), (2.0, 51.0), (4.0, 52.0)]

# files d'attente : 422 navires (chiffre de l'Autorité du canal le 29 mars)
rng = np.random.default_rng(7)
QUEUE = []
for i in range(422):
    if i % 2 == 0:   # au nord, en Méditerranée devant Port-Saïd
        QUEUE.append((rng.uniform(31.75, 33.25) , rng.uniform(31.38, 31.85)))
    else:            # au sud, dans le golfe de Suez (axe du golfe)
        u = rng.uniform(0, 1) ** 0.8
        QUEUE.append((32.58 + 0.55 * u + rng.normal(0, 0.035), 29.86 - 0.85 * u + rng.normal(0, 0.035)))
order = rng.permutation(422)
T_Q0, T_Q1 = 16.0, 26.2                    # les navires s'accumulent
T_FREE = 27.0                              # 29 mars : remis à flot

def ship(f, x, y, L, ang, col, a=1.0, w=None):
    if a <= 0: return
    w = w or L * 0.16
    c = f.c; c.save(); c.translate(x, y); c.rotate(ang); f.color(col, a)
    c.move_to(-L/2, -w/2); c.line_to(L/2 - w*0.8, -w/2); c.line_to(L/2, 0); c.line_to(L/2 - w*0.8, w/2); c.line_to(-L/2, w/2)
    c.close_path(); c.fill(); c.restore()

def canal(f, M, a, col='#3f86a8', width=7):
    f.line([M.xy(*p) for p in CANAL], col, a, width)

def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')

    # question persistante
    ha = ease(seg(t, 12.4, 12.9)) * (1 - seg(t, 29.6, 30.0))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Combien ça coûte ?', W/2, 296, 46, SPARK, ha)

    # S1 — accroche (0–4) : zoom sur le canal, le navire pivote et se met en travers
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        MZ.draw(f, fo); canal(f, MZ, fo)
        x, y = MZ.xy(*STUCK)
        p = ease_io(seg(t, 0.0, 2.2))
        sx, sy = MZ.xy(32.47, 30.55)
        ang = lerp(math.radians(60), math.radians(-15), ease_io(seg(t, 1.6, 2.6)))
        ship(f, lerp(sx, x, p), lerp(sy, y, p), 110, ang, RED, fo)
        if t > 2.6:
            k = seg(t, 2.6, 3.4)
            f.c.new_path(); f.circle(x, y, 40 + 90 * k, RED, (1 - k) * fo, 5)
        words(f, 'Un navire de 400 m', 420, 80, 0.15, INK, t_out=o)
        words(f, 'a coupé la route', 1460, 66, 1.3, INK, t_out=o)
        words(f, 'de 12 % du commerce mondial.', 1540, 56, 1.9, SPARK, t_out=o)

    # S2 — le canal dans le monde (4–12)
    if 4.0 <= t < 12.6:
        ga = ease(seg(t, 4.0, 4.3)) * (1 - seg(t, 12.0, 12.4))
        M = map_between(1 - seg(t, 4.1, 5.5))
        M.draw(f, ga)
        p = ease_io(seg(t, 5.4, 9.0))
        if t >= 5.5:
            MW.route(f, ROUTE, p, ga, SPARK, 6)
            for name in ('Shanghai', 'Rotterdam'):
                MW.port(f, *PORTS[name], name, ga, SPARK, 10, 32, -24)
            x, y = MW.xy(*PORTS['Suez'])
            pul = 0.5 + 0.5 * math.sin(t * 6)
            sa = ease(seg(t, 7.0, 7.3)) * ga
            f.c.new_path(); f.circle(x, y, 14 + 8 * pul, RED, sa, 4)
            f.text('Suez', x + 30, y + 46, 34, INK, sa, DISPLAY, True, 'left')
        v = 12 * ease(seg(t, 5.6, 8.4))
        ta = ease(seg(t, 5.6, 5.9)) * (1 - seg(t, 9.2, 9.5)) * ga
        big_center(f, f'{int(round(v))} %', 480, 130, SPARK, ta, bump(t, 8.4, 0.15))
        words(f, 'du commerce mondial', 1340, 60, 6.0, INK, t_out=9.2)
        words(f, 'passe par ce canal.', 1420, 60, 6.5, INK, t_out=9.2)
        words(f, '23 mars 2021.', 470, 80, 9.5, INK, t_out=12.0)
        words(f, 'L’Ever Given se met en travers.', 1340, 56, 10.0, RED, t_out=12.0)
        words(f, '400 m de long, plus que la tour Eiffel.', 1420, 44, 10.6, MUTED, t_out=12.0, bold=False)

    # S3 — la question (12–14.5)
    if 12.2 <= t < 14.9:
        words(f, 'Combien coûte', 840, 116, 12.4, INK, t_out=14.4)
        words(f, 'un canal bouché ?', 980, 106, 12.8, SPARK, t_out=14.4)

    # S4 — la preuve : 6 jours, les navires s'entassent (14.5–30)
    if 14.4 <= t < 30.2:
        ga = ease(seg(t, 14.5, 14.9)) * (1 - seg(t, 29.6, 30.0))
        MZ.draw(f, ga); canal(f, MZ, ga)
        # libellés de lieux
        f.text('Port-Saïd', MZ.xy(32.31, 31.27)[0] - 20, MZ.xy(32.31, 31.27)[1] + 8, 30, INK, ga, DISPLAY, True, 'right')
        f.text('Suez', MZ.xy(32.56, 29.93)[0] - 26, MZ.xy(32.56, 29.93)[1] + 10, 30, INK, ga, DISPLAY, True, 'right')
        f.text('mer Rouge', *MZ.xy(33.55, 29.05), 30, MUTED, ga * 0.9, DISPLAY, False)
        # navires en attente
        nq = int(422 * ease_io(seg(t, T_Q0, T_Q1)))
        fade_q = 1 - 0.6 * seg(t, T_FREE + 0.5, 29.5)
        for j in range(nq):
            lon, lat = QUEUE[order[j]]
            x, y = MZ.xy(lon, lat)
            tj = T_Q0 + (T_Q1 - T_Q0) * j / 422
            f.c.new_path(); f.circle(x, y, 5, INK, ease(seg(t, tj, tj + 0.3)) * ga * 0.85 * fade_q)
        # l'Ever Given : en travers, puis remis dans l'axe
        x, y = MZ.xy(*STUCK)
        fr = ease_io(seg(t, T_FREE, T_FREE + 1.0))
        ang = lerp(math.radians(-15), math.radians(-73), fr)
        ship(f, x + 0 * fr, y - 60 * fr, 110, ang, EARTH if fr > 0.5 else RED, ga)
        # compteurs
        day = 23 + min(6, int(max(0, t - 15.4) / 1.8))
        da = ease(seg(t, 15.0, 15.4)) * ga
        f.text(f'{day} mars 2021', W/2, 440, 50, MUTED, da, MONO)
        big_center(f, fmt_int(nq), 560, 110, SPARK, da, bump(t, T_Q1, 0.18))
        f.text('navires en attente', W/2, 1440, 46, INK, da, DISPLAY, False)
        fa = ease(seg(t, T_FREE, T_FREE + 0.3)) * ga
        f.text('6 jours plus tard : libéré.', W/2, 1520, 46, EARTH, fa)

    # S5 — la réponse (30–36)
    if 29.9 <= t < 36.4:
        a = ease(seg(t, 30.0, 30.3)) * (1 - seg(t, 35.8, 36.2))
        v = 9.6 * ease(seg(t, 30.0, 31.2))
        big_center(f, f'{v:.1f}'.replace('.', ','), 820, 260, SPARK, a, bump(t, 31.2, 0.12))
        words(f, 'milliards de dollars', 960, 70, 30.6, INK, t_out=35.8)
        words(f, 'de marchandises bloquées', 1060, 58, 31.4, INK, t_out=35.8, bold=False)
        words(f, 'chaque jour.', 1140, 58, 31.9, SPARK, t_out=35.8)
        ra = ease(seg(t, 32.6, 33.0)) * a
        f.text('Soit environ 400 millions de dollars par heure.', W/2, 1300, 38, MUTED, ra, bold=False)
        f.text('Estimation Lloyd’s List, mars 2021.', W/2, 1380, 30, MUTED, ra, bold=False)

    # S6 — le retournement : le détour par l'Afrique (36–48)
    if 36.0 <= t < 48.4:
        words(f, 'Le plan B ?', 760, 120, 36.1, INK, t_out=38.1)
        words(f, 'Faire le tour de l’Afrique.', 900, 76, 36.7, SPARK, t_out=38.1)
        ga = ease(seg(t, 38.3, 38.8)) * (1 - seg(t, 47.9, 48.3))
        if ga > 0:
            MW.draw(f, ga)
            MW.route(f, ROUTE, 1.0, ga * 0.6, MUTED, 4, ghost=False)
            x, y = MW.xy(*PORTS['Suez'])
            f.line([(x - 16, y - 16), (x + 16, y + 16)], RED, ga, 6); f.line([(x - 16, y + 16), (x + 16, y - 16)], RED, ga, 6)
            p = ease_io(seg(t, 38.9, 44.5))
            MW.route(f, ROUTE_CAPE, p, ga, SPARK, 6, ghost=False)
            sx, sy = MW.point_on(ROUTE_CAPE, p)
            f.c.new_path(); f.circle(sx, sy, 11, INK, ga)
            for name in ('Shanghai', 'Rotterdam'):
                MW.port(f, *PORTS[name], name, ga, SPARK, 10, 32, -24)
            ca = ease(seg(t, 41.0, 41.4)) * ga
            cx, cy = MW.xy(*PORTS['Cap de Bonne-Espérance'])
            f.c.new_path(); f.circle(cx, cy, 9, SPARK, ca)
            f.text('Cap de Bonne-Espérance', cx + 24, cy + 46, 30, INK, ca, DISPLAY, True, 'left')
            km = 6000 * ease_io(seg(t, 38.9, 44.5))
            f.text('détour Asie → Europe', W/2, 440, 42, MUTED, ga, bold=False)
            big_center(f, '≈ + ' + fmt_int(km) + ' km', 560, 104, SPARK, ga, bump(t, 44.5, 0.18))
            words(f, 'Jusqu’à 2 semaines de mer en plus.', 1400, 52, 44.9, INK, t_out=47.9)
            words(f, 'Et des tonnes de carburant.', 1480, 52, 45.7, MUTED, t_out=47.9, bold=False)

    # S7 — l'escalade : en 2024, le détour devient la règle (48–56)
    if 48.0 <= t < 56.4:
        out = 1 - seg(t, 55.9, 56.3)
        words(f, 'Début 2024,', 470, 76, 48.1, INK, t_out=55.9)
        words(f, 'attaques en mer Rouge.', 570, 64, 48.6, RED, t_out=55.9)
        f.text('Commerce par Suez (janv.-févr.)', 140, 760, 46, MUTED, ease(seg(t, 49.2, 49.5)) * out, DISPLAY, False, 'left')
        rows = [(49.6, '2023', 1.0, CAPITAL), (50.4, '2024', 0.5, SPARK)]
        for i, (t0, lab, v, col) in enumerate(rows):
            a = ease(seg(t, t0, t0 + 0.3)) * out
            y = 860 + i * 150
            g = 1.0 if i == 0 else lerp(1.0, 0.5, ease_io(seg(t, 51.0, 52.6)))
            f.text(lab, 140, y, 48, INK, a, MONO, True, 'left')
            f.rect(300, y - 40, 640 * g * ease(seg(t, t0, t0 + 0.6)), 50, col, a, 12)
        pa = ease(seg(t, 52.6, 52.9)) * out
        big_center(f, '− 50 %', 1260, 120, SPARK, pa, bump(t, 52.6, 0.18))
        words(f, 'Les navires contournent l’Afrique :', 1400, 46, 53.4, INK, t_out=55.9, bold=False)
        words(f, '+ 10 jours de livraison en moyenne.', 1480, 50, 54.0, INK, t_out=55.9)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        words(f, 'Le commerce mondial', 720, 80, 56.3)
        words(f, 'ne tient qu’à un canal.', 830, 76, 57.3, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        s = bump(t, 60.0, 0.12) * (1 + 0.025 * math.sin(max(0, t - 60.4) * 3.2))
        c = f.c; c.save(); c.translate(W/2, 1105); c.scale(s, s); c.translate(-W/2, -1105)
        f.rect(240, 1030, 600, 150, OCEAN, a, 28)
        f.text('Abonne-toi.', W/2, 1126, 62, INK, a)
        c.restore()

def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    for t0, n in ((0.15, 5), (1.3, 4), (1.9, 6)):
        for i in range(n): ev.append((t0 + i * 0.11, pop(420 + 40 * i, 0.09)))
    ev += [(2.6, ding(330, amp=0.25))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (3.9, 12.1, 14.4, 29.7, 35.9, 47.9, 55.9)]
    ev += [(4.1, whoosh(1.2, 0.14)), (8.4, ding(880, amp=0.22)), (7.0, clink(1700)), (9.5, pop(392)), (10.0, pop(300)), (10.6, pop(440))]
    ev += [(12.4, pop(330)), (12.8, pop(440))]
    for d in range(7): ev.append((15.4 + d * 1.8, clink(1300 + d * 90)))
    x = T_Q0
    while x < T_Q1: ev.append((x, tick())); x += 0.1
    ev += [(T_Q1, ding(880, amp=0.25)), (T_FREE, rise(1.0, 300, 900, 0.1)), (T_FREE + 1.0, ding(1175, amp=0.28))]
    ev += [(30.0, rise(1.2, 300, 1046, 0.1)), (31.2, ding(1046, amp=0.3)), (36.1, pop(300, 0.15)), (36.7, pop(450, 0.15))]
    x = 38.9
    while x < 44.5: ev.append((x, clink(900 + (x - 38.9) * 120))); x += 0.4
    ev += [(44.5, ding(880, amp=0.25)), (44.9, pop(392)), (45.7, pop(330))]
    ev += [(48.1, pop(440)), (48.6, pop(330)), (49.6, pop(500)), (50.4, pop(560)), (52.6, ding(660, amp=0.25)), (53.4, pop(440)), (54.0, pop(550))]
    ev += [(56.3, pop(440)), (57.3, pop(550)), (60.0, ding(784, amp=0.22))]
    return ev
