"""Toutes les bananes du supermarché sont des clones : la Cavendish. Même structure que le pilote.

Sources :
- USITC, Executive Briefing on Trade « Bananas » (DeCarlo et Legrand) : 99 % des bananes exportées sont des Cavendish ;
  variété sans graines propagée par rejets, donc clones ; Gros Michel ravagée par la maladie de Panama (TR1) ;
  TR4 arrivé en Colombie à l'été 2019.
- IFT, Science Meets Food « The Rise and Fall of Bananas » : 99 % des exportations, 47 % de la production mondiale,
  Gros Michel jusqu'à la fin des années 1950, plantes génétiquement identiques, TR4 en Amérique latine en 2019.
- ProMusa « Cavendish subgroup » : domination de la Cavendish dans le commerce depuis la fin des années 1950.
- Wikipedia « Cavendish banana » et « Panama disease » : propagation par clones ; chlamydospores qui survivent
  jusqu'à 30 ans dans le sol ; pathogène résistant aux fongicides ; TR4 en Colombie en août 2019.
"""
import math
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro (ep014 -> cinema) ; 12 h 30 = chill, 20 h 30 = piano.
COVER = dict(tag='Science', l1='Toutes les bananes du', l2='supermarché sont des clones')

BROWN = '#7a5a3a'

def banana(f, x, y, s, a, col=SPARK, rot=0.0):
    """Banane stylisée : un arc épais, bouts arrondis, petite tige foncée."""
    if a <= 0 or s <= 0: return
    c = f.c; c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    f.color(col, a); c.set_line_width(44)
    c.new_sub_path(); c.arc(0, -70, 110, math.radians(25), math.radians(155)); c.stroke()
    # reflet
    f.color('#ffffff', a * 0.18); c.set_line_width(10)
    c.new_sub_path(); c.arc(0, -70, 98, math.radians(50), math.radians(130)); c.stroke()
    # tige et bout
    ex, ey = 110 * math.cos(math.radians(25)), -70 + 110 * math.sin(math.radians(25))
    f.color(BROWN, a); c.set_line_width(16)
    c.move_to(ex, ey); c.line_to(ex + 22, ey - 26); c.stroke()
    bx, by = 110 * math.cos(math.radians(155)), -70 + 110 * math.sin(math.radians(155))
    f.circle(bx - 4, by + 2, 9, '#3a2a1a', a)
    c.restore()

def plant(f, x, y, s, a, col=EARTH, sway=0.0):
    """Bananier stylisé : tronc + quatre feuilles."""
    if a <= 0 or s <= 0: return
    c = f.c; c.save(); c.translate(x, y); c.scale(s, s)
    f.rect(-12, -150, 24, 150, col, a, 10)
    for ang in (-60, -25, 25, 60):
        c.save(); c.translate(0, -150); c.rotate(math.radians(ang + sway)); c.scale(1, 0.32)
        f.color(col, a); c.new_sub_path(); c.arc(0, -95, 95, 0, 2 * math.pi); c.fill()
        c.restore()
    c.restore()

def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')
    sw = 4 * math.sin(t * 2.2)

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.8, 30.2))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Pourquoi toutes identiques ?', W/2, 296, 46, SPARK, ha)

    # S1 — accroche (0–4) : une grille de bananes identiques qui surgit dès la première image
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        words(f, 'Toutes tes bananes', 470, 84, 0.15, INK, t_out=o)
        words(f, 'sont des clones.', 580, 96, 1.2, SPARK, t_out=o)
        for r in range(3):
            for k in range(4):
                i = r * 4 + k
                p = ease(seg(t, i * 0.12, i * 0.12 + 0.3))
                sc = 0.62 * (0.4 + 0.6 * p) * bump(t, 2.4, 0.08)
                banana(f, 210 + k * 220, 900 + r * 190, sc, fo * (0.3 + 0.7 * p), SPARK, math.radians(sw))
        a = ease(seg(t, 2.4, 2.7)) * fo
        f.text('même ADN, 12 fois', W/2, 1480, 44, MUTED, a, MONO, True)

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.0:
        words(f, 'En principe, une plante', 600, 64, 4.2, INK, t_out=6.7)
        words(f, 'naît d’une graine.', 690, 64, 4.6, INK, t_out=6.7)
        a = ease(seg(t, 4.4, 4.7)) * (1 - seg(t, 6.6, 6.9))
        g = ease(seg(t, 5.0, 6.4))
        f.circle(W/2, 1080, 34, BROWN, a)
        if g > 0:
            f.rect(W/2 - 6, 1080 - 220 * g, 12, 220 * g, EARTH, a, 6)
            c = f.c
            for side in (-1, 1):
                c.save(); c.translate(W/2, 1080 - 200 * g); c.rotate(side * 0.9); c.scale(1, 0.4)
                f.color(EARTH, a); c.new_sub_path(); c.arc(side * 60 * g, 0, 60 * g + 1, 0, 2 * math.pi); c.fill()
                c.restore()
        words(f, 'Et chaque graine', 640, 72, 6.9, INK, t_out=8.8)
        words(f, 'est différente.', 740, 72, 7.3, SPARK, t_out=8.8)
        a = ease(seg(t, 7.0, 7.3)) * (1 - seg(t, 8.7, 9.0))
        for i, col in enumerate((BROWN, '#a0703a', '#5a4030', '#c08a4a', '#6a5a3a')):
            ai = a * ease(seg(t, 7.4 + i * 0.15, 7.6 + i * 0.15))
            f.circle(220 + i * 160, 1020 + 16 * math.sin(t * 3 + i), 30 + 6 * (i % 3), col, ai)
        a = ease(seg(t, 9.0, 9.3)) * (1 - seg(t, 10.6, 10.9))
        f.text('Ton intuition :', W/2, 700, 56, MUTED, a, bold=False)
        big_center(f, 'Toutes uniques', 870, 110, INK, a, bump(t, 9.0), DISPLAY)

    # S3 — la question (10.9–13.5)
    if 10.9 <= t < 13.6:
        words(f, 'Alors pourquoi', 820, 110, 11.0, INK, t_out=12.5)
        words(f, 'toutes pareilles ?', 960, 110, 11.4, SPARK, t_out=12.5)

    # S4a — la preuve : coupe une banane (13.5–21)
    if 13.4 <= t < 21.0:
        ga = ease(seg(t, 13.5, 13.9)) * (1 - seg(t, 20.5, 20.9))
        words(f, 'Coupe une banane.', 450, 72, 13.6, INK, t_out=20.5)
        # la banane, puis la coupe
        cut = ease(seg(t, 14.6, 15.0))
        banana(f, W/2 - 30 * cut, 760, 1.5, ga, SPARK, math.radians(sw * 0.5))
        if 14.4 <= t < 15.4:
            ka = 1 - seg(t, 15.0, 15.4)
            yk = lerp(560, 980, ease(seg(t, 14.4, 14.8)))
            f.line([(W/2 + 40, 560), (W/2 + 40, yk)], INK, ka * ga, 6)
        # tranche vue de face
        sa = ga * ease(seg(t, 15.2, 15.6))
        sc = bump(t, 15.2, 0.12)
        c = f.c; c.save(); c.translate(W/2, 1100); c.scale(sc, sc)
        f.circle(0, 0, 190, SPARK, sa)
        f.circle(0, 0, 172, '#f6edc8', sa)
        for i in range(3):
            ang = math.radians(90 + i * 120)
            f.line([(0, 0), (120 * math.cos(ang), 120 * math.sin(ang))], '#e3d39c', sa, 5)
        da = sa * ease(seg(t, 16.2, 16.6))
        for i in range(9):
            ang = i * 2 * math.pi / 9
            f.circle(48 * math.cos(ang), 48 * math.sin(ang), 7, '#3a2a1a', da)
        f.circle(48 * math.cos(0), 0, 26 * (1 - seg(t, 16.2, 17.6)) + 7, SPARK, da * 0.5, stroke=4)
        c.restore()
        words(f, 'Ces points noirs ?', 1380, 56, 16.3, INK, t_out=20.5)
        words(f, 'Pas de vraies graines.', 1460, 56, 17.8, SPARK, t_out=20.5)

    # S4b — la preuve : on replante un rejet, copie de copie (20.8–30)
    if 20.7 <= t < 30.0:
        ga = ease(seg(t, 20.8, 21.2)) * (1 - seg(t, 29.4, 29.8))
        words(f, 'On replante un morceau', 440, 62, 20.9, INK, t_out=29.4)
        words(f, 'de la plante mère.', 520, 62, 21.4, MUTED, t_out=29.4, bold=False)
        rows = [1, 2, 4, 8]
        ys = [720, 880, 1040, 1200]
        n_total = 0
        for r, (n, y) in enumerate(zip(rows, ys)):
            t0 = 21.7 + r * 1.1
            s = 0.62 * (0.82 ** r)
            for k in range(n):
                tk = t0 + k * 0.08
                p = ease(seg(t, tk, tk + 0.3))
                if p > 0: n_total += 1 if p > 0.5 else 0
                x = W/2 + (k - (n - 1) / 2) * min(220, 900 / n)
                plant(f, x, y, s * (0.3 + 0.7 * p), ga * p, EARTH, sw)
            if r > 0:
                la = ga * ease(seg(t, t0 - 0.2, t0))
                f.line([(150, ys[r - 1] + 6), (150, y - 90)], LINE, la, 4)
        # compteur de plantes
        ca = ga * ease(seg(t, 21.7, 22.0))
        f.text('plantes', 150, 640, 30, MUTED, ca, MONO, False)
        f.text(str(max(1, n_total)), 150, 600, 58, SPARK, ca, MONO, True)
        words(f, 'Chaque plante est une copie.', 1360, 54, 26.6, INK, t_out=29.4)
        words(f, 'Même ADN.', 1460, 70, 27.6, SPARK, t_out=29.4)

    # S5 — la réponse (30–35.4)
    if 29.9 <= t < 35.4:
        a = ease(seg(t, 30.0, 30.3)) * (1 - seg(t, 34.8, 35.2))
        words(f, 'Résultat :', 560, 72, 30.0, INK, t_out=34.8)
        p = ease_io(seg(t, 30.4, 31.4))
        big_center(f, f'{int(round(99 * p))}%', 960, 320, SPARK, a, bump(t, 31.4, 0.14))
        words(f, 'des bananes exportées', 1150, 58, 31.6, INK, t_out=34.8)
        words(f, 'sont des Cavendish.', 1235, 58, 32.0, SPARK, t_out=34.8)
        words(f, 'USITC ; IFT', 1320, 32, 32.6, MUTED, t_out=34.8, font=MONO, bold=False)
        for i in range(5):
            banana(f, 200 + i * 170, 1460, 0.38, a * ease(seg(t, 32.4 + i * 0.1, 32.7 + i * 0.1)),
                   SPARK, math.radians(sw + i * 3))

    # S6 — le retournement : la Gros Michel, rayée par un champignon (35–48.4)
    if 35.0 <= t < 48.4:
        words(f, 'Le problème ?', 900, 140, 35.1, INK, t_out=37.1)
        ga = ease(seg(t, 37.3, 37.7)) * (1 - seg(t, 47.9, 48.3))
        if ga > 0:
            words(f, 'Avant, la banane star', 430, 60, 37.4, INK, t_out=47.9)
            words(f, 's’appelait Gros Michel.', 510, 60, 37.8, SPARK, t_out=47.9)
            ox, oy = 0, 0   # le foyer : en haut à gauche
            for r in range(3):
                for k in range(5):
                    x, y = 180 + k * 180, 760 + r * 170
                    d = math.hypot(k - ox, r - oy)
                    sick = ease(seg(t, 40.4 + d * 0.55, 41.0 + d * 0.55))
                    a = ga * ease(seg(t, 38.0 + (r * 5 + k) * 0.05, 38.3 + (r * 5 + k) * 0.05))
                    droop = 1 - 0.25 * sick
                    plant(f, x, y, 0.5 * droop, a * (1 - 0.35 * sick),
                          EARTH if sick < 0.5 else BROWN, sw * (1 - sick) + 30 * sick)
            # le champignon : une tache rouge qui part du foyer
            fa = ga * ease(seg(t, 40.0, 40.3)) * (1 - seg(t, 43.5, 44.0))
            f.circle(180, 770, 20 + 12 * math.sin(t * 8), RED, fa)
            f.text('maladie de Panama', W/2, 1180, 34, RED, ga * ease(seg(t, 40.2, 40.6)), MONO, True)
            words(f, 'Un champignon du sol.', 1300, 56, 40.0, INK, t_out=44.2)
            words(f, 'Mêmes gènes, même faiblesse.', 1390, 56, 41.8, SPARK, t_out=44.2)
            words(f, 'Fin des années 1950 :', 1300, 56, 44.6, INK, t_out=47.9)
            words(f, 'elle quitte les rayons.', 1390, 56, 45.2, SPARK, t_out=47.9)

    # S7 — l'escalade : la Cavendish menacée à son tour (48–56.4)
    if 48.0 <= t < 56.4:
        out = 1 - seg(t, 55.9, 56.3)
        words(f, 'Aujourd’hui, un nouveau', 440, 64, 48.1, INK, t_out=55.9)
        words(f, 'champignon attaque la Cavendish.', 520, 54, 48.6, INK, t_out=55.9)
        a = ease(seg(t, 49.2, 49.5)) * out
        sh = 10 * math.sin((t - 49.2) * 60) * (1 - seg(t, 49.2, 49.7))
        f.c.save(); f.c.translate(sh, 0)
        big_center(f, 'TR4', 760, 200, RED, a, bump(t, 49.2, 0.18))
        f.c.restore()
        a2 = ease(seg(t, 50.4, 50.7)) * out
        f.rect(240, 840, 600, 110, OCEAN, a2, 26)
        f.text('2019 : en Colombie', W/2, 912, 48, INK, a2, MONO, True)
        words(f, 'Il survit dans le sol', 1080, 54, 51.8, INK, t_out=55.9)
        p = ease_io(seg(t, 52.4, 53.6))
        ya = ease(seg(t, 52.2, 52.5)) * out
        big_center(f, f'{int(round(30 * p))} ans', 1250, 150, SPARK, ya, bump(t, 53.6, 0.14))
        f.text('au maximum', W/2, 1310, 34, MUTED, ya * ease(seg(t, 53.6, 53.9)), MONO, False)
        words(f, 'Les fongicides n’y font presque rien.', 1440, 46, 54.0, MUTED, t_out=55.9, bold=False)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        for i in range(5):
            banana(f, 200 + i * 170, 600, 0.38, ease(seg(t, 56.2 + i * 0.08, 56.5 + i * 0.08)),
                   SPARK, math.radians(sw + i * 3))
        words(f, 'Toutes identiques.', 780, 72, 56.3, INK)
        words(f, 'Toutes fragiles.', 880, 72, 57.6, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(240, 1040, 600, 150, OCEAN, a, 28)
        pa = 0.5 + 0.5 * math.sin((t - 60) * 3)
        f.rect(240, 1040, 600, 150, SPARK, a * 0.25 * pa, 28)
        f.text('Abonne-toi.', W/2, 1135, 62, INK, a)

def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    for i in range(4): ev.append((0.15 + i * 0.11, pop(420 + 40 * i, 0.09)))
    ev += [(1.2, ding(880, amp=0.22)), (2.4, clink(1900))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (3.9, 10.6, 12.5, 20.5, 29.6, 34.9, 47.9, 55.9)]
    ev += [(4.2, pop(330)), (5.0, rise(1.4, 300, 700, 0.06)), (6.9, pop(440)), (9.0, ding(660, amp=0.2)),
           (11.0, pop(520)), (11.4, pop(620))]
    ev += [(14.5, whoosh(0.3, 0.2)), (15.2, clink(2100)), (16.3, pop(440)), (17.8, ding(784, amp=0.2))]
    ev += [(20.9, pop(440))]
    for r in range(4): ev.append((21.7 + r * 1.1, pop(420 + r * 60)))
    ev += [(27.6, ding(988, amp=0.26))]
    ev += [(30.4, rise(1.0, 300, 900, 0.07)), (31.4, ding(1046, amp=0.28)), (35.1, pop(300, 0.15))]
    ev += [(37.4, pop(440)), (40.0, pop(250, 0.14)), (41.8, ding(330, amp=0.2)), (44.6, pop(400))]
    ev += [(48.1, pop(440)), (49.2, ding(330, amp=0.25)), (50.4, clink(1900))]
    x = 52.4
    while x < 53.6: ev.append((x, tick())); x += 0.1
    ev += [(53.6, ding(784, amp=0.2))]
    ev += [(56.3, pop(440)), (57.6, pop(550)), (60.0, ding(784, amp=0.22))]
    return ev
