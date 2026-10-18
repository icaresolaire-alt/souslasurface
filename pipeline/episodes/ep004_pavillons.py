"""Pavillons de complaisance : pourquoi tant de navires sont immatriculés au Panama, au Liberia, aux îles Marshall.
Même structure que le pilote, vraie carte du monde (worldmap.py)."""
import math
from lib import *
from kinetic import words, bump, big_center
from worldmap import WorldMap

TOTAL = 66.0

# lieux (lon, lat)
PLACES = {
    'Athènes': (23.6, 37.9), 'Monrovia': (-10.8, 6.3), 'Panama': (-79.6, 9.1), 'Majuro': (171.4, 7.1),
    'La Valette': (14.5, 35.9), 'Shanghai': (121.5, 31.2), 'Tokyo': (139.7, 35.7), 'Virginie': (-77.45, 38.95),
}
# monde : de l'Amérique au Pacifique ouest (Panama à gauche, îles Marshall à droite)
MW = WorldMap(lon=(-100, 180), lat=(-38, 62), x=40, y=700, w=1000)
# zoom Atlantique pour la Virginie -> Liberia
MA = WorldMap(lon=(-95, 5), lat=(-5, 50), x=40, y=760, w=1000)

# ---------- dessins ----------
def flag(f, x, y, w, kind, a=1.0):
    """Drapeaux stylisés, coin haut gauche en (x, y), proportion 3:2."""
    if a <= 0: return
    h = w * 2 / 3; c = f.c
    BLUE, WHITE, REDF = '#2f6fb7', '#f2f2f2', '#c8463d'
    if kind == 'GR':
        for i in range(9): f.rect(x, y + i * h / 9, w, h / 9 + 0.5, BLUE if i % 2 == 0 else WHITE, a)
        f.rect(x, y, w * 0.37, h * 5 / 9, BLUE, a)
        f.rect(x + w * 0.37 / 2 - h / 18, y, h / 9, h * 5 / 9, WHITE, a)
        f.rect(x, y + h * 2 / 9, w * 0.37, h / 9, WHITE, a)
    elif kind == 'LR':
        for i in range(11): f.rect(x, y + i * h / 11, w, h / 11 + 0.5, REDF if i % 2 == 0 else WHITE, a)
        f.rect(x, y, h * 5 / 11, h * 5 / 11, '#22336b', a)
        f.circle(x + h * 2.5 / 11, y + h * 2.5 / 11, h * 0.09, WHITE, a)
    elif kind == 'PA':
        f.rect(x, y, w / 2, h / 2, WHITE, a); f.rect(x + w / 2, y, w / 2, h / 2, REDF, a)
        f.rect(x, y + h / 2, w / 2, h / 2, '#22336b', a); f.rect(x + w / 2, y + h / 2, w / 2, h / 2, WHITE, a)
        f.circle(x + w / 4, y + h / 4, h * 0.09, '#22336b', a); f.circle(x + 3 * w / 4, y + 3 * h / 4, h * 0.09, REDF, a)
    elif kind == 'MH':
        f.rect(x, y, w, h, '#22336b', a)
        f.color('#e8862a', a); c.move_to(x, y + h); c.line_to(x + w, y + h * 0.05); c.line_to(x + w, y + h * 0.2); c.close_path(); c.fill()
        f.color(WHITE, a); c.move_to(x, y + h); c.line_to(x + w, y + h * 0.2); c.line_to(x + w, y + h * 0.35); c.close_path(); c.fill()
        f.circle(x + w * 0.22, y + h * 0.3, h * 0.11, WHITE, a)
    elif kind == 'MT':
        f.rect(x, y, w / 2, h, WHITE, a); f.rect(x + w / 2, y, w / 2, h, REDF, a)

def ship(f, x, y, s, col=INK, a=1.0, flag_kind=None, flag_a=1.0):
    """Petit cargo de profil, centre de la coque en (x, y)."""
    if a <= 0: return
    c = f.c; f.color(col, a)
    c.move_to(x - s, y - s * 0.12); c.line_to(x + s * 1.05, y - s * 0.12); c.line_to(x + s * 0.8, y + s * 0.3); c.line_to(x - s * 0.9, y + s * 0.3); c.close_path(); c.fill()
    for i in range(5): f.rect(x - s * 0.55 + i * s * 0.26, y - s * 0.38, s * 0.22, s * 0.24, SPARK if i % 2 else EARTH, a, 2)
    f.rect(x - s * 0.95, y - s * 0.55, s * 0.28, s * 0.43, col, a, 2)
    f.line([(x - s * 0.82, y - s * 0.55), (x - s * 0.82, y - s * 1.15)], col, a, 3)
    if flag_kind: flag(f, x - s * 0.82, y - s * 1.15, s * 0.6, flag_kind, a * flag_a)

def arc_point(p0, p1, u, lift):
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2 - lift
    return ((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * mx + u * u * p1[0],
            (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * my + u * u * p1[1])

def arc(f, p0, p1, p, lift, col, a, width=4):
    if p <= 0 or a <= 0: return
    n = 40; pts = [arc_point(p0, p1, i / n * p, lift) for i in range(n + 1)]
    f.line(pts, col, a, width)

def pin(f, M, name, a, col=SPARK, r=10, label=None, dy=-24, size=32):
    x, y = M.xy(*PLACES[name])
    f.circle(x, y, r, col, a)
    if label: f.text(label, x, y + dy, size, INK, a)
    return x, y

# vol des drapeaux grecs (S4) : (pavillon, lieu, navires, départ)
FLIGHTS = [('LR', 'Monrovia', 'Liberia', 1279, 16.4), ('MH', 'Majuro', 'Îles Marshall', 1061, 18.6),
           ('MT', 'La Valette', 'Malte', 579, 20.8), ('PA', 'Panama', 'Panama', 330, 23.0)]
OTHERS = 4388 - 463 - sum(fl[3] for fl in FLIGHTS)   # autres pavillons étrangers : 676

def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.6, 30.0))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Pourquoi ces drapeaux ?', W/2, 296, 46, SPARK, ha)

    # S1 — accroche (0–4) : un navire grec, son drapeau change en route
    if t < 4.3:
        o = 3.9; fo = (1 - seg(t, o, o + 0.3)) * ease(seg(t, 0, 0.25))
        MW.draw(f, fo)
        A = MW.xy(*PLACES['Athènes']); L = MW.xy(*PLACES['Monrovia'])
        f.circle(*A, 9, INK, fo)
        f.circle(*L, 9, SPARK, fo * ease(seg(t, 2.0, 2.3)))
        p = ease_io(seg(t, 1.6, 3.2))
        arc(f, A, L, p, 160, SPARK, fo * 0.8, 3)
        # le drapeau grec quitte le navire, un drapeau libérien arrive
        sx, sy = W/2, 1300
        ship(f, sx + 30 * math.sin(t * 1.3), sy + 6 * math.sin(t * 2.4), 130, INK, fo, 'LR' if t > 3.2 else None, ease(seg(t, 3.2, 3.5)))
        if t < 3.2:
            fx, fy = arc_point(A, L, p, 160) if t > 1.6 else (sx - 130 * 0.82 + 30 * math.sin(t * 1.3), sy - 130 * 1.15 + 6 * math.sin(t * 2.4))
            flag(f, fx - (0 if t <= 1.6 else 22), fy - (0 if t <= 1.6 else 15), lerp(78, 44, seg(t, 1.6, 2.2)), 'GR', fo)
        words(f, 'Ce navire est grec.', 420, 84, 0.15, INK, t_out=o)
        words(f, 'Mais officiellement,', 560, 64, 1.5, MUTED, t_out=o, bold=False)
        words(f, 'il est libérien.', 1520, 84, 2.3, SPARK, t_out=o)

    # S2 — enjeu : le podium des pavillons (4–12)
    if 4.0 <= t < 12.6:
        ga = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, 12.0, 12.4))
        MW.draw(f, ga)
        words(f, 'Les drapeaux les plus portés', 440, 60, 4.2, INK, t_out=12.0)
        words(f, 'ne sont ni chinois, ni grecs.', 520, 60, 4.8, INK, t_out=12.0)
        ranks = [('Monrovia', 'Liberia', '1er', 'LR', 6.2), ('Panama', 'Panama', '2e', 'PA', 7.4), ('Majuro', 'Îles Marshall', '3e', 'MH', 8.6)]
        for i, (pl, lab, rk, fk, t0) in enumerate(ranks):
            a = ease(seg(t, t0, t0 + 0.3)) * ga
            x, y = MW.xy(*PLACES[pl])
            pu = 1 + 0.3 * math.sin((t - t0) * 6) * (1 - seg(t, t0, t0 + 1.2))
            f.circle(x, y, 10 * pu, SPARK, a)
            f.circle(x, y, 10 + 40 * seg(t, t0, t0 + 0.6), SPARK, a * (1 - seg(t, t0, t0 + 0.6)), 3)
            fx = min(max(x - 30, 60), 960)
            flag(f, fx, y - 70, 60, fk, a)
            # légende sous la carte
            row_y = 1120 + i * 88
            flag(f, 260, row_y - 34, 54, fk, a)
            f.text(rk, 240, row_y, 46, SPARK, a, MONO, True, 'right')
            f.text(lab, 340, row_y, 50, INK, a, DISPLAY, True, 'left')
        words(f, 'Ces 3 pays immatriculent', 1440, 50, 9.8, MUTED, t_out=12.0, bold=False)
        words(f, 'des navires qu’ils ne possèdent pas.', 1510, 50, 10.2, SPARK, t_out=12.0)

    # S3 — la question (12–14.5)
    if 12.2 <= t < 14.9:
        words(f, 'Pourquoi', 840, 120, 12.4, INK, t_out=14.4)
        words(f, 'ces pays-là ?', 980, 120, 12.8, SPARK, t_out=14.4)

    # S4 — la preuve : la flotte grecque s'envole (14.5–30)
    if 14.4 <= t < 30.2:
        ga = ease(seg(t, 14.5, 14.9)) * (1 - seg(t, 29.6, 30.0))
        M = MW
        M.draw(f, ga)
        A = M.xy(*PLACES['Athènes'])
        f.text('Navires grecs partis sous un autre drapeau', W/2, 470, 42, MUTED, ga, bold=False)
        gone = 0
        for fk, pl, lab, n, t0 in FLIGHTS:
            P1 = M.xy(*PLACES[pl]); lift = 120 if pl != 'La Valette' else 60
            p = ease_io(seg(t, t0, t0 + 1.6))
            arc(f, A, P1, p, lift, SPARK, ga * 0.7, 3)
            # nuée de petits drapeaux qui partent d'Athènes
            for k in range(6):
                u = seg(t, t0 + k * 0.12, t0 + 1.4 + k * 0.12)
                if 0 < u < 1:
                    x, y = arc_point(A, P1, ease_io(u), lift)
                    flag(f, x - 12, y - 8, 24, 'GR', ga)
            if p >= 1:
                x, y = P1
                flag(f, min(max(x - 26, 50), 980), y - 56, 52, fk, ga)
            gone += n * ease(seg(t, t0, t0 + 1.6))
        gone += OTHERS * ease(seg(t, 24.6, 25.4))
        f.circle(*A, 12, INK, ga)
        left = gone
        big_center(f, fmt_int(left), 600, 110, SPARK, ga, max(bump(t, fl[4] + 1.6, 0.12) for fl in FLIGHTS))
        # tableau sous la carte
        for i, (fk, pl, lab, n, t0) in enumerate(FLIGHTS):
            a = ease(seg(t, t0 + 1.2, t0 + 1.5)) * ga
            col, row = i % 2, i // 2
            x0 = 110 + col * 450; y0 = 1150 + row * 80
            flag(f, x0, y0 - 32, 48, fk, a)
            f.text(lab, x0 + 64, y0, 34, INK, a, DISPLAY, False, 'left')
            f.text(fmt_int(n), x0 + 410, y0, 34, SPARK, a, MONO, True, 'right')
        oa = ease(seg(t, 24.6, 24.9)) * ga
        f.text('Autres pavillons', 174, 1330, 36, INK, oa, DISPLAY, False, 'left')
        f.text(fmt_int(OTHERS), 970, 1330, 36, SPARK, oa, MONO, True, 'right')
        ea = ease(seg(t, 26.0, 26.4)) * ga
        if ea > 0:
            f.rect(110, 1380, 860, 100, OCEAN, ea, 24)
            flag(f, 140, 1406, 66, 'GR', ea)
            f.text('Restés grecs :', 230, 1444, 40, INK, ea, DISPLAY, True, 'left')
            f.text('463 sur 4 388', 940, 1444, 44, RED, ea, MONO, True, 'right')
        f.text('Navires sous contrôle grec, mars 2026 (GSCC)', W/2, 1530, 28, MUTED, ga, bold=False)

    # S5 — la réponse (30–35.4)
    if 29.9 <= t < 35.4:
        a = ease(seg(t, 30.0, 30.3)) * (1 - seg(t, 34.8, 35.2))
        v = 45 * ease(seg(t, 30.0, 31.0))
        words(f, 'Près de', 640, 72, 30.0, INK, t_out=34.8)
        big_center(f, f'{int(round(v))} %', 880, 240, SPARK, a, bump(t, 31.0, 0.15), DISPLAY)
        words(f, 'de la capacité mondiale', 1040, 60, 31.3, INK, t_out=34.8)
        words(f, 'sous 3 drapeaux.', 1120, 60, 31.8, INK, t_out=34.8)
        for i, fk in enumerate(('LR', 'PA', 'MH')):
            fa = ease(seg(t, 32.3 + i * 0.25, 32.6 + i * 0.25)) * a
            flag(f, W/2 - 200 + i * 145, 1200, 110, fk, fa)
        f.text('En tonnage (tpl), au 1er janvier 2026. Source : CNUCED.', W/2, 1400, 30, MUTED, ease(seg(t, 33.0, 33.4)) * a, bold=False)

    # S6 — le retournement : on loue un drapeau (35–48)
    if 35.0 <= t < 48.4:
        words(f, 'Le secret ?', 760, 120, 35.1, INK, t_out=37.1)
        words(f, 'Un drapeau, ça se loue.', 900, 84, 35.7, SPARK, t_out=37.1)
        ga = ease(seg(t, 37.3, 37.7)) * (1 - seg(t, 42.6, 43.0))
        if ga > 0:
            f.text('Ce que l’armateur y gagne', W/2, 470, 46, MUTED, ga, bold=False)
            cards = [(37.6, 'Impôts', 'Au Panama : pas d’impôt sur les', 'bénéfices faits hors du pays.'),
                     (39.0, 'Équipage', 'Des marins de n’importe où,', 'payés moins cher.'),
                     (40.4, 'Formalités', 'Inscription rapide,', 'règles plus souples.')]
            for i, (t0, h, l1, l2) in enumerate(cards):
                a = ease(seg(t, t0, t0 + 0.35)) * ga
                y = 600 + i * 290; dx = 60 * (1 - ease(seg(t, t0, t0 + 0.35)))
                f.rect(100 + dx, y, 880, 240, OCEAN, a, 26)
                f.rect(100 + dx, y, 12, 240, SPARK, a, 6)
                f.text(h, 150 + dx, y + 80, 56, SPARK, a, DISPLAY, True, 'left')
                f.text(l1, 150 + dx, y + 150, 40, INK, a, DISPLAY, False, 'left')
                f.text(l2, 150 + dx, y + 202, 40, INK, a, DISPLAY, False, 'left')
        ma = ease(seg(t, 42.9, 43.3)) * (1 - seg(t, 47.9, 48.3))
        if ma > 0:
            MA.draw(f, ma)
            V = MA.xy(*PLACES['Virginie']); L = MA.xy(*PLACES['Monrovia'])
            words(f, 'Et le registre du Liberia', 470, 62, 43.0, INK, t_out=47.9)
            words(f, 'est géré… depuis la Virginie,', 560, 62, 43.7, SPARK, t_out=47.9)
            words(f, 'aux États-Unis.', 650, 62, 44.3, SPARK, t_out=47.9)
            p = ease_io(seg(t, 44.6, 46.0))
            arc(f, V, L, p, 140, SPARK, ma, 5)
            f.circle(*V, 12, SPARK, ma * ease(seg(t, 43.6, 43.9)))
            f.text('Virginie', V[0] + 20, V[1] - 20, 36, INK, ma * ease(seg(t, 43.6, 43.9)), DISPLAY, True, 'left')
            la = ease(seg(t, 45.8, 46.1)) * ma
            f.circle(*L, 12, SPARK, la)
            flag(f, L[0] - 30, L[1] - 70, 60, 'LR', la)
            f.text('Liberia', L[0], L[1] + 56, 36, INK, la)

    # S7 — l'escalade : les propriétaires d'un côté, les drapeaux de l'autre (48–56)
    if 48.0 <= t < 56.4:
        out = 1 - seg(t, 55.9, 56.3)
        ga = ease(seg(t, 48.1, 48.5)) * out
        MW.draw(f, ga)
        words(f, 'Les navires appartiennent', 440, 58, 48.2, INK, t_out=55.9)
        words(f, 'à la Grèce, la Chine, le Japon…', 520, 58, 48.6, INK, t_out=55.9)
        owners = ['Athènes', 'Shanghai', 'Tokyo']; flags_ = [('Monrovia', 'LR'), ('Panama', 'PA'), ('Majuro', 'MH')]
        for i, o in enumerate(owners):
            a = ease(seg(t, 49.0 + i * 0.3, 49.3 + i * 0.3)) * ga
            f.circle(*MW.xy(*PLACES[o]), 11, INK, a)
        for j, (pl, fk) in enumerate(flags_):
            P1 = MW.xy(*PLACES[pl])
            for i, o in enumerate(owners):
                t0 = 50.4 + j * 0.5 + i * 0.15
                P0 = MW.xy(*PLACES[o])
                lift = 90 + 40 * i
                arc(f, P0, P1, ease_io(seg(t, t0, t0 + 1.4)), lift, SPARK, ga * 0.45, 2)
                u = (t - t0) / 1.4
                if u > 0:
                    uu = u % 1.0
                    x, y = arc_point(P0, P1, uu, lift)
                    f.circle(x, y, 6, SPARK, ga * min(1, u * 3))
            la = ease(seg(t, 51.4 + j * 0.5, 51.7 + j * 0.5)) * ga
            flag(f, min(max(P1[0] - 26, 50), 980), P1[1] - 58, 52, fk, la)
        words(f, '…et naviguent sous', 1200, 58, 52.6, INK, t_out=55.9)
        words(f, 'des drapeaux de location.', 1280, 64, 53.1, SPARK, t_out=55.9)
        f.text('Grèce, Chine et Japon : plus de 40 % de la capacité mondiale (CNUCED).', W/2, 1400, 28, MUTED, ease(seg(t, 53.8, 54.2)) * out, bold=False)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        words(f, 'Un navire a un propriétaire.', 760, 64, 56.3, INK)
        words(f, 'Son drapeau, il le choisit.', 860, 64, 57.6, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(140, 1030, 800, 170, OCEAN, a, 28)
        f.text('Abonne-toi.', W/2, 1135, 64, INK, a)

def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    for t0, n in ((0.15, 4), (1.5, 2), (2.3, 3)):
        for i in range(n): ev.append((t0 + i * 0.11, pop(420 + 40 * i, 0.09)))
    ev += [(1.6, rise(1.6, 300, 900, 0.08)), (3.2, ding(988, amp=0.22))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (3.9, 12.1, 14.4, 29.7, 34.9, 42.7, 47.9, 55.9)]
    ev += [(4.2, pop(330)), (4.8, pop(392))]
    for t0 in (6.2, 7.4, 8.6): ev.append((t0, clink(1700)))
    ev += [(9.8, pop(440)), (10.2, pop(523)), (12.4, pop(330)), (12.8, pop(440))]
    for fk, pl, lab, n, t0 in FLIGHTS:
        for k in range(6): ev.append((t0 + k * 0.12, tick()))
        ev.append((t0 + 1.6, clink(1300 + 150 * FLIGHTS.index((fk, pl, lab, n, t0)))))
    ev += [(24.6, pop(392)), (26.0, ding(660, amp=0.22)), (30.0, rise(1.0, 300, 1046, 0.1)), (31.0, ding(1046, amp=0.3))]
    for i in range(3): ev.append((32.3 + i * 0.25, pop(500 + i * 60)))
    ev += [(35.1, pop(300, 0.15)), (35.7, pop(450, 0.15))]
    for t0 in (37.6, 39.0, 40.4): ev.append((t0, pop(520)))
    ev += [(43.0, pop(392)), (43.7, pop(440)), (44.6, rise(1.4, 300, 900, 0.08)), (46.0, ding(880, amp=0.25))]
    for i in range(3): ev.append((49.0 + i * 0.3, pop(400 + i * 50)))
    for j in range(3): ev.append((51.4 + j * 0.5, clink(1500 + j * 200)))
    ev += [(52.6, pop(440)), (53.1, pop(550)), (56.3, pop(440)), (57.6, pop(550)), (60.0, ding(784, amp=0.22))]
    return ev
