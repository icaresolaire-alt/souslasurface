"""Pourquoi un QR code abîmé se lit quand même. Même structure que le pilote.

Sources :
- IEEE Spectrum, « How a Board Game and Skyscrapers Inspired the Development of the QR Code » : créé par
  Masahiro Hara chez Denso, présenté en 1994, pour suivre les pièces automobiles ; « peut être lu même si
  30 % de sa surface est sale ou abîmée » ; carrés de repérage au rapport 1:1:3:1:1.
- Office japonais des brevets (JPO), « QR code » (jpo.go.jp/e/news/koho/innovation/01_qrcode_e.html) :
  1994, Hara Masahiro, DENSO (aujourd'hui DENSO WAVE), brevet laissé libre d'usage.
- Niveaux de correction L 7 %, M 15 %, Q 25 %, H 30 % (codes de Reed-Solomon) : Wikipedia « QR code »
  (via Wikiwand) et GIGAZINE (4 mai 2025, « QR code error correction »), concordants.
- Reed-Solomon, 1960, CD et Voyager : PBS NOVA « The Codes of Modern Life » (Reed et Solomon, 1960 ;
  Voyager, CD, QR codes) et B. A. Cipra, « The Ubiquitous Reed-Solomon Codes », SIAM News 1993
  (« rayer un CD et toujours écouter la musique », photos de Voyager II).
- L'exemple « 2 + 3 + 7 = 12 » est une illustration simplifiée (une somme de contrôle), présentée comme telle.
- Le QR code affiché est un vrai code (version 2, niveau H) qui contient « SOUS LA SURFACE ».
"""
import math
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro (ep024 -> cinema ; ep023 était guitare).
COVER = dict(tag='Tech', l1='Pourquoi un QR code abîmé', l2='se lit quand même')

QR = ['1111111010111011001111111', '1000001000110001001000001', '1011101000000011101011101',
      '1011101010010001001011101', '1011101000100101101011101', '1000001001110101101000001',
      '1111111010101010101111111', '0000000001000110000000000', '0010111011111000010001001',
      '0010000110000111001100010', '1100011100110101000101110', '0010100100001111110001111',
      '1110101011111111110011100', '0111010010001001111011110', '1011111001000111101110011',
      '0100110101101110110110010', '1011011010100111111110101', '0000000011010100100010100',
      '1111111000000100101011010', '1000001011010101100011001', '1011101010100110111111011',
      '1011101001011000010000010', '1011101011100110101001101', '1000001001110001001111011',
      '1111111000001101000000101']
N = len(QR)
PAPER = '#eef3ee'


def qr(f, cx, cy, size, a, pop=1.0):
    """QR code centré, côté = size (zone blanche comprise). pop 0..1 = apparition des modules."""
    if a <= 0: return
    m = size / (N + 4)
    x0, y0 = cx - size / 2, cy - size / 2
    f.rect(x0, y0, size, size, PAPER, a, m * 0.8)
    for i, row in enumerate(QR):
        for j, v in enumerate(row):
            if v == '1':
                k = ((i * 7 + j * 13) % 25) / 25
                if pop >= 1 or k < pop:
                    f.rect(x0 + (j + 2) * m, y0 + (i + 2) * m, m + 0.6, m + 0.6, DEEP, a)


def hole(f, cx, cy, size, frac, a, ox=0.0, oy=0.0, col=None, ring=RED):
    """Trou rond qui couvre la fraction frac de la surface du code."""
    if a <= 0 or frac <= 0: return
    r = size * math.sqrt(frac / math.pi)
    f.circle(cx + ox * size, cy + oy * size, r, col or OCEAN, a)
    f.circle(cx + ox * size, cy + oy * size, r, ring, a * 0.8, 5)


def check(f, x, y, s, a, ok=True):
    if a <= 0: return
    if ok:
        f.circle(x, y, s, EARTH, a)
        f.line([(x - s * 0.45, y + s * 0.02), (x - s * 0.1, y + s * 0.35), (x + s * 0.5, y - s * 0.35)], INK, a, s * 0.18)
    else:
        f.circle(x, y, s, RED, a)
        f.line([(x - s * 0.38, y - s * 0.38), (x + s * 0.38, y + s * 0.38)], INK, a, s * 0.18)
        f.line([(x + s * 0.38, y - s * 0.38), (x - s * 0.38, y + s * 0.38)], INK, a, s * 0.18)


def scanline(f, cx, cy, size, t, a):
    if a <= 0: return
    y = cy - size / 2 + size * (0.5 + 0.5 * math.sin(t * 3.2))
    f.rect(cx - size / 2 - 20, y - 3, size + 40, 6, SPARK, a * 0.85, 3)


def box(f, x, y, txt, a, col=INK, bg=OCEAN, s=1.0):
    if a <= 0: return
    c = f.c; c.save(); c.translate(x, y); c.scale(s, s)
    f.rect(-80, -80, 160, 160, bg, a, 24)
    f.rect(-80, -80, 160, 160, col, a * 0.18, 24)
    f.text(txt, 0, 34, 96, col, a, MONO, True)
    c.restore()


def cd(f, x, y, r, a):
    if a <= 0: return
    f.circle(x, y, r, MUTED, a)
    f.circle(x, y, r * 0.8, CAPITAL, a * 0.6)
    f.circle(x, y, r * 0.18, DEEP, a)
    f.line([(x - r * 0.7, y - r * 0.2), (x + r * 0.5, y + r * 0.45)], DEEP, a, 7)


def probe(f, x, y, s, a):
    """Sonde stylisée : grande antenne parabolique + bras."""
    if a <= 0: return
    c = f.c
    c.save(); f.color(INK, a); c.set_line_width(8); c.new_sub_path()
    c.arc(x, y - s * 0.2, s * 0.75, math.pi * 0.15, math.pi * 0.85); c.stroke(); c.restore()
    f.line([(x - s * 0.62, y + s * 0.15), (x + s * 0.62, y + s * 0.15)], INK, a, 8)
    f.line([(x, y + s * 0.15), (x, y - s * 0.55)], SPARK, a, 6)
    f.rect(x - s * 0.3, y + s * 0.2, s * 0.6, s * 0.4, MUTED, a, 8)
    f.line([(x + s * 0.3, y + s * 0.4), (x + s * 1.1, y + s * 0.9)], MUTED, a, 6)
    f.line([(x - s * 0.3, y + s * 0.4), (x - s * 1.0, y + s * 0.6)], MUTED, a, 6)


def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')
    c = f.c

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.8, 30.2))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Comment il survit ?', W/2, 296, 46, SPARK, ha)

    # S1 — accroche (0–4) : le code se construit dès la première image, puis on lui arrache un morceau
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        cx, cy, sz = W/2, 1080, 600
        c.save(); c.translate(cx, cy); s = lerp(0.85, 1.0, ease(seg(t, 0, 0.8))); c.scale(s, s)
        qr(f, 0, 0, sz, fo, seg(t, 0.0, 0.9))
        hole(f, 0, 0, sz, 0.12 * ease(seg(t, 1.0, 1.3)), fo, 0.18, 0.16)
        c.restore()
        scanline(f, cx, cy, sz, t, fo * ease(seg(t, 2.0, 2.3)))
        words(f, 'Il lui manque un bout.', 470, 84, 0.1, INK, t_out=o)
        a = ease(seg(t, 2.3, 2.6)) * fo
        c.save(); c.translate(W/2, 600); s = bump(t, 2.3, 0.2); c.scale(s, s)
        f.text('Il se lit quand même.', 0, 0, 84, SPARK, a); c.restore()
        check(f, cx + 270, cy + 270, 70, ease(seg(t, 2.5, 2.8)) * fo)

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.0:
        o1 = 7.4
        g1 = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'Une tache.', 470, 96, 4.2, INK, t_out=o1)
            words(f, 'Un logo au milieu.', 590, 84, 5.4, SPARK, t_out=o1)
            cx, cy, sz = W/2, 1060, 560
            qr(f, cx, cy, sz, g1)
            # tache qui s'étale
            hole(f, cx, cy, sz, 0.07 * ease(seg(t, 4.4, 5.0)), g1, -0.22, 0.2, '#6b4a2e', '#6b4a2e')
            # logo collé au centre
            la = g1 * ease(seg(t, 5.5, 5.8))
            c.save(); c.translate(cx, cy); s = bump(t, 5.5, 0.25); c.scale(s, s)
            f.rect(-80, -80, 160, 160, SPARK, la, 30)
            f.text('S', 0, 36, 110, DEEP, la); c.restore()
        o2 = 10.7
        g2 = ease(seg(t, 7.6, 8.0)) * (1 - seg(t, o2, o2 + 0.3))
        if g2 > 0:
            words(f, 'Ton intuition :', 560, 72, 7.7, MUTED, t_out=o2)
            words(f, 'il faut chaque pixel.', 680, 84, 8.1, INK, t_out=o2)
            # grille de pixels qui clignotent
            for i in range(5):
                for j in range(5):
                    k = (i * 3 + j * 7) % 5
                    aa = g2 * (0.35 + 0.65 * (0.5 + 0.5 * math.sin(t * 4 + k)))
                    f.rect(W/2 - 250 + j * 100, 900 + i * 100, 84, 84, INK if (i + j) % 2 else CAPITAL, aa, 10)

    # S3 — la question (10.9–13.6)
    if 10.9 <= t < 13.6:
        words(f, 'Comment il survit', 820, 100, 11.0, INK, t_out=12.5)
        words(f, 'aux dégâts ?', 950, 116, 11.4, SPARK, t_out=12.5)

    # S4 — la preuve (13.5–30)
    if 13.4 <= t < 30.0:
        # A : le trou grandit, le code reste lisible jusqu'à 30 % (13.6–21.6)
        oa = 21.3
        ga = ease(seg(t, 13.5, 13.9)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'On l’abîme peu à peu.', 430, 78, 13.6, INK, t_out=oa)
            cx, cy, sz = W/2, 940, 560
            p = ease_io(seg(t, 14.6, 19.0))
            frac = 0.34 * p
            qr(f, cx, cy, sz, ga)
            hole(f, cx, cy, sz, frac, ga)
            if frac < 0.30:
                scanline(f, cx, cy, sz, t, ga)
            a = ga * ease(seg(t, 14.6, 14.9))
            pct = int(round(frac * 100))
            f.text('surface abîmée', W/2, 1330, 40, MUTED, a, MONO, False)
            c.save(); c.translate(W/2, 1450); s = bump(t, 19.0, 0.12); c.scale(s, s)
            f.text(f'{pct} %', 0, 0, 110, SPARK if pct <= 30 else RED, a, MONO, True); c.restore()
            ok = frac < 0.30
            check(f, cx + 250, cy - 250, 56, a, ok)
            f.text('lu' if ok else 'illisible', W/2, 1550, 48, EARTH if ok else RED, a, DISPLAY, True)
        # B : quatre niveaux de secours (21.5–29.6)
        gb = ease(seg(t, 21.5, 21.9)) * (1 - seg(t, 29.4, 29.8))
        if gb > 0:
            words(f, 'Quatre niveaux', 430, 84, 21.6, INK, t_out=29.4)
            words(f, 'de secours :', 540, 76, 22.0, MUTED, t_out=29.4)
            base, maxh = 1340, 600
            LV = (('L', 7), ('M', 15), ('Q', 25), ('H', 30))
            XS = (195, 425, 655, 885)
            f.line([(90, base), (990, base)], MUTED, gb * ease(seg(t, 22.4, 22.7)), 4)
            for j, (lab, v) in enumerate(LV):
                t0 = 22.8 + j * 1.2
                pr = ease_io(seg(t, t0, t0 + 1.4))
                ba = gb * ease(seg(t, t0, t0 + 0.3))
                h = max(6, maxh * v * pr / 30)
                col = SPARK if j == 3 else CAPITAL
                f.rect(XS[j] - 90, base - h, 180, h, col, ba, 12)
                f.text(f'{int(round(v * pr))} %', XS[j], base - h - 30, 60, SPARK if j == 3 else INK, ba, MONO, True)
                f.text(lab, XS[j], base + 76, 64, MUTED, ba, MONO, True)
            f.text('niveau choisi à la création du code', W/2, 1520, 30, MUTED, gb * 0.9 * ease(seg(t, 23.0, 23.3)), MONO, False)

    # S5 — la réponse (30–36)
    if 29.9 <= t < 36.0:
        o = 35.6
        words(f, 'Jusqu’à', 620, 90, 30.0, INK, t_out=o)
        a = ease(seg(t, 30.3, 30.6)) * (1 - seg(t, o, o + 0.3))
        big_center(f, '30 %', 920, 250, SPARK, a, bump(t, 30.3, 0.18))
        words(f, 'du code peut manquer.', 1120, 76, 31.2, INK, t_out=o)
        words(f, 'Inventé en 1994, chez Denso.', 1300, 50, 33.2, MUTED, t_out=o)

    # S6 — le retournement (36–48.4)
    if 36.0 <= t < 48.4:
        words(f, 'Le secret ?', 900, 150, 36.1, SPARK, t_out=37.9)
        # A : on ajoute des chiffres en plus
        gall = ease(seg(t, 38.1, 38.5)) * (1 - seg(t, 47.9, 48.3))
        if gall > 0:
            oa = 42.6
            words(f, 'Il ajoute des chiffres', 440, 76, 38.2, INK, t_out=oa)
            words(f, 'en plus.', 540, 76, 38.7, SPARK, t_out=oa)
            ob = 47.9
            words(f, 'Un morceau disparaît ?', 440, 76, 42.9, INK, t_out=ob)
            words(f, 'On le recalcule.', 540, 76, 43.5, SPARK, t_out=ob)
            XS = (165, 395, 625, 900)
            y = 950
            vals = ('2', '3', '7')
            for j, v in enumerate(vals):
                t0 = 39.2 + j * 0.35
                aa = gall * ease(seg(t, t0, t0 + 0.3))
                if j == 1 and t > 44.2:
                    lost = seg(t, 44.2, 44.6)
                    back = seg(t, 46.0, 46.3)
                    if back > 0:
                        box(f, XS[j], y, '3', aa, EARTH, OCEAN, bump(t, 46.0, 0.25))
                    else:
                        box(f, XS[j], y, '?', aa, RED, OCEAN, 1.0)
                        f.circle(XS[j], y, 95 * (1 - lost) + 1, RED, aa * (1 - lost) * 0.5)
                else:
                    box(f, XS[j], y, v, aa, INK, OCEAN, bump(t, t0, 0.15))
            # signes
            sa = gall * ease(seg(t, 40.4, 40.7))
            for x in ((XS[0] + XS[1]) / 2, (XS[1] + XS[2]) / 2):
                f.text('+', x, y + 30, 70, MUTED, sa, MONO, True)
            f.text('=', (XS[2] + XS[3]) / 2 + 5, y + 30, 70, MUTED, sa, MONO, True)
            ea = gall * ease(seg(t, 40.9, 41.2))
            box(f, XS[3], y, '12', ea, SPARK, OCEAN, bump(t, 40.9, 0.2))
            f.text('le chiffre en plus', XS[3] - 60, y + 160, 34, SPARK, ea * (1 - seg(t, 42.6, 42.9)), DISPLAY, True)
            ra = gall * ease(seg(t, 46.0, 46.3))
            f.text('12 − 2 − 7 = 3', W/2, 1240, 70, EARTH, ra, MONO, True)
            f.text('exemple simplifié · le vrai calcul : Reed-Solomon, 1960', W/2, 1480, 28, MUTED,
                   gall * 0.9 * ease(seg(t, 39.5, 39.9)), MONO, False)

    # S7 — l'escalade (48–56.4)
    if 48.0 <= t < 56.4:
        o = 55.9
        ga = ease(seg(t, 48.1, 48.4)) * (1 - seg(t, o, o + 0.3))
        if ga > 0:
            words(f, 'Le même calcul', 430, 84, 48.1, INK, t_out=o)
            words(f, 'protège aussi :', 540, 76, 48.6, MUTED, t_out=o)
            a1 = ga * ease(seg(t, 49.6, 50.0))
            c.save(); c.translate(300, 900); c.rotate(t * 1.5 * a1); s = bump(t, 49.6, 0.2); c.scale(s, s)
            cd(f, 0, 0, 170, a1); c.restore()
            f.text('tes CD rayés', 300, 1170, 54, INK, a1)
            a2 = ga * ease(seg(t, 51.4, 51.8))
            c.save(); c.translate(790, 900 + 14 * math.sin(t * 2)); s = bump(t, 51.4, 0.2); c.scale(s, s)
            probe(f, 0, 0, 180, a2); c.restore()
            f.text('les photos', 790, 1170, 54, INK, a2)
            f.text('de Voyager', 790, 1236, 54, SPARK, a2)
            a3 = ga * ease(seg(t, 53.0, 53.3))
            f.text('envoyées depuis le bout du système solaire', W/2, 1420, 36, MUTED, a3, DISPLAY, False)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        a = ease(seg(t, 56.1, 56.4))
        c.save(); c.translate(W/2, 620); s = bump(t, 56.1, 0.12); c.scale(s, s)
        qr(f, 0, 0, 260, a)
        c.restore()
        words(f, 'Un QR code contient', 900, 84, 56.3, INK)
        words(f, 'de quoi se réparer.', 1020, 96, 57.6, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(240, 1160, 600, 150, OCEAN, a, 28)
        pa = 0.5 + 0.5 * math.sin((t - 60) * 3)
        f.rect(240, 1160, 600, 150, SPARK, a * 0.25 * pa, 28)
        f.text('Abonne-toi.', W/2, 1255, 62, INK, a)


def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    ev += [(0.15, pop(440, 0.09)), (2.3, ding(880, amp=0.18))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (12.5, 29.6, 47.9, 55.9)]
    ev += [(5.5, pop(300, 0.15)), (11.0, pop(520))]
    ev += [(15.0, rise(3.6, 300, 900, 0.07)), (19.0, clink(1500))]
    ev += [(26.4, ding(784, amp=0.2))]
    ev += [(30.3, ding(1046, amp=0.28)), (36.1, pop(300, 0.15))]
    ev += [(40.9, pop(520, 0.12)), (46.0, ding(784, amp=0.22))]
    ev += [(49.6, pop(440, 0.12))]
    ev += [(56.3, pop(440)), (60.0, ding(784, amp=0.22))]
    return ev
