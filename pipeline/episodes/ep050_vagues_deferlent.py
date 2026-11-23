"""Pourquoi les vagues cassent en arrivant sur la plage. Même structure que le pilote.

Sources :
- NOAA Ocean Explorer « What causes ocean waves? » (oceanexplorer.noaa.gov/facts/waves.html) :
  « The only thing waves do transmit across the sea is energy », « the water in waves doesn't travel
  much at all », mouvement circulaire ; près du bord, le fond « causes the lower portion of the wave to
  slow down and compress, forcing the wave's crest higher ».
- P. Webb, Introduction to Oceanography, 10.3 « Waves on the Shore » (LibreTexts / RWU) : la vague
  touche le fond à une profondeur égale à la moitié de sa longueur d'onde ; elle ralentit, se resserre
  et grandit ; « the bottom of the wave begins to slow down before the top of the wave », la crête
  passe devant et n'a plus d'eau dessous.
- Vitesse en eau peu profonde c = racine(g × profondeur) : Bosboom et Stive, Coastal Dynamics, 5.2.5
  (« shallow water speed c = sqrt(gh) ») et NOAA JetStream « Tsunami Propagation » (même formule en
  mots). Calculs : 10 m -> 9,9 m/s = 35,7 km/h (affiché ≈ 36) ; 1 m -> 3,13 m/s = 11,3 km/h (≈ 11).
- Critère de déferlement H ≈ 0,78 × profondeur : McCowan 1894, cité par RWU Pressbooks « Breaking
  Waves » (H = 0.78h) ; Bosboom et Stive (γ ≈ 0,78, moyenne « ca. 0.8 ») ; D. Apsley, Univ. de
  Manchester, cours « Wave Transformation » (γ_b = 0,78 sur pente douce). Exemple calculé :
  1,5 / 0,78 = 1,9 m, affiché « environ 2 m ». Mécanisme : l'eau de la crête va plus vite que la
  vague (Bosboom et Stive, Apsley).
- Tsunami : NOAA JetStream (« as fast as a jet plane, over 500 mph (800 km/h) », rarement plus d'un
  mètre au large, ralentit à 30-50 km/h près des côtes et grandit) ; Humboldt State, Redwood Coast
  Tsunami Work Group FAQ (« about as fast as a jet airplane, traveling around 500 miles per hour »,
  25 à 30 mph près des côtes). Pas de drame humain affiché.
"""
import math
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro (ep049 précédent = cinema).
COVER = dict(tag='Mer', l1='Pourquoi les vagues', l2='cassent sur la plage')

SEA = '#1d5a7a'
SEA2 = '#2b7a9a'
SAND = '#b89a62'
FOAM = '#eaf1ec'


def poly(f, pts, col, a):
    if a <= 0: return
    c = f.c; f.color(col, a)
    for i, (x, y) in enumerate(pts):
        (c.move_to if i == 0 else c.line_to)(x, y)
    c.close_path(); c.fill()


def bed_y(x, y_deep, y_shore, x0=140, x1=940):
    """Fond marin qui remonte vers la plage (à droite)."""
    u = clamp((x - x0) / (x1 - x0))
    return lerp(y_deep, y_shore, u ** 1.6)


def sea_scene(f, a, t, y_surf, y_deep, y_shore, xc=None, h=0.0, w=80, skew=0.0, x0=140, x1=940):
    """Vue en coupe : eau, fond, une vague centrée en xc de hauteur h (px)."""
    if a <= 0: return
    xs = [x0 + i * 8 for i in range(int((x1 - x0) / 8) + 1)]
    surf = []
    for x in xs:
        y = y_surf + 6 * math.sin(x * 0.03 - t * 3)
        if xc is not None:
            d = (x - xc) / w
            dd = d * (1 + skew * 2.5) if d > 0 else d / (1 + skew)  # front raide vers la plage
            y -= h * math.exp(-dd * dd)
        surf.append((x, min(y, bed_y(x, y_deep, y_shore, x0, x1) - 4)))
    bed = [(x, bed_y(x, y_deep, y_shore, x0, x1)) for x in reversed(xs)]
    poly(f, surf + bed, SEA, a * 0.9)
    sand = [(x, bed_y(x, y_deep, y_shore, x0, x1)) for x in xs] + [(x1, y_deep + 40), (x0, y_deep + 40)]
    poly(f, sand, SAND, a)
    f.line(surf, FOAM, a * 0.7, 5)


def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.8, 30.2))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Pourquoi elle casse ?', W/2, 296, 46, SPARK, ha)

    # S1 — accroche (0–4) : une vague file vers la plage dès la première image
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        words(f, 'Une vague ne casse pas.', 440, 76, 0.05, INK, t_out=o)
        words(f, 'Elle trébuche.', 550, 92, 0.6, SPARK, t_out=o)
        u = ease_io(seg(t, 0, 3.8))
        xc = lerp(220, 800, u)
        sea_scene(f, fo, t, 980, 1450, 1000, xc, lerp(60, 200, u ** 2), lerp(110, 70, u), skew=u * 1.2)

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.0:
        o1 = 7.6
        g1 = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'Au large, elle roule.', 440, 76, 4.2, INK, t_out=o1)
            words(f, 'Sans jamais casser.', 550, 76, 4.9, SPARK, t_out=o1)
            # houle régulière en pleine mer
            for k in range(3):
                pts = [(x, 1000 + k * 140 + 40 * math.sin(x * 0.012 - (t - 4) * 2.2 + k))
                       for x in range(140, 945, 10)]
                f.line(pts, SEA2 if k else FOAM, g1 * (0.9 - 0.25 * k), 10 - 2 * k)
            f.text('pleine mer', W/2, 1480, 42, MUTED, g1 * ease(seg(t, 5.6, 5.9)), DISPLAY, True)
        o2 = 10.7
        g2 = ease(seg(t, 7.8, 8.2)) * (1 - seg(t, o2, o2 + 0.3))
        if g2 > 0:
            words(f, 'Près du bord,', 440, 84, 7.9, INK, t_out=o2)
            words(f, 'elle s’écroule.', 550, 84, 8.5, RED, t_out=o2)
            u = ease_io(seg(t, 8.0, 10.6))
            sea_scene(f, g2, t, 980, 1300, 960, lerp(300, 820, u), lerp(80, 180, u), 90, skew=u * 1.4)
            # écume qui jaillit
            for i in range(7):
                p = seg(t, 9.8 + 0.06 * i, 10.5 + 0.06 * i)
                if p > 0:
                    ang = -math.pi * (0.2 + 0.09 * i)
                    f.circle(820 + 140 * p * math.cos(ang), 800 + 160 * p * math.sin(ang) + 200 * p * p,
                             12 - 5 * p, FOAM, g2 * (1 - p))

    # S3 — la question (10.9–13.6)
    if 10.9 <= t < 13.6:
        words(f, 'Pourquoi', 820, 120, 11.0, INK, t_out=12.5)
        words(f, 'elle casse ?', 950, 120, 11.4, SPARK, t_out=12.5)

    # S4 — la preuve (13.5–30)
    if 13.4 <= t < 30.0:
        # A : l'eau tourne sur place (13.6–21.6)
        oa = 21.6
        ga = ease(seg(t, 13.5, 13.9)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'D’abord, l’eau ne voyage pas.', 430, 64, 13.6, INK, t_out=oa)
            words(f, 'Elle tourne sur place.', 530, 70, 14.4, SPARK, t_out=oa)
            ph = (t - 13.6) * 1.9
            ys = 980
            pts = [(x, ys - 70 * math.sin(x * 0.0105 - ph)) for x in range(140, 945, 8)]
            poly(f, pts + [(940, 1500), (140, 1500)], SEA, ga * 0.9)
            f.line(pts, FOAM, ga * 0.7, 5)
            # bouchons qui tournent en rond, de plus en plus petits en profondeur
            for row, (yy, r) in enumerate(((ys, 70), (ys + 190, 38), (ys + 340, 18))):
                for x0 in (300, 540, 780):
                    ang = x0 * 0.0105 - ph
                    cx, cy = x0 + r * math.cos(ang), yy - r * math.sin(ang)
                    f.circle(x0, yy, r, INK, ga * 0.35 * ease(seg(t, 15.5, 16.0)), stroke=3)
                    f.circle(cx, cy, 16 if row == 0 else 11, SPARK, ga)
            f.text('ce qui avance, c’est l’énergie', W/2, 1440, 44, MUTED,
                   ga * ease(seg(t, 17.2, 17.5)), DISPLAY, True)
            f.text('NOAA', W/2, 1510, 30, MUTED, ga * ease(seg(t, 17.6, 17.9)), MONO, False)
        # B : le fond remonte, la vague ralentit (21.8–29.6)
        ob = 29.4
        gb = ease(seg(t, 21.7, 22.1)) * (1 - seg(t, ob, ob + 0.3))
        if gb > 0:
            words(f, 'Puis le fond remonte.', 430, 76, 21.8, INK, t_out=ob)
            words(f, 'Et la vague ralentit.', 540, 76, 22.5, SPARK, t_out=ob)
            u = ease_io(seg(t, 23.4, 28.4))
            x0, x1, yd, ysh = 140, 940, 1300, 940
            xc = lerp(240, 820, u)
            sea_scene(f, gb, t, 900, yd, ysh, xc, lerp(50, 120, u), lerp(110, 75, u), skew=u * 0.6)
            # profondeur sous la crête : 10 m -> 1 m
            depth = lerp(10, 1, u)
            v = math.sqrt(9.81 * depth) * 3.6
            ya = 1400
            f.text('profondeur', 300, ya, 36, MUTED, gb, DISPLAY, True)
            f.text(f'{depth:.0f} m', 300, ya + 80, 72, INK, gb, MONO, True)
            f.text('vitesse', 780, ya, 36, MUTED, gb, DISPLAY, True)
            f.text(f'≈ {v:.0f} km/h', 780, ya + 80, 72, SPARK, gb * bump(t, 28.4, 0.12), MONO, True)
            f.line([(xc, 900 - lerp(50, 120, u) - 30), (xc, bed_y(xc, yd, ysh))], INK, gb * 0.5, 3, dash=[10, 10])

    # S5 — la réponse (30–36)
    if 29.9 <= t < 36.0:
        o = 35.6
        a = ease(seg(t, 30.3, 30.6)) * (1 - seg(t, o, o + 0.3))
        words(f, 'Elle casse quand sa hauteur', 520, 64, 30.0, MUTED, t_out=o)
        words(f, 'atteint environ', 610, 64, 30.4, MUTED, t_out=o)
        big_center(f, '78 %', 900, 280, SPARK, a, bump(t, 30.6, 0.18), font=DISPLAY)
        words(f, 'de la profondeur.', 1040, 72, 31.4, INK, t_out=o)
        f.rect(170, 1150, 740, 190, OCEAN, a * ease(seg(t, 32.6, 32.9)) * 0.9, 28)
        words(f, 'Une vague de 1,5 m', 1230, 54, 32.8, INK, t_out=o)
        words(f, 'casse dans environ 2 m d’eau.', 1300, 54, 33.3, SPARK, t_out=o)
        f.text('McCowan, 1894', W/2, 1420, 34, MUTED, a * ease(seg(t, 34.0, 34.3)), MONO, False)

    # S6 — le retournement (36–48.4)
    if 36.0 <= t < 48.4:
        words(f, 'Le secret ?', 900, 120, 36.1, SPARK, t_out=37.9)
        # A : les pieds freinent, la tête continue (38.1–43.4)
        oa = 43.4
        ga = ease(seg(t, 38.1, 38.5)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Ses pieds freinent', 430, 80, 38.2, INK, t_out=oa)
            words(f, 'sur le fond.', 540, 80, 38.7, SPARK, t_out=oa)
            u = ease_io(seg(t, 39.0, 42.6))
            sea_scene(f, ga, t, 1150, 1460, 1300, 520 + 60 * u, 230, 120, skew=0.3 + 1.0 * u)
            # flèches : bas lent, haut rapide
            pa = ga * ease(seg(t, 39.6, 40.0))
            f.line([(420, 1340), (500, 1340)], INK, pa, 8)
            f.line([(485, 1325), (500, 1340), (485, 1355)], INK, pa, 8)
            f.text('lent', 460, 1400, 38, INK, pa, DISPLAY, True)
            pb = ga * ease(seg(t, 40.6, 41.0))
            L = 120 + 120 * u
            f.line([(480, 870), (480 + L, 870)], SPARK, pb, 8)
            f.line([(465 + L, 855), (480 + L, 870), (465 + L, 885)], SPARK, pb, 8)
            f.text('rapide', 480 + L / 2, 830, 38, SPARK, pb, DISPLAY, True)
        # B : le sommet n'a plus rien dessous (43.6–47.9)
        ob = 47.9
        gb = ease(seg(t, 43.5, 43.9)) * (1 - seg(t, ob, ob + 0.3))
        if gb > 0:
            words(f, 'Le sommet passe devant.', 430, 72, 43.6, INK, t_out=ob)
            words(f, 'Rien dessous : il tombe.', 540, 72, 44.2, SPARK, t_out=ob)
            sea_scene(f, gb, t, 1200, 1460, 1340, 520, 250, 120, skew=1.6)
            # lèvre qui s'enroule et retombe
            p = ease_io(seg(t, 44.6, 46.6))
            cx, cy, R = 610, 1050, 105
            ang_end = -math.pi / 2 + p * math.pi * 1.05
            arc = [(cx + R * math.cos(-math.pi / 2 + k / 20 * (ang_end + math.pi / 2)) * 1.0,
                    cy + R * math.sin(-math.pi / 2 + k / 20 * (ang_end + math.pi / 2)))
                   for k in range(21)]
            f.line([(520, 948)] + arc, FOAM, gb, 40)
            f.line([(520, 948)] + arc, SEA, gb, 24)
            q = seg(t, 46.4, 47.4)
            for i in range(8):
                if q > 0:
                    f.circle(cx + 40 + 22 * i * q, cy + 90 + 120 * q - 30 * math.sin(i), 14 * (1 - q * 0.6),
                             FOAM, gb * (1 - q * 0.5))

    # S7 — l'escalade (48–56.4) : le tsunami
    if 48.0 <= t < 56.4:
        o1 = 55.9
        g1 = ease(seg(t, 48.1, 48.4)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'Même règle pour un tsunami.', 430, 64, 48.1, INK, t_out=o1)
            u = ease_io(seg(t, 49.0, 54.4))
            xc = lerp(220, 840, u)
            sea_scene(f, g1, t, 820, 1200, 860, xc, lerp(20, 150, u ** 2.2), lerp(220, 90, u), skew=u * 0.4)
            # avion au-dessus au début
            pa = g1 * (1 - seg(t, 51.0, 51.4)) * ease(seg(t, 49.0, 49.4))
            xp = lerp(160, 500, seg(t, 49.0, 51.4))
            f.rect(xp, 610, 120, 22, INK, pa, 11)
            f.rect(xp + 40, 590, 30, 62, INK, pa, 6)
            f.text('aussi vite qu’un avion', 640, 640, 36, MUTED, pa, DISPLAY, True)
            ya = 1300
            fa = g1 * ease(seg(t, 49.2, 49.5))
            f.text('au large', 300, ya, 36, MUTED, fa, DISPLAY, True)
            f.text('≈ 800 km/h', 300, ya + 76, 60, INK, fa, MONO, True)
            f.text('moins d’1 m de haut', 300, ya + 140, 32, MUTED, fa, DISPLAY, True)
            fb = g1 * ease(seg(t, 52.6, 52.9))
            f.text('près du bord', 780, ya, 36, MUTED, fb, DISPLAY, True)
            f.text('30-50 km/h', 780, ya + 76, 60, SPARK, fb * bump(t, 52.6, 0.12), MONO, True)
            f.text('et il grandit', 780, ya + 140, 32, SPARK, fb, DISPLAY, True)
            f.text('NOAA', W/2, 1530, 30, MUTED, g1 * ease(seg(t, 53.4, 53.7)), MONO, False)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        a = ease(seg(t, 56.1, 56.4))
        u = ease_io(seg(t, 56.1, 59.6))
        sea_scene(f, a, t, 820, 1000, 760, lerp(260, 800, u), lerp(40, 120, u), lerp(100, 70, u), skew=u * 1.3,)
        words(f, 'Une vague ne casse pas de fatigue.', 1100, 52, 56.3, INK)
        words(f, 'Elle trébuche sur le fond.', 1180, 66, 57.8, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(240, 1270, 600, 150, OCEAN, a, 28)
        pa = 0.5 + 0.5 * math.sin((t - 60) * 3)
        f.rect(240, 1270, 600, 150, SPARK, a * 0.25 * pa, 28)
        f.text('Abonne-toi.', W/2, 1365, 62, INK, a)


def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    ev += [(0.15, rise(1.2, 300, 900, 0.07))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (12.5, 29.6, 47.9, 55.9)]
    ev += [(11.0, pop(520))]
    ev += [(30.6, ding(1046, amp=0.28)), (36.1, pop(300, 0.15))]
    ev += [(46.4, clink())]
    ev += [(56.3, pop(440)), (60.0, ding(784, amp=0.22))]
    return ev
