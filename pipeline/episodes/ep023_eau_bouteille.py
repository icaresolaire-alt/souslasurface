"""Eau en bouteille ou eau du robinet : combien de fois plus cher ? Même structure que le pilote.

Sources :
- Observatoire SISPEA (OFB), rapport 2023 (synthèse publiée en juillet 2025,
  economie.eaufrance.fr/sites/default/files/2025-07/rapport_sispea_2023_resume_vf.pdf) : prix moyen TTC au
  1er janvier 2024 de l'eau et de l'assainissement collectif = 4,69 €/m³ (2,32 eau potable + 2,37 assainissement),
  pour 120 m³/an. Repris par Selectra (2026). Soit 0,469 centime le litre.
- UFC-Que Choisir, cité par Économie Matin (« Eau : comment choisir entre minérale, naturelle et robinet ? ») :
  eau de source en bouteille ≈ 0,20 €/L, eau minérale ≈ 0,40 €/L. Concordant avec Selectra 2026 (0,30 €/L en
  moyenne, de 0,20 à 1,50 €/L) et Que Choisir déc. 2022 (eau de source la moins chère ≈ 0,13 €/L).
  Calculs : 0,20 / 0,00469 ≈ 43 (affiché « ×40 », arrondi prudent) ; 0,40 / 0,00469 ≈ 85.
  Avec le seul prix de l'eau potable, l'ADEME (via la CLCV) et le CIEAU donnent 100 à 300 fois : on garde le
  calcul le plus prudent, assainissement compris.
- Ministère de la Santé, sante.fr « Le contrôle de la qualité de l'eau du robinet » : « l'eau du robinet est
  en France l'aliment le plus contrôlé », près de 320 000 prélèvements et plus de 18,5 millions d'analyses par an.
  Concordant : CLCV (« le produit alimentaire le plus contrôlé », 310 000 prélèvements par an).
- Escalade : exemple de calcul, 1,5 L par jour pendant 365 jours = 547,5 L ;
  × 0,00469 € = 2,57 € ; × 0,40 € = 219 €.
"""
import math
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro (ep023 -> guitare ; ep022 était electro).
COVER = dict(tag='Science', l1='L’eau en bouteille coûte', l2='jusqu’à 85 fois plus cher')

WATER = '#5aa9d6'


def bottle(f, x, y, s, a, fill=0.0, col=INK):
    """Bouteille centrée en (x, y) (centre du corps), hauteur ~ 3.4*s. fill = niveau d'eau 0..1."""
    if a <= 0: return
    c = f.c
    bw, bh = s * 1.15, s * 2.4
    top = y - bh / 2
    # eau
    if fill > 0:
        h = bh * fill
        f.rect(x - bw / 2 + 6, y + bh / 2 - h, bw - 12, h - 6, WATER, a * 0.75, s * 0.18)
    # contour du corps
    c.save(); f.color(col, a); c.set_line_width(max(4, s * 0.06))
    r = s * 0.22
    c.new_sub_path()
    c.move_to(x - bw / 2, top + r)
    c.curve_to(x - bw / 2, top - s * 0.25, x - s * 0.28, top - s * 0.35, x - s * 0.28, top - s * 0.6)
    c.line_to(x - s * 0.28, top - s * 0.85)
    c.line_to(x + s * 0.28, top - s * 0.85)
    c.line_to(x + s * 0.28, top - s * 0.6)
    c.curve_to(x + s * 0.28, top - s * 0.35, x + bw / 2, top - s * 0.25, x + bw / 2, top + r)
    c.line_to(x + bw / 2, y + bh / 2 - r)
    c.arc(x + bw / 2 - r, y + bh / 2 - r, r, 0, math.pi / 2)
    c.line_to(x - bw / 2 + r, y + bh / 2)
    c.arc(x - bw / 2 + r, y + bh / 2 - r, r, math.pi / 2, math.pi)
    c.close_path(); c.stroke(); c.restore()
    # bouchon
    f.rect(x - s * 0.34, top - s * 1.05, s * 0.68, s * 0.24, SPARK, a, 6)
    # étiquette
    f.rect(x - bw / 2 + 4, y - s * 0.35, bw - 8, s * 0.5, CAPITAL, a * 0.85)


def tap(f, x, y, s, a, flow=0.0, t=0.0):
    """Robinet : bec vers le bas à (x, y). flow 0..1 = filet d'eau."""
    if a <= 0: return
    f.rect(x - s * 1.6, y - s * 1.1, s * 1.9, s * 0.55, MUTED, a, s * 0.2)       # corps
    f.rect(x - s * 0.3, y - s * 1.1, s * 0.6, s * 1.1, MUTED, a, s * 0.15)        # bec
    f.rect(x - s * 1.3, y - s * 1.55, s * 0.9, s * 0.25, INK, a, s * 0.1)         # manette
    f.rect(x - s * 1.95, y - s * 1.25, s * 0.4, s * 0.85, CAPITAL, a, 6)          # fixation
    if flow > 0:
        L = s * 3.2 * flow
        f.rect(x - s * 0.13, y, s * 0.26, L, WATER, a * 0.85, s * 0.1)
        for k in range(3):   # gouttes qui défilent
            yy = y + ((t * 520 + k * L / 3) % max(L, 1))
            f.circle(x, yy, s * 0.08, INK, a * 0.5 * flow)


def glass(f, x, y, s, a, fill=0.0):
    """Verre : base centrée en (x, y)."""
    if a <= 0: return
    c = f.c
    tw, bw, h = s * 1.3, s * 1.0, s * 1.6
    if fill > 0:
        hh = h * fill * 0.92
        k = hh / h
        c.move_to(x - bw / 2 + 5, y - 5); c.line_to(x + bw / 2 - 5, y - 5)
        c.line_to(x + lerp(bw, tw, k) / 2 - 5, y - hh); c.line_to(x - lerp(bw, tw, k) / 2 + 5, y - hh); c.close_path()
        f.color(WATER, a * 0.75); c.fill()
    f.line([(x - tw / 2, y - h), (x - bw / 2, y), (x + bw / 2, y), (x + tw / 2, y - h)], INK, a, max(4, s * 0.06))


def euro(v, d=2):
    return f'{v:.{d}f}'.replace('.', ',') + ' €'


def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')
    c = f.c

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.8, 30.2))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Combien de fois plus cher ?', W/2, 296, 46, SPARK, ha)

    # S1 — accroche (0–4) : l'eau coule dès la première image
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        p = ease(seg(t, 0.0, 0.6))
        tap(f, lerp(-200, 330, p), 900, 90, fo, 1.0, t)
        glass(f, lerp(-200, 330, p), 1360, 120, fo, 0.2 + 0.6 * seg(t, 0, 3.8))
        bottle(f, lerp(1280, 760, p), 1130, 130, fo, 0.85)
        words(f, 'Deux litres d’eau.', 470, 92, 0.15, INK, t_out=o)
        a = ease(seg(t, 1.2, 1.5)) * fo
        c.save(); c.translate(W/2, 620); s = bump(t, 1.2, 0.2); c.scale(s, s)
        f.text('Pas le même prix.', 0, 0, 96, SPARK, a); c.restore()

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.0:
        o1 = 7.3
        words(f, 'Un litre au robinet…', 470, 80, 4.2, INK, t_out=o1)
        a1 = ease(seg(t, 4.2, 4.6)) * (1 - seg(t, o1, o1 + 0.3))
        tap(f, W/2, 820, 100, a1, ease(seg(t, 4.4, 4.8)), t)
        glass(f, W/2, 1380, 150, a1, seg(t, 4.6, 7.0))
        o2 = 10.7
        words(f, '… et un litre en bouteille.', 470, 72, 7.5, INK, t_out=o2)
        a2 = ease(seg(t, 7.5, 7.9)) * (1 - seg(t, o2, o2 + 0.3))
        c.save(); c.translate(W/2, 1000); s = bump(t, 7.6, 0.12); c.scale(s, s)
        bottle(f, 0, 0, 150, a2, 0.85); c.restore()
        a = a2 * ease(seg(t, 8.6, 8.9))
        f.text('Deux fois plus cher ? Trois ?', W/2, 1440, 54, MUTED, a, bold=False)

    # S3 — la question (10.9–13.6)
    if 10.9 <= t < 13.6:
        words(f, 'Combien de fois', 820, 104, 11.0, INK, t_out=12.5)
        words(f, 'plus cher ?', 950, 116, 11.4, SPARK, t_out=12.5)

    # S4 — la preuve (13.5–30)
    if 13.4 <= t < 30.0:
        # A : 1 000 litres au robinet (13.6–21)
        oa = 20.8
        ga = ease(seg(t, 13.5, 13.9)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Au robinet,', 430, 80, 13.6, INK, t_out=oa)
            words(f, '1 000 litres coûtent…', 530, 72, 14.1, MUTED, t_out=oa)
            # cuve de 1 m³ qui se remplit
            x0, y0, sz = W/2 - 210, 640, 420
            p = ease_io(seg(t, 14.6, 17.6))
            f.rect(x0 + 6, y0 + sz - sz * p, sz - 12, sz * p - 6, WATER, ga * 0.7)
            f.line([(x0, y0), (x0, y0 + sz), (x0 + sz, y0 + sz), (x0 + sz, y0)], INK, ga, 7)
            f.text('1 m³', W/2, y0 + sz / 2 + 20, 60, INK, ga * ease(seg(t, 14.8, 15.1)), MONO, True)
            v = 4.69 * p
            a = ga * ease(seg(t, 14.6, 14.9))
            c.save(); c.translate(W/2, 1240); s = bump(t, 17.6, 0.12); c.scale(s, s)
            f.text(euro(v), 0, 0, 120, SPARK, a, MONO, True); c.restore()
            a = ga * ease(seg(t, 18.0, 18.3))
            f.text('Soit 0,5 centime le litre.', W/2, 1400, 58, INK, a)
            f.text('eau + assainissement, SISPEA 2023', W/2, 1520, 30, MUTED, ga * ease(seg(t, 15.0, 15.4)) * 0.9, MONO, False)
        # B : le prix d'un litre (21–29.6)
        gb = ease(seg(t, 21.0, 21.4)) * (1 - seg(t, 29.4, 29.8))
        if gb > 0:
            words(f, 'Le prix d’un litre', 430, 84, 21.1, INK, t_out=29.4)
            base, maxh = 1340, 640
            XS = (220, 540, 860)
            BARS = ((0.469, 'robinet', CAPITAL, INK, '0,5 c'), (20, 'eau de source', INK, INK, '20 c'),
                    (40, 'eau minérale', SPARK, SPARK, '40 c'))
            f.line([(90, base), (990, base)], MUTED, gb * ease(seg(t, 21.6, 21.9)), 4)
            for j, (val, lab, col, tcol, txt) in enumerate(BARS):
                x = XS[j]
                t0 = 22.0 + j * 1.6
                pr = ease_io(seg(t, t0, t0 + 1.8))
                ba = gb * ease(seg(t, t0, t0 + 0.3))
                h = max(6, maxh * val * pr / 40)
                f.rect(x - 105, base - h, 210, h, col, ba, 12)
                if j == 0:
                    c.save(); c.translate(x, base - h - 30)
                    k = 1 + 0.12 * max(0, math.sin((t - 27.4) * 6)) * seg(t, 27.4, 27.7)
                    c.scale(k, k); f.text(txt, 0, 0, 64, SPARK if t > 27.4 else tcol, ba, MONO, True); c.restore()
                else:
                    f.text(f'{int(round(val * pr))} c', x, base - h - 30, 64, tcol, ba, MONO, True)
                f.text(lab, x, base + 60, 38, MUTED, ba, DISPLAY, True)
            # le robinet clignote : la barre est presque invisible
            f.text('c = centime   ·   UFC-Que Choisir', W/2, 1520, 30, MUTED, gb * 0.9, MONO, False)

    # S5 — la réponse (30–36)
    if 29.9 <= t < 36.0:
        o = 33.0
        a = ease(seg(t, 30.3, 30.6)) * (1 - seg(t, o, o + 0.3))
        words(f, 'L’eau minérale :', 600, 84, 30.0, INK, t_out=o)
        big_center(f, '×85', 920, 230, SPARK, a, bump(t, 30.3, 0.18))
        o2 = 35.6
        words(f, 'L’eau de source :', 600, 84, 33.2, MUTED, t_out=o2)
        a = ease(seg(t, 33.7, 34.0)) * (1 - seg(t, o2, o2 + 0.3))
        big_center(f, '×40', 900, 190, INK, a, bump(t, 33.7, 0.12))

    # S6 — le retournement (36–48.4)
    if 36.0 <= t < 48.4:
        words(f, 'Pourquoi ?', 900, 150, 36.1, SPARK, t_out=37.9)
        # A : ce que tu paies dans une bouteille
        oa = 42.6
        ga = ease(seg(t, 38.1, 38.5)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Le robinet : un tuyau.', 440, 72, 38.3, INK, t_out=oa)
            words(f, 'La bouteille, tu paies aussi :', 540, 60, 39.0, MUTED, t_out=oa)
            bottle(f, W/2, 1060, 140, ga, 0.85)
            TAGS = (('le plastique', 250, 820), ('le transport', 830, 820), ('le magasin', 250, 1300), ('la marque', 830, 1300))
            for k, (lab, x, y) in enumerate(TAGS):
                t0 = 39.8 + k * 0.5
                aa = ga * ease(seg(t, t0, t0 + 0.3))
                wdt = f.width(lab, 46) + 50
                c.save(); c.translate(x, y); s = bump(t, t0, 0.2); c.scale(s, s)
                f.rect(-wdt / 2, -48, wdt, 76, OCEAN, aa * 0.95, 38)
                f.text(lab, 0, 4, 46, SPARK, aa); c.restore()
        # B : l'eau du robinet, la plus contrôlée
        gb = ease(seg(t, 42.8, 43.2)) * (1 - seg(t, 47.9, 48.3))
        if gb > 0:
            words(f, 'Et l’eau du robinet est', 440, 66, 42.9, INK, t_out=47.9)
            words(f, 'l’aliment le plus contrôlé.', 530, 70, 43.4, SPARK, t_out=47.9)
            # grille de points : 1 point = 1 000 prélèvements
            N, cols = 320, 20
            gx0, gy0, step = W/2 - 19 * 22, 700, 44
            p = seg(t, 44.0, 46.6)
            n = int(N * ease_io(p))
            for i in range(N):
                xx = gx0 + (i % cols) * step; yy = gy0 + (i // cols) * step
                f.circle(xx, yy, 13, SPARK if i < n else LINE, gb * (1 if i < n else 0.6))
            a = gb * ease(seg(t, 44.0, 44.3))
            f.text(f'{fmt_int(n * 1000)}', W/2, 1480, 76, INK, a, MONO, True)
            f.text('prélèvements par an, en France', W/2, 1540, 32, MUTED, a, MONO, False)

    # S7 — l'escalade : sur un an (48–56.4)
    if 48.0 <= t < 56.4:
        o = 55.9
        ga = ease(seg(t, 48.1, 48.4)) * (1 - seg(t, o, o + 0.3))
        if ga > 0:
            words(f, '1,5 litre par jour,', 430, 80, 48.1, INK, t_out=o)
            words(f, 'pendant un an :', 530, 72, 48.8, MUTED, t_out=o)
            base, maxh = 1340, 600
            XS = (300, 780)
            for j, (val, lab, col) in enumerate(((2.57, 'robinet', CAPITAL), (219, 'eau minérale', SPARK))):
                x = XS[j]
                t0 = 49.8 + j * 0.9
                pr = ease_io(seg(t, t0, t0 + 2.2))
                ba = ga * ease(seg(t, t0, t0 + 0.3))
                h = max(6, maxh * val * pr / 219)
                f.rect(x - 120, base - h, 240, h, col, ba, 14)
                txt = euro(val * pr) if j == 0 else f'{int(round(val * pr))} €'
                f.text(txt, x, base - h - 30, 72, SPARK if j else INK, ba, MONO, True)
                f.text(lab, x, base + 60, 40, MUTED, ba, DISPLAY, True)
            f.line([(120, base), (960, base)], MUTED, ga * ease(seg(t, 49.6, 49.9)), 4)
            f.text('547 litres × prix moyen', W/2, 1520, 30, MUTED, ga * 0.9 * ease(seg(t, 52.5, 52.8)), MONO, False)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        a = ease(seg(t, 56.1, 56.4))
        c.save(); c.translate(W/2, 600); s = bump(t, 56.1, 0.12); c.scale(s, s)
        bottle(f, 0, 0, 80, a, 0.85 * (1 - 0.6 * seg(t, 56.5, 59.5)))
        c.restore()
        words(f, 'Tu paies la bouteille,', 880, 84, 56.3, INK)
        words(f, 'pas l’eau.', 1000, 100, 57.6, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(240, 1120, 600, 150, OCEAN, a, 28)
        pa = 0.5 + 0.5 * math.sin((t - 60) * 3)
        f.rect(240, 1120, 600, 150, SPARK, a * 0.25 * pa, 28)
        f.text('Abonne-toi.', W/2, 1215, 62, INK, a)


def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    ev += [(0.15, pop(440, 0.09)), (1.2, clink(1900))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (12.5, 29.6, 47.9, 55.9)]
    ev += [(7.6, pop(300, 0.15)), (11.0, pop(520))]
    ev += [(15.0, rise(2.4, 300, 900, 0.07)), (17.6, ding(784, amp=0.2))]
    ev += [(25.2, rise(1.6, 300, 900, 0.07))]
    ev += [(30.3, ding(1046, amp=0.28)), (36.1, pop(300, 0.15))]
    ev += [(44.0, rise(2.4, 300, 900, 0.07)), (50.7, rise(2.0, 300, 900, 0.08))]
    ev += [(56.3, pop(440)), (60.0, ding(784, amp=0.22))]
    return ev
