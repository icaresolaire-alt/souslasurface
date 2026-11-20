"""Pourquoi une minute a 60 secondes (et pas 100). Même structure que le pilote.

Sources :
- Base 60 venue des Sumériens vers 2000 av. J.-C., reprise par les Babyloniens : Scientific American,
  M. Lombardi (NIST), « Why is a minute divided into 60 seconds, an hour into 60 minutes, yet there are
  only 24 hours in a day? » (« developed it around 2000 B.C. ») ; MacTutor (St Andrews) « Babylonian
  numerals » (« the sexagesimal system originated with the Sumerians ») ; Live Science, R. Coolman,
  « Keeping Time: Why 60 Minutes? » (« The use of 60 began with the Sumerians »).
- 60 divisible par 1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30 : Scientific American (« smallest number divisible
  by the first six counting numbers as well as by 10, 12, 15, 20 and 30 ») ; MacTutor (argument rapporté
  par Théon d'Alexandrie). 12 diviseurs pour 60, 4 pour 10 : calcul. On dit « une raison pratique » : la
  raison exacte du choix reste inconnue (Scientific American, MacTutor).
- Ptolémée, Almageste vers 150 apr. J.-C., degré coupé en 60 puis en 60 ; « partes minutae primae » →
  minute, « partes minutae secundae » → seconde : Scientific American ; Live Science (« subdivided degree
  coordinates into 60ths (minutes) and 60ths of 60ths (seconds) »).
- Minutes sur les horloges seulement vers la fin du XVIe siècle : Scientific American ; Live Science
  (« in practical use for only about 400 years »).
- Compter jusqu'à 12 avec le pouce sur les phalanges, fois 5 doigts = 60 : hypothèse (Live Science,
  « It is hypothesized… », d'après G. Ifrah ; MacTutor, conjecture). Affichée comme une piste. Main en schéma.
- Heure décimale : décret de la Convention en 1793 (10 heures, 100 minutes, 100 secondes), usage obligatoire
  suspendu le 7 avril 1795 : Mental Floss, C. Higgins, « Decimal Time: How the French Made a 10-Hour Day »
  (24 nov. 1793, non obligatoire au 7 avril 1795, 17 mois) ; Engadget, A. Tarantola, 17 janv. 2022 (« formally
  adopted by National Convention decree in 1793 », « officially suspended on April 7th, 1795 », les gens
  avaient déjà des horloges). 1 heure décimale = 2 h 24 : calcul (24 h / 10).
- Tablette et coins cunéiformes : illustratifs.
"""
import math
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro (ep046 précédent).
COVER = dict(tag='Histoire', l1='Pourquoi une minute a 60 secondes', l2='et pas 100')

DIVS = [2, 3, 4, 5, 6, 10, 12, 15, 20, 30]
PAL = [SPARK, INK, EARTH, RED]


def clock(f, cx, cy, R, a, ang, n=60, major=5, labels=None, hand_col=SPARK, lab_size=None):
    """Cadran : n graduations, aiguille à l'angle ang (0 = midi, sens horaire)."""
    if a <= 0: return
    f.circle(cx, cy, R, OCEAN, a)
    f.circle(cx, cy, R, LINE, a, stroke=8)
    for i in range(n):
        th = 2 * math.pi * i / n - math.pi / 2
        big = (i % major == 0)
        r1 = R - (40 if big else 20); r2 = R - 10
        f.line([(cx + r1 * math.cos(th), cy + r1 * math.sin(th)),
                (cx + r2 * math.cos(th), cy + r2 * math.sin(th))], INK if big else MUTED, a, 6 if big else 3)
    if labels:
        ls = lab_size or R * 0.17
        for i, s in enumerate(labels):
            th = 2 * math.pi * i / len(labels) - math.pi / 2
            rr = R - 80
            f.text(s, cx + rr * math.cos(th), cy + rr * math.sin(th) + ls * 0.36, ls, INK, a, MONO, True)
    th = ang - math.pi / 2
    f.line([(cx - 40 * math.cos(th), cy - 40 * math.sin(th)),
            (cx + (R - 50) * math.cos(th), cy + (R - 50) * math.sin(th))], hand_col, a, 9)
    f.circle(cx, cy, 16, hand_col, a)


def wedge(f, x, y, s, col, a, horiz=False):
    """Coin cunéiforme stylisé (triangle + trait)."""
    if a <= 0: return
    c = f.c; c.save(); c.translate(x, y)
    if horiz: c.rotate(-math.pi / 2)
    f.color(col, a)
    c.move_to(-s * 0.45, 0); c.line_to(s * 0.45, 0); c.line_to(0, s * 0.6); c.close_path(); c.fill()
    c.rectangle(-s * 0.07, s * 0.4, s * 0.14, s * 0.9); c.fill()
    c.restore()


def dots60(f, a, k, mix):
    """60 points en grille 10×6, regroupés en paquets de taille 60/k (couleurs alternées)."""
    size = 60 // k
    for i in range(60):
        gx, gy = i % 10, i // 10
        x = W / 2 - 4.5 * 82 + gx * 82; y = 840 + gy * 82
        col = PAL[(i // size) % len(PAL)] if k > 1 else INK
        f.circle(x, y, 26, col, a * (0.55 + 0.45 * mix))


def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')
    c = f.c

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.8, 30.2))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Pourquoi 60 et pas 100 ?', W/2, 296, 44, SPARK, ha)

    # S1 — accroche (0–4) : la trotteuse tourne dès la première image
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        words(f, 'Une minute :', 430, 92, 0.05, INK, t_out=o)
        words(f, '60 secondes.', 545, 100, 0.5, SPARK, t_out=o)
        clock(f, W/2, 1000, 300, fo, 2 * math.pi * (t * 3.2) / 60)
        f.text('Pas 100.', W/2, 1440, 72, RED, fo * ease(seg(t, 2.2, 2.5)), DISPLAY, True)

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.0:
        o1 = 7.5
        g1 = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'Tout le reste', 440, 92, 4.2, INK, t_out=o1)
            words(f, 'compte par 10.', 555, 92, 4.6, SPARK, t_out=o1)
            rows = [('1 m', '100 cm', 5.0), ('1 kg', '1 000 g', 5.5), ('1 €', '100 centimes', 6.0)]
            for i, (l, r, ts) in enumerate(rows):
                ra = g1 * ease(seg(t, ts, ts + 0.3))
                y = 820 + i * 170
                f.rect(140, y - 70, 800, 120, OCEAN, ra * 0.9, 24)
                f.text(l, 250, y + 12, 56, INK, ra, MONO, True)
                f.text('=', 380, y + 12, 56, MUTED, ra, MONO, True)
                f.text(r, 660, y + 12, 56, SPARK, ra * (0.5 + 0.5 * bump(t, ts, 1.0)), MONO, True)
        o2 = 10.7
        g2 = ease(seg(t, 7.7, 8.1)) * (1 - seg(t, o2, o2 + 0.3))
        if g2 > 0:
            words(f, 'Sauf le temps.', 460, 100, 7.8, INK, t_out=o2)
            f.rect(140, 760, 800, 120, OCEAN, g2 * 0.9, 24)
            f.text('1 h = 60 min', W/2, 842, 64, SPARK, g2 * ease(seg(t, 8.3, 8.6)), MONO, True)
            f.rect(140, 930, 800, 120, OCEAN, g2 * 0.9, 24)
            f.text('1 min = 60 s', W/2, 1012, 64, SPARK, g2 * ease(seg(t, 8.8, 9.1)), MONO, True)
            clock(f, W/2, 1330, 170, g2 * ease(seg(t, 9.2, 9.5)), 2 * math.pi * (t * 4) / 60, lab_size=1)

    # S3 — la question (10.9–13.6)
    if 10.9 <= t < 13.6:
        words(f, 'Pourquoi 60', 820, 110, 11.0, INK, t_out=12.5)
        words(f, 'et pas 100 ?', 950, 110, 11.4, SPARK, t_out=12.5)

    # S4 — la preuve (13.5–30)
    if 13.4 <= t < 30.0:
        # A : les Sumériens (13.6–20.8)
        oa = 20.8
        ga = ease(seg(t, 13.5, 13.9)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Il y a 4 000 ans,', 430, 80, 13.6, INK, t_out=oa)
            words(f, 'les Sumériens comptent par 60.', 540, 64, 14.2, SPARK, t_out=oa)
            # tablette d'argile qui se remplit de coins
            f.rect(200, 700, 680, 520, '#7a6248', ga, 40)
            f.rect(220, 720, 640, 480, '#94785a', ga, 32)
            for i in range(24):
                gx, gy = i % 6, i // 6
                ts = 15.0 + 0.12 * i
                wa = ga * ease(seg(t, ts, ts + 0.2))
                x = 300 + gx * 96; y = 760 + gy * 104
                wedge(f, x, y, 52, '#4b3a29', wa, horiz=(i * 7) % 3 == 0)
            f.text('(schéma)', W/2, 1290, 32, MUTED, ga * ease(seg(t, 16.0, 16.3)) * 0.8, MONO, False)
            f.text('vers 2000 av. J.-C.', W/2, 1400, 54, INK, ga * ease(seg(t, 17.6, 17.9)), MONO, True)
            words(f, 'Les Babyloniens', 1480, 46, 18.6, MUTED, t_out=oa)
            words(f, 'le reprennent.', 1540, 46, 19.0, MUTED, t_out=oa)
        # B : 60 se coupe de partout (21.0–29.6)
        gb = ease(seg(t, 20.9, 21.3)) * (1 - seg(t, 29.4, 29.8))
        if gb > 0:
            words(f, 'Le secret de 60 :', 430, 80, 21.0, INK, t_out=29.3)
            words(f, 'il se partage bien.', 540, 80, 21.5, SPARK, t_out=29.3)
            # parcourt les diviseurs : 2, 3, 4, 5, 6, 10, 12, 15, 20, 30
            u = seg(t, 22.4, 28.4) * len(DIVS)
            idx = min(len(DIVS) - 1, int(u))
            k = DIVS[idx] if t >= 22.4 else 1
            mix = 1 - abs(2 * (u - int(u)) - 1) * 0.3 if t >= 22.4 else 0
            dots60(f, gb, k, mix)
            if t >= 22.4:
                txt = f'60 ÷ {k} = {60 // k}'
                f.text(txt, W/2, 1430, 84, SPARK, gb * (0.7 + 0.3 * bump(t, 22.4 + idx * 0.6, 1.0)), MONO, True)

    # S5 — la réponse (30–36)
    if 29.9 <= t < 36.0:
        o = 35.6
        a = ease(seg(t, 30.3, 30.6)) * (1 - seg(t, o, o + 0.3))
        words(f, '60 a', 600, 80, 30.0, MUTED, t_out=o)
        big_center(f, '12', 880, 320, SPARK, a, bump(t, 30.3, 0.18), font=DISPLAY)
        words(f, 'diviseurs.', 1060, 96, 31.0, INK, t_out=o)
        f.rect(190, 1180, 700, 130, OCEAN, a * ease(seg(t, 32.4, 32.7)) * 0.9, 28)
        words(f, '10 n’en a que 4.', 1270, 64, 32.6, RED, t_out=o)

    # S6 — le retournement (36–48.4)
    if 36.0 <= t < 48.4:
        words(f, 'Et la seconde ?', 900, 116, 36.1, SPARK, t_out=37.9)
        # A : Ptolémée découpe en 60, puis encore en 60 (38.1–43.0)
        oa = 43.0
        ga = ease(seg(t, 38.1, 38.5)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Vers l’an 150,', 430, 80, 38.2, MUTED, t_out=oa)
            words(f, 'Ptolémée coupe en 60…', 540, 76, 38.6, INK, t_out=oa)
            # barre coupée en 60, puis un morceau zoomé recoupé en 60
            x0, x1 = 140, 940
            p1 = ease_io(seg(t, 39.2, 40.0))
            f.rect(x0, 760, x1 - x0, 80, OCEAN, ga, 12)
            for i in range(1, 60):
                if i / 60 <= p1:
                    xx = x0 + (x1 - x0) * i / 60
                    f.line([(xx, 764), (xx, 836)], MUTED if i % 5 else INK, ga, 2 if i % 5 else 4)
            hl = ga * ease(seg(t, 40.2, 40.5))
            f.rect(x0, 756, (x1 - x0) / 60, 88, SPARK, hl, 4)
            zp = ease_io(seg(t, 40.4, 41.0))
            f.line([(x0, 846), (x0, 960)], SPARK, hl * zp, 3)
            f.line([(x0 + (x1 - x0) / 60, 846), (x1, 960)], SPARK, hl * zp, 3)
            f.rect(x0, 960, (x1 - x0) * zp, 80, OCEAN, hl, 12)
            p2 = ease_io(seg(t, 41.0, 41.8))
            for i in range(1, 60):
                if i / 60 <= p2:
                    xx = x0 + (x1 - x0) * i / 60
                    f.line([(xx, 964), (xx, 1036)], MUTED if i % 5 else INK, hl, 2 if i % 5 else 4)
            f.text('…puis encore en 60.', W/2, 1140, 60, SPARK, ga * ease(seg(t, 41.0, 41.3)), DISPLAY, True)
            f.text('pars minuta prima → minute', W/2, 1300, 42, INK, ga * ease(seg(t, 41.8, 42.1)), MONO, True)
            f.text('pars minuta secunda → seconde', W/2, 1370, 42, SPARK, ga * ease(seg(t, 42.1, 42.4)), MONO, True)
        # B : une piste, compter sur ses doigts (43.2–47.9)
        ob = 47.9
        gb = ease(seg(t, 43.1, 43.5)) * (1 - seg(t, ob, ob + 0.3))
        if gb > 0:
            words(f, 'Une piste :', 430, 76, 43.2, MUTED, t_out=ob)
            words(f, 'compter sur ses doigts.', 540, 76, 43.6, INK, t_out=ob)
            # main gauche : 4 doigts × 3 phalanges, le pouce compte jusqu'à 12
            n12 = int(clamp((t - 44.2) / 1.6) * 12)
            for d in range(4):
                for p in range(3):
                    i = d * 3 + p
                    x = 180 + d * 92; y = 1040 - p * 96
                    on = i < n12
                    f.rect(x - 36, y - 42, 72, 84, SPARK if on else OCEAN, gb, 18)
            f.rect(130, 1100, 400, 120, OCEAN, gb, 30)
            f.text(str(max(n12, 0)), 330, 1290, 72, SPARK, gb * ease(seg(t, 44.2, 44.4)), MONO, True)
            # main droite : 5 doigts levés un à un
            n5 = int(clamp((t - 45.8) / 1.2) * 5)
            for d in range(5):
                x = 640 + d * 72; h = 260 if d < n5 else 110
                f.rect(x - 28, 1100 - h, 56, h, INK if d < n5 else OCEAN, gb, 26)
            f.rect(600, 1100, 360, 120, OCEAN, gb, 30)
            f.text('× ' + str(n5), 780, 1290, 72, INK, gb * ease(seg(t, 45.8, 46.0)), MONO, True)
            f.text('12 × 5 = 60', W/2, 1440, 76, SPARK, gb * ease(seg(t, 47.0, 47.3)), MONO, True)

    # S7 — l'escalade (48–56.4)
    if 48.0 <= t < 56.4:
        o1 = 52.4
        g1 = ease(seg(t, 48.1, 48.4)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, '1793 : la France', 430, 80, 48.1, INK, t_out=o1)
            words(f, 'passe au système 10.', 540, 80, 48.6, SPARK, t_out=o1)
            labels = [str(i) for i in range(10)]
            clock(f, W/2, 1000, 290, g1 * ease(seg(t, 49.0, 49.3)), 2 * math.pi * (t - 49) / 3.2,
                  n=100, major=10, labels=labels, lab_size=50)
            f.text('10 heures par jour', W/2, 1410, 50, INK, g1 * ease(seg(t, 49.8, 50.1)), DISPLAY, True)
            f.text('1 heure = 2 h 24', W/2, 1490, 50, SPARK, g1 * ease(seg(t, 50.6, 50.9)), MONO, True)
        o2 = 55.9
        g2 = ease(seg(t, 52.6, 52.9)) * (1 - seg(t, o2, o2 + 0.3))
        if g2 > 0:
            words(f, 'Abandonné', 440, 96, 52.7, INK, t_out=o2)
            words(f, 'en 1795.', 560, 96, 53.1, RED, t_out=o2)
            # les horloges décimales s'éteignent une à une
            for i in range(9):
                gx, gy = i % 3, i // 3
                x = W/2 - 260 + 260 * gx; y = 820 + 220 * gy
                off = seg(t, 53.6 + 0.12 * i, 53.9 + 0.12 * i)
                clock(f, x, y, 90, g2 * (1 - 0.75 * off), 2 * math.pi * (t * 0.3 + i / 9),
                      n=10, major=1, hand_col=SPARK if off < 0.5 else MUTED)
            f.text('Tout le monde avait déjà une horloge.', W/2, 1500, 42, MUTED,
                   g2 * ease(seg(t, 54.4, 54.7)), DISPLAY, True)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        a = ease(seg(t, 56.1, 56.4))
        clock(f, W/2, 780, 170, a, 2 * math.pi * (t - 56) * 4 / 60)
        words(f, 'Ta montre compte encore', 1030, 62, 56.3, INK)
        words(f, 'comme à Babylone.', 1120, 66, 57.8, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(240, 1220, 600, 150, OCEAN, a, 28)
        pa = 0.5 + 0.5 * math.sin((t - 60) * 3)
        f.rect(240, 1220, 600, 150, SPARK, a * 0.25 * pa, 28)
        f.text('Abonne-toi.', W/2, 1315, 62, INK, a)


def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    ev += [(0.15, rise(1.2, 300, 900, 0.07))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (12.5, 29.6, 47.9, 55.9)]
    ev += [(11.0, pop(520))]
    ev += [(30.3, ding(1046, amp=0.28)), (36.1, pop(300, 0.15))]
    ev += [(47.0, clink())]
    ev += [(56.3, pop(440)), (60.0, ding(784, amp=0.22))]
    return ev
