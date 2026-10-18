"""Le conteneur : la boîte qui a changé le monde. Même structure que le pilote (ep002)."""
import math
from lib import *
from kinetic import words, bump, big_center
from worldmap import WorldMap

TOTAL = 66.0

# carte côte Est / golfe du Mexique : Newark -> Houston (Ideal X, 26 avril 1956)
MAP = WorldMap(lon=(-99, -67), lat=(22.5, 43.5), x=60, y=560, w=960)
NEWARK, HOUSTON = (-74.15, 40.69), (-95.0, 29.73)
ROUTE = [(-74.1, 40.55), (-73.6, 40.2), (-73.8, 39.2), (-74.6, 37.5), (-75.2, 35.4), (-77.0, 33.6),
         (-79.6, 31.5), (-80.0, 29.0), (-79.8, 26.5), (-79.9, 25.2), (-80.6, 24.4), (-81.8, 24.2),
         (-83.2, 24.4), (-84.8, 26.0), (-87.5, 28.4), (-90.0, 28.6), (-92.5, 29.1), (-94.6, 29.3), (-95.0, 29.7)]

def container(f, x, y, w, h, col, a=1.0, ribs=True):
    f.rect(x, y, w, h, col, a, 4)
    if ribs:
        n = max(3, int(w / 22))
        for i in range(1, n):
            f.line([(x + i*w/n, y + 6), (x + i*w/n, y + h - 6)], DEEP, a * 0.35, 3)

def hull(f, x0, x1, y, depth, a, col=CAPITAL):
    c = f.c; f.color(col, a)
    c.move_to(x0, y); c.line_to(x1, y); c.line_to(x1 - 50, y + depth); c.line_to(x0 + 50, y + depth); c.close_path(); c.fill()

def sack(f, x, y, s, col, a):
    f.rect(x - s/2, y - s*0.6, s, s*1.2, col, a, s*0.35)

def docker(f, x, y, s, col, a, phase=0.0):
    """Silhouette simple d'un docker qui marche."""
    f.circle(x, y - s*1.55, s*0.28, col, a)
    f.line([(x, y - s*1.25), (x, y - s*0.45)], col, a, s*0.22)
    sw = math.sin(phase) * s * 0.35
    f.line([(x, y - s*0.45), (x + sw, y + s*0.25)], col, a, s*0.2)
    f.line([(x, y - s*0.45), (x - sw, y + s*0.25)], col, a, s*0.2)

def ship_icon(f, x, y, s, a):
    c = f.c; f.color(INK, a)
    c.move_to(x - s, y - s*0.25); c.line_to(x + s, y - s*0.25); c.line_to(x + s*0.7, y + s*0.3); c.line_to(x - s*0.75, y + s*0.3); c.close_path(); c.fill()
    for i in range(4): f.rect(x - s*0.75 + i * s*0.36, y - s*0.6, s*0.32, s*0.33, SPARK, a, 2)

def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.6, 30.0))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Charger une tonne ?', W/2, 296, 46, SPARK, ha)

    # S1 — accroche (0–4) : une grue dépose une boîte dorée sur un navire
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        hull(f, 120, 960, 1360, 140, fo)
        for i in range(6):
            container(f, 170 + i * 120, 1360 - 70, 112, 66, CAPITAL if i % 2 else MUTED, fo * 0.8)
        drop = ease_io(seg(t, 0.0, 2.4))
        cy = lerp(880, 1360 - 140, drop)
        f.line([(W/2, 830), (W/2, cy)], INK, fo * 0.7, 4)
        container(f, W/2 - 150, cy, 300, 70, SPARK, fo)
        words(f, 'Une simple boîte', 420, 86, 0.15, INK, t_out=o)
        words(f, 'a rendu le chargement', 530, 72, 0.7, INK, t_out=o)
        words(f, '36 fois moins cher.', 660, 96, 1.6, SPARK, t_out=o)

    # S2 — enjeu : avant, tout à la main (4–12.6)
    if 4.0 <= t < 12.6:
        ga = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, 12.0, 12.4))
        words(f, 'Avant 1956,', 480, 96, 4.2, INK, t_out=12.0)
        words(f, 'on chargeait les navires', 600, 66, 4.8, INK, t_out=12.0)
        words(f, 'à la main.', 690, 80, 5.5, SPARK, t_out=12.0)
        # quai, coque, file de dockers portant des sacs, caisses et barils
        hull(f, 560, 1010, 1080, 170, ga)
        f.rect(60, 1080, 470, 24, LINE, ga, 4)            # quai
        for k in range(7):
            ph = ((t - 4.2) * 0.32 + k / 7) % 1.0          # progression de chaque docker vers le navire
            x = lerp(90, 600, ph); yb = 1070 - 90 * math.sin(math.pi * clamp((x - 450) / 200)) if x > 450 else 1070
            dk = ga * (1 - seg(ph, 0.9, 1.0)) * seg(ph, 0.0, 0.06)
            docker(f, x, yb, 40, MUTED, dk, (t + k) * 9)
            sack(f, x, yb - 84, 30, [SPARK, EARTH, RED][k % 3], dk)
        # pile qui monte dans la cale
        n = int(36 * seg(t, 4.6, 11.8))
        for i in range(n):
            r, cidx = divmod(i, 12)
            sack(f, 640 + cidx * 28, 1060 - r * 36, 22, [SPARK, EARTH, RED, CAPITAL][(i * 7) % 4], ga)
        words(f, 'Sacs, caisses, barils : un par un.', 1330, 50, 7.0, INK, t_out=12.0, bold=False)
        words(f, 'Le chargement pouvait durer', 1420, 50, 8.8, MUTED, t_out=12.0, bold=False)
        words(f, 'autant que la traversée.', 1488, 50, 9.3, SPARK, t_out=12.0)

    # S3 — la question (12.2–14.9)
    if 12.2 <= t < 14.9:
        words(f, 'Combien coûtait', 820, 104, 12.4, INK, t_out=14.4)
        words(f, 'une tonne chargée ?', 960, 96, 12.9, SPARK, t_out=14.4)

    # S4 — la preuve : l'Ideal X (14.5–21.8) puis les coûts (21.6–30)
    if 14.4 <= t < 22.2:
        ga = ease(seg(t, 14.5, 14.9)) * (1 - seg(t, 21.6, 22.0))
        p = ease_io(seg(t, 15.4, 20.4))
        MAP.draw(f, ga)
        MAP.route(f, ROUTE, p, ga, SPARK, 6)
        MAP.port(f, *NEWARK, 'Newark', ga, SPARK, 11, 34, -24, True, 'right')
        MAP.port(f, *HOUSTON, 'Houston', ga, SPARK if p >= 1 else MUTED, 11, 34, 52, True, 'center')
        x, y = MAP.point_on(ROUTE, p)
        ship_icon(f, x, y - 6, 34, ga)
        words(f, '26 avril 1956.', 440, 66, 14.7, MUTED, t_out=21.6, bold=False)
        words(f, 'Malcom McLean lance l’Ideal X.', 520, 58, 15.2, INK, t_out=21.6)
        f.text('conteneurs à bord', W/2, 1340, 44, MUTED, ga, bold=False)
        big_center(f, str(int(round(58 * ease(seg(t, 15.6, 18.6))))), 1470, 120, SPARK, ga, bump(t, 18.6, 0.2))
    if 21.6 <= t < 30.2:
        ga = ease(seg(t, 21.7, 22.1)) * (1 - seg(t, 29.6, 30.0))
        words(f, 'Coût pour charger 1 tonne', 470, 54, 21.8, MUTED, t_out=29.6, bold=False)
        f.text('(dollars de 1956)', W/2, 525, 34, MUTED, ga * ease(seg(t, 22.2, 22.5)), bold=False)
        base = 1300; hmax = 640
        # colonne gauche : à la main
        ha1 = ease_io(seg(t, 22.4, 24.6))
        f.rect(170, base - hmax * ha1, 300, hmax * ha1, RED, ga, 10)
        f.text('À la main', 320, base + 70, 46, INK, ga)
        f.text(f'{5.86 * ha1:.2f} $'.replace('.', ','), 320, base - hmax * ha1 - 30, 70, RED, ga * seg(t, 22.4, 22.6), MONO)
        # colonne droite : en conteneur
        a2 = ease(seg(t, 25.4, 25.8)) * ga
        h2 = hmax * 0.16 / 5.86 * ease(seg(t, 25.6, 26.4))
        f.rect(610, base - h2, 300, h2, SPARK, a2, 6)
        f.text('En conteneur', 760, base + 70, 46, INK, a2)
        f.text('0,16 $', 760, base - h2 - 30, 70, SPARK, a2, MONO)
        f.line([(120, base + 2), (960, base + 2)], LINE, ga, 3)
        sa = ease(seg(t, 27.4, 27.8)) * ga
        f.text('Estimations de l’époque, ports américains.', W/2, 1490, 32, MUTED, sa, bold=False)

    # S5 — la réponse (30–35.4)
    if 29.9 <= t < 35.4:
        a = ease(seg(t, 30.0, 30.3)) * (1 - seg(t, 34.8, 35.2))
        v = 36 * ease(seg(t, 30.0, 31.2))
        big_center(f, f'÷ {int(round(v))}', 860, 250, SPARK, a, bump(t, 31.2, 0.12))
        words(f, 'Le coût du chargement', 1010, 66, 31.4, INK, t_out=34.8)
        words(f, 'divisé par 36.', 1100, 66, 32.0, INK, t_out=34.8)
        words(f, 'Des jours au port deviennent des heures.', 1250, 46, 33.0, MUTED, t_out=34.8, bold=False)

    # S6 — le retournement : une boîte standard qui ne s'ouvre jamais (35–48)
    if 35.0 <= t < 48.4:
        words(f, 'Le secret ?', 760, 130, 35.1, INK, t_out=37.1)
        words(f, 'On n’ouvre plus rien.', 900, 96, 35.7, SPARK, t_out=37.1)
        ga = ease(seg(t, 37.3, 37.8)) * (1 - seg(t, 47.9, 48.3))
        if ga > 0:
            # trois postes : camion, navire, train ; la même boîte passe de l'un à l'autre
            ys = [700, 980, 1260]
            labels = ['Camion', 'Navire', 'Train']
            for i, (yy, lab) in enumerate(zip(ys, labels)):
                la = ease(seg(t, 37.5 + i * 0.3, 37.9 + i * 0.3)) * ga
                f.text(lab, 140, yy - 70, 40, MUTED, la, DISPLAY, False, 'left')
                if i == 0:   # camion
                    f.rect(160, yy, 120, 70, CAPITAL, la, 8); f.rect(280, yy + 60, 560, 14, CAPITAL, la, 4)
                    for wx in (200, 420, 760): f.circle(wx, yy + 92, 22, MUTED, la)
                elif i == 1:  # navire
                    hull(f, 140, 940, yy + 40, 70, la)
                    for j in range(5): container(f, 170 + j * 145, yy - 30, 136, 66, [CAPITAL, MUTED, EARTH, CAPITAL, RED][j], la * 0.8)
                else:         # train
                    f.rect(150, yy + 60, 780, 12, CAPITAL, la, 4)
                    for wx in (220, 400, 680, 860): f.circle(wx, yy + 86, 18, MUTED, la)
                    f.line([(120, yy + 108), (960, yy + 108)], LINE, la, 4)
            # trajet de la boîte dorée : camion -> navire -> train
            p1 = ease_io(seg(t, 38.8, 40.8)); p2 = ease_io(seg(t, 41.6, 43.6))
            bx = 320 + 0 * p1; by = lerp(ys[0] - 10, ys[1] - 100, p1)
            if p1 >= 1: bx = lerp(320, 400, p2); by = lerp(ys[1] - 100, ys[2] - 10, p2)
            if p1 > 0 and p1 < 1 or (p2 > 0 and p2 < 1):
                f.line([(bx + 230, 600), (bx + 230, by)], INK, ga * 0.5, 3)    # câble de grue
            container(f, bx, by, 460, 70, SPARK, ga)
            words(f, 'La même boîte, scellée,', 1430, 52, 44.0, INK, t_out=47.9)
            words(f, 'du départ jusqu’à l’arrivée.', 1500, 52, 44.5, SPARK, t_out=47.9)
            f.text('Une seule taille de référence : 20 pieds = 1 EVP', W/2, 470, 36, MUTED, ease(seg(t, 38.2, 38.6)) * ga, bold=False)

    # S7 — l'escalade : aujourd'hui (48–56)
    if 48.0 <= t < 56.4:
        out = 1 - seg(t, 55.9, 56.3)
        words(f, 'Aujourd’hui,', 470, 70, 48.1, INK, t_out=55.9)
        v = 51.4 * ease(seg(t, 48.6, 50.4))
        big_center(f, f'{v:.0f} millions'.replace('.', ','), 640, 120, SPARK, out * ease(seg(t, 48.5, 48.8)), bump(t, 50.4, 0.12))
        words(f, 'de conteneurs (en EVP) dans le monde.', 730, 46, 49.4, INK, t_out=55.9)
        f.text('Drewry, fin 2023', W/2, 790, 30, MUTED, out * ease(seg(t, 49.8, 50.1)), bold=False)
        # mur de conteneurs qui se remplit
        cols, rows = 16, 7; n = int(cols * rows * ease_io(seg(t, 48.8, 53.0)))
        pal = [SPARK, EARTH, RED, CAPITAL, MUTED]
        for i in range(n):
            r, c = divmod(i, cols)
            container(f, 100 + c * 55, 1240 - r * 46, 51, 40, pal[(c * 3 + r * 7) % 5], out * 0.9, ribs=False)
        words(f, 'Plus de 800 millions d’EVP manutentionnés', 1380, 46, 53.2, INK, t_out=55.9, bold=False)
        words(f, 'par an dans les ports.', 1440, 46, 53.6, INK, t_out=55.9, bold=False)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        words(f, 'Pas un moteur, pas une puce.', 720, 66, 56.3)
        words(f, 'Une boîte a changé le monde.', 830, 66, 57.4, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(140, 1000, 800, 170, OCEAN, a, 28)
        f.text('Abonne-toi.', W/2, 1105, 64, INK, a)

def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    for t0, n in ((0.15, 3), (0.7, 3), (1.6, 4)):
        for i in range(n): ev.append((t0 + i * 0.11, pop(420 + 40 * i, 0.09)))
    ev += [(2.4, clink(900)), (2.45, ding(660, amp=0.18))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (3.9, 12.1, 14.4, 21.6, 29.7, 34.9, 47.9, 55.9)]
    ev += [(4.2, pop(330)), (4.8, pop(392)), (5.5, pop(523)), (7.0, pop(440)), (8.8, pop(392)), (9.3, pop(523))]
    x = 4.8
    while x < 11.8: ev.append((x, tick())); x += 0.2
    ev += [(12.4, pop(330)), (12.9, pop(440))]
    for xx in (15.4, 20.4): ev.append((xx, clink(1700)))
    x = 15.6
    while x < 18.6: ev.append((x, tick())); x += 3.0 / 58
    ev += [(18.6, ding(880, amp=0.25)), (22.4, rise(2.2, 200, 600, 0.08)), (24.6, pop(300, 0.15)),
           (25.6, pop(900, 0.1)), (26.4, ding(1175, amp=0.28)), (30.0, rise(1.2, 300, 1046, 0.1)), (31.2, ding(1046, amp=0.28)),
           (35.1, pop(300, 0.15)), (35.7, pop(450, 0.15))]
    for xx in (37.5, 37.8, 38.1): ev.append((xx, pop(500, 0.08)))
    ev += [(38.8, rise(2.0, 300, 600, 0.06)), (40.8, clink(900)), (41.6, rise(2.0, 300, 600, 0.06)), (43.6, clink(900)), (44.0, pop(440))]
    ev += [(48.6, rise(1.8, 300, 1046, 0.1)), (50.4, ding(1046, amp=0.25))]
    x = 48.8
    while x < 53.0: ev.append((x, clink(900 + (x - 48.8) * 150))); x += 0.3
    ev += [(53.2, pop(392)), (56.3, pop(440)), (57.4, pop(550)), (60.0, ding(784, amp=0.22))]
    return ev
