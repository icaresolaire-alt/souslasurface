"""Pourquoi le clavier n'est pas rangé dans l'ordre alphabétique. Même structure que le pilote.

Sources :
- Premier clavier alphabétique, comme un piano : Smithsonian Magazine, « Fact of Fiction? The Legend of the
  QWERTY Keyboard » (« resembled a piano », « alphabetical arrangement of 28 keys », machine brevetée en 1868) ;
  WI101 (University of Wisconsin), C. Kaufenberg, sept. 2021 (clavier façon piano, ordre alphabétique, deux
  rangées) ; SlashGear, févr. 2022 (« The very first versions and prototypes actually had an alphabetical
  layout »). Clavier en deux rangées affiché en schéma.
- 1873, accord avec Remington : Smithsonian, SlashGear (« early 1873 »), The Economist via Independent Institute,
  3 avril 1999 (« patented by Christopher Sholes in 1868 and sold to Remington in 1873 »).
- 1878, brevet US n° 207 559 : Hagley Museum and Library (27 août 1878, « first documented appearance of the
  QWERTY keyboard layout ») ; Smithsonian (« Issued in 1878, U.S. Patent No. 207,559 »). 148 ans = 2026 - 1878.
- Légende des tiges qui se coincent et contre-exemple E/R (« er », 4e paire la plus fréquente en anglais) :
  Smithsonian et WI101.
- Piste des télégraphistes : Yasuoka et Yasuoka, Kyoto University, 2011, d'après Smithsonian et SlashGear
  (premiers utilisateurs : opérateurs télégraphiques ; la mécanique n'aurait pas dicté l'ordre). Présentée comme
  une piste.
- AZERTY dérivé du QWERTY (A/Q et Z/W permutés) : Wikipedia « AZERTY » (« modelled on the English-language
  QWERTY layout ») et comparaison directe des deux dispositions.
- Dvorak (1936), supériorité discutée : The Economist via Independent Institute 1999 (« patented by August
  Dvorak in 1936 », preuves « extremely thin », étude GSA 1956) ; J. Bigler, MIT (étude de la Navy 1944 jugée
  biaisée, GSA : vitesses égales, pas supérieures) ; Smithsonian et SlashGear (années 1930).
- Tiges, morse et claviers qui se multiplient : illustratifs.
"""
import math
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro (ep045 précédent).
COVER = dict(tag='Tech', l1='Pourquoi ton clavier', l2='n’est pas rangé de A\u00a0à\u00a0Z')

ABC = ['ABCDEFGHIJ', 'KLMNOPQRST', 'UVWXYZ']
AZE = ['AZERTYUIOP', 'QSDFGHJKLM', 'WXCVBN']
QWE = ['QWERTYUIOP', 'ASDFGHJKL', 'ZXCVBNM']


def key(f, x, y, s, ch, a, col=OCEAN, txt=INK, sc=1.0):
    if a <= 0: return
    c = f.c; c.save(); c.translate(x, y); c.scale(sc, sc)
    f.rect(-s / 2, -s / 2 + 6, s, s, DEEP, a * 0.8, s * 0.18)
    f.rect(-s / 2, -s / 2, s, s, col, a, s * 0.18)
    f.text(ch, 0, s * 0.2, s * 0.52, txt, a, DISPLAY, True)
    c.restore()


def keyboard(f, rows, y, s, a, gap=10, hi=(), hi_col=SPARK, offs=(0, 0.4, 1.2), t0=None, per=0.03):
    if a <= 0: return {}
    pos = {}
    for r, row in enumerate(rows):
        n = len(row)
        x0 = W / 2 - (10 * s + 9 * gap) / 2 + s / 2 + offs[r] * (s + gap) * 0.5
        for i, ch in enumerate(row):
            ka = a
            if t0 is not None:
                ka = a * ease(seg(f.t, t0 + per * (r * 10 + i), t0 + per * (r * 10 + i) + 0.2))
            x = x0 + i * (s + gap); yy = y + r * (s + gap)
            on = ch in hi
            key(f, x, yy, s, ch, ka, SPARK if on else OCEAN, DEEP if on else INK)
            pos[ch] = (x, yy)
    return pos


def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')
    c = f.c

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.8, 30.2))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Pourquoi tout mélanger ?', W/2, 296, 44, SPARK, ha)

    # S1 — accroche (0–4) : les touches se mélangent dès la première image
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        words(f, 'Ton clavier', 460, 96, 0.05, INK, t_out=o)
        words(f, 'n’est pas en ordre.', 580, 88, 0.6, SPARK, t_out=o)
        s = 80; gap = 10
        for r in range(3):
            for i in range(len(ABC[r])):
                k = r * 10 + i
                tk = 0.3 + 0.05 * k
                p = seg(t, tk, tk + 0.25)
                ch = ABC[r][i] if p < 0.5 else AZE[r][i]
                x0 = W / 2 - (10 * s + 9 * gap) / 2 + s / 2 + (0, 0.4, 1.2)[r] * (s + gap) * 0.5
                key(f, x0 + i * (s + gap), 880 + r * (s + gap), s, ch, fo,
                    OCEAN, INK if p >= 0.5 else MUTED, sc=1 - 0.12 * math.sin(math.pi * p))
        f.text('A, B, C… perdus ?', W/2, 1260, 48, MUTED, fo * ease(seg(t, 2.4, 2.7)), MONO, True)

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.0:
        o1 = 7.4
        g1 = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'Au début,', 460, 92, 4.2, INK, t_out=o1)
            words(f, 'c’était de A à Z.', 575, 92, 4.6, SPARK, t_out=o1)
            # clavier façon piano, deux rangées
            top = 'ABCDEFGHIJKLM'; bot = 'NOPQRSTUVWXYZ'
            w = 62; x0 = W / 2 - 13 * w / 2 + w / 2
            f.rect(110, 780, 860, 400, CAPITAL, g1 * 0.5, 24)
            for i in range(13):
                ka = g1 * ease(seg(t, 4.8 + 0.06 * i, 5.0 + 0.06 * i))
                f.rect(x0 + i * w - 27, 820, 54, 150, INK, ka, 8)
                f.text(top[i], x0 + i * w, 920, 38, DEEP, ka, MONO, True)
                kb = g1 * ease(seg(t, 5.3 + 0.06 * i, 5.5 + 0.06 * i))
                f.rect(x0 + i * w - 27, 995, 54, 150, INK, kb, 8)
                f.text(bot[i], x0 + i * w, 1095, 38, DEEP, kb, MONO, True)
            f.text('comme un piano', W/2, 1290, 52, SPARK, g1 * ease(seg(t, 6.1, 6.4)), MONO, True)
            f.text('(schéma)', W/2, 1360, 32, MUTED, g1 * ease(seg(t, 6.3, 6.6)) * 0.8, MONO, False)
        o2 = 10.7
        g2 = ease(seg(t, 7.6, 8.0)) * (1 - seg(t, o2, o2 + 0.3))
        if g2 > 0:
            words(f, 'Puis les lettres', 460, 84, 7.7, INK, t_out=o2)
            words(f, 'ont tout changé.', 575, 84, 8.1, SPARK, t_out=o2)
            # les touches s'envolent et retombent ailleurs
            letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            for k, ch in enumerate(letters):
                ang = k * 2.4
                p = ease_io(seg(t, 8.4 + 0.02 * k, 9.6 + 0.02 * k))
                xa = 160 + (k % 9) * 95; ya = 820 + (k // 9) * 110
                xb = W / 2 + 330 * math.cos(ang + t * 0.5); yb = 1050 + 260 * math.sin(ang + t * 0.5)
                key(f, lerp(xa, xb, p), lerp(ya, yb, p), 76, ch, g2, OCEAN, INK)

    # S3 — la question (10.9–13.6)
    if 10.9 <= t < 13.6:
        words(f, 'Pourquoi tout', 820, 96, 11.0, INK, t_out=12.5)
        words(f, 'mélanger ?', 945, 110, 11.4, SPARK, t_out=12.5)

    # S4 — la preuve (13.5–30)
    if 13.4 <= t < 30.0:
        # A : frise 1868 → 1873 → 1878 (13.6–21.6)
        oa = 21.6
        ga = ease(seg(t, 13.5, 13.9)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Inventeur :', 430, 72, 13.6, MUTED, t_out=oa)
            words(f, 'Christopher Sholes.', 540, 80, 14.0, SPARK, t_out=oa)
            x0, x1, y = 200, 880, 900
            f.line([(x0, y), (lerp(x0, x1, ease_io(seg(t, 14.8, 19.0))), y)], LINE, ga, 10)
            steps = [(15.0, '1868', 'premier brevet', 'clavier A B C'),
                     (16.8, '1873', 'vendu à', 'Remington'),
                     (18.6, '1878', 'brevet du', 'QWERTY')]
            for i, (ts, yr, l1, l2) in enumerate(steps):
                x = lerp(x0, x1, i / 2)
                sa = ga * ease(seg(t, ts, ts + 0.3))
                f.circle(x, y, 28 * bump(t, ts, 0.3), SPARK if i == 2 else INK, sa)
                f.text(yr, x, y - 70, 60, SPARK if i == 2 else INK, sa, MONO, True)
                f.text(l1, x, y + 100, 38, MUTED, sa, DISPLAY, True)
                f.text(l2, x, y + 150, 42, INK, sa, DISPLAY, True)
            words(f, 'Les touches bougent', 1260, 60, 19.4, INK, t_out=oa)
            words(f, 'pendant dix ans.', 1350, 60, 19.8, SPARK, t_out=oa)
        # B : le QWERTY apparaît (21.8–29.6)
        gb = ease(seg(t, 21.7, 22.1)) * (1 - seg(t, 29.4, 29.8))
        if gb > 0:
            words(f, '1878 : le brevet', 430, 80, 21.8, INK, t_out=29.3)
            words(f, 'du clavier QWERTY.', 540, 80, 22.3, SPARK, t_out=29.3)
            hi = set('QWERTY') if t > 25.0 else set()
            keyboard(f, QWE, 820, 82, gb, hi=hi, t0=22.8, per=0.06)
            # balayage doré sur Q W E R T Y
            for i, ch in enumerate('QWERTY'):
                ts = 25.0 + 0.25 * i
                f.text(ch, 270 + 108 * i, 1240, 96, SPARK, gb * ease(seg(t, ts, ts + 0.2)), MONO, True)
            f.text('brevet US n° 207 559', W/2, 1400, 44, MUTED, gb * ease(seg(t, 27.0, 27.3)), MONO, True)

    # S5 — la réponse (30–36)
    if 29.9 <= t < 36.0:
        o = 35.6
        a = ease(seg(t, 30.3, 30.6)) * (1 - seg(t, o, o + 0.3))
        words(f, 'Ton clavier a', 600, 76, 30.0, MUTED, t_out=o)
        big_center(f, '148', 880, 300, SPARK, a, bump(t, 30.3, 0.18), font=DISPLAY)
        words(f, 'ans.', 1060, 96, 31.0, INK, t_out=o)
        words(f, 'L’AZERTY en dérive :', 1220, 50, 32.2, INK, t_out=o)
        words(f, 'A↔Q et Z↔W échangés.', 1300, 50, 32.8, SPARK, t_out=o, font=MONO)

    # S6 — le retournement (36–48.4)
    if 36.0 <= t < 48.4:
        words(f, 'Mais pourquoi ?', 900, 116, 36.1, SPARK, t_out=37.9)
        # A : la légende des tiges qui se coincent (38.1–42.6)
        oa = 42.6
        ga = ease(seg(t, 38.1, 38.5)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'La légende :', 440, 80, 38.2, MUTED, t_out=oa)
            words(f, 'les tiges se coinçaient.', 550, 76, 38.6, INK, t_out=oa)
            # éventail de tiges qui frappent vers le centre
            px, py = W / 2, 700
            for k in range(9):
                ang0 = math.pi * (0.15 + 0.7 * k / 8)
                L = 360
                hit = 0.0
                if k in (3, 5):
                    hit = ease_io(seg(t, 39.4, 40.0))
                ang = lerp(ang0, math.pi / 2, hit * 0.92)
                bx = px + L * math.cos(ang); by = py + L * math.sin(ang)
                col = RED if (k in (3, 5) and hit > 0.9) else MUTED
                f.line([(bx, by), (px + 30 * math.cos(ang), py + 30 * math.sin(ang))], col, ga, 8)
                f.circle(bx, by, 16, col, ga)
            ja = ga * ease(seg(t, 40.0, 40.2))
            f.circle(px, py - 20, 70 * bump(t, 40.0, 0.3), RED, ja * 0.3)
            f.text('CLAC', px, py - 2, 54, RED, ja, MONO, True)
            words(f, 'Alors on a séparé', 1330, 60, 40.6, INK, t_out=oa)
            words(f, 'les lettres fréquentes.', 1420, 60, 41.0, SPARK, t_out=oa)
        # B : contre-exemple E et R (42.9–47.9)
        ob = 47.9
        gb = ease(seg(t, 42.8, 43.2)) * (1 - seg(t, ob, ob + 0.3))
        if gb > 0:
            words(f, 'Problème : E et R', 430, 80, 42.9, INK, t_out=ob)
            words(f, 'sont collés.', 540, 88, 43.4, RED, t_out=ob)
            hi = set('ER') if t > 44.0 else set()
            ra = gb * ease(seg(t, 44.0, 44.3))
            pos = keyboard(f, QWE, 800, 82, 0.001)
            (ex, ey), (rx, _) = pos['E'], pos['R']
            f.rect(ex - 58, ey - 58, rx - ex + 116, 116, SPARK, ra * 0.3 * (0.6 + 0.4 * math.sin(t * 6)), 24)
            keyboard(f, QWE, 800, 82, gb, hi=hi)
            f.text('« ER » : 4e paire de lettres', W/2, 1240, 48, INK, gb * ease(seg(t, 44.8, 45.1)), DISPLAY, True)
            f.text('la plus fréquente en anglais', W/2, 1310, 48, INK, gb * ease(seg(t, 44.9, 45.2)), DISPLAY, True)
            f.text('La légende ne tient pas.', W/2, 1440, 52, SPARK, gb * ease(seg(t, 45.9, 46.2)), DISPLAY, True)

    # S7 — l'escalade (48–56.4)
    if 48.0 <= t < 56.4:
        o1 = 51.9
        g1 = ease(seg(t, 48.1, 48.4)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'Une piste :', 430, 76, 48.1, MUTED, t_out=o1)
            words(f, 'les télégraphistes.', 540, 80, 48.6, SPARK, t_out=o1)
            # signal morse qui défile
            seq = '.-.. .. ... -- --- .-. ... .'
            x = 140 - (t - 48.6) * 160
            for ch in seq * 2:
                if ch == '.':
                    if 120 < x < 960: f.circle(x, 900, 22, INK, g1)
                    x += 70
                elif ch == '-':
                    if 100 < x < 940: f.rect(x - 20, 880, 90, 40, SPARK, g1, 20)
                    x += 130
                else:
                    x += 80
            f.text('premiers clients de la machine', W/2, 1080, 44, INK, g1 * ease(seg(t, 49.4, 49.7)), DISPLAY, True)
            f.text('étude de Yasuoka, Kyoto, 2011', W/2, 1180, 36, MUTED, g1 * ease(seg(t, 49.9, 50.2)), MONO, False)
        o2 = 55.9
        g2 = ease(seg(t, 52.1, 52.4)) * (1 - seg(t, o2, o2 + 0.3))
        if g2 > 0:
            words(f, 'Puis tout le monde', 430, 80, 52.2, INK, t_out=o2)
            words(f, 'l’a appris.', 540, 88, 52.7, SPARK, t_out=o2)
            # les claviers se multiplient
            for i in range(16):
                gx, gy = i % 4, i // 4
                x = W/2 - 330 + 220 * gx; y = 740 + 120 * gy
                tk = 53.0 + 0.08 * i
                la = g2 * ease(seg(t, tk, tk + 0.2))
                f.rect(x - 90, y - 40, 180, 80, OCEAN, la, 12)
                for r in range(3):
                    f.rect(x - 75 + r * 6, y - 28 + r * 22, 150 - r * 14, 14, MUTED if i % 5 else SPARK, la * 0.8, 4)
            f.text('Le Dvorak (1936) promettait mieux.', W/2, 1300, 44, INK, g2 * ease(seg(t, 54.0, 54.3)), DISPLAY, True)
            f.text('Gain contesté. Il n’a pas percé.', W/2, 1380, 44, RED, g2 * ease(seg(t, 54.5, 54.8)), DISPLAY, True)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        a = ease(seg(t, 56.1, 56.4))
        for i, ch in enumerate('AZERTY'):
            key(f, W/2 - 5 * 52 + 104 * i, 860, 88, ch, a * ease(seg(t, 56.1 + 0.08 * i, 56.4 + 0.08 * i)))
        words(f, 'Ton clavier n’est pas logique.', 1010, 62, 56.3, INK)
        words(f, 'C’est une habitude de 1878.', 1110, 62, 57.8, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(240, 1200, 600, 150, OCEAN, a, 28)
        pa = 0.5 + 0.5 * math.sin((t - 60) * 3)
        f.rect(240, 1200, 600, 150, SPARK, a * 0.25 * pa, 28)
        f.text('Abonne-toi.', W/2, 1295, 62, INK, a)


def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    ev += [(0.15, rise(1.2, 300, 900, 0.07))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (12.5, 29.6, 47.9, 55.9)]
    ev += [(11.0, pop(520))]
    ev += [(30.3, ding(1046, amp=0.28)), (36.1, pop(300, 0.15))]
    ev += [(40.0, clink())]
    ev += [(56.3, pop(440)), (60.0, ding(784, amp=0.22))]
    return ev
