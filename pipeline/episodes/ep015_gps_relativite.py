"""Ton GPS doit corriger la relativité d'Einstein. Même structure que le pilote.

Sources :
- R. Pogge, Ohio State University, « Real-World Relativity: The GPS Navigation System »
  (astronomy.ohio-state.edu/pogge.1/Ast162/Unit5/gps) : orbite à environ 20 000 km, environ 14 000 km/h ;
  vitesse : -7 µs/jour ; gravité : +45 µs/jour ; net : +38 µs/jour ; sans correction, erreurs qui
  s'accumulent d'environ 10 km par jour ; horloges réglées plus lentes avant le lancement.
- Penn State, GEOG 862 « The Satellite Clock » : -7 / +45 / +38 µs par jour ; horloges réglées à
  10,22999999543 MHz au sol pour donner 10,23 MHz en orbite.
- GPS World, « Inside the Box: GPS and Relativity » : mêmes valeurs ; sans correction, les distances
  seraient faussées d'un même écart, jusqu'à environ 11 km entre deux mises à jour quotidiennes.
- N. Ashby, « Relativity in the Global Positioning System », Living Reviews in Relativity 2003 :
  une erreur de 1 ns donne une erreur de position de l'ordre de 30 cm.
- Calcul : 38 µs × 299 792 km/s ≈ 11,4 km.
"""
import math
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro d'épisode.
COVER = dict(tag='Tech', l1='Ton GPS doit corriger', l2='la relativité d’Einstein')

BLUE = '#2f6f9a'

def earth(f, x, y, r, a):
    if a <= 0: return
    f.circle(x, y, r, '#163a55', a)
    c = f.c; c.save(); c.translate(x, y)
    for (dx, dy, rx, ry) in ((-0.35, -0.25, 0.32, 0.22), (0.25, 0.1, 0.28, 0.35), (-0.1, 0.45, 0.2, 0.12)):
        c.save(); c.translate(dx * r, dy * r); c.scale(rx * r, ry * r)
        f.color(EARTH, a * 0.85); c.new_sub_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.fill(); c.restore()
    c.restore()
    f.circle(x, y, r, BLUE, a * 0.6, stroke=4)

def satellite(f, x, y, s, a, rot=0.0):
    if a <= 0 or s <= 0: return
    c = f.c; c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    for side in (-1, 1):
        f.rect(side * 46 - (60 if side < 0 else 0), -20, 60, 40, BLUE, a, 4)
        for k in range(1, 3):
            xx = side * 46 - (60 if side < 0 else 0) + k * 20
            f.line([(xx, -20), (xx, 20)], DEEP, a * 0.7, 2)
    f.rect(-30, -28, 60, 56, SPARK, a, 8)
    f.line([(0, 28), (0, 46)], INK, a, 4)
    f.circle(0, 50, 8, INK, a)
    c.restore()

def phone(f, x, y, s, a, pin=1.0):
    if a <= 0: return
    c = f.c; c.save(); c.translate(x, y); c.scale(s, s)
    f.rect(-70, -130, 140, 260, INK, a, 22)
    f.rect(-60, -112, 120, 224, OCEAN, a, 12)
    for k in range(4):
        f.line([(-60, -80 + k * 56), (60, -60 + k * 50)], LINE, a, 3)
    if pin > 0:
        f.circle(0, -10, 22 * pin, RED, a)
        f.circle(0, -10, 8 * pin, INK, a)
    c.restore()

def clock(f, x, y, r, a, ang, col=INK):
    if a <= 0: return
    f.circle(x, y, r, OCEAN, a)
    f.circle(x, y, r, col, a, stroke=6)
    for k in range(12):
        q = k * math.pi / 6
        f.line([(x + 0.8 * r * math.cos(q), y + 0.8 * r * math.sin(q)),
                (x + 0.9 * r * math.cos(q), y + 0.9 * r * math.sin(q))], MUTED, a, 3)
    f.line([(x, y), (x + 0.75 * r * math.sin(ang), y - 0.75 * r * math.cos(ang))], col, a, 6)
    f.circle(x, y, 8, col, a)

def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.8, 30.2))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Pourquoi corriger le temps ?', W/2, 296, 46, SPARK, ha)

    # S1 — accroche (0–4) : la Terre et un satellite en orbite dès la première image
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        words(f, 'Ton GPS a besoin', 480, 92, 0.15, INK, t_out=o)
        words(f, 'd’Einstein.', 600, 110, 1.0, SPARK, t_out=o)
        earth(f, W/2, 1080, 190, fo)
        ang = -math.pi / 2 + t * 1.1
        f.circle(W/2, 1080, 330, LINE, fo * 0.8, stroke=3)
        sx, sy = W/2 + 330 * math.cos(ang), 1080 + 330 * math.sin(ang)
        satellite(f, sx, sy, 0.9 * bump(t, 2.2, 0.12), fo, ang + math.pi / 2)
        a = ease(seg(t, 2.2, 2.5)) * fo
        f.text('relativité', W/2, 1520, 44, MUTED, a, MONO, True)

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.0:
        words(f, 'La relativité,', 600, 80, 4.2, INK, t_out=6.7)
        words(f, 'ça semble abstrait.', 700, 72, 4.6, MUTED, t_out=6.7, bold=False)
        a = ease(seg(t, 4.4, 4.7)) * (1 - seg(t, 6.6, 6.9))
        clock(f, W/2, 1050, 170, a, t * 2.0)
        words(f, 'Pourtant, sans elle,', 640, 72, 6.9, INK, t_out=8.8)
        words(f, 'ton GPS se perdrait.', 740, 72, 7.3, SPARK, t_out=8.8)
        a = ease(seg(t, 7.0, 7.3)) * (1 - seg(t, 8.7, 9.0))
        dr = 160 * ease_io(seg(t, 7.6, 8.6))
        phone(f, W/2 + dr * 0.6, 1100 + dr * 0.3, 1.2, a)
        a = ease(seg(t, 9.0, 9.3)) * (1 - seg(t, 10.6, 10.9))
        f.text('Ton intuition :', W/2, 700, 56, MUTED, a, bold=False)
        c = f.c; c.save(); c.translate(W/2, 860); s = bump(t, 9.0); c.scale(s, s)
        f.text('Le temps passe', 0, 0, 96, INK, a); f.text('pareil partout.', 0, 110, 96, INK, a)
        c.restore()

    # S3 — la question (10.9–13.5)
    if 10.9 <= t < 13.6:
        words(f, 'Alors pourquoi', 820, 110, 11.0, INK, t_out=12.5)
        words(f, 'corriger le temps ?', 960, 96, 11.4, SPARK, t_out=12.5)

    # S4a — la preuve : le GPS mesure un temps de trajet (13.5–21)
    if 13.4 <= t < 21.0:
        ga = ease(seg(t, 13.5, 13.9)) * (1 - seg(t, 20.5, 20.9))
        words(f, 'Le satellite envoie l’heure.', 430, 64, 13.6, INK, t_out=20.5)
        satellite(f, W/2, 600, 1.0, ga, 0.15 * math.sin(t))
        phone(f, W/2, 1130, 0.9, ga)
        # impulsions qui descendent
        for k in range(3):
            p = ((t - 14.3 - k * 0.6) % 1.8) / 1.2
            if t > 14.3 + k * 0.6 and p <= 1:
                yy = lerp(660, 1000, p)
                f.c.save(); f.c.translate(W/2, yy); f.c.scale(1, 0.35)
                f.circle(0, 0, 40 + 60 * p, SPARK, ga * (1 - p) * 0.9, stroke=6)
                f.c.restore()
        words(f, 'Ton téléphone mesure', 1330, 56, 15.6, INK, t_out=17.7)
        words(f, 'le temps du trajet.', 1410, 56, 16.0, MUTED, t_out=17.7, bold=False)
        a = ga * ease(seg(t, 17.9, 18.2))
        f.rect(170, 1290, 740, 210, OCEAN, a, 28)
        f.text('1 milliardième de seconde', W/2, 1365, 46, INK, a)
        big_center(f, '= 30 cm', 1465, 80, SPARK, a, bump(t, 18.6, 0.14))

    # S4b — la preuve : deux horloges, deux temps (20.8–30)
    if 20.7 <= t < 30.0:
        ga = ease(seg(t, 20.8, 21.2)) * (1 - seg(t, 29.4, 29.8))
        words(f, 'Là-haut, le temps', 430, 72, 20.9, INK, t_out=29.4)
        words(f, 'ne passe pas pareil.', 520, 72, 21.4, SPARK, t_out=29.4)
        # deux horloges
        f.text('au sol', 290, 640, 36, MUTED, ga, MONO, True)
        f.text('à 20 000 km', 790, 640, 36, SPARK, ga, MONO, True)
        clock(f, 290, 790, 120, ga, t * 1.6, INK)
        clock(f, 790, 790, 120, ga, t * 1.6 + 0.4 * seg(t, 22, 29), SPARK)
        # bilan vitesse / gravité
        a1 = ga * ease(seg(t, 23.0, 23.3))
        f.text('Vitesse : 14 000 km/h', W/2, 1030, 46, INK, a1)
        p1 = ease_io(seg(t, 23.4, 24.2))
        f.rect(W/2 - 56 * p1, 1065, 56 * p1, 50, RED, a1, 8)
        f.text(f'-{int(round(7 * p1))} µs', W/2 - 76, 1104, 40, RED, a1, MONO, True, align='right')
        a2 = ga * ease(seg(t, 25.0, 25.3))
        f.text('Gravité plus faible', W/2, 1210, 46, INK, a2)
        p2 = ease_io(seg(t, 25.4, 26.6))
        f.rect(W/2, 1245, 8 * 45 * p2, 50, EARTH, a2, 8)
        f.text(f'+{int(round(45 * p2))} µs', W/2 - 20, 1284, 40, EARTH, a2, MONO, True, align='right')
        f.line([(W/2, 1058), (W/2, 1122)], MUTED, a1 * 0.7, 3)
        f.line([(W/2, 1238), (W/2, 1302)], MUTED, a2 * 0.7, 3)
        words(f, 'par jour', 1420, 48, 26.8, MUTED, t_out=29.4, font=MONO, bold=False)

    # S5 — la réponse (30–35.4)
    if 29.9 <= t < 35.4:
        a = ease(seg(t, 30.0, 30.3)) * (1 - seg(t, 34.8, 35.2))
        words(f, 'Bilan :', 560, 72, 30.0, INK, t_out=34.8)
        p = ease_io(seg(t, 30.4, 31.4))
        big_center(f, f'+{int(round(38 * p))}µs', 960, 200, SPARK, a, bump(t, 31.4, 0.14))
        words(f, 'd’avance par jour', 1150, 64, 31.6, INK, t_out=34.8)
        words(f, 'pour l’horloge du satellite.', 1240, 54, 32.0, MUTED, t_out=34.8, bold=False)
        words(f, 'Ohio State ; GPS World', 1340, 32, 32.6, MUTED, t_out=34.8, font=MONO, bold=False)

    # S6 — le retournement : 38 µs, c'est 11 km de lumière (35–48.4)
    if 35.0 <= t < 48.4:
        words(f, 'Le problème ?', 900, 120, 35.1, INK, t_out=37.1)
        ga = ease(seg(t, 37.3, 37.7)) * (1 - seg(t, 47.9, 48.3))
        if ga > 0:
            words(f, 'En 38 µs,', 450, 72, 37.4, INK, t_out=42.6)
            words(f, 'la lumière parcourt', 550, 64, 37.9, INK, t_out=42.6)
            p = ease_io(seg(t, 38.6, 40.0))
            a = ga * ease(seg(t, 38.5, 38.8)) * (1 - seg(t, 42.5, 42.8))
            big_center(f, f'{int(round(11 * p))} km', 820, 220, SPARK, a, bump(t, 40.0, 0.14))
            # rayon de lumière qui file
            f.line([(120, 940), (120 + 840 * p, 940)], SPARK, a, 8)
            f.circle(120 + 840 * p, 940, 14, INK, a)
            # carte : la vraie position et la position qui dérive
            ma = ga * ease(seg(t, 42.8, 43.2))
            words(f, 'Sans correction,', 450, 72, 42.9, INK, t_out=47.9)
            words(f, 'ta position dérive.', 550, 72, 43.3, SPARK, t_out=47.9)
            f.rect(140, 660, 800, 560, OCEAN, ma, 30)
            for k in range(1, 6):
                f.line([(140 + k * 133, 660), (140 + k * 133, 1220)], LINE, ma, 3)
            for k in range(1, 4):
                f.line([(140, 660 + k * 140), (940, 660 + k * 140)], LINE, ma, 3)
            f.circle(330, 1000, 22, EARTH, ma); f.circle(330, 1000, 8, INK, ma)
            f.text('toi', 330, 1060, 32, EARTH, ma, MONO, True)
            d = ease_io(seg(t, 43.8, 46.0))
            px, py = lerp(330, 760, d), lerp(1000, 820, d)
            f.line([(330, 1000), (px, py)], RED, ma * 0.8, 4, dash=[14, 10])
            f.circle(px, py, 22, RED, ma); f.circle(px, py, 8, INK, ma)
            ya = ga * ease(seg(t, 45.0, 45.3))
            f.text('≈ 10 km par jour', W/2, 1330, 64, RED, ya, MONO, True)
            f.text('Ohio State', W/2, 1400, 30, MUTED, ya, MONO, False)

    # S7 — l'escalade : chaque horloge est déréglée exprès avant le lancement (48–56.4)
    if 48.0 <= t < 56.4:
        out = 1 - seg(t, 55.9, 56.3)
        words(f, 'La parade :', 440, 72, 48.1, INK, t_out=55.9)
        words(f, 'des horloges déréglées exprès.', 530, 58, 48.6, SPARK, t_out=55.9)
        a = ease(seg(t, 49.4, 49.7)) * out
        lift = ease_io(seg(t, 52.6, 54.0))
        satellite(f, W/2, lerp(940, 790, lift), 1.1, a, 0.1 * math.sin(t * 2) * lift)
        f.text('au sol' if lift < 0.5 else 'en orbite', W/2, 690, 38, MUTED, a, MONO, True)
        f.rect(110, 1030 - 0 * lift, 860, 120, OCEAN, a, 26)
        if lift < 0.5:
            f.text('10,22999999543 MHz', W/2, 1110, 64, INK, a * (1 - seg(t, 52.8, 53.2)), MONO, True)
        else:
            c = f.c; c.save(); c.translate(W/2, 1110); s = bump(t, 53.4, 0.14); c.scale(s, s)
            f.text('10,23 MHz', 0, 0, 72, SPARK, a * seg(t, 53.2, 53.6), MONO, True); c.restore()
        words(f, 'Un peu trop lentes au sol,', 1300, 52, 50.4, INK, t_out=55.9)
        words(f, 'pile justes là-haut.', 1385, 56, 54.0, SPARK, t_out=55.9)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        phone(f, W/2, 560, 0.8, ease(seg(t, 56.1, 56.4)) * bump(t, 56.1, 0.1),
              pin=0.6 + 0.4 * ease(seg(t, 56.3, 56.8)))
        words(f, 'Einstein ?', 820, 80, 56.3, INK)
        words(f, 'Il est dans ta poche.', 920, 76, 57.6, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(240, 1040, 600, 150, OCEAN, a, 28)
        pa = 0.5 + 0.5 * math.sin((t - 60) * 3)
        f.rect(240, 1040, 600, 150, SPARK, a * 0.25 * pa, 28)
        f.text('Abonne-toi.', W/2, 1135, 62, INK, a)

def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    ev += [(0.15, pop(440, 0.09)), (1.0, ding(880, amp=0.22))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (3.9, 10.6, 12.5, 20.5, 29.6, 34.9, 47.9, 55.9)]
    ev += [(4.2, pop(330)), (6.9, pop(440)), (9.0, ding(660, amp=0.2)), (11.0, pop(520))]
    ev += [(13.6, pop(440)), (17.9, clink(1900)), (18.6, ding(784, amp=0.2))]
    ev += [(20.9, pop(440)), (23.4, pop(300, 0.12)), (25.4, rise(1.2, 300, 700, 0.06))]
    ev += [(30.4, rise(1.0, 300, 900, 0.07)), (31.4, ding(1046, amp=0.28)), (35.1, pop(300, 0.15))]
    ev += [(38.6, rise(1.4, 400, 1000, 0.06)), (40.0, ding(988, amp=0.24)), (42.9, pop(440)),
           (45.0, ding(330, amp=0.2))]
    ev += [(48.1, pop(440)), (53.4, ding(1046, amp=0.24))]
    ev += [(56.3, pop(440)), (57.6, pop(550)), (60.0, ding(784, amp=0.22))]
    return ev
