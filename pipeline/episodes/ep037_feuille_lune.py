"""Combien de fois plier une feuille pour atteindre la Lune. Même structure que le pilote.

Sources :
- Épaisseur d'une feuille : Scientific American, « How a sheet of paper can take you to the moon »
  (scientificamerican.com/article/how-many-paper-folds-would-get-you-to-the-moon) : feuille standard
  « approximately 0.1 millimeter thick » ; 42 pliages pour dépasser 384 000 km, 41 pliages ≈ 220 000 km.
  Concordant : Live Science, C. Q. Choi, 7 janvier 2023, « How many times can you fold a piece of paper
  in half? » (feuille de 0,1 mm, 42 pliages pour atteindre la Lune).
- Distance Terre-Lune : NASA Space Place « How far away is the Moon? » (spaceplace.nasa.gov/moon-distance) :
  « an average of 238,855 miles (384,400 km) ».
- Calculs exacts (0,1 mm × 2^n) : 12 plis = 40,96 cm ; 20 plis = 104,9 m ; 30 plis = 107,4 km ;
  41 plis = 219 902 km ; 42 plis = 439 805 km ; 51 plis = 225,2 millions de km.
- Record réel : Guinness World Records « Most times to fold a piece of paper » : Britney Gallivan,
  27 janvier 2002, 12 pliages, papier de soie de 4 000 pieds (1 219 m). Concordant : Live Science 2023
  (12 fois en 2002, 1 219 m) et Mental Floss, 7 avril 2015 (janvier 2002, 12 plis, 4 000 pieds).
- Limite de l'espace : ligne de Kármán, 100 km, retenue par la FAI (Wikipedia « Kármán line »,
  Popular Science « Where does outer space start? »). Affiché comme limite conventionnelle.
- Distance Terre-Soleil : unité astronomique = 149 597 870 700 m (UAI 2012 ; NASA JPL SSD glossaire « au »,
  Nature 2012 « The astronomical unit gets fixed »), affichée « 150 millions de km ».
"""
import math
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro (ep036 précédent).
COVER = dict(tag='Maths', l1='Plie une feuille', l2='jusqu’à la Lune')

PAPER = '#dfe6e1'
PAPER2 = '#a9b8b1'
MOON = '#c9cfcb'


def sheet(f, cx, cy, n, a, w0=520, h0=700):
    """Feuille vue de face, pliée n fois (n réel : la partie décimale anime le pli en cours)."""
    if a <= 0: return
    k = int(n); p = ease_io(n - k)
    w, h = w0, h0
    for i in range(k):
        if i % 2 == 0: w /= 2
        else: h /= 2
    layers = min(1 + k, 8)
    if p <= 0:
        f.rect(cx - w / 2, cy - h / 2, w, h, PAPER, a, 6)
    elif k % 2 == 0:
        # pli vertical : la moitié droite se rabat sur la gauche
        sh = p * w / 4
        x0 = cx - w / 2 + sh; xf = cx + sh
        f.rect(x0, cy - h / 2, w / 2, h, PAPER, a, 6)
        fw = (w / 2) * (1 - 2 * p)
        col = PAPER if fw > 0 else PAPER2
        if fw >= 0: f.rect(xf, cy - h / 2, fw, h, col, a, 6)
        else: f.rect(xf + fw, cy - h / 2, -fw, h, col, a, 6)
    else:
        sh = p * h / 4
        y0 = cy - h / 2 + sh; yf = cy + sh
        f.rect(cx - w / 2, y0, w, h / 2, PAPER, a, 6)
        fh = (h / 2) * (1 - 2 * p)
        col = PAPER if fh > 0 else PAPER2
        if fh >= 0: f.rect(cx - w / 2, yf, w, fh, col, a, 6)
        else: f.rect(cx - w / 2, yf + fh, w, -fh, col, a, 6)
    # liseré d'épaisseur
    for j in range(layers - 1):
        f.line([(cx - w / 2 + 8, cy + h / 2 + 6 + 5 * j), (cx + w / 2 - 8, cy + h / 2 + 6 + 5 * j)], PAPER2, a * 0.6, 2)


def moon(f, x, y, r, a):
    if a <= 0: return
    f.circle(x, y, r * 1.25, SPARK, a * 0.08)
    f.circle(x, y, r, MOON, a)
    for dx, dy, rr in ((-0.35, -0.25, 0.18), (0.3, 0.1, 0.24), (-0.1, 0.45, 0.12), (0.15, -0.45, 0.1)):
        f.circle(x + dx * r, y + dy * r, rr * r, '#a7aeaa', a)


def earth(f, x, y, r, a):
    if a <= 0: return
    f.circle(x, y, r, '#2f6f8f', a)
    f.circle(x - r * 0.3, y - r * 0.2, r * 0.45, EARTH, a)
    f.circle(x + r * 0.35, y + r * 0.3, r * 0.3, EARTH, a)


def sun(f, x, y, r, a):
    if a <= 0: return
    f.circle(x, y, r * 1.4, SPARK, a * 0.12)
    f.circle(x, y, r, SPARK, a)


def thick(n):
    mm = 0.1 * 2 ** n
    if mm < 10: return f'{mm:.1f}'.replace('.', ',') + ' mm'
    if mm < 1000: return f'{mm / 10:.0f} cm' if mm >= 100 else f'{mm / 10:.1f}'.replace('.', ',') + ' cm'
    if mm < 1e6: return fmt_int(mm / 1000) + ' m'
    return fmt_int(mm / 1e6) + ' km'


def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')
    c = f.c

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.8, 30.2))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Comment 42 plis suffisent ?', W/2, 296, 42, SPARK, ha)

    # S1 — accroche (0–4) : la feuille se plie dès la première image
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        words(f, 'Plie une feuille 42 fois.', 470, 80, 0.05, INK, t_out=o)
        words(f, 'Elle touche la Lune.', 590, 88, 0.8, SPARK, t_out=o)
        n = 3.0 * seg(t, 0.0, 3.6)
        sheet(f, W/2, 1060, n, fo)
        moon(f, 880, 790, 60, fo * ease(seg(t, 1.2, 1.6)))

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.0:
        o1 = 7.4
        g1 = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'Une feuille fait', 470, 92, 4.2, INK, t_out=o1)
            words(f, '0,1 mm d’épaisseur.', 590, 88, 4.7, SPARK, t_out=o1)
            # feuille vue de profil, loupe sur la tranche
            f.rect(190, 980, 700, 5, PAPER, g1, 2)
            la = g1 * ease(seg(t, 5.4, 5.8))
            f.circle(W/2, 982, 150, SPARK, la, 6)
            z = 0.4 + 0.6 * ease(seg(t, 5.6, 6.4))
            f.rect(W/2 - 140, 982 - 20 * z, 280, 40 * z, PAPER, la, 4)
            f.text('0,1 mm', W/2, 1230, 56, SPARK, la, MONO, True)
        o2 = 10.7
        g2 = ease(seg(t, 7.6, 8.0)) * (1 - seg(t, o2, o2 + 0.3))
        if g2 > 0:
            words(f, 'Ton intuition :', 480, 72, 7.7, MUTED, t_out=o2)
            words(f, '42 plis, ça tient', 600, 84, 8.1, INK, t_out=o2)
            words(f, 'dans la main.', 710, 84, 8.6, SPARK, t_out=o2)
            hb = g2 * ease(seg(t, 8.9, 9.2))
            # main stylisée qui tient une petite liasse
            f.rect(400, 1080, 280, 230, '#c99d7c', hb, 60)
            f.rect(380, 1000, 70, 150, '#c99d7c', hb, 35)
            for j in range(6):
                f.rect(430, 1030 - 9 * j - 6 * math.sin(t * 3) * (j / 6), 220, 7, PAPER, hb, 3)

    # S3 — la question (10.9–13.6)
    if 10.9 <= t < 13.6:
        words(f, 'Alors comment 42 plis', 820, 84, 11.0, INK, t_out=12.5)
        words(f, 'vont jusqu’à la Lune ?', 950, 92, 11.4, SPARK, t_out=12.5)

    # S4 — la preuve (13.5–30)
    if 13.4 <= t < 30.0:
        # A : on plie pour de vrai, 0 → 12 plis (13.6–21.2)
        oa = 21.0
        ga = ease(seg(t, 13.5, 13.9)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Plie, et mesure :', 440, 84, 13.6, INK, t_out=oa)
            n = 12 * ease_io(seg(t, 14.4, 18.8))
            k = int(n)
            f.text(f'{k} plis', 300, 640, 70, SPARK, ga, MONO, True, 'left')
            f.text(thick(n), 300, 730, 56, INK, ga, MONO, True, 'left')
            # pile vue de profil, hauteur réelle à l'échelle (41 cm = 560 px)
            base = 1330; px = 560 / 409.6
            hh = max(3, 0.1 * 2 ** n * px)
            f.rect(200, base - hh, 260, hh, PAPER, ga, 3)
            nl = min(int(hh / 9), 40)
            for j in range(1, nl):
                yy = base - hh * j / nl
                f.line([(205, yy), (455, yy)], PAPER2, ga * 0.5, 1.5)
            # règle
            f.line([(500, base), (500, base - 560)], LINE, ga, 4)
            for j in range(5):
                yy = base - 560 * j / 4
                f.line([(500, yy), (530, yy)], LINE, ga, 3)
            f.text('41 cm', 545, base - 548, 34, MUTED, ga, MONO, False, 'left')
            ra = ga * ease(seg(t, 19.0, 19.3))
            c.save(); c.translate(780, 1080); s = bump(t, 19.0, 0.15); c.scale(s, s)
            f.text('record', 0, -60, 52, SPARK, ra, DISPLAY, True)
            f.text('du monde', 0, 0, 52, SPARK, ra, DISPLAY, True)
            c.restore()
            f.text('12 plis réels', 780, 1150, 36, INK, ra, MONO, True)
            f.text('Britney Gallivan, 2002', W/2, 1440, 34, MUTED, ra, MONO, False)
        # B : on continue sur le papier, 12 → 30 plis (21.4–29.6)
        gb = ease(seg(t, 21.3, 21.7)) * (1 - seg(t, 29.4, 29.8))
        if gb > 0:
            words(f, 'Ensuite, on calcule.', 440, 84, 21.4, INK, t_out=29.3)
            n = 12 + 18 * ease_io(seg(t, 22.2, 27.2))
            k = int(n)
            # colonne qui monte (échelle par plis)
            base, top = 1400, 620
            x0 = 200
            hh = (base - top) * (n / 30)
            f.rect(x0, base - hh, 90, hh, SPARK, gb, 8)
            f.line([(x0 - 20, base), (x0 + 110, base)], LINE, gb, 4)
            f.text(f'{k} plis', 360, 690, 64, SPARK, gb, MONO, True, 'left')
            f.text(thick(k), 360, 780, 56, INK, gb, MONO, True, 'left')
            m1 = gb * ease(seg(t, 24.6, 24.9))
            f.text('20 plis : 105 m', 360, 960, 50, INK, m1, MONO, True, 'left')
            m2 = gb * ease(seg(t, 27.2, 27.5))
            f.text('30 plis : 107 km', 360, 1120, 50, SPARK, m2, MONO, True, 'left')
            m3 = gb * ease(seg(t, 27.8, 28.1))
            f.text('déjà dans l’espace', 360, 1190, 44, INK, m3, DISPLAY, True, 'left')
            f.text('(limite : 100 km)', 360, 1250, 32, MUTED, m3, MONO, False, 'left')

    # S5 — la réponse (30–36)
    if 29.9 <= t < 36.0:
        o = 35.6
        a = ease(seg(t, 30.3, 30.6)) * (1 - seg(t, o, o + 0.3))
        moon(f, W/2, 560, 110, a * ease(seg(t, 30.0, 30.4)))
        big_center(f, '42 plis', 900, 200, SPARK, a, bump(t, 30.3, 0.18))
        f.text('439 800 km', W/2, 1060, 90, INK, a * ease(seg(t, 31.0, 31.3)), MONO, True)
        words(f, 'plus loin que la Lune.', 1180, 72, 31.6, INK, t_out=o)
        f.text('Lune : 384 400 km', W/2, 1330, 52, MUTED, a * ease(seg(t, 33.0, 33.3)), MONO, True)

    # S6 — le retournement (36–48.4)
    if 36.0 <= t < 48.4:
        words(f, 'Le secret ?', 900, 150, 36.1, SPARK, t_out=37.9)
        # A : chaque pli double tout (38.1–42.6)
        oa = 42.6
        ga = ease(seg(t, 38.1, 38.5)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Chaque pli', 440, 92, 38.2, INK, t_out=oa)
            words(f, 'double tout.', 560, 100, 38.7, SPARK, t_out=oa)
            sz, gap = 34, 6
            cols = [1, 2, 4, 8, 16]
            xs = [150, 300, 450, 620, 830]
            base = 1360
            for i, (nb, x) in enumerate(zip(cols, xs)):
                q = ga * ease(seg(t, 39.2 + 0.55 * i, 39.5 + 0.55 * i))
                if q <= 0: continue
                for j in range(nb):
                    f.rect(x - 50, base - (j + 1) * (sz + gap), 100, sz, SPARK if i == 4 else PAPER, q, 6)
                f.text(f'×2' if i else '1', x, base + 60, 40, MUTED, q, MONO, True)
        # B : le dernier pli ajoute 220 000 km à lui seul (42.9–47.9)
        ob = 47.9
        gb = ease(seg(t, 42.8, 43.2)) * (1 - seg(t, ob, ob + 0.3))
        if gb > 0:
            words(f, 'Le 42e pli, à lui seul,', 440, 80, 42.9, INK, t_out=ob)
            words(f, 'ajoute 220 000 km.', 560, 88, 43.5, SPARK, t_out=ob)
            x0, x1, y = 140, 940, 960
            earth(f, x0, y, 40, gb)
            xm = x0 + (x1 - x0) * 384400 / 439805
            moon(f, xm, y - 130, 34, gb)
            f.line([(xm, y - 90), (xm, y + 60)], MUTED, gb, 3, [8, 8])
            xh = x0 + (x1 - x0) * 0.5
            q1 = ease(seg(t, 44.0, 44.8))
            f.rect(x0 + 50, y - 22, (xh - x0 - 50) * q1, 44, PAPER2, gb, 10)
            q2 = ease(seg(t, 45.2, 46.4))
            f.rect(xh, y - 22, (x1 - xh) * q2, 44, SPARK, gb, 10)
            f.text('41 plis', (x0 + xh) / 2 + 25, y + 110, 40, MUTED, gb * ease(seg(t, 44.4, 44.7)), MONO, True)
            f.text('+ 1 pli', (xh + x1) / 2, y + 110, 40, SPARK, gb * ease(seg(t, 45.6, 45.9)), MONO, True)
            f.text('autant que les 41 premiers réunis', W/2, 1300, 40, INK, gb * ease(seg(t, 46.0, 46.3)), DISPLAY, True)

    # S7 — l'escalade (48–56.4) : 51 plis, plus loin que le Soleil
    if 48.0 <= t < 56.4:
        o = 55.9
        ga = ease(seg(t, 48.1, 48.4)) * (1 - seg(t, o, o + 0.3))
        if ga > 0:
            words(f, 'Et avec 51 plis ?', 440, 88, 48.1, INK, t_out=o)
            x0, x1, y = 140, 900, 900
            xs = x0 + (x1 - x0) * 149.6 / 225.2
            earth(f, x0, y, 30, ga)
            moon(f, x0 + 22, y - 60, 12, ga)
            sun(f, xs, y, 70, ga * ease(seg(t, 48.8, 49.2)))
            q = ease_io(seg(t, 49.6, 52.4))
            f.rect(x0 + 40, y - 12, (x1 - x0 - 40) * q, 24, PAPER, ga, 8)
            f.circle(x0 + 40 + (x1 - x0 - 40) * q, y, 18, SPARK, ga * (q > 0))
            aa = ga * ease(seg(t, 52.4, 52.7))
            c.save(); c.translate(W/2, 1150); s = bump(t, 52.4, 0.15); c.scale(s, s)
            f.text('plus loin que le Soleil', 0, 0, 76, SPARK, aa, DISPLAY, True); c.restore()
            f.text('225 millions de km', W/2, 1260, 50, INK, ga * ease(seg(t, 53.0, 53.3)), MONO, True)
            f.text('Soleil : 150 millions de km', W/2, 1340, 36, MUTED, ga * ease(seg(t, 53.0, 53.3)), MONO, False)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        a = ease(seg(t, 56.1, 56.4))
        moon(f, W/2 + 200, 600 - 20 * math.sin((t - 56) * 1.5), 80 * bump(t, 56.1, 0.12), a)
        sheet(f, W/2 - 170, 650, 1.0 + 2.0 * seg(t, 56.2, 59.0), a, 300, 400)
        words(f, 'Ton cerveau additionne.', 920, 72, 56.3, INK)
        words(f, 'Le papier, lui, double.', 1030, 80, 57.6, SPARK)
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
    ev += [(19.0, ding(784, amp=0.18))]
    ev += [(30.3, ding(1046, amp=0.28)), (36.1, pop(300, 0.15))]
    ev += [(52.4, ding(784, amp=0.18))]
    ev += [(56.3, pop(440)), (60.0, ding(784, amp=0.22))]
    return ev
