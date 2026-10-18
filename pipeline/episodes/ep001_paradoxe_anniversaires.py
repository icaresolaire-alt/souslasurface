"""Pilote nouvelle structure : accroche choc, enjeu, preuve, retournement, chute + abonnement."""
import math, sys, numpy as np
from lib import *

TOTAL = 66.0

def P(n):
    q = 1.0
    for k in range(n): q *= (365 - k) / 365
    return 1 - q

for seed in range(1, 100000):
    rng = np.random.default_rng(seed)
    days = rng.integers(0, 365, 23)
    if len(set(days[:22])) == 22 and days[22] in set(days[:22]): break
MONTH_LEN = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
MONTH_LAB = 'JFMAMJJASOND'
MOIS = ['janvier','février','mars','avril','mai','juin','juillet','août','septembre','octobre','novembre','décembre']
def day_pos(d):
    m = 0
    while d >= MONTH_LEN[m]: d -= MONTH_LEN[m]; m += 1
    return m, d
CX0, CY0, CW, CH = 140, 760, 27.5, 36
def cell_xy(m, d): return CX0 + d * CW + CW/2, CY0 + m * CH + CH/2

T_ARR0, T_ARR = 13.6, 0.6            # arrivées des 23 élèves
T_HIT = T_ARR0 + 22 * T_ARR          # 26.8 : la coïncidence
rng2 = np.random.default_rng(5)
START = [(rng2.uniform(-200, W + 200), rng2.uniform(-300, -60) if i % 2 else rng2.uniform(H + 60, H + 300)) for i in range(23)]

from kinetic import words, bump, big_center

# ---------- scènes ----------
def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')

    # en-tête persistant : la question tant qu'on n'a pas la réponse
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 34.6, 35.0))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Même anniversaire ?', W/2, 296, 46, SPARK, ha)

    # S1 — accroche (0–4)
    if t < 4.3:
        o = 3.9
        for i in range(23):  # les élèves arrivent dès la première image
            p = ease(seg(t, 0.0 + i * 0.03, 1.4 + i * 0.03))
            tx = W/2 + (i % 8 - 3.5) * 92; ty = 1250 + (i // 8) * 92
            x = lerp(START[i][0], tx, p); y = lerp(START[i][1], ty, p)
            f.circle(x, y, 26, SPARK if i in (4, 17) and t > 3.0 else CAPITAL, 1 - seg(t, o, o + 0.3))
        words(f, 'Dans une classe', 620, 86, 0.15, INK, t_out=o)
        words(f, 'de 23 élèves,', 730, 86, 0.55, INK, t_out=o)
        words(f, 'deux ont sûrement', 880, 86, 1.25, INK, t_out=o)
        words(f, 'le même anniversaire.', 990, 86, 1.75, SPARK, t_out=o)

    # S2 — enjeu (4–10.7)
    if 4.0 <= t < 11.0:
        ga = ease(seg(t, 4.1, 4.6)) * (1 - seg(t, 10.4, 10.8))
        for m in range(12):
            for d in range(MONTH_LEN[m]):
                x, y = cell_xy(m, d)
                f.rect(x - CW/2 + 3, y - CH/2 + 4 + 260, CW - 6, CH - 8, LINE, ga * 0.7, 4)
        words(f, '365 jours.', 760, 130, 4.2, INK, t_out=5.7)
        words(f, '23 élèves.', 760, 130, 5.9, INK, t_out=7.4)
        words(f, 'Ça paraît rare…', 760, 96, 7.6, INK, t_out=8.9)
        a = ease(seg(t, 9.0, 9.3)) * (1 - seg(t, 10.4, 10.8))
        f.text('Ton intuition :', W/2, 700, 56, MUTED, a, bold=False)
        big_center(f, '≈ 6 %', 860, 150, INK, a, bump(t, 9.0))

    # S3 — on teste (10.7–13.3)
    if 10.7 <= t < 13.6:
        words(f, 'Faisons', 820, 120, 10.9, INK, t_out=12.4)
        words(f, 'le test.', 960, 120, 11.2, SPARK, t_out=12.4)

    # S4 — preuve : arrivées sur le calendrier (13.3–29.3)
    if 13.0 <= t < 29.8:
        ga = ease(seg(t, 13.0, 13.5)) * (1 - seg(t, 29.2, 29.7))
        n = 0 if t < T_ARR0 else min(23, 1 + int((t - T_ARR0) / T_ARR))
        p = P(n)
        col = INK if p < 0.25 else (SPARK if p < 0.5 else EARTH)
        f.text(f'{n} élève' + ('s' if n > 1 else ''), W/2, 470, 58, MUTED, ga, MONO)
        mil = {10: T_ARR0 + 9*T_ARR, 15: T_ARR0 + 14*T_ARR, 20: T_ARR0 + 19*T_ARR, 23: T_HIT}
        sc = max([bump(t, tm, 0.22) for tm in mil.values()])
        big_center(f, fmt_pct(p), 620, 120, col, ga, sc)
        for m in range(12):
            f.text(MONTH_LAB[m], CX0 - 28, CY0 + m * CH + CH/2, 26, MUTED, ga, MONO, False, 'center', 'middle')
            for d in range(MONTH_LEN[m]):
                x, y = cell_xy(m, d)
                f.rect(x - CW/2 + 3, y - CH/2 + 4, CW - 6, CH - 8, LINE, ga, 4)
        hit = days[22]
        for i in range(n):
            ti = T_ARR0 + i * T_ARR
            m, d = day_pos(days[i]); x, y = cell_xy(m, d)
            dup = days[i] == hit and n == 23
            ap = ease(seg(t, ti, ti + 0.2)) * ga
            f.rect(x - CW/2 + 3, y - CH/2 + 4, CW - 6, CH - 8, RED if dup else SPARK, ap, 4)
            if t - ti < 0.45:
                f.circle(x, y, 16 + 50 * seg(t, ti, ti + 0.45), SPARK, (1 - seg(t, ti, ti + 0.45)) * ga, 4)
        if n == 23:
            hc = ease(seg(t, T_HIT, T_HIT + 0.3)) * ga
            m, d = day_pos(hit); x, y = cell_xy(m, d)
            pul = 0.5 + 0.5 * math.sin((t - T_HIT) * 8)
            f.circle(x, y, 34 + 10 * pul, RED, hc, 6)
            sh = 8 * math.sin((t - T_HIT) * 60) * (1 - seg(t, T_HIT, T_HIT + 0.5))
            f.text(f'{d+1} {MOIS[m]} : deux fois !', W/2 + sh, CY0 + 12 * CH + 110, 64, RED, hc)

    # S5 — la réponse (29.3–35)
    if 29.3 <= t < 35.4:
        a = ease(seg(t, 29.4, 29.7)) * (1 - seg(t, 34.8, 35.2))
        v = 0.507 * ease(seg(t, 29.5, 30.9))
        big_center(f, fmt_pct(v), 900, 230, SPARK, a, bump(t, 30.9, 0.15))
        words(f, 'Plus d’une chance sur deux.', 1100, 66, 31.3, INK, t_out=34.8)
        words(f, 'Avec seulement 23 personnes.', 1200, 52, 32.4, MUTED, t_out=34.8, bold=False)

    # S6 — le retournement : les paires (35–48)
    if 35.0 <= t < 48.4:
        words(f, 'Pourquoi ?', 900, 150, 35.1, INK, t_out=37.1)
        ga = ease(seg(t, 37.3, 37.8)) * (1 - seg(t, 47.9, 48.3))
        if ga > 0:
            cx, cy, R = W/2, 1000, 330
            pts = [(cx + R * math.cos(-math.pi/2 + 2*math.pi*i/23), cy + R * math.sin(-math.pi/2 + 2*math.pi*i/23)) for i in range(23)]
            pairs = [(i, j) for i in range(23) for j in range(i + 1, 23)]
            k = int(253 * ease_io(seg(t, 38.0, 44.5)))
            for (i, j) in pairs[:k]:
                f.line([pts[i], pts[j]], SPARK, ga * 0.22, 2)
            for (x, y) in pts: f.circle(x, y, 18, INK, ga)
            f.text('duels possibles', W/2, 470, 46, MUTED, ga, bold=False)
            big_center(f, str(k), 610, 130, SPARK, ga, bump(t, 44.5, 0.2))
            words(f, 'Chaque duel est une chance', 1440, 50, 45.0, INK, t_out=47.9)
            words(f, 'de tomber sur le même jour.', 1510, 50, 45.4, INK, t_out=47.9)

    # S7 — escalade (48–56)
    if 48.0 <= t < 56.4:
        out = 1 - seg(t, 55.9, 56.3)
        rows = [(48.3, 40, 0.891, '89 %'), (50.3, 57, 0.990, '99 %'), (52.3, 70, 0.9992, '99,9 %')]
        words(f, 'Et ça grimpe vite.', 480, 70, 48.1, INK, t_out=55.9)
        for i, (t0, n, p, lab) in enumerate(rows):
            a = ease(seg(t, t0, t0 + 0.3)) * out
            y = 680 + i * 250
            f.text(f'{n} élèves', 140, y, 56, INK, a, DISPLAY, True, 'left')
            f.text(lab, 940, y, 56, SPARK, a, MONO, True, 'right')
            f.rect(140, y + 40, 800, 26, OCEAN, a, 13)
            f.rect(140, y + 40, 800 * p * ease(seg(t, t0 + 0.2, t0 + 1.2)), 26, EARTH if p > 0.95 else SPARK, a, 13)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        words(f, 'Ton cerveau compte les gens.', 760, 64, 56.3, INK)
        words(f, 'Le hasard compte les paires.', 860, 64, 57.6, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(140, 1040, 800, 210, OCEAN, a, 28)
        f.text('Abonne-toi.', W/2, 1120, 58, INK, a)
        f.text('Demain : pourquoi le casino gagne toujours.', W/2, 1196, 38, MUTED, a, bold=False)

# événements sonores (temps en secondes)
def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    for t0, n in ((0.15, 3), (0.55, 3), (1.25, 3), (1.75, 3)):
        for i in range(n): ev.append((t0 + i * 0.11, pop(420 + 40 * i, 0.09)))
    ev += [(x, whoosh(0.5, 0.18)) for x in (3.9, 10.6, 12.5, 29.2, 34.9, 47.9, 55.9)]
    ev += [(4.2, pop(330)), (5.9, pop(392)), (7.6, pop(440)), (9.0, ding(660, amp=0.2)), (10.9, pop(520)), (11.2, pop(620))]
    for i in range(23): ev.append((T_ARR0 + i * T_ARR, pop(380 + i * 16, 0.1)))
    ev += [(T_HIT + 0.02, ding(988, amp=0.32)), (T_HIT + 0.2, ding(1318, amp=0.32))]
    ev += [(29.5, rise(1.4, 300, 1046, 0.1)), (30.9, ding(1046, amp=0.28)), (35.1, pop(300, 0.15))]
    x = 38.0
    while x < 44.5: ev.append((x, tick())); x += 0.12
    ev += [(44.5, ding(880, amp=0.25))]
    for t0 in (48.3, 50.3, 52.3): ev += [(t0, pop(500)), (t0 + 1.2, clink(1900))]
    ev += [(56.3, pop(440)), (57.6, pop(550)), (60.0, ding(784, amp=0.22))]
    return ev

