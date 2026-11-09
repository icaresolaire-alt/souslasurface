"""Pourquoi l'essence monte vite et baisse lentement (effet « fusée et plume »). Même structure que le pilote.

Sources :
- Borenstein, Cameron et Gilbert, « Do Gasoline Prices Respond Asymmetrically to Crude Oil Price Changes? »,
  Quarterly Journal of Economics 112(1), février 1997, p. 305-339 (NBER w4138, nber.org/papers/w4138) :
  « Nearly all of the response to a crude oil price increase shows up in the pump price within 4 weeks » ;
  « decreases are passed along gradually over 8 weeks ». Données américaines. Affiché : 4 semaines contre 8,
  soit 2 fois plus de temps pour baisser.
- Concordant : M. Chesnes, FTC Bureau of Economics, Working Paper 302, juin 2010, « Asymmetric Pass-Through
  in U.S. Gasoline Prices » : « On average, retail prices rise more than four times as fast as they fall ».
- Nom « rockets and feathers » : Oxford Institute for Energy Studies (oxfordenergy.org/?p=28122), d'après la
  Monopolies and Mergers Commission britannique (1990) ; R. Bacon, Energy Economics 1991 (cité par Chesnes).
- Mécanisme : M. Lewis, « Asymmetric Price Adjustment and Consumer Search », Journal of Economics & Management
  Strategy 20(2), 2011, p. 409-449 (RePEc) et document de travail UC Berkeley CSEM (escholarship.org/uc/item/
  6266b54f) : « consumers search less when prices are falling, which results in higher profit margins and a
  slower price response ». Chesnes 2010 : « if prices are falling, consumers may search less ».
- Escalade : S. Peltzman, « Prices Rise Faster than They Fall », Journal of Political Economy 108, 2000,
  p. 466-502 (résumé, DOI 10.1086/262126) : « 77 consumer and 165 produced goods » (242) ; « more than two of
  every three markets » ; réponse immédiate à une hausse « at least twice » celle à une baisse. Concordant :
  Toolsema, ESB, 5 octobre 2001 (77 + 165 biens, « meer dan twee van iedere drie markten »).
- Courbes affichées comme schéma simplifié, sans prix inventé.
"""
import math
import random
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro (ep035 précédent).
COVER = dict(tag='Argent', l1='Pourquoi l’essence monte vite', l2='et baisse si lentement')

PUMP = '#2f4f66'


def rocket(f, x, y, s, a, flame=0.0):
    if a <= 0: return
    c = f.c; c.save(); c.translate(x, y); c.scale(s, s)
    if flame > 0:
        fl = 60 + 30 * flame
        f.color(RED, a * 0.9)
        c.move_to(-26, 70); c.line_to(0, 70 + fl); c.line_to(26, 70); c.close_path(); c.fill()
        f.color(SPARK, a)
        c.move_to(-14, 70); c.line_to(0, 70 + fl * 0.6); c.line_to(14, 70); c.close_path(); c.fill()
    f.color(INK, a)
    c.move_to(0, -120); c.curve_to(45, -80, 45, 20, 38, 70); c.line_to(-38, 70)
    c.curve_to(-45, 20, -45, -80, 0, -120); c.close_path(); c.fill()
    f.color(RED, a)
    c.move_to(-38, 20); c.line_to(-70, 80); c.line_to(-38, 70); c.close_path(); c.fill()
    c.move_to(38, 20); c.line_to(70, 80); c.line_to(38, 70); c.close_path(); c.fill()
    f.circle(0, -35, 18, OCEAN, a)
    c.restore()


def feather(f, x, y, s, a, rot=0.0):
    if a <= 0: return
    c = f.c; c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    f.color(SPARK, a * 0.9)
    c.move_to(0, -130); c.curve_to(70, -80, 60, 60, 0, 110); c.curve_to(-60, 60, -70, -80, 0, -130)
    c.close_path(); c.fill()
    c.restore()
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    f.line([(0, -120), (0, 150)], DEEP, a, 5)
    for k in range(5):
        yy = -80 + 35 * k
        f.line([(0, yy), (40, yy - 25)], DEEP, a * 0.5, 3)
        f.line([(0, yy), (-40, yy - 25)], DEEP, a * 0.5, 3)
    c.restore()


def pump(f, x, y, s, a, col=PUMP, label=''):
    if a <= 0: return
    c = f.c; c.save(); c.translate(x, y); c.scale(s, s)
    f.rect(-60, -110, 120, 220, col, a, 14)
    f.rect(-40, -85, 80, 50, DEEP, a * 0.8, 6)
    f.line([(60, -60), (95, -40), (95, 50)], col, a, 10)
    f.rect(-75, 105, 150, 18, col, a, 6)
    c.restore()
    if label: f.text(label, x, y + 52 * s, 34 * s, SPARK, a, MONO, True)


def barrel(f, x, y, s, a):
    if a <= 0: return
    f.rect(x - 70 * s, y - 100 * s, 140 * s, 200 * s, '#3b4a52', a, 20 * s)
    for dy in (-55, 0, 55):
        f.rect(x - 70 * s, y + (dy - 6) * s, 140 * s, 12 * s, MUTED, a * 0.7, 0)


def arrow(f, x, y, up, a, col):
    if a <= 0: return
    c = f.c; f.color(col, a)
    d = -1 if up else 1
    c.move_to(x - 40, y); c.line_to(x + 40, y); c.line_to(x, y + 60 * d); c.close_path(); c.fill()
    f.rect(x - 14, y - (70 if up else 0), 28, 70, col, a)


def person(f, x, y, s, a, col=INK):
    if a <= 0: return
    c = f.c; c.save(); c.translate(x, y); c.scale(s, s)
    f.circle(0, -70, 38, col, a)
    f.rect(-55, -20, 110, 110, col, a, 40)
    c.restore()


def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')
    c = f.c

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.8, 30.2))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Pourquoi la baisse traîne ?', W/2, 296, 42, SPARK, ha)

    # S1 — accroche (0–4) : la fusée décolle dès la première image
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        words(f, 'Le prix à la pompe', 470, 88, 0.05, INK, t_out=o)
        words(f, 'monte comme une fusée.', 590, 84, 0.7, SPARK, t_out=o)
        p = ease_io(seg(t, 0.0, 3.6))
        yr = 1450 - 480 * p
        n = 12
        for k in range(n):
            yy = yr + 160 + k * 26
            if yy < 1500:
                f.circle(W/2 + 6 * math.sin(k + t * 9), yy, 10 + 2 * k, MUTED, fo * 0.25 * (1 - k / n))
        rocket(f, W/2, yr, 1.5, fo, 0.5 + 0.5 * math.sin(t * 20))

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.0:
        o1 = 7.4
        g1 = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'Et il redescend', 470, 92, 4.2, INK, t_out=o1)
            words(f, 'comme une plume.', 590, 92, 4.8, SPARK, t_out=o1)
            p = seg(t, 4.1, 7.6)
            feather(f, W/2 + 120 * math.sin(p * 5.5), 820 + 400 * p, 1.4, g1, 0.5 * math.cos(p * 5.5))
        o2 = 10.7
        g2 = ease(seg(t, 7.6, 8.0)) * (1 - seg(t, o2, o2 + 0.3))
        if g2 > 0:
            words(f, 'Ton intuition :', 480, 72, 7.7, MUTED, t_out=o2)
            words(f, 'le prix suit le pétrole', 600, 80, 8.1, INK, t_out=o2)
            words(f, 'dans les deux sens.', 710, 80, 8.7, SPARK, t_out=o2)
            ab = g2 * ease(seg(t, 8.4, 8.7))
            barrel(f, 330, 1100, 1.0, ab)
            pump(f, 750, 1100, 1.0, ab)
            f.text('pétrole', 330, 1290, 38, MUTED, ab, MONO, True)
            f.text('pompe', 750, 1290, 38, MUTED, ab, MONO, True)
            up = t < 9.6
            aa = ab * ease(seg(t, 8.9, 9.1) if up else seg(t, 9.7, 9.9))
            dy = 20 * math.sin(t * 6)
            arrow(f, 330, 930 + dy, up, aa, SPARK if up else EARTH)
            arrow(f, 750, 930 + dy, up, aa, SPARK if up else EARTH)

    # S3 — la question (10.9–13.6)
    if 10.9 <= t < 13.6:
        words(f, 'Alors pourquoi la baisse', 820, 84, 11.0, INK, t_out=12.5)
        words(f, 'traîne autant ?', 950, 110, 11.4, SPARK, t_out=12.5)

    # S4 — la preuve (13.5–30)
    if 13.4 <= t < 30.0:
        # A : schéma pétrole / pompe (13.6–21.2)
        oa = 21.0
        ga = ease(seg(t, 13.5, 13.9)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Le pétrole monte,', 440, 84, 13.6, INK, t_out=oa)
            words(f, 'puis redescend.', 550, 84, 14.2, MUTED, t_out=oa)
            x0, x1, yb, yt = 170, 910, 1240, 760
            f.line([(x0, yb), (x1, yb)], LINE, ga, 4)
            f.line([(x0, yt - 40), (x0, yb)], LINE, ga, 4)

            def crude(u):
                return 0.15 + 0.7 * (1 if 0.2 <= u < 0.55 else 0)

            def pmp(u):
                if u < 0.2: return 0.10
                if u < 0.55: return 0.10 + 0.7 * (1 - math.exp(-(u - 0.2) / 0.025))
                top = 0.10 + 0.7 * (1 - math.exp(-0.35 / 0.025))
                return 0.10 + (top - 0.10) * math.exp(-(u - 0.55) / 0.16)

            prog = ease_io(seg(t, 15.0, 19.8))
            N = 160
            for fn, col, w in ((crude, MUTED, 6), (pmp, SPARK, 9)):
                pts = []
                for i in range(int(N * prog) + 1):
                    u = i / N
                    pts.append((x0 + (x1 - x0) * u, yb - (yb - yt) * fn(u)))
                if len(pts) > 1: f.line(pts, col, ga, w)
            la = ga * ease(seg(t, 15.4, 15.7))
            f.text('pétrole', 230, 1310, 40, MUTED, la, MONO, True, 'left')
            f.text('pompe', 600, 1310, 40, SPARK, la, MONO, True, 'left')
            if prog > 0.72:
                aa = ga * ease(seg(t, 18.6, 18.9))
                f.text('la pompe traîne', 760, 980, 40, SPARK, aa, DISPLAY, True)
            f.text('schéma simplifié', W/2, 1400, 32, MUTED, ga * ease(seg(t, 16.0, 16.3)), MONO, False)
        # B : l'étude de 1997 (21.4–29.6)
        gb = ease(seg(t, 21.3, 21.7)) * (1 - seg(t, 29.4, 29.8))
        if gb > 0:
            words(f, 'Une étude de 1997', 440, 84, 21.4, INK, t_out=29.3)
            words(f, 'sur l’essence aux États-Unis', 540, 56, 22.0, MUTED, t_out=29.3)
            sz, gap = 90, 14
            xs0 = W/2 - (8 * sz + 7 * gap) / 2
            f.text('Hausse', xs0, 700, 48, INK, gb * ease(seg(t, 22.6, 22.9)), DISPLAY, True, 'left')
            for k in range(4):
                x = xs0 + k * (sz + gap)
                f.rect(x, 730, sz, sz, LINE, gb, 12)
                q = ease(seg(t, 23.2 + 0.25 * k, 23.5 + 0.25 * k))
                f.rect(x, 730, sz, sz, SPARK, gb * q, 12)
            f.text('presque tout en 4 semaines', W/2, 890, 44, SPARK, gb * ease(seg(t, 24.4, 24.7)), MONO, True)
            f.text('Baisse', xs0, 1020, 48, INK, gb * ease(seg(t, 24.9, 25.2)), DISPLAY, True, 'left')
            for k in range(8):
                x = xs0 + k * (sz + gap)
                f.rect(x, 1050, sz, sz, LINE, gb, 12)
                q = ease(seg(t, 25.4 + 0.42 * k, 25.9 + 0.42 * k))
                f.rect(x, 1050, sz, sz, EARTH, gb * q, 12)
            f.text('étalée sur 8 semaines', W/2, 1210, 44, EARTH, gb * ease(seg(t, 28.4, 28.7)), MONO, True)
            f.text('Borenstein, Cameron et Gilbert, QJE', W/2, 1350, 30, MUTED,
                   gb * ease(seg(t, 26.0, 26.3)), MONO, False)

    # S5 — la réponse (30–36)
    if 29.9 <= t < 36.0:
        o = 35.6
        a = ease(seg(t, 30.3, 30.6)) * (1 - seg(t, o, o + 0.3))
        big_center(f, '2 fois', 820, 240, SPARK, a, bump(t, 30.3, 0.18))
        words(f, 'plus de temps', 1000, 76, 31.0, INK, t_out=o)
        words(f, 'pour baisser.', 1110, 76, 31.5, INK, t_out=o)
        words(f, '4 semaines contre 8', 1280, 56, 33.0, MUTED, t_out=o)

    # S6 — le retournement (36–48.4)
    if 36.0 <= t < 48.4:
        words(f, 'Le secret ?', 900, 150, 36.1, SPARK, t_out=37.9)
        xs = (230, 540, 850)
        # A : quand ça monte, tu compares (38.1–42.6)
        oa = 42.6
        ga = ease(seg(t, 38.1, 38.5)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Quand ça monte,', 440, 84, 38.2, INK, t_out=oa)
            words(f, 'tu compares les stations.', 550, 72, 38.7, SPARK, t_out=oa)
            for i, x in enumerate(xs):
                pump(f, x, 1000, 0.9, ga * ease(seg(t, 39.2 + 0.15 * i, 39.5 + 0.15 * i)))
            p = seg(t, 39.9, 42.2) * 2
            i = min(int(p), 1); q = ease_io(p - i)
            nx = xs[i] + (xs[i + 1] - xs[i]) * q
            person(f, nx, 1300 - 50 * math.sin(math.pi * q), 0.6, ga * ease(seg(t, 39.7, 39.9)), SPARK)
            f.text('tu cherches le moins cher', W/2, 1460, 38, MUTED, ga * ease(seg(t, 40.4, 40.7)), MONO, False)
        # B : quand ça baisse, tu ne cherches plus (42.9–47.9)
        ob = 47.9
        gb = ease(seg(t, 42.8, 43.2)) * (1 - seg(t, ob, ob + 0.3))
        if gb > 0:
            words(f, 'Quand ça baisse,', 440, 84, 42.9, INK, t_out=ob)
            words(f, 'tu ne cherches plus.', 550, 80, 43.5, RED, t_out=ob)
            pump(f, 380, 1010, 1.1, gb)
            person(f, 380, 1330, 0.6, gb, INK)
            # barre « marge » qui reste haute
            ab = gb * ease(seg(t, 44.4, 44.7))
            hx, hy, hw, hh = 640, 760, 140, 420
            f.rect(hx, hy, hw, hh, LINE, ab, 14)
            m = 0.35 + 0.25 * ease(seg(t, 44.8, 46.2))
            f.rect(hx, hy + hh * (1 - m), hw, hh * m, SPARK, ab, 14)
            f.text('marge', hx + hw / 2, hy + hh + 60, 40, SPARK, ab, MONO, True)
            f.text('alors la station garde', W/2, 1440, 38, MUTED, gb * ease(seg(t, 45.4, 45.7)), MONO, False)
            f.text('sa marge plus longtemps', W/2, 1495, 38, MUTED, gb * ease(seg(t, 45.4, 45.7)), MONO, False)

    # S7 — l'escalade (48–56.4) : 242 produits, plus de 2 sur 3
    if 48.0 <= t < 56.4:
        o = 55.9
        ga = ease(seg(t, 48.1, 48.4)) * (1 - seg(t, o, o + 0.3))
        if ga > 0:
            words(f, 'Et pas que l’essence.', 430, 84, 48.1, INK, t_out=o)
            words(f, 'Sur 242 produits étudiés :', 540, 60, 48.8, MUTED, t_out=o)
            rng = random.Random(36)
            order = list(range(242)); rng.shuffle(order)
            gold = set(order[:166])
            rank = {k: r for r, k in enumerate(order[:166])}
            sz, gap, cols = 30, 8, 22
            gx = W/2 - (cols * sz + (cols - 1) * gap) / 2
            for k in range(242):
                cx, ry = k % cols, k // cols
                x = gx + cx * (sz + gap); y = 640 + ry * (sz + gap)
                ak = ga * ease(seg(t, 49.4 + 0.004 * k, 49.7 + 0.004 * k))
                f.rect(x, y, sz, sz, LINE, ak, 6)
                if k in gold:
                    q = ease(seg(t, 50.8 + 0.012 * rank[k], 51.1 + 0.012 * rank[k]))
                    f.rect(x, y, sz, sz, SPARK, ak * q, 6)
            aa = ga * ease(seg(t, 52.4, 52.7))
            c.save(); c.translate(W/2, 1190); s = bump(t, 52.4, 0.15); c.scale(s, s)
            f.text('plus de 2 sur 3', 0, 0, 96, SPARK, aa, DISPLAY, True); c.restore()
            f.text('leur prix monte plus vite qu’il ne baisse', W/2, 1300, 46, INK, ga * ease(seg(t, 53.2, 53.5)), DISPLAY, True)
            f.text('(Peltzman, 2000)', W/2, 1380, 30, MUTED, ga * ease(seg(t, 53.2, 53.5)), MONO, False)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        a = ease(seg(t, 56.1, 56.4))
        rocket(f, W/2 - 170, 640 - 30 * math.sin((t - 56) * 2), 0.9 * bump(t, 56.1, 0.15), a, 0.5 + 0.5 * math.sin(t * 20))
        feather(f, W/2 + 170, 650 + 25 * math.sin((t - 56) * 1.5), 0.9, a, 0.3 * math.sin((t - 56) * 1.5))
        words(f, 'Les prix montent en fusée', 900, 64, 56.3, INK)
        words(f, 'et baissent en plume.', 1010, 78, 57.6, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(240, 1160, 600, 150, OCEAN, a, 28)
        pa = 0.5 + 0.5 * math.sin((t - 60) * 3)
        f.rect(240, 1160, 600, 150, SPARK, a * 0.25 * pa, 28)
        f.text('Abonne-toi.', W/2, 1255, 62, INK, a)


def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    ev += [(0.15, rise(1.2, 300, 900, 0.07))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (12.5, 29.6, 47.9, 55.9)]
    ev += [(11.0, pop(520))]
    ev += [(23.2, ding(784, amp=0.18))]
    ev += [(30.3, ding(1046, amp=0.28)), (36.1, pop(300, 0.15))]
    ev += [(52.4, ding(784, amp=0.18))]
    ev += [(56.3, pop(440)), (60.0, ding(784, amp=0.22))]
    return ev
