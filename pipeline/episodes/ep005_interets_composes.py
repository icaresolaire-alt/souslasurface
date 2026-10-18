"""Intérêts composés : 10 000 € à 7 % pendant 40 ans. Même structure que le pilote."""
import math
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
P0, R = 10000, 0.07
def val(y): return P0 * (1 + R) ** y              # capital composé
def simple(y): return P0 * R * y                   # intérêts simples cumulés
FINAL = val(40)                                    # 149 744,58 €

# graphique année par année
BX0, BX1, BASE, BH = 110, 970, 1320, 600
BW = (BX1 - BX0) / 40
T_Y0, T_DY = 15.0, 0.3                             # année n apparaît à T_Y0 + (n-1)*T_DY  -> 40e à 26,7 s

def coin(f, x, y, r, a):
    f.circle(x, y, r, SPARK, a)
    f.circle(x, y, r * 0.68, DEEP, a * 0.35, 3)

def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')

    # question persistante
    ha = ease(seg(t, 12.4, 12.9)) * (1 - seg(t, 29.6, 30.0))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('D’où vient l’écart ?', W/2, 296, 46, SPARK, ha)

    # S1 — accroche (0–4) : une colonne qui monte dès la première image
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        p = ease_io(seg(t, 0.0, 3.5))
        v = lerp(P0, FINAL, p ** 2.2)
        h = 520 * v / FINAL
        f.rect(390, 1480 - h, 300, h, SPARK, fo, 10)
        f.rect(390, 1480 - 520 * P0 / FINAL, 300, 520 * P0 / FINAL, CAPITAL, fo, 10)
        big_center(f, fmt_int(v) + ' €', 1480 - h - 40, 84, SPARK, fo, bump(t, 3.5, 0.15))
        words(f, 'Tu places 10 000 €.', 400, 82, 0.15, INK, t_out=o)
        words(f, 'Tu n’y touches plus.', 510, 66, 0.75, MUTED, t_out=o, bold=False)
        words(f, '40 ans plus tard :', 640, 70, 1.6, INK, t_out=o)
        words(f, 'presque 150 000 €.', 740, 80, 2.3, SPARK, t_out=o)

    # S2 — l'intuition (4–12) : 700 € par an, 40 fois
    if 4.0 <= t < 12.6:
        out = 1 - seg(t, 12.0, 12.4)
        words(f, '7 % de 10 000 €,', 520, 72, 4.2, INK, t_out=12.0)
        words(f, 'c’est 700 € par an.', 620, 72, 4.8, SPARK, t_out=12.0)
        n = int(40 * ease_io(seg(t, 5.6, 9.2)))
        for i in range(n):
            r, cidx = divmod(i, 10)
            ap = ease(seg(t, 5.6 + i * 0.09, 5.8 + i * 0.09)) * out
            coin(f, 180 + cidx * 80, 760 + r * 80 + 30 * (1 - ap), 30, ap)
        ca = ease(seg(t, 5.6, 5.9)) * out
        f.text(f'{n} an' + ('s' if n > 1 else ''), 140, 1150, 44, MUTED, ca, MONO, False, 'left')
        f.text('+ ' + fmt_int(700 * n) + ' €', 940, 1150, 60, INK, ca, MONO, True, 'right')
        ia = ease(seg(t, 9.6, 9.9)) * out
        f.text('Ton intuition :', W/2, 1290, 52, MUTED, ia, bold=False)
        big_center(f, '38 000 €', 1420, 110, INK, ia, bump(t, 9.6))
        f.text('10 000 € + 40 × 700 €', W/2, 1500, 38, MUTED, ia, MONO, False)

    # S3 — la question (12–14.5)
    if 12.2 <= t < 14.9:
        words(f, 'Alors d’où sortent', 820, 96, 12.4, INK, t_out=14.4)
        words(f, 'les 111 745 € de plus ?', 960, 84, 12.9, SPARK, t_out=14.4)

    # S4 — la preuve : 40 barres, 3 couches (14.5–30)
    if 14.4 <= t < 30.2:
        ga = ease(seg(t, 14.5, 14.9)) * (1 - seg(t, 29.6, 30.0))
        n = 0 if t < T_Y0 else min(40, 1 + int((t - T_Y0) / T_DY))
        f.text(f'Année {n}', W/2, 450, 54, MUTED, ga, MONO)
        big_center(f, fmt_int(val(n)) + ' €', 570, 104, SPARK, ga, bump(t, T_Y0 + 39 * T_DY, 0.18))
        f.line([(BX0, BASE), (BX1, BASE)], LINE, ga, 3)
        k = BH / FINAL
        for y in range(1, n + 1):
            gp = ease(seg(t, T_Y0 + (y - 1) * T_DY, T_Y0 + (y - 1) * T_DY + 0.25))
            x = BX0 + (y - 1) * BW + 2
            hc, hs, hv = P0 * k, simple(y) * k, (val(y) - P0 - simple(y)) * k
            yy = BASE
            for hh, col in ((hc, CAPITAL), (hs, EARTH), (hv, SPARK)):
                hh *= gp
                f.rect(x, yy - hh, BW - 4, hh, col, ga); yy -= hh
        for i, (col, lab) in enumerate(((CAPITAL, 'tes 10 000 € de départ'), (EARTH, 'intérêts simples : 700 € par an'),
                                         (SPARK, 'intérêts sur tes intérêts'))):
            la = ease(seg(t, 15.2 + i * 0.5, 15.5 + i * 0.5)) * ga
            f.rect(140, 1380 + i * 56, 34, 34, col, la, 6)
            f.text(lab, 196, 1408 + i * 56, 38, INK if i < 2 else SPARK, la, DISPLAY, i == 2, 'left')
        # lecture du doré, dans le vide en haut à gauche du graphique
        ea = ease(seg(t, 27.2, 27.6)) * ga
        f.text('Le doré grossit tout seul :', 140, 760, 46, INK, ea, DISPLAY, True, 'left')
        f.text('tes intérêts rapportent', 140, 822, 46, INK, ea, DISPLAY, False, 'left')
        f.text('à leur tour des intérêts.', 140, 884, 46, SPARK, ea, DISPLAY, True, 'left')

    # S5 — la réponse (30–36)
    if 29.9 <= t < 36.4:
        a = ease(seg(t, 30.0, 30.3)) * (1 - seg(t, 35.8, 36.2))
        v = lerp(38000, FINAL, ease(seg(t, 30.0, 31.2)))
        big_center(f, fmt_int(v) + ' €', 860, 150, SPARK, a, bump(t, 31.2, 0.12))
        words(f, 'au lieu de 38 000 €.', 990, 66, 31.4, INK, t_out=35.8)
        words(f, 'Presque 4 fois plus.', 1090, 58, 32.2, MUTED, t_out=35.8, bold=False)
        na = ease(seg(t, 32.9, 33.3)) * a
        f.text('Hypothèse : 7 % par an, chaque année,', W/2, 1340, 32, MUTED, na, bold=False)
        f.text('sans frais ni impôts. Rendement non garanti.', W/2, 1386, 32, MUTED, na, bold=False)

    # S6 — le retournement : le temps (36–48)
    if 36.0 <= t < 48.4:
        words(f, 'Le secret ?', 760, 120, 36.1, INK, t_out=38.1)
        words(f, 'Le temps.', 900, 120, 36.7, SPARK, t_out=38.1)
        ga = ease(seg(t, 38.3, 38.8)) * (1 - seg(t, 47.9, 48.3))
        if ga > 0:
            f.text('La règle de 72', W/2, 450, 46, MUTED, ga, bold=False)
            big_center(f, '72 ÷ 7 ≈ 10 ans', 560, 88, SPARK, ga, bump(t, 38.5, 0.12))
            f.text('pour doubler ton argent.', W/2, 640, 46, INK, ga, bold=False)
            steps = [0, 10, 20, 30, 40]
            k = 560 / FINAL
            for i, y in enumerate(steps):
                t0 = 39.2 + i * 1.1
                ap = ease(seg(t, t0, t0 + 0.4)) * ga
                if ap <= 0: continue
                x = 180 + i * 180
                h = val(y) * k * ease(seg(t, t0, t0 + 0.5))
                hl = i >= 3 and t > 44.8
                col = SPARK if (i == 4 or not hl) else EARTH
                if hl and i == 3: col = EARTH
                f.rect(x - 60, BASE - h, 120, h, col, ap, 8)
                f.text(fmt_int(val(y)), x, BASE - h - 18, 32, INK, ap, MONO)
                f.text(f'{y} ans' if y else 'départ', x, BASE + 46, 30, MUTED, ap, DISPLAY, False)
                if i > 0:
                    f.text('×2', x - 90, BASE - 30, 30, MUTED, ap, MONO)
            words(f, 'Commence 10 ans plus tard :', 1440, 52, 45.0, INK, t_out=47.9)
            words(f, '76 123 €. Deux fois moins.', 1520, 52, 45.8, EARTH, t_out=47.9)

    # S7 — l'escalade (48–56)
    if 48.0 <= t < 56.4:
        out = 1 - seg(t, 55.9, 56.3)
        words(f, 'Le plus fou ?', 480, 76, 48.1, INK, t_out=55.9)
        rows = [(48.9, '30 premières années', val(30) - P0, CAPITAL), (50.6, '10 dernières années', FINAL - val(30), SPARK)]
        for i, (t0, lab, v, col) in enumerate(rows):
            a = ease(seg(t, t0, t0 + 0.3)) * out
            y = 680 + i * 260
            g = ease(seg(t, t0 + 0.2, t0 + 1.4))
            f.text(lab, 140, y, 52, INK, a, DISPLAY, True, 'left')
            f.text('+ ' + fmt_int(v * g) + ' €', 940, y + 110, 52, col if i else INK, a, MONO, True, 'right')
            f.rect(140, y + 30, 800, 30, OCEAN, a, 15)
            f.rect(140, y + 30, 800 * v / (FINAL - val(30)) * g, 30, col, a, 15)
        words(f, 'Les 10 dernières années', 1260, 58, 52.6, INK, t_out=55.9)
        words(f, 'rapportent plus que les 30 premières.', 1340, 50, 53.2, SPARK, t_out=55.9)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        words(f, 'Tes intérêts font des petits.', 740, 68, 56.3)
        words(f, 'Laisse-leur le temps.', 850, 76, 57.4, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        s = bump(t, 60.0, 0.12) * (1 + 0.025 * math.sin(max(0, t - 60.4) * 3.2))   # léger battement : rien de figé
        c = f.c; c.save(); c.translate(W/2, 1105); c.scale(s, s); c.translate(-W/2, -1105)
        f.rect(240, 1030, 600, 150, OCEAN, a, 28)
        f.text('Abonne-toi.', W/2, 1126, 62, INK, a)
        c.restore()
        da = ease(seg(t, 60.8, 61.2))
        f.text('Contenu éducatif, pas un conseil financier.', W/2, 1300, 32, MUTED, da, bold=False)
        f.text('Rendement non garanti.', W/2, 1346, 32, MUTED, da, bold=False)

def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    for t0, n in ((0.15, 4), (0.75, 4), (1.6, 4), (2.3, 3)):
        for i in range(n): ev.append((t0 + i * 0.11, pop(420 + 40 * i, 0.09)))
    ev += [(3.5, ding(880, amp=0.22))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (3.9, 12.1, 14.4, 29.7, 35.9, 47.9, 55.9)]
    ev += [(4.2, pop(330)), (4.8, pop(440))]
    for i in range(40): ev.append((5.6 + i * 0.09, clink(1500 + i * 12)))
    ev += [(9.6, ding(660, amp=0.2)), (12.4, pop(330)), (12.9, pop(440))]
    for i in range(40): ev.append((T_Y0 + i * T_DY, pop(360 + i * 14, 0.08)))
    ev += [(T_Y0 + 39 * T_DY, ding(988, amp=0.3)), (27.2, pop(520))]
    ev += [(30.0, rise(1.2, 300, 1046, 0.1)), (31.2, ding(1046, amp=0.3)), (36.1, pop(300, 0.15)), (36.7, pop(450, 0.15))]
    ev += [(38.5, pop(500))]
    for i in range(5): ev.append((39.2 + i * 1.1, clink(1200 + i * 200)))
    ev += [(45.0, pop(392)), (45.8, ding(784, amp=0.2))]
    ev += [(48.1, pop(440)), (48.9, pop(500)), (50.6, pop(600)), (52.0, ding(1046, amp=0.25))]
    ev += [(52.6, pop(440)), (53.2, pop(550))]
    ev += [(56.3, pop(440)), (57.4, pop(550)), (60.0, ding(784, amp=0.22))]
    return ev
