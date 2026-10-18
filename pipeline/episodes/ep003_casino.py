"""Pourquoi le casino gagne toujours : roulette européenne, avantage 1/37, loi des grands nombres. Même structure que le pilote."""
import math, numpy as np
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0

# roulette européenne : ordre réel des cases sur le cylindre, cases rouges
WHEEL = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14,
         31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
REDS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
BLACK = '#2b3742'
def ccol(n): return EARTH if n == 0 else (RED if n in REDS else BLACK)

# simulation : un joueur mise 10 € sur rouge 1 000 fois (graine choisie pour une trajectoire lisible)
_r = np.random.default_rng(54)
PLAYER = np.concatenate([[0], np.cumsum(np.where(_r.random(1000) < 18/37, 10, -10))])
# le casino : 1 million de mises de 10 € sur rouge
_r2 = np.random.default_rng(7)
_g = np.cumsum(np.where(_r2.random(10**6) < 18/37, -10, 10))
CASINO = np.concatenate([[0], _g[999::1000]])       # 1 000 points
CASINO_END = int(_g[-1])                            # 272 880 € (attendu : 270 270 €)

# chances de finir gagnant après n mises de 10 € sur rouge (calcul exact, binomiale)
def p_ahead(n):
    p, q = 18/37, 19/37
    return sum(math.exp(math.lgamma(n+1) - math.lgamma(k+1) - math.lgamma(n-k+1) + k*math.log(p) + (n-k)*math.log(q))
               for k in range(n//2 + 1, n + 1))

def wheel(f, cx, cy, R, rot, a, ball=None):
    if a <= 0: return
    c = f.c; n = 37; da = 2 * math.pi / n
    f.circle(cx, cy, R + 26, CAPITAL, a)
    f.circle(cx, cy, R + 10, DEEP, a)
    for i, num in enumerate(WHEEL):
        a0 = rot + i * da - da/2
        f.color(ccol(num), a); c.move_to(cx, cy); c.arc(cx, cy, R, a0, a0 + da); c.close_path(); c.fill()
    for i, num in enumerate(WHEEL):
        ang = rot + i * da; rr = R - 34
        c.save(); c.translate(cx + rr * math.cos(ang), cy + rr * math.sin(ang)); c.rotate(ang + math.pi/2)
        f.text(str(num), 0, 8, 22, INK, a, MONO); c.restore()
    f.circle(cx, cy, R * 0.62, OCEAN, a)
    f.circle(cx, cy, R * 0.62, SPARK, a * 0.6, 4)
    for k in range(4):
        ang = rot * 1.0 + k * math.pi / 2
        f.line([(cx, cy), (cx + R * 0.5 * math.cos(ang), cy + R * 0.5 * math.sin(ang))], SPARK, a, 8)
    f.circle(cx, cy, 30, SPARK, a)
    if ball is not None:
        br = R + 2 - 22
        f.circle(cx + br * math.cos(ball), cy + br * math.sin(ball), 13, INK, a)

# tapis : zéro à gauche, 12 colonnes de 3
TX0, TCW, TCH = 85, 70, 84
def table_cells(y0):
    cells = [(0, TX0, y0, TCW, 3 * TCH)]
    for col in range(12):
        for row in range(3):
            cells.append((3 * col + 3 - row, TX0 + TCW + col * TCW, y0 + row * TCH, TCW, TCH))
    return cells

def table(f, y0, a, lit=lambda n: 1.0):
    if a <= 0: return
    for num, x, y, w, h in table_cells(y0):
        l = lit(num)
        f.rect(x + 3, y + 3, w - 6, h - 6, ccol(num) if num else EARTH, a * (0.25 + 0.75 * l), 6)
        f.text(str(num), x + w/2, y + h/2 + 11, 30, INK, a * (0.35 + 0.65 * l), MONO)

def chart_box(f, a):
    f.rect(100, 690, 880, 580, OCEAN, a * 0.55, 20)

def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.6, 30.0))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Combien garde le casino ?', W/2, 296, 46, SPARK, ha)

    # S1 — accroche (0–4) : la roulette tourne dès la première image
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        rot = -0.4 + 2.2 * t; ball = 1.0 - 4.5 * t
        wheel(f, W/2, 1090, 290, rot, fo * ease(seg(t, 0, 0.3)), ball)
        words(f, 'Le casino ne triche pas.', 400, 78, 0.15, INK, t_out=o)
        words(f, 'Et pourtant,', 520, 78, 1.2, INK, t_out=o)
        words(f, 'il gagne toujours.', 630, 88, 1.7, SPARK, t_out=o)

    # S2 — l'intuition : une chance sur deux ? (4–12)
    if 4.0 <= t < 12.6:
        a1 = ease(seg(t, 4.1, 4.4)) * (1 - seg(t, 6.8, 7.1))
        if a1 > 0:
            wheel(f, W/2, 1130, 250, 8.4 + 1.2 * (t - 4), a1, 7.0 - 2.4 * (t - 4))
        words(f, 'Rouge ou noir :', 470, 80, 4.2, INK, t_out=6.8)
        words(f, 'une chance sur deux ?', 580, 80, 4.7, INK, t_out=6.8)
        f.text('Ton intuition : 50 %', W/2, 720, 52, MUTED, ease(seg(t, 5.6, 5.9)) * a1, bold=False)
        ga = ease(seg(t, 7.0, 7.4)) * (1 - seg(t, 12.0, 12.4))
        if ga > 0:
            def lit(n):
                if t < 7.6: return 0.0
                if n in REDS: return ease(seg(t, 7.6, 8.0))
                if n == 0: return ease(seg(t, 9.4, 9.8))
                return ease(seg(t, 8.5, 8.9))
            table(f, 560, ga, lit)
            if t >= 9.4:
                pu = 0.5 + 0.5 * math.sin((t - 9.4) * 7)
                f.rect(TX0 - 4, 556, TCW + 8, 3 * TCH + 8, SPARK, ga * (0.4 + 0.6 * pu), 10)
                f.rect(TX0 + 3, 563, TCW - 6, 3 * TCH - 6, EARTH, ga, 6)
                f.text('0', TX0 + TCW/2, 560 + 1.5 * TCH + 11, 30, INK, ga, MONO)
            words(f, '18 rouges,', 990, 72, 7.6, RED, t_out=12.0)
            words(f, '18 noirs,', 1080, 72, 8.5, INK, t_out=12.0)
            words(f, 'et le zéro, vert.', 1170, 72, 9.4, EARTH, t_out=12.0)
            words(f, 'Sur rouge, tu gagnes', 1320, 56, 10.4, MUTED, t_out=12.0, bold=False)
            words(f, '18 fois sur 37.', 1400, 64, 10.9, SPARK, t_out=12.0)

    # S3 — la question (12–14.5)
    if 12.2 <= t < 14.9:
        words(f, 'Combien garde', 840, 112, 12.4, INK, t_out=14.4)
        words(f, 'le casino ?', 980, 112, 12.8, SPARK, t_out=14.4)

    # S4 — la preuve : simulation (14.5–30)
    if 14.4 <= t < 30.2:
        ga = ease(seg(t, 14.5, 14.9)) * (1 - seg(t, 29.6, 30.0))
        X0, X1 = 130, 950
        # phase 1 : un joueur, 1 000 mises
        pa = ga * (1 - seg(t, 22.0, 22.4))
        if pa > 0:
            chart_box(f, pa)
            Y0, K = 980, 0.78                      # ligne du zéro, px par euro
            f.line([(X0, Y0), (X1, Y0)], MUTED, pa * 0.6, 2, [10, 8])
            f.text('0 €', X0 + 4, Y0 - 12, 26, MUTED, pa, MONO, False, 'left')
            n = int(1000 * seg(t, 15.0, 21.4))
            pts = [(X0 + i / 1000 * (X1 - X0), Y0 - PLAYER[i] * K) for i in range(n + 1)]
            if len(pts) > 1: f.line(pts, INK, pa, 3)
            v = int(PLAYER[n]); x, y = pts[-1]
            f.circle(x, y, 11, EARTH if v > 0 else (RED if v < 0 else INK), pa)
            f.text('Toi : 10 € sur rouge, 1 000 fois', W/2, 470, 44, MUTED, pa, bold=False)
            s = ('+' if v > 0 else ('−' if v < 0 else '')) + fmt_int(abs(v)) + ' €'
            big_center(f, s, 600, 110, EARTH if v > 0 else (RED if v < 0 else INK), pa)
            f.text(f'simulation · mise n° {fmt_int(n)}', W/2, 1340, 40, MUTED, pa, MONO, False)
            words(f, 'Ça monte… puis ça redescend.', 1440, 50, 17.6, INK, t_out=22.0)
        # phase 2 : le casino, 1 million de mises
        ca = ease(seg(t, 22.3, 22.7)) * ga
        if ca > 0:
            chart_box(f, ca)
            Y0, K = 1230, 500 / 300000
            f.line([(X0, Y0), (X1, Y0)], MUTED, ca * 0.6, 2, [10, 8])
            k = int(1000 * ease_io(seg(t, 23.0, 27.4)))
            pts = [(X0 + i / 1000 * (X1 - X0), Y0 - CASINO[i] * K) for i in range(k + 1)]
            if len(pts) > 1: f.line(pts, SPARK, ca, 5)
            x, y = pts[-1]
            f.circle(x, y, 12 + 4 * math.sin(t * 8), SPARK, ca)
            f.text('Le casino : 1 million de mises de 10 €', W/2, 470, 42, MUTED, ca, bold=False)
            v = CASINO_END if k >= 1000 else int(CASINO[k])
            big_center(f, '+' + fmt_int(v) + ' €', 600, 100, SPARK, ca, bump(t, 27.4, 0.15))
            f.text(f'simulation · {fmt_int(k * 1000)} mises', W/2, 1340, 40, MUTED, ca, MONO, False)
            words(f, 'Une ligne presque droite.', 1440, 54, 26.0, INK, t_out=29.6)

    # S5 — la réponse (30–35.4)
    if 29.9 <= t < 35.4:
        a = ease(seg(t, 30.0, 30.3)) * (1 - seg(t, 34.8, 35.2))
        v = 2.7 * ease(seg(t, 30.0, 31.0))
        big_center(f, f'{v:.1f} %'.replace('.', ','), 880, 260, SPARK, a, bump(t, 31.0, 0.15), DISPLAY)
        words(f, 'C’est ce que le casino garde,', 1070, 60, 31.3, INK, t_out=34.8)
        words(f, 'en moyenne, sur chaque mise.', 1150, 60, 31.8, INK, t_out=34.8)
        f.text('Roulette européenne : 37 cases, un seul zéro.', W/2, 1320, 36, MUTED, ease(seg(t, 32.6, 33.0)) * a, bold=False)
        f.text('Avec la règle du « partage » sur le zéro : 1,35 %.', W/2, 1380, 30, MUTED, ease(seg(t, 33.2, 33.6)) * a, bold=False)

    # S6 — le retournement : le zéro (35–48)
    if 35.0 <= t < 48.4:
        words(f, 'Pourquoi ?', 900, 150, 35.1, INK, t_out=37.1)
        ga = ease(seg(t, 37.3, 37.8)) * (1 - seg(t, 47.9, 48.3))
        if ga > 0:
            f.text('Tu mises 10 € sur rouge, 37 fois.', W/2, 470, 46, MUTED, ga, bold=False)
            win = ease(seg(t, 38.2, 38.6)); lose = ease(seg(t, 39.6, 40.0))
            def lit(n):
                return win if n in REDS else lose
            table(f, 560, ga, lit)
            # +10 / −10 qui jaillissent des cases
            for num, x, y, w, h in table_cells(560):
                t0 = 38.2 if num in REDS else 39.6
                p = seg(t, t0 + (num % 7) * 0.05, t0 + 0.9 + (num % 7) * 0.05)
                if 0 < p < 1:
                    f.text('+10' if num in REDS else '−10', x + w/2, y + 20 - 70 * p, 26, EARTH if num in REDS else RED, ga * (1 - p), MONO)
            words(f, '18 cases : tu gagnes 10 €.', 980, 58, 38.4, EARTH, t_out=47.9)
            words(f, '19 cases : tu perds 10 €.', 1070, 58, 39.8, RED, t_out=47.9)
            ra = ease(seg(t, 41.4, 41.8)) * ga
            big_center(f, '180 − 190 = −10 €', 1230, 72, INK, ra, bump(t, 41.4))
            words(f, 'tous les 37 coups, en moyenne.', 1310, 50, 42.2, MUTED, t_out=47.9, bold=False)
            words(f, 'Le zéro,', 1440, 64, 44.0, INK, t_out=47.9)
            words(f, 'c’est la marge du casino.', 1520, 64, 44.5, SPARK, t_out=47.9)

    # S7 — l'escalade : plus tu joues, plus c'est sûr (48–56)
    if 48.0 <= t < 56.4:
        out = 1 - seg(t, 55.9, 56.3)
        words(f, 'Plus tu joues,', 460, 70, 48.1, INK, t_out=55.9)
        words(f, 'moins tu as de chances.', 550, 70, 48.5, SPARK, t_out=55.9)
        f.text('Chance de finir gagnant, mises de 10 € sur rouge', W/2, 650, 34, MUTED, ease(seg(t, 48.9, 49.2)) * out, bold=False)
        rows = [(49.4, '100 mises', p_ahead(100), '36 %'), (51.2, '1 000 mises', p_ahead(1000), '19 %'), (53.0, '10 000 mises', p_ahead(10000), '0,3 %')]
        for i, (t0, lab, p, txt) in enumerate(rows):
            a = ease(seg(t, t0, t0 + 0.3)) * out
            y = 820 + i * 230
            f.text(lab, 140, y, 56, INK, a, DISPLAY, True, 'left')
            f.text(txt, 940, y, 56, SPARK if p > 0.1 else RED, a, MONO, True, 'right')
            f.rect(140, y + 40, 800, 26, OCEAN, a, 13)
            f.rect(140, y + 40, max(26, 800 * p * ease(seg(t, t0 + 0.2, t0 + 1.2))), 26, SPARK if p > 0.1 else RED, a, 13)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        words(f, 'Sur un coup, c’est la chance.', 760, 64, 56.3, INK)
        words(f, 'Sur un million, c’est le calcul.', 860, 64, 57.6, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(140, 1030, 800, 170, OCEAN, a, 28)
        f.text('Abonne-toi.', W/2, 1135, 64, INK, a)
        f.text('Contenu éducatif, pas un conseil financier.', W/2, 1290, 32, MUTED, ease(seg(t, 60.6, 61.0)), bold=False)

def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    for t0, n in ((0.15, 5), (1.2, 2), (1.7, 3)):
        for i in range(n): ev.append((t0 + i * 0.11, pop(420 + 40 * i, 0.09)))
    x = 0.0
    while x < 3.8: ev.append((x, tick())); x += 0.07 + 0.03 * x   # la bille qui ralentit
    ev += [(x, whoosh(0.5, 0.18)) for x in (3.9, 6.8, 12.1, 14.4, 22.0, 29.7, 34.9, 47.9, 55.9)]
    ev += [(4.2, pop(330)), (4.7, pop(392)), (5.6, ding(660, amp=0.2)), (7.6, clink(1500)), (8.5, clink(1200)), (9.4, ding(988, amp=0.25)),
           (10.9, pop(523)), (12.4, pop(330)), (12.8, pop(440))]
    x = 15.0
    while x < 21.4: ev.append((x, tick())); x += 0.08
    ev += [(17.6, pop(392))]
    x = 23.0
    while x < 27.4: ev.append((x, clink(900 + (x - 23) * 150))); x += 0.22
    ev += [(27.4, ding(880, amp=0.25)), (26.0, pop(440)),
           (30.0, rise(1.0, 300, 1046, 0.1)), (31.0, ding(1046, amp=0.3)), (35.1, pop(300, 0.15))]
    for i in range(18): ev.append((38.2 + (i % 7) * 0.05, pop(600 + i * 10, 0.06)))
    ev += [(39.6, pop(260, 0.15)), (41.4, ding(660, amp=0.22)), (44.0, pop(440)), (44.5, pop(550))]
    for t0 in (49.4, 51.2, 53.0): ev += [(t0, pop(500)), (t0 + 1.2, clink(1900))]
    ev += [(48.1, pop(392)), (56.3, pop(440)), (57.6, pop(550)), (60.0, ding(784, amp=0.22))]
    return ev
