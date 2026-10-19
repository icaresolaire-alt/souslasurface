"""10 amis qui invitent 10 amis : la croissance exponentielle. Même structure que le pilote."""
import math
import numpy as np
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
COVER = dict(tag='Maths', l1='10 amis qui invitent', l2='10 amis', big='×10')
POP = 8.2e9                      # population mondiale mi-2026 (US Census Bureau, IDB)

# anneaux concentriques : un anneau par étape
CX, CY = W/2, 965
def ring_r(k): return 34 + 26 * k          # rayon de l'anneau k (1..10), max 304
rng = np.random.default_rng(11)
RINGS = {}
for k in range(1, 11):
    n = 10 if k == 1 else (100 if k == 2 else 260 + 30 * k)
    if k <= 2:
        ang = np.linspace(0, 2*math.pi, n, endpoint=False) + (0.3 if k == 2 else 0)
        rad = np.full(n, ring_r(k))
    else:
        ang = rng.uniform(0, 2*math.pi, n); rad = ring_r(k) + rng.uniform(-10, 10, n)
    RINGS[k] = list(zip(CX + rad * np.cos(ang), CY + rad * np.sin(ang)))

# temps d'apparition de chaque étape
LT = {1: 14.0, 2: 15.4, 3: 16.8, 4: 18.2, 5: 19.6, 6: 21.0, 7: 22.4, 8: 23.8, 9: 26.8, 10: 28.0}
def level_at(t):
    n = 0
    for k, tk in LT.items():
        if t >= tk: n = k
    return n
def cumul(n): return sum(10 ** k for k in range(1, n + 1))   # invités au total après n étapes

def draw_rings(f, t, n, a, t_birth=LT):
    f.circle(CX, CY, 16, SPARK, a)
    for k in range(1, n + 1):
        tk = t_birth[k]; p = ease(seg(t, tk, tk + 0.5))
        r = 9 if k == 1 else (5 if k == 2 else max(2.2, 4.6 - 0.25 * k))
        col = SPARK if k == n else (INK if k >= 8 else CAPITAL)
        pts = RINGS[k]
        for (x, y) in pts:
            xx = lerp(CX, x, p); yy = lerp(CY, y, p)
            f.circle(xx, yy, r, col, a * (0.55 + 0.45 * p))
        if t - tk < 0.6:
            f.circle(CX, CY, ring_r(k) + 30 * seg(t, tk, tk + 0.6), SPARK, a * (1 - seg(t, tk, tk + 0.6)), 4)

def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.8, 30.2))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Combien d’étapes ?', W/2, 296, 46, SPARK, ha)

    # S1 — accroche (0–4) : un point en fait naître 10, puis 100
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        hb = {1: 0.05, 2: 0.9, 3: 1.7}
        draw_rings(f, t, 1 if t < 0.9 else (2 if t < 1.7 else 3), fo, hb)
        words(f, 'Invite 10 amis.', 470, 84, 0.15, INK, t_out=o)
        words(f, 'Chacun en invite 10.', 1380, 72, 0.9, INK, t_out=o)
        words(f, 'En 10 étapes, la Terre', 1490, 64, 2.0, SPARK, t_out=o)
        words(f, 'entière est invitée.', 1570, 64, 2.6, SPARK, t_out=o)

    # S2 — enjeu (4–10.8) : l'intuition linéaire
    if 4.0 <= t < 11.0:
        words(f, '10 amis.', 760, 130, 4.2, INK, t_out=5.7)
        words(f, '10 étapes.', 760, 130, 5.9, INK, t_out=7.4)
        words(f, 'Ça fait combien ?', 760, 96, 7.6, INK, t_out=8.9)
        a = ease(seg(t, 9.0, 9.3)) * (1 - seg(t, 10.4, 10.8))
        f.text('Ton intuition :', W/2, 700, 56, MUTED, a, bold=False)
        big_center(f, '10 × 10 = 100', 860, 110, INK, a, bump(t, 9.0))
        # petits points qui s'alignent sagement (pensée linéaire)
        for i in range(10):
            pa = ease(seg(t, 9.2 + i * 0.08, 9.4 + i * 0.08)) * a
            f.circle(W/2 + (i - 4.5) * 70, 1010, 14, CAPITAL, pa)

    # S3 — on compte (10.8–13.5)
    if 10.7 <= t < 13.6:
        words(f, 'Comptons', 820, 120, 10.9, INK, t_out=12.4)
        words(f, 'pour de vrai.', 960, 110, 11.2, SPARK, t_out=12.4)

    # S4 — la preuve : anneaux + jauge de l'humanité (13.5–29.8)
    if 13.4 <= t < 30.0:
        ga = ease(seg(t, 13.5, 13.9)) * (1 - seg(t, 29.4, 29.8))
        n = level_at(t)
        draw_rings(f, t, n, ga)
        sc = bump(t, LT[n], 0.18) if n else 1.0
        f.text(f'Étape {n}' if n else 'Toi', W/2, 440, 54, MUTED, ga, MONO)
        big_center(f, fmt_int(10 ** n) if n else '1', 560, 86 if n < 10 else 80, SPARK if n < 10 else RED, ga, sc)
        f.text('nouveaux invités' if n else 'tu lances l’invitation', W/2, 615, 36, MUTED, ga, bold=False)
        # jauge : part de l'humanité invitée (cumul)
        tot = cumul(n); fr = tot / POP
        f.text('Part de l’humanité invitée', W/2, 1330, 40, INK, ga, bold=False)
        gx, gy, gw, gh = 140, 1360, 800, 44
        f.rect(gx, gy, gw, gh, OCEAN, ga, 22)
        f.rect(gx, gy, gw, gh, LINE, ga, 22)
        # remplissage animé entre deux étapes
        prev = cumul(max(0, n - 1)) / POP
        vis = lerp(prev, fr, ease(seg(t, LT.get(n, 0), LT.get(n, 0) + 0.6))) if n else 0
        wfill = gw * min(1.0, vis)
        if wfill > 0: f.rect(gx, gy, max(wfill, 10), gh, RED if vis >= 1 else SPARK, ga, 22)
        if vis >= 1:
            sh = 10 * math.sin((t - LT[10]) * 60) * (1 - seg(t, LT[10], LT[10] + 0.6))
            f.text('> 100 %', W/2 + sh, 1480, 72, RED, ga, MONO)
            f.text('Plus que toute la Terre !', W/2 + sh, 1550, 46, RED, ga * ease(seg(t, LT[10] + 0.2, LT[10] + 0.5)))
        else:
            pct = fmt_pct(vis, 1 if vis < 0.1 else 0) if vis >= 0.001 else ('0 %' if n == 0 else '< 0,1 %')
            f.text(pct, W/2, 1480, 72, INK if vis < 0.05 else SPARK, ga, MONO)
            if n == 8:
                ka = ease(seg(t, 24.4, 24.8)) * (1 - seg(t, 26.6, 26.8)) * ga
                f.text('100 millions… et à peine plus de 1 %.', W/2, 1550, 40, MUTED, ka, bold=False)

    # S5 — la réponse (30–35)
    if 29.9 <= t < 35.4:
        a = ease(seg(t, 30.0, 30.3)) * (1 - seg(t, 34.8, 35.2))
        big_center(f, '10 étapes', 880, 190, SPARK, a, bump(t, 30.0, 0.12), DISPLAY)
        words(f, 'pour dépasser', 1030, 66, 30.7, INK, t_out=34.8)
        words(f, 'les 8,2 milliards d’humains.', 1110, 66, 31.1, INK, t_out=34.8)
        words(f, '10 milliards de nouveaux invités à la dernière.', 1250, 40, 32.3, MUTED, t_out=34.8, bold=False)

    # S6 — le retournement : +10 contre ×10 (35–48)
    if 35.0 <= t < 48.4:
        words(f, 'Pourquoi ?', 760, 150, 35.1, INK, t_out=37.1)
        words(f, 'Ton cerveau pense', 920, 72, 35.8, INK, t_out=37.1)
        words(f, 'en ligne droite.', 1010, 72, 36.2, SPARK, t_out=37.1)
        ga = ease(seg(t, 37.3, 37.8)) * (1 - seg(t, 47.9, 48.3))
        if ga > 0:
            la = ease(seg(t, 37.4, 37.8)) * ga; ra = ease(seg(t, 38.0, 38.4)) * ga
            f.rect(110, 400, 410, 190, OCEAN, la, 28)
            f.text('+ 10', 315, 500, 96, MUTED, la, MONO, True)
            f.text('ce qu’on imagine', 315, 560, 34, MUTED, la, bold=False)
            f.rect(560, 400, 410, 190, OCEAN, ra, 28)
            c = f.c; c.save(); c.translate(765, 500); sc2 = bump(t, 38.0, 0.2); c.scale(sc2, sc2)
            f.text('× 10', 0, 0, 96, SPARK, ra, MONO, True); c.restore()
            f.text('ce qui se passe', 765, 560, 34, SPARK, ra, bold=False)
            # graphique : axe étapes 0..10, axe vertical jusqu'à 10 milliards
            x0, y0, x1, y1 = 150, 1300, 950, 700
            f.line([(x0, y1 - 20), (x0, y0), (x1 + 10, y0)], MUTED, ga, 3)
            f.text('étapes', W/2, y0 + 85, 28, MUTED, ga, bold=False)
            for s in range(0, 11, 2):
                f.text(str(s), x0 + (x1 - x0) * s / 10, y0 + 50, 30, MUTED, ga, MONO, False)
            # repère population mondiale
            ypop = y0 - (y0 - y1) * POP / 1e10
            f.line([(x0, ypop), (x1, ypop)], INK, ga * 0.5, 2, [10, 10])
            f.text('8,2 milliards d’humains', x0 + 12, ypop - 16, 30, INK, ga * 0.8, bold=False, align='left')
            pl = ease_io(seg(t, 38.8, 42.4)); pe = ease_io(seg(t, 40.0, 44.4))
            def curve(fn, p):
                pts = []
                for i in range(int(200 * p) + 1):
                    s = 10 * i / 200
                    pts.append((x0 + (x1 - x0) * s / 10, y0 - (y0 - y1) * min(1.05, fn(s) / 1e10)))
                return pts
            lin = curve(lambda s: 10 * s, pl)
            if len(lin) > 1: f.line(lin, MUTED, ga, 6)
            ex = curve(lambda s: 10 ** s, pe)
            if len(ex) > 1:
                f.line(ex, SPARK, ga, 7)
                f.circle(*ex[-1], 12, SPARK, ga)
            f.text('+10 : 100 personnes', x0 + 20, y0 - 30, 32, MUTED, ga * ease(seg(t, 42.2, 42.6)), MONO, True, 'left')
            words(f, 'Plat, plat, plat… puis tout explose.', 1440, 48, 44.6, INK, t_out=47.9)
            words(f, 'Chaque étape écrase toutes les autres.', 1520, 44, 45.6, SPARK, t_out=47.9, bold=False)

    # S7 — l'escalade : même avec 2 amis (48–56)
    if 48.0 <= t < 56.4:
        out = 1 - seg(t, 55.9, 56.3)
        words(f, 'Et avec seulement', 480, 66, 48.1, INK, t_out=55.9)
        words(f, '2 amis chacun ?', 570, 66, 48.5, INK, t_out=55.9)
        v = int(round(32 * ease(seg(t, 49.2, 50.6))))
        a = out * ease(seg(t, 49.1, 49.4))
        big_center(f, f'{v} étapes', 780, 170, SPARK, a, bump(t, 50.6, 0.14), DISPLAY)
        words(f, 'et toute la Terre est invitée.', 880, 52, 50.8, INK, t_out=55.9)
        words(f, 'C’est ainsi que se propagent', 1040, 50, 51.8, MUTED, t_out=55.9, bold=False)
        items = ['un virus', 'une rumeur', 'une vidéo virale']
        for i, s in enumerate(items):
            ia = ease(seg(t, 52.6 + i * 0.6, 52.9 + i * 0.6)) * out
            y = 1170 + i * 110
            f.rect(290, y - 62, 500, 88, OCEAN, ia, 44)
            f.text(s, W/2, y - 4, 46, INK, ia)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        words(f, 'Ton cerveau additionne.', 760, 72, 56.3, INK)
        words(f, 'Le monde multiplie.', 860, 72, 57.6, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(240, 1040, 600, 150, OCEAN, a, 28)
        # léger battement pour garder du mouvement
        pa = 0.5 + 0.5 * math.sin((t - 60) * 3)
        f.rect(240, 1040, 600, 150, SPARK, a * 0.25 * pa, 28)
        f.text('Abonne-toi.', W/2, 1135, 62, INK, a)

def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    for t0, n in ((0.15, 3), (0.9, 4), (2.0, 4), (2.6, 3)):
        for i in range(n): ev.append((t0 + i * 0.11, pop(420 + 40 * i, 0.09)))
    ev += [(x, whoosh(0.5, 0.18)) for x in (3.9, 10.6, 12.5, 29.6, 34.9, 47.9, 55.9)]
    ev += [(4.2, pop(330)), (5.9, pop(392)), (7.6, pop(440)), (9.0, ding(660, amp=0.2)), (10.9, pop(520)), (11.2, pop(620))]
    for k, tk in LT.items():
        ev.append((tk, pop(360 + k * 40, 0.1)))
        if k >= 3:
            for j in range(4): ev.append((tk + 0.05 + j * 0.06, tick()))
    ev += [(LT[10] + 0.02, ding(988, amp=0.32)), (LT[10] + 0.2, ding(1318, amp=0.32))]
    ev += [(30.0, ding(1046, amp=0.28)), (35.1, pop(300, 0.15)), (37.4, pop(392)), (38.0, ding(784, amp=0.2))]
    ev += [(40.0, rise(4.4, 200, 1046, 0.08)), (44.4, ding(880, amp=0.25))]
    ev += [(48.1, pop(440)), (49.2, rise(1.4, 300, 1046, 0.1)), (50.6, ding(1046, amp=0.25))]
    for i in range(3): ev.append((52.6 + i * 0.6, pop(500 + i * 60)))
    ev += [(56.3, pop(440)), (57.6, pop(550)), (60.0, ding(784, amp=0.22))]
    return ev
