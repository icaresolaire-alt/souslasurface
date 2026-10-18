"""DCA ou tout investir d'un coup ? Même structure que le pilote (ep001/ep002)."""
import math
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0

PRICES = [10, 8, 6, 5, 6, 8, 9, 8, 10, 11, 10, 12]          # série d'exemple (illustrative)
RISING = [10 + 0.5 * i for i in range(12)]                    # 10 -> 15,5 : marché qui monte
PARTS = [100 / p for p in PRICES]
CUM = [sum(PARTS[:i + 1]) for i in range(12)]                 # 149,4 parts au total

def fr(x, d=1): return f'{x:.{d}f}'.replace('.', ',')

X0, X1 = 150, 930
def mx(i): return X0 + i * (X1 - X0) / 11
def py(p): return 960 - (p - 4) / 8 * 260                     # 4 € -> 960, 12 € -> 700
def py2(p): return 1120 - (p - 4) / 12 * 420                  # 4 € -> 1120, 16 € -> 700

def curve(f, ys, p, col, a, width=6, dots=True):
    """Trace la courbe des prix jusqu'à la fraction p (0..1)."""
    if a <= 0 or p <= 0: return
    pts = [(mx(i), y) for i, y in enumerate(ys)]
    n = p * 11; k = int(n); pp = [pts[0]]
    for i in range(1, k + 1): pp.append(pts[i])
    if k < 11:
        u = n - k; pp.append((lerp(pts[k][0], pts[k+1][0], u), lerp(pts[k][1], pts[k+1][1], u)))
    f.line(pp, col, a, width)
    if dots:
        for i in range(k + 1): f.circle(*pts[i], 9, col, a)

def coin_stack(f, x, base, h, col, a):
    f.rect(x - 24, base - h, 48, h, col, a, 6)

def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')

    # question persistante
    ha = ease(seg(t, 12.4, 12.9)) * (1 - seg(t, 29.6, 30.0))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Lequel gagne ?', W/2, 296, 46, SPARK, ha)

    # S1 — accroche (0–4) : la courbe des prix se dessine dès la première image
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        curve(f, [py(p) + 420 for p in PRICES], ease_io(seg(t, 0.0, 3.6)), SPARK, fo * 0.9)
        words(f, '1 200 € à placer.', 560, 92, 0.15, INK, t_out=o)
        words(f, 'Tout d’un coup,', 720, 84, 1.1, INK, t_out=o)
        words(f, 'ou 100 € par mois ?', 830, 84, 1.8, SPARK, t_out=o)

    # S2 — enjeu (4–12)
    if 4.0 <= t < 12.6:
        ga = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, 12.0, 12.4))
        words(f, 'Même argent. Même marché.', 480, 64, 4.2, INK, t_out=12.0)
        # carte gauche : un seul bloc
        la = ease(seg(t, 5.0, 5.4)) * ga
        f.rect(110, 580, 400, 520, OCEAN, la, 28)
        f.text('D’un coup', 310, 650, 46, INK, la)
        hb = 300 * ease(seg(t, 5.4, 5.9))
        f.rect(190, 1040 - hb, 240, hb, SPARK, la, 10)
        f.text('1 200 €', 310, 1040 - hb / 2 + 14, 44, DEEP, la * seg(t, 5.7, 5.9), MONO)
        f.text('mois 1', 310, 1080, 30, MUTED, la, bold=False)
        # carte droite : 12 petits blocs
        ra = ease(seg(t, 6.0, 6.4)) * ga
        f.rect(570, 580, 400, 520, OCEAN, ra, 28)
        f.text('Petit à petit', 770, 650, 46, INK, ra)
        n = int(12 * ease_io(seg(t, 6.4, 8.6)) + 0.001)
        for i in range(n):
            f.rect(600 + i * 28.5, 1040 - 25, 22, 25, SPARK, ra, 4)
        f.text(f'{n} × 100 €', 770, 980, 40, SPARK, ra, MONO)
        f.text('12 mois', 770, 1080, 30, MUTED, ra, bold=False)
        words(f, 'Ton intuition : ça revient au même.', 1240, 50, 8.9, MUTED, t_out=12.0, bold=False)
        words(f, 'Pas du tout.', 1350, 70, 10.4, SPARK, t_out=12.0)

    # S3 — la question (12–14.5)
    if 12.2 <= t < 14.9:
        words(f, 'Lequel', 840, 130, 12.4, INK, t_out=14.4)
        words(f, 'gagne ?', 990, 130, 12.8, SPARK, t_out=14.4)

    # S4 — la preuve : 100 € par mois sur une série de prix (14.5–30)
    if 14.4 <= t < 30.2:
        ga = ease(seg(t, 14.5, 14.9)) * (1 - seg(t, 29.6, 30.0))
        T0, DT = 15.0, 0.9
        k = 0 if t < T0 else min(12, 1 + int((t - T0) / DT))
        f.text('parts achetées', W/2, 420, 40, MUTED, ga, bold=False)
        sc = bump(t, T0 + 3 * DT, 0.2) if k == 4 else bump(t, T0 + 11 * DT, 0.2)
        big_center(f, fr(CUM[k-1] if k else 0), 530, 100, SPARK, ga, sc)
        f.text('Prix de la part', W/2, 650, 34, MUTED, ga, bold=False)
        pp = clamp((t - T0) / (11 * DT)) if t >= T0 else 0
        curve(f, [py(p) for p in PRICES], pp, INK, ga, 5, dots=False)
        f.text('Parts achetées chaque mois avec 100 €', W/2, 1030, 34, MUTED, ga, bold=False)
        f.line([(X0 - 40, 1320), (X1 + 40, 1320)], LINE, ga, 3)
        for i in range(k):
            ti = T0 + i * DT
            ap = ease(seg(t, ti, ti + 0.25)) * ga
            low = PRICES[i] <= 6
            col = SPARK if low else CAPITAL
            f.circle(mx(i), py(PRICES[i]), 10, col if low else INK, ap)
            f.text(f'{PRICES[i]} €', mx(i), py(PRICES[i]) - 22, 26, MUTED, ap, MONO)
            coin_stack(f, mx(i), 1320, PARTS[i] * 12 * ease(seg(t, ti, ti + 0.35)), col, ap)
            f.text(fr(PARTS[i]), mx(i), 1320 - PARTS[i] * 12 - 14, 24, SPARK if low else INK, ap, MONO)
            if t - ti < 0.45:
                f.circle(mx(i), py(PRICES[i]), 14 + 40 * seg(t, ti, ti + 0.45), SPARK, (1 - seg(t, ti, ti + 0.45)) * ga, 4)
        # moyennes
        a1 = ease(seg(t, 25.6, 26.0)) * ga
        f.text('Prix moyen payé', 130, 1410, 44, INK, a1, DISPLAY, True, 'left')
        f.text('8,03 €', 950, 1410, 48, SPARK, a1, MONO, True, 'right')
        a2 = ease(seg(t, 26.8, 27.2)) * ga
        f.text('Moyenne du marché', 130, 1490, 44, MUTED, a2, DISPLAY, False, 'left')
        f.text('8,58 €', 950, 1490, 48, MUTED, a2, MONO, True, 'right')
        a3 = ease(seg(t, 28.0, 28.3)) * ga
        if a3 > 0:
            f.rect(110, 1355, 860, 80, SPARK, a3 * 0.12 * (0.6 + 0.4 * math.sin((t - 28) * 6)), 20)

    # S5 — la réponse (30–36)
    if 29.9 <= t < 36.4:
        a = ease(seg(t, 30.0, 30.3)) * (1 - seg(t, 35.8, 36.2))
        words(f, 'Au bout d’un an, la part vaut 12 €.', 600, 50, 30.0, MUTED, t_out=35.8, bold=False)
        v = 1792 * ease(seg(t, 30.4, 31.6))
        big_center(f, fmt_int(v) + ' €', 860, 170, SPARK, a, bump(t, 31.6, 0.12))
        words(f, 'avec 100 € par mois.', 980, 64, 31.8, INK, t_out=35.8)
        b = ease(seg(t, 32.8, 33.2)) * a
        f.text('contre 1 440 €', W/2, 1180, 72, MUTED, b, MONO)
        f.text('en investissant tout d’un coup.', W/2, 1260, 50, MUTED, b, bold=False)
        f.text('149 parts × 12 €  contre  120 parts × 12 €', W/2, 1400, 34, MUTED, ease(seg(t, 33.8, 34.2)) * a, MONO, False)

    # S6 — le retournement (35–48)
    if 35.0 <= t < 48.4:
        words(f, 'Le piège ?', 900, 150, 35.1, INK, t_out=37.1)
        ga = ease(seg(t, 37.3, 37.8)) * (1 - seg(t, 47.9, 48.3))
        if ga > 0:
            words(f, 'Ici, le prix a d’abord chuté.', 470, 58, 37.4, INK, t_out=47.9)
            words(f, 'Et si le marché monte ?', 560, 58, 39.0, SPARK, t_out=47.9)
            curve(f, [py2(p) for p in PRICES], 1.0, MUTED, ga * 0.5, 4, dots=False)
            curve(f, [py2(p) for p in RISING], ease_io(seg(t, 39.4, 42.0)), SPARK, ga, 6)
            f.text('10 €', mx(0) - 20, py2(10) + 48, 28, MUTED, ga * seg(t, 39.4, 39.8), MONO)
            f.text('15,5 €', mx(11), py2(15.5) - 26, 30, SPARK, ga * seg(t, 41.8, 42.2), MONO)
            r1 = ease(seg(t, 42.5, 42.9)) * ga
            f.text('100 € par mois', 130, 1260, 46, INK, r1, DISPLAY, False, 'left')
            f.text('1 486 €', 950, 1260, 52, MUTED, r1, MONO, True, 'right')
            r2 = ease(seg(t, 43.6, 44.0)) * ga
            f.text('Tout d’un coup', 130, 1350, 46, INK, r2, DISPLAY, True, 'left')
            c = f.c; c.save(); s = bump(t, 43.6, 0.2); c.translate(950, 1350); c.scale(s, s)
            f.text('1 860 €', 0, 0, 52, SPARK, r2, MONO, True, 'right'); c.restore()
            words(f, 'Attendre, ça coûte quand ça monte.', 1480, 50, 45.0, INK, t_out=47.9)

    # S7 — l'escalade : les vrais marchés (48–56)
    if 48.0 <= t < 56.4:
        out = 1 - seg(t, 55.9, 56.3)
        words(f, 'Sur les vrais marchés,', 470, 64, 48.1, INK, t_out=55.9)
        words(f, 'tout d’un coup gagne', 560, 64, 48.6, INK, t_out=55.9)
        words(f, 'environ 2 fois sur 3.', 650, 64, 49.1, SPARK, t_out=55.9)
        rows = [(50.0, 'États-Unis', 0.67), (50.9, 'Royaume-Uni', 0.67), (51.8, 'Australie', 0.66)]
        for i, (t0, lab, p) in enumerate(rows):
            a = ease(seg(t, t0, t0 + 0.3)) * out
            y = 840 + i * 190
            f.text(lab, 140, y, 52, INK, a, DISPLAY, True, 'left')
            f.text(f'{int(p*100 * ease(seg(t, t0 + 0.2, t0 + 1.2)))} %', 940, y, 52, SPARK, a, MONO, True, 'right')
            f.rect(140, y + 34, 800, 26, OCEAN, a, 13)
            f.rect(140, y + 34, 800 * p * ease(seg(t, t0 + 0.2, t0 + 1.2)), 26, SPARK, a, 13)
        sa = ease(seg(t, 53.0, 53.4)) * out
        f.text('Étude Vanguard (2012), périodes de 10 ans,', W/2, 1440, 32, MUTED, sa, bold=False)
        f.text('versements étalés sur 12 mois.', W/2, 1484, 32, MUTED, sa, bold=False)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        words(f, 'D’un coup : plus de gain en moyenne.', 750, 48, 56.3, INK)
        words(f, 'Petit à petit : moins de stress.', 840, 56, 57.6, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(240, 1010, 600, 150, OCEAN, a, 28)
        f.rect(300, 1130, 480 * ease_io(seg(t, 60.4, 65.5)), 5, SPARK, a * 0.8, 3)
        c = f.c; c.save(); s = 1 + 0.03 * math.sin((t - 60.0) * 3) if t > 60.4 else bump(t, 60.0, 0.12); c.translate(W/2, 1085); c.scale(s, s)
        f.text('Abonne-toi.', 0, 21, 62, INK, a); c.restore()
        f.text('Contenu éducatif, pas un conseil financier.', W/2, 1300, 32, MUTED, ease(seg(t, 60.8, 61.2)), bold=False)

def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    for t0, n in ((0.15, 4), (1.1, 3), (1.8, 5)):
        for i in range(n): ev.append((t0 + i * 0.11, pop(420 + 40 * i, 0.09)))
    ev += [(x, whoosh(0.5, 0.18)) for x in (3.9, 12.1, 14.4, 29.7, 34.9, 47.9, 55.9)]
    ev += [(4.2, pop(330)), (5.4, ding(660, amp=0.18)), (6.0, pop(392))]
    x = 6.4
    while x < 8.6: ev.append((x, clink(1500 + (x - 6.4) * 200))); x += 2.2 / 12
    ev += [(8.9, pop(330)), (10.4, ding(784, amp=0.2)), (12.4, pop(330)), (12.8, pop(440))]
    for i in range(12):
        ev.append((15.0 + i * 0.9, pop(700 - PRICES[i] * 30, 0.1)))
    ev += [(25.6, ding(880, amp=0.22)), (26.8, pop(330)), (30.4, rise(1.2, 300, 1046, 0.1)),
           (31.6, ding(1046, amp=0.3)), (32.8, pop(392)), (35.1, pop(300, 0.15))]
    x = 39.4
    while x < 42.0: ev.append((x, tick())); x += 0.12
    ev += [(42.5, pop(392)), (43.6, ding(1175, amp=0.28)), (45.0, pop(440))]
    for t0 in (50.0, 50.9, 51.8): ev += [(t0, pop(500)), (t0 + 1.2, clink(1900))]
    ev += [(56.3, pop(440)), (57.6, pop(550)), (60.0, ding(784, amp=0.22))]
    return ev
