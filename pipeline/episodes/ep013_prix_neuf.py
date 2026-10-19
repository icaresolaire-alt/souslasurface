"""Pourquoi 9,99 € te paraît bien moins cher que 10 € : l'effet du chiffre de gauche. Même structure que le pilote.

Sources :
- Thomas et Morwitz (2005), Journal of Consumer Research 32(1) : l'effet n'apparaît que si le chiffre de gauche change
  (ex. 2,99 contre 3,00) ; il existe aussi avec d'autres nombres que les prix.
- Anderson et Simester (2003), Quantitative Marketing and Economics : le prix en 9 augmente la demande dans les trois
  expériences ; robe de catalogue vendue mieux à 39 $ qu'à 34 $ (environ un tiers de plus), pas de différence 34 $ / 44 $
  (citation des auteurs, HBR 2003).
- Lacetera, Pope et Sydnor (2012), American Economic Review / NBER w17030 : 22 millions de ventes de voitures d'occasion,
  environ 200 $ de moins en passant de 79 900 à 80 000 miles.
"""
import math
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
MUSIC_STYLE = 'electro'   # le casino (12 h 30, guitare) et les pavillons (20 h 30, cinéma) encadrent cette vidéo
COVER = dict(tag='Psychologie', l1='Pourquoi 9,99 € te paraît', l2='bien moins cher que 10 €')

def tag(f, x, y, w, h, a, glow=0.0):
    """Étiquette de prix : rectangle arrondi + trou."""
    if a <= 0: return
    f.rect(x - w/2 - 4, y - h/2 - 4, w + 8, h + 8, SPARK if glow else LINE, a * (0.35 + 0.65 * glow), 30)
    f.rect(x - w/2, y - h/2, w, h, OCEAN, a, 26)
    f.circle(x - w/2 + 34, y, 11, DEEP, a)

def price_chars(f, s, x, y, size, a, weights, cols):
    """Prix centré, caractère par caractère (police mono), chaque caractère avec son poids d'opacité/couleur."""
    cw = f.width('0', size, MONO)
    x0 = x - cw * len(s) / 2
    pos = []
    for i, ch in enumerate(s):
        cx = x0 + cw * (i + 0.5)
        f.text(ch, cx, y, size, cols[i], a * weights[i], MONO, True)
        pos.append(cx)
    return pos, cw

def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.8, 30.2))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Que lit ton cerveau ?', W/2, 296, 46, SPARK, ha)

    # S1 — accroche (0–4) : l'étiquette passe de 10,00 à 9,99 dès la première image
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        sc = lerp(0.85, 1.0, ease(seg(t, 0.0, 0.6))) * bump(t, 1.3, 0.16)
        c = f.c; c.save(); c.translate(W/2, 1180); c.scale(sc, sc)
        tag(f, 0, 0, 760, 300, fo, glow=float(t >= 1.3))
        if t < 1.3:
            flick = 6 * math.sin(t * 40) * seg(t, 0.8, 1.3)
            f.text('10,00 €', flick, 60, 170, INK, fo, MONO, True)
        else:
            pg = ease(seg(t, 1.8, 2.4))
            cols = [SPARK] + [INK] * 5
            wts = [1.0] + [lerp(1.0, 0.35, pg)] * 5
            price_chars(f, '9,99 €', 0, 60, 170, fo, wts, cols)
        c.restore()
        words(f, '9,99 €, c’est 10 €.', 520, 84, 0.15, INK, t_out=o)
        words(f, 'Mais ton cerveau', 680, 84, 1.4, INK, t_out=o)
        words(f, 'voit un 9.', 790, 96, 1.9, SPARK, t_out=o)

    # S2 — enjeu (4–10.8)
    if 4.0 <= t < 11.0:
        words(f, '1 centime.', 760, 130, 4.2, INK, t_out=5.7)
        # la pièce de 1 centime qui tombe et rebondit
        if t < 5.9:
            pa = ease(seg(t, 4.2, 4.4)) * (1 - seg(t, 5.6, 5.9))
            p = seg(t, 4.2, 5.2)
            yb = 1000 - 260 * abs(math.cos(p * math.pi * 2.5)) * (1 - p)
            f.circle(W/2, yb, 60, SPARK, pa)
            f.text('1 c', W/2, yb, 44, DEEP, pa, MONO, True, 'center', 'middle')
        words(f, '0,1 % du prix.', 760, 120, 5.9, INK, t_out=7.4)
        words(f, 'Ça ne change rien…', 760, 96, 7.6, INK, t_out=8.9)
        a = ease(seg(t, 9.0, 9.3)) * (1 - seg(t, 10.4, 10.8))
        f.text('Ton intuition :', W/2, 700, 56, MUTED, a, bold=False)
        big_center(f, 'Aucun effet', 860, 120, INK, a, bump(t, 9.0), DISPLAY)

    # S3 — on regarde (10.7–13.6)
    if 10.7 <= t < 13.6:
        words(f, 'Regarde comment', 820, 110, 10.9, INK, t_out=12.4)
        words(f, 'tu lis un prix.', 960, 110, 11.3, SPARK, t_out=12.4)

    # S4a — la preuve : lecture de gauche à droite (13.5–20.2)
    if 13.4 <= t < 20.4:
        ga = ease(seg(t, 13.5, 13.9)) * (1 - seg(t, 19.8, 20.2))
        s = '9,99 €'
        scan = seg(t, 14.0, 16.6) * len(s)          # position du regard, en caractères
        wts, cols = [], []
        for i in range(len(s)):
            seen = scan > i
            if i == 0: wts.append(1.0); cols.append(SPARK if seen else INK)
            else: wts.append(lerp(1.0, 0.32, ease(seg(scan, i + 0.4, i + 1.2))) if seen else 1.0); cols.append(INK)
        sc0 = bump(t, 14.1, 0.14)
        c = f.c; c.save(); c.translate(W/2, 700); c.scale(sc0, sc0)
        tag(f, 0, -60, 860, 300, ga, glow=float(t > 14.1))
        pos, cw = price_chars(f, s, 0, 0, 190, ga, wts, cols)
        c.restore()
        # le regard : un trait doré qui glisse sous les caractères
        if 14.0 <= t < 17.0:
            k = min(len(s) - 1, int(scan))
            xx = W/2 + (pos[k]) if scan < len(s) else W/2 + pos[-1]
            f.rect(xx - cw/2, 830, cw, 10, SPARK, ga * (1 - seg(t, 16.6, 17.0)), 5)
        words(f, 'Ton œil lit de gauche à droite.', 960, 52, 14.2, INK, t_out=19.8, bold=False)
        words(f, 'Le premier chiffre fixe la taille.', 1040, 52, 15.6, SPARK, t_out=19.8)
        words(f, 'Le reste compte à peine.', 1120, 52, 17.0, MUTED, t_out=19.8, bold=False)
        # règle 8 → 11 : vrai prix contre ressenti
        la = ease(seg(t, 17.4, 17.8)) * ga
        if la > 0:
            x8, x11, yl = 140, 940, 1350
            X = lambda v: x8 + (x11 - x8) * (v - 8) / 3
            f.line([(x8, yl), (x11, yl)], MUTED, la, 4)
            for v in (8, 9, 10, 11):
                f.line([(X(v), yl - 16), (X(v), yl + 16)], MUTED, la, 3)
                f.text(str(v), X(v), yl + 60, 34, MUTED, la, MONO, False)
            f.circle(X(9.99), yl, 16, INK, la)
            f.text('vrai prix', X(9.99), yl - 40, 32, INK, la, bold=False)
            pr = ease_io(seg(t, 18.0, 19.2))
            xp = lerp(X(9.99), X(9.25), pr)
            f.circle(xp, yl, 20, SPARK, la * ease(seg(t, 17.9, 18.1)))
            f.text('ressenti', xp, yl + 110, 36, SPARK, la * ease(seg(t, 18.4, 18.8)))

    # S4b — la preuve : la robe à 34, 39 et 44 $ (20.2–29.8)
    if 20.1 <= t < 30.0:
        ga = ease(seg(t, 20.2, 20.6)) * (1 - seg(t, 29.4, 29.8))
        words(f, 'Une vraie expérience :', 440, 58, 20.3, INK, t_out=29.4)
        words(f, 'la même robe, à trois prix.', 520, 48, 20.7, MUTED, t_out=29.4, bold=False)
        f.text('Anderson et Simester, 2003', W/2, 580, 30, MUTED, ga * ease(seg(t, 21.0, 21.4)), MONO, False)
        xs = [240, 540, 840]; labs = ['34 $', '39 $', '44 $']; hs = [300, 400, 300]
        base = 1280
        for i in range(3):
            ta = 21.3 + i * 0.4
            a = ease(seg(t, ta, ta + 0.3)) * ga
            win = i == 1 and t >= 25.0
            sc = bump(t, ta, 0.18) * (bump(t, 25.0, 0.2) if i == 1 else 1.0)
            c = f.c; c.save(); c.translate(xs[i], 700); c.scale(sc, sc)
            tag(f, 0, 0, 250, 120, a, glow=float(win))
            f.text(labs[i], 14, 22, 62, SPARK if win else INK, a, MONO, True)
            c.restore()
            g = ease(seg(t, 22.4, 24.6))
            h = hs[i] * g
            f.rect(xs[i] - 80, base - h, 160, h, SPARK if win else CAPITAL, a, 14)
            if win:
                f.text('le plus vendu', xs[i], base - h - 30, 36, SPARK, a * ease(seg(t, 25.0, 25.3)))
        f.text('ventes', W/2, base + 50, 32, MUTED, ga * ease(seg(t, 22.4, 22.8)), bold=False)
        words(f, 'Plus chère que 34 $…', 1400, 54, 26.0, INK, t_out=29.4)
        words(f, 'et pourtant plus vendue.', 1480, 54, 26.8, SPARK, t_out=29.4)

    # S5 — la réponse (30–35.4)
    if 29.9 <= t < 35.4:
        a = ease(seg(t, 30.0, 30.3)) * (1 - seg(t, 34.8, 35.2))
        words(f, 'Ton cerveau retient', 560, 72, 30.0, INK, t_out=34.8)
        big_center(f, '9', 1040, 460, SPARK, a, bump(t, 30.6, 0.16))
        words(f, 'le chiffre de gauche, d’abord.', 1220, 58, 31.2, INK, t_out=34.8)
        words(f, 'Thomas et Morwitz, 2005', 1310, 34, 32.2, MUTED, t_out=34.8, font=MONO, bold=False)

    # S6 — le retournement : l'effet ne marche que si le premier chiffre change (35–48.4)
    if 35.0 <= t < 48.4:
        words(f, 'Le secret ?', 900, 150, 35.1, INK, t_out=37.1)
        ga = ease(seg(t, 37.3, 37.8)) * (1 - seg(t, 47.9, 48.3))
        if ga > 0:
            rows = [(37.6, '2,99 €', '3,00 €', True, 400), (41.4, '2,98 €', '2,99 €', False, 880)]
            for (t0, pa, pb, diff, y) in rows:
                a = ease(seg(t, t0, t0 + 0.35)) * ga
                if a <= 0: continue
                for x, s in ((270, pa), (810, pb)):
                    tag(f, x, y + 90, 400, 150, a)
                    cols = [SPARK if diff else INK] + [INK] * 5
                    wts = [1.0] + [0.5] * 5
                    price_chars(f, s, x + 14, y + 120, 84, a, wts, cols)
                # l'écart ressenti entre les deux étiquettes
                gp = ease(seg(t, t0 + 0.8, t0 + 1.8))
                gw = (240 if diff else 30) * gp
                yy = y + 260
                f.rect(W/2 - gw/2, yy - 10, max(gw, 1), 20, SPARK if diff else MUTED, a, 10)
                lab = 'premier chiffre différent :' if diff else 'premier chiffre identique :'
                lab2 = 'l’écart paraît grand.' if diff else 'aucun effet.'
                la = a * ease(seg(t, t0 + 1.6, t0 + 2.0))
                f.text(lab, W/2, yy + 70, 44, INK, la, bold=False)
                f.text(lab2, W/2, yy + 130, 52, SPARK if diff else MUTED, la)
            words(f, 'Seul le premier chiffre', 1440, 52, 45.0, INK, t_out=47.9)
            words(f, 'trompe ton cerveau.', 1515, 52, 45.4, SPARK, t_out=47.9)

    # S7 — l'escalade : les voitures d'occasion (48–56.4)
    if 48.0 <= t < 56.4:
        out = 1 - seg(t, 55.9, 56.3)
        words(f, 'Ça marche même', 470, 66, 48.1, INK, t_out=55.9)
        words(f, 'sur une voiture d’occasion.', 560, 66, 48.5, INK, t_out=55.9)
        a = ease(seg(t, 49.0, 49.3)) * out
        f.rect(190, 640, 700, 200, OCEAN, a, 28)
        p = ease_io(seg(t, 49.4, 51.0))
        miles = int(round(79900 + 100 * p))
        digits = fmt_int(miles)
        col = INK if miles < 80000 else SPARK
        big_center(f, digits, 780, 120, col, a, bump(t, 51.0, 0.14))
        f.text('miles au compteur', W/2, 900, 40, MUTED, a, bold=False)
        ra = ease(seg(t, 51.1, 51.4)) * out
        sh = 10 * math.sin((t - 51.1) * 60) * (1 - seg(t, 51.1, 51.6))
        big_center(f, '≈ − 200 $', 1060, 120, RED, ra, bump(t, 51.1, 0.18))
        f.c.save(); f.c.translate(sh, 0)
        f.text('sur le prix de vente', W/2, 1140, 44, INK, ra, bold=False)
        f.c.restore()
        words(f, '22 millions de ventes étudiées.', 1260, 48, 52.4, MUTED, t_out=55.9, bold=False)
        words(f, 'Lacetera, Pope et Sydnor, 2012', 1330, 30, 52.9, MUTED, t_out=55.9, font=MONO, bold=False)
        words(f, 'Le 7 devient 8. Le prix chute.', 1460, 56, 53.6, SPARK, t_out=55.9)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        words(f, 'Tu lis le premier chiffre.', 760, 68, 56.3, INK)
        words(f, 'Le vendeur le sait.', 860, 68, 57.6, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(240, 1040, 600, 150, OCEAN, a, 28)
        pa = 0.5 + 0.5 * math.sin((t - 60) * 3)
        f.rect(240, 1040, 600, 150, SPARK, a * 0.25 * pa, 28)
        f.text('Abonne-toi.', W/2, 1135, 62, INK, a)

def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    for t0, n in ((0.15, 4), (1.4, 3), (1.9, 3)):
        for i in range(n): ev.append((t0 + i * 0.11, pop(420 + 40 * i, 0.09)))
    for i in range(8): ev.append((0.8 + i * 0.06, tick()))
    ev += [(1.3, clink(1900))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (3.9, 10.6, 12.5, 19.9, 29.6, 34.9, 47.9, 55.9)]
    ev += [(4.2, pop(330)), (4.6, clink(2300)), (4.95, clink(2100)), (5.9, pop(392)), (7.6, pop(440)),
           (9.0, ding(660, amp=0.2)), (10.9, pop(520)), (11.3, pop(620))]
    ev += [(14.1, ding(880, amp=0.22))]
    for i in range(1, 6): ev.append((14.0 + i * 2.6 / 6, tick()))
    ev += [(14.2, pop(440)), (15.6, pop(520)), (17.0, pop(400)), (18.0, rise(1.2, 500, 300, 0.07))]
    ev += [(20.3, pop(440))]
    for i in range(3): ev.append((21.3 + i * 0.4, pop(480 + i * 60)))
    ev += [(22.4, rise(2.2, 300, 900, 0.08)), (25.0, ding(988, amp=0.3)), (25.2, ding(1318, amp=0.28))]
    ev += [(26.0, pop(440)), (26.8, pop(550))]
    ev += [(30.6, ding(1046, amp=0.28)), (35.1, pop(300, 0.15))]
    ev += [(37.6, pop(440)), (38.4, rise(1.0, 300, 900, 0.08)), (39.2, ding(784, amp=0.2)),
           (41.4, pop(440)), (42.2, tick()), (43.0, pop(300, 0.1))]
    ev += [(48.1, pop(440)), (49.0, pop(500))]
    x = 49.4
    while x < 51.0: ev.append((x, tick())); x += 0.08
    ev += [(51.0, clink(1900)), (51.1, ding(330, amp=0.25)), (52.4, pop(400)), (53.6, pop(550))]
    ev += [(56.3, pop(440)), (57.6, pop(550)), (60.0, ding(784, amp=0.22))]
    return ev
