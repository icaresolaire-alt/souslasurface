"""Pourquoi la boîte de conserve est née avant l'ouvre-boîte. Même structure que le pilote.

Sources :
- Boîte en fer-blanc, 1810 : Guinness World Records « First tin-canned food » (« In 1810, Peter Durand (UK)...
  received the first patent for preserving food by heating it in a sealed container ») ; FoodIngredientsFirst
  « Canned food marks 200th anniversary » (brevet britannique n° 3372 du 25 août 1810) ; Bitesized Britain.
- Premières conserves pour la marine et l'armée britanniques (Donkin, Hall et Gamble, Bermondsey, 1812-1813) :
  Guinness (usine en 1813), FoodIngredientsFirst (« for the British Admiralty »), The Microbiologist
  (« supplying the navy »). Affiché sans date précise : « les marins et les soldats ».
- Ouverture au marteau et au burin : Invention & Technology, C. Wohleber, été 2000, « The Can Opener » (étiquette
  d'une boîte de veau rôti des expéditions Parry, années 1820 : « Cut round on the top with a chisel and hammer » ;
  soldats « attacked them with bayonets ») ; Smithsonian Magazine « Why the Can Opener Wasn't Invented Until
  Almost 50 Years After the Can » (« it was the manufacturer's suggested method »).
- Boîtes en fer forgé épaisses : Smithsonian (« made of wrought iron... lined with tin », « as thick as 3/16 of an
  inch » ≈ 4,8 mm) ; Invention & Technology (« heavy-gauge wrought iron that often weighed more than the food they
  contained »). Affiché : « parfois plus lourde que la nourriture ».
- Ouvre-boîte d'Ezra Warner, brevet du 5 janvier 1858 : Smithsonian et Invention & Technology. 1858 − 1810 = 48 ans
  (calcul). Nuance non affichée : FoodIngredientsFirst cite un ouvre-boîte de Robert Yeates (Londres) en 1855.
- Raison : acier plus fin à la fin des années 1850 : Smithsonian (« iron cans were just starting to be replaced by
  thinner steel cans ») et Invention & Technology (« in the late 1850s, when manufacturers became able to produce
  thinner cans from steel »).
- Roulette de William Lyman, 1870 : Smithsonian (« first to use a rotary cutter ») et Invention & Technology
  (« 1870 patent: He introduced the cutting wheel »).
"""
import math
import random
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro (ep039 précédent).
COVER = dict(tag='Histoire', l1='Pourquoi la boîte de conserve', l2='est née avant l’ouvre-boîte')

TIN = '#a7b1b8'
TIN2 = '#7d8a93'
TIN3 = '#d4dbe0'
WOOD = '#9a6b3f'
STEEL = '#c9d2d8'
FOOD = '#c0674a'


def ellipse(f, x, y, rx, ry, col, a):
    if a <= 0: return
    c = f.c; c.save(); c.translate(x, y); c.scale(1, ry / rx)
    f.color(col, a); c.arc(0, 0, rx, 0, 2 * math.pi); c.fill(); c.restore()


def can(f, x, y, w, h, a, label=True, lid=1.0, tilt=0.0):
    """Boîte de conserve vue de trois quarts ; (x, y) = centre du bas."""
    if a <= 0: return
    c = f.c; c.save(); c.translate(x, y); c.rotate(tilt)
    ry = w * 0.16
    ellipse(f, 0, 0, w / 2, ry, TIN2, a)
    f.rect(-w / 2, -h, w, h, TIN, a, 0)
    for k in range(1, 4):
        f.rect(-w / 2, -h + k * h / 4 - 3, w, 6, TIN2, a * 0.6, 0)
    if label:
        f.rect(-w / 2, -h * 0.72, w, h * 0.42, SPARK, a * 0.9, 0)
        f.text('VEAU', 0, -h * 0.45, w * 0.2, DEEP, a, DISPLAY, True)
    ellipse(f, 0, -h, w / 2, ry, TIN3, a)
    if lid < 1.0:
        ellipse(f, 0, -h, w / 2 * (1 - lid) + 1, ry * (1 - lid) + 1, FOOD, a)
    c.restore()


def hammer(f, x, y, ang, a):
    """Marteau qui pivote autour de son manche (x, y = tête)."""
    if a <= 0: return
    c = f.c; c.save(); c.translate(x, y); c.rotate(ang)
    f.rect(-10, 0, 20, 230, WOOD, a, 8)
    f.rect(-70, -40, 140, 60, STEEL, a, 10)
    c.restore()


def chisel(f, x, y, a):
    if a <= 0: return
    f.rect(x - 9, y - 210, 18, 120, WOOD, a, 6)
    f.rect(x - 7, y - 95, 14, 85, STEEL, a, 2)
    c = f.c; f.color(STEEL, a)
    c.move_to(x - 7, y - 10); c.line_to(x + 7, y - 10); c.line_to(x, y + 6); c.close_path(); c.fill()


def scale_beam(f, cx, cy, ang, a, left, right):
    """Balance : left / right = fonctions qui dessinent sur chaque plateau (x, y)."""
    if a <= 0: return
    f.rect(cx - 10, cy, 20, 260, LINE, a, 6)
    f.rect(cx - 120, cy + 250, 240, 24, LINE, a, 8)
    L = 330
    lx, ly = cx - L * math.cos(ang), cy - L * math.sin(ang)
    rx, ry = cx + L * math.cos(ang), cy + L * math.sin(ang)
    f.line([(lx, ly), (rx, ry)], MUTED, a, 12)
    for (px, py, fn) in ((lx, ly, left), (rx, ry, right)):
        f.line([(px, py), (px - 90, py + 150)], MUTED, a, 3)
        f.line([(px, py), (px + 90, py + 150)], MUTED, a, 3)
        f.rect(px - 120, py + 150, 240, 14, MUTED, a, 6)
        fn(px, py + 150)
    f.circle(cx, cy, 16, SPARK, a)


def wall(f, x, y, thick, h, a, col=TIN2):
    """Coupe d'une paroi de boîte, vue de près."""
    if a <= 0: return
    f.rect(x - thick / 2, y, thick, h, col, a, 4)


def wheel(f, x, y, r, ang, a):
    if a <= 0: return
    f.circle(x, y, r, STEEL, a)
    f.circle(x, y, r * 0.35, DEEP, a)
    for k in range(12):
        t = ang + k * math.pi / 6
        f.line([(x + r * 0.95 * math.cos(t), y + r * 0.95 * math.sin(t)),
                (x + (r + 14) * math.cos(t), y + (r + 14) * math.sin(t))], STEEL, a, 8)


def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')
    c = f.c

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.8, 30.2))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Comment l’ouvrir ?', W/2, 296, 46, SPARK, ha)

    # S1 — accroche (0–4) : la boîte arrive et oscille dès la première image
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        words(f, 'La boîte de conserve : 1810.', 460, 70, 0.05, INK, t_out=o)
        words(f, 'L’ouvre-boîte : 1858.', 570, 76, 1.2, SPARK, t_out=o)
        drop_in = 1 - ease(seg(t, 0.0, 0.9))
        can(f, W/2, 1260 - 500 * drop_in, 300, 380, fo, tilt=0.12 * math.sin(t * 3.0))
        f.text('?', W/2 + 230, 900, 120, SPARK, fo * ease(seg(t, 2.2, 2.6)), DISPLAY, True)

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.0:
        o1 = 7.4
        g1 = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'Une boîte', 470, 90, 4.2, INK, t_out=o1)
            words(f, 'impossible à ouvrir ?', 580, 84, 4.7, SPARK, t_out=o1)
            can(f, W/2, 1250, 300, 380, g1, tilt=0.06 * math.sin(t * 5))
            for k in range(3):
                p = ((t - 4.0) * 0.8 + k / 3) % 1.0
                f.circle(W/2 + 260 * math.cos(p * 6.28), 1060 + 60 * math.sin(p * 6.28),
                         10, MUTED, g1 * 0.6)
        o2 = 10.7
        g2 = ease(seg(t, 7.6, 8.0)) * (1 - seg(t, o2, o2 + 0.3))
        if g2 > 0:
            words(f, 'Ton intuition :', 480, 72, 7.7, MUTED, t_out=o2)
            words(f, 'personne n’y avait', 600, 80, 8.1, INK, t_out=o2)
            words(f, 'pensé.', 710, 80, 8.7, SPARK, t_out=o2)
            ab = g2 * ease(seg(t, 8.6, 8.9))
            for k in range(3):
                can(f, 260 + 280 * k, 1280 + 12 * math.sin(t * 2 + k), 200, 260, ab, tilt=0.05 * math.sin(t * 2 + k))

    # S3 — la question (10.9–13.6)
    if 10.9 <= t < 13.6:
        words(f, 'Alors comment', 820, 96, 11.0, INK, t_out=12.5)
        words(f, 'on l’ouvrait ?', 950, 116, 11.4, SPARK, t_out=12.5)

    # S4 — la preuve (13.5–30)
    if 13.4 <= t < 30.0:
        # A : au marteau et au burin (13.6–21.4)
        oa = 21.4
        ga = ease(seg(t, 13.5, 13.9)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Au marteau', 430, 90, 13.6, INK, t_out=oa)
            words(f, 'et au burin.', 540, 90, 14.1, SPARK, t_out=oa)
            # le burin tourne autour du couvercle, le marteau frappe
            prog = seg(t, 15.0, 20.5)
            lid_open = ease(prog)
            cx, cy = W/2 - 60, 1290
            can(f, cx, cy, 340, 300, ga, lid=lid_open)
            ang = math.pi * 1.1 + prog * math.pi * 1.6
            px = cx + 150 * math.cos(ang); py = cy - 300 + 26 * math.sin(ang)
            chisel(f, px, py, ga * ease(seg(t, 14.6, 15.0)))
            hit = (t * 2.4) % 1.0
            hang = -0.9 + 0.9 * (hit ** 3) if t > 15.0 else -0.9
            hammer(f, px + 150, py - 260, hang - 1.2, ga * ease(seg(t, 14.6, 15.0)))
            if t > 15.0 and hit > 0.9:
                f.circle(px, py - 215, 26, SPARK, ga * 0.7)
            words(f, 'C’était écrit sur l’étiquette :', 1415, 44, 16.6, MUTED, t_out=oa)
            words(f, '« couper le haut au burin', 1480, 50, 17.6, INK, t_out=oa)
            words(f, 'et au marteau »', 1540, 50, 18.2, INK, t_out=oa)
        # B : la boîte pèse plus que la nourriture (21.6–29.6)
        gb = ease(seg(t, 21.5, 21.9)) * (1 - seg(t, 29.4, 29.8))
        if gb > 0:
            words(f, 'La boîte en fer', 430, 84, 21.6, INK, t_out=29.3)
            words(f, 'pesait parfois plus', 540, 84, 22.1, INK, t_out=29.3)
            words(f, 'que la nourriture.', 650, 84, 22.7, SPARK, t_out=29.3)
            tip = -0.22 * ease_io(seg(t, 24.0, 25.6)) + 0.02 * math.sin(t * 3) * seg(t, 25.6, 26.0)
            sa = gb * ease(seg(t, 23.0, 23.4))

            def empty_can(x, y):
                can(f, x, y, 170, 200, sa, label=False)
                f.text('boîte vide', x, y + 70, 38, INK, sa, MONO, True)

            def food(x, y):
                for k in range(5):
                    f.circle(x - 70 + 35 * k, y - 22 - 8 * (k % 2), 30, FOOD, sa)
                f.text('contenu', x, y + 70, 38, INK, sa, MONO, True)
            scale_beam(f, W/2, 980, tip, sa, empty_can, food)
            f.text('fer forgé, paroi jusqu’à ~5 mm', W/2, 1440, 38, MUTED,
                   gb * ease(seg(t, 26.2, 26.5)), MONO, False)

    # S5 — la réponse (30–36)
    if 29.9 <= t < 36.0:
        o = 35.6
        a = ease(seg(t, 30.3, 30.6)) * (1 - seg(t, o, o + 0.3))
        words(f, '1810 → 1858', 580, 76, 30.0, MUTED, t_out=o, font=MONO)
        big_center(f, '48', 870, 300, SPARK, a, bump(t, 30.3, 0.18))
        words(f, 'ans sans ouvre-boîte.', 1050, 76, 31.0, INK, t_out=o)
        words(f, 'brevet d’Ezra Warner, 5 janvier 1858', 1200, 36, 32.5, MUTED, t_out=o, font=MONO, bold=False)

    # S6 — le retournement (36–48.4)
    if 36.0 <= t < 48.4:
        words(f, 'Pourquoi ?', 900, 150, 36.1, SPARK, t_out=37.9)
        # A : paroi épaisse, l'outil rebondit (38.1–42.6)
        oa = 42.6
        ga = ease(seg(t, 38.1, 38.5)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Le fer forgé', 440, 90, 38.2, INK, t_out=oa)
            words(f, 'était trop épais.', 550, 84, 38.7, RED, t_out=oa)
            wall(f, W/2, 760, 120, 560, ga)
            bounce = abs(math.sin((t - 38.6) * 4.0)) if t > 38.6 else 1.0
            bx = W/2 - 80 - 160 * bounce
            c.save(); c.translate(bx, 1040); c.rotate(-math.pi / 2)
            chisel(f, 0, 0, ga); c.restore()
            f.text('l’outil ne mord pas', W/2, 1420, 44, MUTED, ga * ease(seg(t, 39.8, 40.1)), MONO, False)
        # B : l'acier plus fin, la lame passe (42.9–47.9)
        ob = 47.9
        gb = ease(seg(t, 42.8, 43.2)) * (1 - seg(t, ob, ob + 0.3))
        if gb > 0:
            words(f, 'Fin des années 1850 :', 440, 76, 42.9, INK, t_out=ob)
            words(f, 'l’acier, bien plus fin.', 550, 84, 43.4, SPARK, t_out=ob)
            cut = ease_io(seg(t, 44.3, 46.3))
            wall(f, W/2, 760, 24, 560, gb, STEEL)
            for k in range(3):
                q = ((t * 1.5) + k / 3) % 1.0
                f.circle(W/2 + 60 + 50 * q, 760 + 560 * cut - 30 * q, 6, SPARK, gb * (1 - q) * (0 < cut < 1))
            wheel(f, W/2, 760 + 560 * cut, 70, t * 4, gb * ease(seg(t, 44.0, 44.3)))
            f.text('enfin un outil possible', W/2, 1420, 48, SPARK, gb * ease(seg(t, 46.0, 46.3)), MONO, True)

    # S7 — l'escalade (48–56.4) : frise
    if 48.0 <= t < 56.4:
        o = 55.9
        ga = ease(seg(t, 48.1, 48.4)) * (1 - seg(t, o, o + 0.3))
        if ga > 0:
            words(f, 'Ensuite,', 430, 84, 48.1, INK, t_out=o)
            words(f, 'tout s’accélère.', 540, 84, 48.6, SPARK, t_out=o)
            prog = ease_io(seg(t, 49.2, 54.0))
            y0 = 760; y1 = 1440
            f.line([(220, y0), (220, y0 + (y1 - y0) * prog)], LINE, ga, 10)
            items = [(0.0, '1810', 'la boîte', 49.2), (0.5, '1858', 'le levier qui perce', 51.0),
                     (1.0, '1870', 'la roulette qui tourne', 53.0)]
            for (u, yr, lab, ts) in items:
                ia = ga * ease(seg(t, ts, ts + 0.3))
                yy = y0 + (y1 - y0) * u
                f.circle(220, yy, 26 * bump(t, ts, 0.3), SPARK, ia)
                f.text(yr, 300, yy + 18, 64, SPARK, ia, MONO, True, align='left')
                f.text(lab, 300, yy + 80, 46, INK, ia, DISPLAY, True, align='left')
            wheel(f, 860, y1 - 20, 60, t * 3, ga * ease(seg(t, 53.3, 53.6)))
            f.text('brevet de William Lyman', 300, y1 + 135, 32, MUTED,
                   ga * ease(seg(t, 53.6, 53.9)), MONO, False, align='left')

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        a = ease(seg(t, 56.1, 56.4))
        can(f, W/2, 780, 220, 260, a, lid=0.85, tilt=0.04 * math.sin(t * 2))
        words(f, 'L’ouvre-boîte n’était pas en retard.', 920, 54, 56.3, INK)
        words(f, 'La boîte était trop dure.', 1020, 74, 57.6, SPARK)
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
    ev += [(15.4, clink())]
    ev += [(30.3, ding(1046, amp=0.28)), (36.1, pop(300, 0.15))]
    ev += [(46.0, ding(784, amp=0.18))]
    ev += [(56.3, pop(440)), (60.0, ding(784, amp=0.22))]
    return ev
