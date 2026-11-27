"""Pourquoi la tartine tombe côté beurre. Même structure que le pilote.

Sources :
- R. A. J. Matthews, « Tumbling toast, Murphy's Law and the fundamental constants », European Journal
  of Physics 16(4), 172-176, 1995 (texte intégral sur Fermat's Library) : table conventionnelle h ≈ 75 cm ;
  beurre ≈ 4 g contre ≈ 35 g pour la tranche ; il faudrait h ≈ 3 m pour éviter la face beurrée ;
  la taille humaine est limitée (≈ 3 m) par l'énergie d'une chute sur la tête, liée aux constantes
  fondamentales ; Robert Wadlow, 2,72 m, sous cette limite ; tests BBC « QED » 1991 : tartine lancée
  en l'air 300 fois, résultat indiscernable de 50/50.
- Wikipedia « Buttered toast phenomenon » : environ un demi-tour depuis une table, retombe à l'envers ;
  table de plus de 3 m (10 ft) = tour complet, côté beurre en haut ; effet du beurre négligeable
  (Ian Stewart) ; QED 1991 : lancée en l'air, côté beurre une fois sur deux ; Ig Nobel de physique 1996.
- BBC Science Focus (R. Matthews) : « nothing to do with one side being buttered » ; rotation trop lente
  pour remettre le beurre en haut ; 2001 : plus de 1 000 écoliers, « almost two-thirds of the time ».
- Gizmodo / io9 (E. Inglis-Arkell, 2011) : un millier d'enfants, 62 % côté beurre ; Seattle DJC
  « Strange But True! » (2010) : 62 %, demi-tour seulement ; Stackvenn (2026) : table d'environ 75 cm,
  demi-tour, il faudrait environ 3 m, 62 %, Ig Nobel 1996.
  Nombre de chutes non affiché (10 000, 9 821 ou 21 000 selon les sources).
"""
import math
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro (ep053 précédent).
COVER = dict(tag='Science', l1='Pourquoi ta tartine tombe', l2='côté beurre')

BREAD = '#d9a35f'
CRUMB = '#b97c3e'
BUTTER = '#ffe45c'
WOOD = '#6b4a35'
WOOD_D = '#4e3526'


def toast(f, cx, cy, ang, a, w=240, th=34):
    """Tartine vue de profil : pain + couche de beurre (en haut quand ang = 0). ang en degrés."""
    if a <= 0: return
    c = f.c
    c.save(); c.translate(cx, cy); c.rotate(math.radians(ang))
    f.rect(-w / 2, -th / 2, w, th, BREAD, a, 8)
    f.rect(-w / 2 + 6, -th / 2 + 6, w - 12, th - 12, CRUMB, a, 5)
    f.rect(-w / 2 + 4, -th / 2 - 12, w - 8, 14, BUTTER, a, 6)
    c.restore()


def table(f, x0, x1, top, floor, a):
    if a <= 0: return
    f.rect(x0, top, x1 - x0, 26, WOOD, a, 6)
    f.rect(x0 + 30, top + 26, 26, floor - top - 26, WOOD_D, a)
    f.rect(x1 - 56, top + 26, 26, floor - top - 26, WOOD_D, a)


def floor_line(f, y, a, x0=120, x1=960):
    f.line([(x0, y), (x1, y)], MUTED, a * 0.7, 4)


def fall(f, t, t0, dur, x_edge, top, floor, turns, a):
    """Tartine qui glisse du bord, bascule puis tombe en tournant ; renvoie l'angle courant."""
    p = seg(t, t0, t0 + dur)
    slide = ease(seg(p, 0, 0.25))
    q = seg(p, 0.25, 1.0)
    x = x_edge - 100 + 130 * slide + 60 * q
    y = top - 30 + (floor - 30 - (top - 30)) * q * q
    ang = 20 * slide + (turns * 360 - 20) * q
    toast(f, x, y, ang, a)
    return ang


def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')

    # question persistante
    ha = ease(seg(t, 12.8, 13.3)) * (1 - seg(t, 29.8, 30.2))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Pourquoi côté beurre ?', W/2, 296, 46, SPARK, ha)

    # S1 — accroche (0–4) : une tartine tombe dès la première image
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        words(f, 'Ta tartine tombe', 440, 84, 0.05, INK, t_out=o)
        words(f, 'côté beurre.', 550, 84, 0.6, SPARK, t_out=o)
        table(f, 160, 560, 900, 1400, fo)
        floor_line(f, 1400, fo)
        ang = fall(f, t, 0.0, 1.6, 560, 900, 1400, 0.5, fo)
        if t > 1.6:
            f.text('splatch', 720, 1300, 50, RED, fo * ease(seg(t, 1.6, 1.8)) * bump(t, 1.6, 0.2), DISPLAY, True)
        f.text('Ce n’est pas de la malchance.', W/2, 1500, 46, MUTED, fo * ease(seg(t, 2.2, 2.5)), DISPLAY, True)

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.2:
        o1 = 7.6
        g1 = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'On accuse le beurre,', 440, 76, 4.2, INK, t_out=o1)
            words(f, 'plus lourd.', 550, 76, 4.9, SPARK, t_out=o1)
            # balance : 35 g de pain contre 4 g de beurre
            tilt = 14 * ease_io(seg(t, 5.4, 6.6))
            cx, cy = W/2, 1000
            f.line([(cx, cy), (cx, cy + 300)], MUTED, g1, 8)
            dx = 300 * math.cos(math.radians(tilt)); dy = 300 * math.sin(math.radians(tilt))
            f.line([(cx - dx, cy - dy), (cx + dx, cy + dy)], INK, g1, 8)
            f.rect(cx - dx - 110, cy - dy - 60, 220, 60, BREAD, g1, 10)
            f.text('pain 35 g', cx - dx, cy - dy + 70, 40, INK, g1, DISPLAY, True)
            f.rect(cx + dx - 50, cy + dy - 30, 100, 30, BUTTER, g1, 8)
            f.text('beurre 4 g', cx + dx, cy + dy + 70, 40, SPARK, g1, DISPLAY, True)
        o2 = 10.9
        g2 = ease(seg(t, 7.8, 8.2)) * (1 - seg(t, o2, o2 + 0.3))
        if g2 > 0:
            words(f, 'Lance-la en l’air :', 440, 80, 7.9, INK, t_out=o2)
            words(f, '1 fois sur 2.', 550, 80, 8.5, RED, t_out=o2)
            p = seg(t, 8.0, 10.0)
            y = 1250 - 420 * math.sin(math.pi * p)
            toast(f, W/2, y, 720 * p + 30, g2)
            floor_line(f, 1290, g2)
            f.text('BBC, 1991 · 300 lancers', W/2, 1420, 34, MUTED, g2 * ease(seg(t, 9.4, 9.7)), MONO, False)

    # S3 — la question (11–13.8)
    if 11.0 <= t < 13.8:
        words(f, 'Le vrai coupable', 820, 110, 11.1, INK, t_out=12.7)
        words(f, 'est ailleurs.', 950, 110, 11.5, SPARK, t_out=12.7)

    # S4 — la preuve (13.6–30)
    if 13.5 <= t < 30.0:
        # A : elle bascule au bord (13.7–21.6)
        oa = 21.6
        ga = ease(seg(t, 13.6, 14.0)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Elle glisse de l’assiette', 430, 68, 13.7, INK, t_out=oa)
            words(f, 'et bascule au bord.', 530, 68, 14.4, SPARK, t_out=oa)
            table(f, 140, 600, 1000, 1480, ga)
            # boucle lente : glisse, bascule, se met à tourner, recommence
            cyc = (t - 15.0) % 3.2 if t > 15.0 else 0.0
            p = seg(cyc, 0, 2.4)
            slide = ease(seg(p, 0, 0.4))
            q = seg(p, 0.4, 1.0)
            x = 480 + 110 * slide + 50 * q
            y = 970 + 380 * q * q
            ang = 25 * slide + 160 * q
            toast(f, x, y, ang, ga * (1 - seg(cyc, 2.7, 3.1)))
            # flèche de rotation
            fa = ga * ease(seg(t, 16.4, 16.8))
            pts = [(760 + 120 * math.cos(math.radians(k)), 1060 + 120 * math.sin(math.radians(k))) for k in range(-80, 60, 5)]
            f.line(pts, SPARK, fa, 8)
            f.text('elle se met à tourner', W/2, 1580 - 60, 44, INK, ga * ease(seg(t, 17.2, 17.5)), DISPLAY, True)
        # B : le temps de tomber de 75 cm (21.8–29.6)
        ob = 29.4
        gb = ease(seg(t, 21.7, 22.1)) * (1 - seg(t, ob, ob + 0.3))
        if gb > 0:
            words(f, 'Mais elle tourne lentement.', 430, 64, 21.8, INK, t_out=ob)
            words(f, 'Et la table est basse.', 530, 64, 22.5, SPARK, t_out=ob)
            table(f, 140, 520, 800, 1400, gb)
            floor_line(f, 1400, gb)
            # cote de hauteur
            f.line([(220, 830), (220, 1390)], MUTED, gb, 3, dash=[10, 8])
            f.text('75 cm', 220, 1130, 40, INK, gb, MONO, True)
            ang = fall(f, t, 23.6, 2.6, 520, 800, 1400, 0.5, gb)
            deg = clamp(ang, 0, 180)
            f.rect(640, 830, 300, 120, OCEAN, gb * 0.9, 24)
            f.text(f'{int(round(deg))}°', 790, 912, 72, SPARK, gb, MONO, True)
            f.text('un demi-tour, puis le sol', W/2, 1520, 46, INK,
                   gb * ease(seg(t, 26.4, 26.7)) * bump(t, 26.4, 0.1), DISPLAY, True)

    # S5 — la réponse (30–36)
    if 29.9 <= t < 36.0:
        o = 35.6
        a = ease(seg(t, 30.3, 30.6)) * (1 - seg(t, o, o + 0.3))
        words(f, 'Le coupable :', 560, 72, 30.0, MUTED, t_out=o)
        big_center(f, 'ta table', 860, 210, SPARK, a, bump(t, 30.6, 0.18), font=DISPLAY)
        f.rect(150, 1040, 780, 230, OCEAN, a * ease(seg(t, 32.2, 32.5)) * 0.9, 28)
        words(f, 'Trop basse pour un tour', 1130, 56, 32.4, INK, t_out=o)
        words(f, 'complet.', 1210, 56, 32.9, SPARK, t_out=o)
        f.text('Matthews, Eur. J. Phys. 1995', W/2, 1360, 32, MUTED, a * ease(seg(t, 33.6, 33.9)), MONO, False)

    # S6 — le retournement (36–48.4)
    if 36.0 <= t < 48.4:
        words(f, 'Le secret ?', 900, 130, 36.1, SPARK, t_out=37.9)
        oa = 43.2
        ga = ease(seg(t, 38.1, 38.5)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Pour retomber côté pain,', 430, 66, 38.2, INK, t_out=oa)
            words(f, 'il faut une table de 3 m.', 530, 66, 38.9, SPARK, t_out=oa)
            # table géante, tour complet
            top, flo = 700, 1480
            f.rect(560, top, 240, 20, WOOD, ga, 6)
            f.rect(760, top + 20, 22, flo - top - 20, WOOD_D, ga)
            floor_line(f, flo, ga)
            f.line([(880, top + 20), (880, flo - 10)], MUTED, ga, 3, dash=[10, 8])
            f.text('3 m', 930, 1100, 40, INK, ga, MONO, True)
            p = ease_io(seg(t, 39.6, 41.8))
            ang = 360 * p
            toast(f, lerp(620, 470, p), lerp(top - 30, flo - 30, p * p), ang, ga)
            f.text('un tour complet', 380, 1560, 42, SPARK,
                   ga * ease(seg(t, 41.8, 42.1)) * bump(t, 41.8, 0.1), DISPLAY, True)
            # repère humain à l'échelle (1,8 m)
            hh = 780 * 1.8 / 3
            f.circle(300, flo - hh + 30, 30, MUTED, ga * 0.8)
            f.rect(278, flo - hh + 64, 44, hh - 64, MUTED, ga * 0.8, 18)
        ob = 47.9
        gb = ease(seg(t, 43.4, 43.8)) * (1 - seg(t, ob, ob + 0.3))
        if gb > 0:
            words(f, 'En 2001, un millier', 430, 66, 43.5, INK, t_out=ob)
            words(f, 'd’élèves font le test.', 530, 66, 44.1, INK, t_out=ob)
            p = ease_io(seg(t, 44.6, 46.4))
            f.rect(140, 760, 800, 90, OCEAN, gb, 45)
            f.rect(140, 760, 800 * 0.62 * p, 90, SPARK, gb, 45)
            big_center(f, f'{int(round(62 * p))} %', 1060, 170, SPARK, gb * ease(seg(t, 44.6, 44.9)), bump(t, 46.4, 0.16), font=DISPLAY)
            f.text('côté beurre', W/2, 1200, 56, INK, gb * ease(seg(t, 46.4, 46.7)), DISPLAY, True)
            f.text('presque 2 fois sur 3', W/2, 1300, 42, MUTED, gb * ease(seg(t, 46.8, 47.1)), DISPLAY, True)

    # S7 — l'escalade (48–56.4) : notre taille fixe celle des tables
    if 48.0 <= t < 56.4:
        o1 = 55.9
        g1 = ease(seg(t, 48.1, 48.4)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'Et des humains de 3 m ?', 430, 70, 48.1, INK, t_out=o1)
            words(f, 'Leur crâne casserait', 530, 64, 48.8, SPARK, t_out=o1)
            words(f, 'à la moindre chute.', 610, 64, 49.3, SPARK, t_out=o1)
            base = 1400
            p = ease_io(seg(t, 49.8, 51.8))
            for x, hm, lab, col in ((330, 1.8, '1,80 m', INK), (540, 2.72, '2,72 m', MUTED), (760, 3.0, '3 m', RED)):
                hh = 600 * hm / 3 * p
                if hh > 70:
                    f.circle(x, base - hh + 32, 32, col, g1 * 0.9)
                    f.rect(x - 26, base - hh + 70, 52, hh - 70, col, g1 * 0.9, 20)
                f.text(lab, x, base + 60, 40, col, g1 * ease(seg(t, 51.0, 51.3)), MONO, True)
            floor_line(f, base, g1)
            f.text('record humain : 2,72 m', W/2, 1520, 40, MUTED, g1 * ease(seg(t, 52.2, 52.5)), DISPLAY, True)
            f.text('Notre taille fixe celle des tables.', W/2, 740, 48, INK,
                   g1 * ease(seg(t, 53.4, 53.7)) * bump(t, 53.4, 0.1), DISPLAY, True)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        a = ease(seg(t, 56.1, 56.4))
        table(f, 300, 700, 560, 1000, a)
        floor_line(f, 1000, a)
        fall(f, t, 56.4, 1.8, 700, 560, 1000, 0.5, a)
        words(f, 'Ta tartine n’est pas maudite.', 1180, 56, 56.3, INK)
        words(f, 'Ta table est juste trop basse.', 1260, 56, 57.8, SPARK)
        a2 = ease(seg(t, 60.0, 60.4))
        f.rect(240, 1320, 600, 150, OCEAN, a2, 28)
        pa = 0.5 + 0.5 * math.sin((t - 60) * 3)
        f.rect(240, 1320, 600, 150, SPARK, a2 * 0.25 * pa, 28)
        f.text('Abonne-toi.', W/2, 1415, 62, INK, a2)


def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    ev += [(0.15, rise(1.2, 300, 900, 0.07)), (1.6, pop(260, 0.2))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (12.7, 29.6, 47.9, 55.9)]
    ev += [(11.1, pop(520))]
    ev += [(30.6, ding(1046, amp=0.28)), (36.1, pop(300, 0.15))]
    ev += [(46.4, clink())]
    ev += [(56.3, pop(440)), (60.0, ding(784, amp=0.22))]
    return ev
