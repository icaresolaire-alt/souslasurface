"""Les détroits qui tiennent le monde. Même structure que le pilote, vraie carte du monde."""
import math
from lib import *
from kinetic import words, bump, big_center
from worldmap import WorldMap, PORTS, ROUTE_SHANGHAI_ROTTERDAM as ROUTE

TOTAL = 66.0
COVER = dict(tag='Mer', l1='Les détroits qui', l2='tiennent le monde', big='1 / 5')
WORLD = WorldMap(lon=(-115, 135), lat=(-42, 52), x=40, y=600, w=1000)      # monde, Panama compris
ZOOM = WorldMap(lon=(25, 110), lat=(-8, 39), x=60, y=560, w=960)          # Afrique - Asie

PTS = {'Ormuz': PORTS['Ormuz'], 'Malacca': (101.2, 2.6), 'Bab-el-Mandeb': PORTS['Bab-el-Mandeb'],
       'Suez': PORTS['Suez'], 'Panama': PORTS['Panama']}
# ordre d'allumage dans la preuve : (nom, t0, ligne chiffre, ligne détail, libellé dx, dy, alignement)
STEPS = [
    ('Suez', 14.8, '12 à 15 %', 'du commerce mondial (2023)', 0, -26, 'center'),
    ('Bab-el-Mandeb', 18.0, '29 km', 'de large au plus étroit', 0, 46, 'center'),
    ('Malacca', 21.2, '23 millions', 'de barils de pétrole par jour', 0, 46, 'center'),
    ('Ormuz', 24.4, '< 40 km', 'au plus étroit, 2 couloirs d’environ 3 km', 0, -26, 'center'),
]

def clip_rect(f, M):
    f.c.save(); f.c.rectangle(M.x, M.y, M.w, M.h); f.c.clip()

def glow(f, M, name, t, t0, a, label=True, size=30, dy=-26, col=SPARK):
    if a <= 0: return
    x, y = M.xy(*PTS[name])
    p = ease(seg(t, t0, t0 + 0.3))
    if t >= t0:
        ph = ((t - t0) % 1.4) / 1.4
        f.circle(x, y, 14 + 40 * ph, col, a * p * (1 - ph) * 0.8, 3)
    f.circle(x, y, 7 + 5 * p, col if t >= t0 else MUTED, a * (0.5 + 0.5 * p))
    if label and t >= t0:
        f.text(name, x, y + dy, size, INK, a * p)

def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')

    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.6, 30.0))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Lequel est le plus critique ?', W/2, 296, 44, SPARK, ha)

    # S1 — accroche (0–4) : carte du monde, les 5 goulets s'allument
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        WORLD.draw(f, fo)
        for i, n in enumerate(['Panama', 'Suez', 'Bab-el-Mandeb', 'Ormuz', 'Malacca']):
            glow(f, WORLD, n, t, 0.2 + i * 0.45, fo, label=False)
        words(f, 'Quelques kilomètres de mer', 400, 66, 0.15, INK, t_out=o)
        words(f, 'tiennent l’économie', 1150, 80, 1.6, INK, t_out=o)
        words(f, 'du monde entier.', 1250, 80, 2.2, SPARK, t_out=o)

    # S2 — enjeu (4–12.4) : l'océan est immense, mais tout passe par les mêmes portes
    if 4.0 <= t < 12.6:
        ga = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, 12.0, 12.4))
        ZOOM.draw(f, ga)
        p = ease_io(seg(t, 4.4, 10.6))
        clip_rect(f, ZOOM); ZOOM.route(f, ROUTE, p, ga, SPARK, 6); f.c.restore()
        x, y = ZOOM.point_on(ROUTE, p)
        if ZOOM.x < x < ZOOM.x + ZOOM.w: f.circle(x, y, 13, INK, ga)
        for n, tt in (('Malacca', 5.7), ('Bab-el-Mandeb', 8.4), ('Suez', 9.6)):
            glow(f, ZOOM, n, t, tt, ga, label=False)
        words(f, 'L’océan est immense.', 440, 70, 4.3, INK, t_out=6.9)
        words(f, 'Mais les navires passent', 400, 60, 7.1, INK, t_out=12.0)
        words(f, 'tous par les mêmes portes.', 480, 60, 7.6, SPARK, t_out=12.0)
        words(f, 'Shanghai → Europe', 1180, 50, 4.8, MUTED, t_out=12.0, bold=False)

    # S3 — la question (12.2–14.8)
    if 12.2 <= t < 14.9:
        words(f, 'Lequel', 840, 120, 12.4, INK, t_out=14.4)
        words(f, 'est le plus critique ?', 980, 90, 12.8, SPARK, t_out=14.4)

    # S4 — la preuve : les détroits s'allument un par un (14.6–29.8)
    if 14.5 <= t < 30.0:
        ga = ease(seg(t, 14.6, 15.0)) * (1 - seg(t, 29.4, 29.8))
        ZOOM.draw(f, ga)
        clip_rect(f, ZOOM); ZOOM.route(f, ROUTE, 1.0, ga * 0.35, SPARK, 3, ghost=False); f.c.restore()
        cur = None
        for i, (n, t0, big, small, dx, dy, al) in enumerate(STEPS):
            if t >= t0: cur = i
            glow(f, ZOOM, n, t, t0, ga, True, 32, dy, RED if n == 'Ormuz' else SPARK)
        if cur is not None:
            n, t0, big, small, *_ = STEPS[cur]
            t1 = STEPS[cur + 1][1] if cur + 1 < len(STEPS) else 29.4
            ca = ease(seg(t, t0, t0 + 0.3)) * (1 - seg(t, t1 - 0.25, t1)) * ga if cur + 1 < len(STEPS) else ease(seg(t, t0, t0 + 0.3)) * ga
            f.rect(110, 1120, 860, 330, OCEAN, ca * 0.95, 30)
            f.text(n.upper(), W/2, 1190, 40, MUTED, ca, MONO, True)
            big_center(f, big, 1310, 100, RED if n == 'Ormuz' else SPARK, ca, bump(t, t0 + 0.1, 0.15), MONO)
            f.text(small, W/2, 1395, 42, INK, ca, bold=False)
        # compteur des goulets
        k = 0 if cur is None else cur + 1
        f.text(f'{k} / 4', W/2, 470, 54, MUTED, ga, MONO)
        if t >= 27.0:
            za = ease(seg(t, 27.0, 27.4)) * ga
            f.text('Le trou de serrure du pétrole.', W/2, 1520, 44, RED, za)

    # S5 — la réponse (29.9–35.4)
    if 29.9 <= t < 35.4:
        a = ease(seg(t, 30.0, 30.3)) * (1 - seg(t, 34.8, 35.2))
        words(f, 'Ormuz.', 640, 110, 30.0, RED, t_out=34.8)
        big_center(f, '1 baril sur 5', 880, 150, SPARK, a, bump(t, 30.5, 0.12), DISPLAY)
        words(f, 'du pétrole consommé dans le monde', 1010, 52, 31.0, INK, t_out=34.8)
        words(f, 'passe par ce détroit.', 1080, 52, 31.4, INK, t_out=34.8)
        # 5 barils, un rouge
        for i in range(5):
            ba = ease(seg(t, 31.9 + i * 0.15, 32.2 + i * 0.15)) * a
            x = W/2 + (i - 2) * 130
            f.rect(x - 40, 1180, 80, 120, RED if i == 2 else CAPITAL, ba, 14)
            f.rect(x - 40, 1215, 80, 8, DEEP, ba * 0.5); f.rect(x - 40, 1260, 80, 8, DEEP, ba * 0.5)
        f.text('Source : EIA, données 2024.', W/2, 1400, 32, MUTED, ease(seg(t, 32.8, 33.2)) * a, bold=False)

    # S6 — le retournement : pas de plan B (35–48.4)
    if 35.0 <= t < 48.4:
        words(f, 'Le secret ?', 760, 120, 35.1, INK, t_out=37.1)
        words(f, 'Pas de plan B.', 900, 120, 35.7, SPARK, t_out=37.1)
        ga = ease(seg(t, 37.3, 37.8)) * (1 - seg(t, 47.9, 48.3))
        if ga > 0:
            f.text('Pétrole par Ormuz, par jour', W/2, 470, 44, MUTED, ga, bold=False)
            p1 = ease_io(seg(t, 37.8, 40.2))
            big_center(f, f'{int(round(20 * p1))} millions de barils', 580, 64, RED, ga, bump(t, 40.2, 0.15))
            bx, bw = 140, 800
            f.rect(bx, 640, bw, 70, OCEAN, ga, 18)
            f.rect(bx, 640, max(1, bw * p1), 70, RED, ga, 18)
            # contournement
            pa = ease(seg(t, 41.0, 41.4)) * ga
            f.text('Oléoducs capables de le contourner', W/2, 860, 44, MUTED, pa, bold=False)
            p2 = ease_io(seg(t, 41.4, 43.0))
            big_center(f, f'{2.6 * p2:.1f}'.replace('.', ',') + ' millions', 970, 64, EARTH, pa, bump(t, 43.0, 0.15))
            f.rect(bx, 1030, bw, 70, OCEAN, pa, 18)
            f.rect(bx, 1030, max(1, bw * 2.6 / 20 * p2), 70, EARTH, pa, 18)
            # le reste : bloqué
            ra = ease(seg(t, 43.8, 44.2)) * ga
            pul = 0.5 + 0.5 * math.sin((t - 43.8) * 6)
            f.rect(bx + bw * 2.6 / 20, 1030, bw * (1 - 2.6 / 20), 70, RED, ra * (0.25 + 0.2 * pul), 18)
            f.text('aucun autre chemin', bx + bw * 0.56, 1078, 36, INK, ra)
            words(f, 'Si le détroit se ferme,', 1300, 56, 44.6, INK, t_out=47.9)
            words(f, 'le reste reste à quai.', 1380, 56, 45.4, SPARK, t_out=47.9)

    # S7 — escalade : le monde entier (48–56.4)
    if 48.0 <= t < 56.4:
        out = ease(seg(t, 48.1, 48.5)) * (1 - seg(t, 55.9, 56.3))
        WORLD.draw(f, out)
        for i, n in enumerate(['Suez', 'Bab-el-Mandeb', 'Malacca', 'Ormuz']):
            glow(f, WORLD, n, t, 48.3 + i * 0.12, out, False, col=RED if n == 'Ormuz' else SPARK)
        glow(f, WORLD, 'Panama', t, 49.2, out, True, 32, 46)
        words(f, 'Et Panama :', 420, 64, 48.6, INK, t_out=55.9)
        words(f, '5 % du commerce maritime mondial.', 500, 52, 49.2, SPARK, t_out=55.9)
        f.text('selon l’Autorité du canal de Panama', W/2, 560, 32, MUTED, out * ease(seg(t, 49.8, 50.2)), bold=False)
        words(f, 'Un seul détroit bloqué,', 1120, 56, 51.4, INK, t_out=55.9)
        words(f, 'et c’est ton plein d’essence qui grimpe.', 1210, 48, 52.4, SPARK, t_out=55.9)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        words(f, 'L’océan est immense.', 760, 70, 56.3, INK)
        words(f, 'Le monde passe par un trou de serrure.', 860, 52, 57.6, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(240, 1040, 600, 150, OCEAN, a, 28)
        pa = 0.5 + 0.5 * math.sin((t - 60) * 3)
        f.rect(240, 1040, 600, 150, SPARK, a * 0.25 * pa, 28)
        f.text('Abonne-toi.', W/2, 1135, 62, INK, a)

def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    for t0, n in ((0.15, 4), (1.6, 2), (2.2, 3)):
        for i in range(n): ev.append((t0 + i * 0.11, pop(420 + 40 * i, 0.09)))
    for i in range(5): ev.append((0.2 + i * 0.45, clink(1500 + i * 120)))
    ev += [(x, whoosh(0.5, 0.18)) for x in (3.9, 12.1, 14.4, 29.6, 34.9, 47.9, 55.9)]
    ev += [(4.3, pop(392)), (7.1, pop(440)), (7.6, pop(523)), (5.7, clink(1700)), (8.4, clink(1700)), (9.6, clink(1700))]
    ev += [(12.4, pop(330)), (12.8, pop(440))]
    for i, s in enumerate(STEPS):
        ev += [(s[1], ding(660 + i * 110, amp=0.22)), (s[1] + 0.1, pop(500 + i * 40))]
    ev += [(27.0, pop(300, 0.15)), (30.0, ding(1046, amp=0.3))]
    for i in range(5): ev.append((31.9 + i * 0.15, pop(450 + i * 30)))
    ev += [(35.1, pop(300, 0.15)), (35.7, pop(450, 0.15)), (37.8, rise(2.4, 250, 880, 0.08)), (40.2, ding(880, amp=0.25)),
           (41.4, rise(1.6, 250, 600, 0.07)), (43.0, clink(1200)), (43.8, ding(523, amp=0.22))]
    for i in range(4): ev.append((48.3 + i * 0.12, clink(1600 + i * 100)))
    ev += [(49.2, ding(784, amp=0.22)), (51.4, pop(392)), (52.6, rise(1.2, 300, 1046, 0.1)), (53.8, ding(1046, amp=0.28))]
    ev += [(56.3, pop(440)), (57.6, pop(550)), (60.0, ding(784, amp=0.22))]
    return ev
