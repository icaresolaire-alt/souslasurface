"""Le vrai génie de Gutenberg n'était pas la presse. Même structure que le pilote.

Sources :
- Europeana, « From manuscript production to the printing press » : Gutenberg pouvait imprimer
  « des centaines de pages par jour », contre « deux ou trois pages » pour un copiste dans le même temps.
- Wikipedia « Printing press » : une presse de la Renaissance produisait « jusqu'à 3 600 pages par jour »
  (Wolf 1974), contre quelques-unes à la main ; « plus de vingt millions d'exemplaires » imprimés en Europe
  de l'Ouest avant 1500 (Febvre et Martin, The Coming of the Book, 1976) ; presse inspirée des pressoirs à
  vis pour le raisin et les olives ; moule à main ; alliage plomb, étain, antimoine.
- New Learning Online, « Febvre and Martin on the Coming of the Book » : « environ 20 millions de livres
  imprimés avant 1500 », sur 30 000 à 35 000 éditions.
- HistoryofInformation.com (J. Norman), d'après l'ISTC de la British Library : 29 777 éditions avant 1501 ;
  production totale estimée entre 15 et 20 millions d'exemplaires. D'où « environ 20 millions ».
- ASME « Johannes Gutenberg » : adaptation d'un pressoir à vis à huile ou à vin ; lettres en métal
  réutilisables ; Bible commencée vers 1450, terminée en 1455. MIT Lemelson « Johann Gutenberg » :
  « il adapta un pressoir à vin ».
- drupa, « Gutenberg's Inventions, Part 2: Hand Mould » : le moule à main produit en série des lettres identiques.
- Britannica « Pi Sheng » : caractères mobiles conçus vers 1041–1048, en argile et colle durcies à la cuisson.
  Wikipedia « Movable type » : Bi Sheng, vers 1040, matériaux céramiques. 1040 -> 1450 : environ 400 ans.
- L'exemple CHIEN -> NICHE est une illustration (mêmes lettres, autre mot).
"""
import math
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro (ep024 était cinema).
COVER = dict(tag='Histoire', l1='Le génie de Gutenberg', l2='n’était pas la presse')

PAPER = '#efe6d2'
INKB = '#2a2118'
WOOD = '#9a6b3f'
METAL = '#b8c2c8'
CLAY = '#b4744a'
GRAPE = '#7b4a8c'


def page(f, x, y, w, h, a, frac=1.0, rot=0.0):
    """Feuille avec des lignes d'écriture ; frac = part écrite."""
    if a <= 0: return
    c = f.c; c.save(); c.translate(x, y); c.rotate(rot)
    f.rect(-w/2, -h/2, w, h, PAPER, a, 10)
    n = 9; lh = (h - 80) / n
    tot = frac * n
    for i in range(n):
        p = clamp(tot - i)
        if p <= 0: break
        y0 = -h/2 + 50 + i * lh
        f.line([(-w/2 + 36, y0), (-w/2 + 36 + (w - 72) * p, y0)], INKB, a * 0.8, max(3, h * 0.012))
    c.restore()


def quill(f, x, y, s, a):
    if a <= 0: return
    c = f.c; c.save(); c.translate(x, y); c.rotate(-0.7)
    f.color(INK, a); c.new_sub_path()
    c.move_to(0, 0); c.curve_to(s * 0.15, -s * 0.5, s * 0.1, -s * 1.0, 0, -s * 1.3)
    c.curve_to(-s * 0.3, -s * 0.9, -s * 0.2, -s * 0.4, 0, 0); c.close_path(); c.fill()
    f.line([(0, 0), (0, -s * 1.2)], MUTED, a, 3)
    c.restore()


def press(f, x, y, s, a, down=0.0):
    """Presse à vis stylisée ; down 0..1 = plateau abaissé."""
    if a <= 0: return
    c = f.c; c.save(); c.translate(x, y); c.scale(s, s)
    f.rect(-160, -260, 30, 360, WOOD, a, 6)
    f.rect(130, -260, 30, 360, WOOD, a, 6)
    f.rect(-180, -290, 360, 40, WOOD, a, 8)
    f.rect(-180, 70, 360, 40, WOOD, a, 8)
    py = -150 + down * 120
    f.line([(0, -250), (0, py)], METAL, a, 14)
    for k in range(5):
        yy = -240 + k * (py + 240) / 5
        f.line([(-14, yy), (14, yy + 10)], DEEP, a * 0.6, 4)
    f.line([(-90, -215), (90, -195)], METAL, a, 10)
    f.rect(-110, py, 220, 30, METAL, a, 6)
    f.rect(-100, 40, 200, 30, PAPER, a, 4)
    c.restore()


def tblock(f, x, y, ch, a, s=1.0, col=METAL, txt=DEEP):
    """Caractère mobile vu de face (bloc de métal + lettre)."""
    if a <= 0: return
    c = f.c; c.save(); c.translate(x, y); c.scale(s, s)
    f.rect(-62, -80, 124, 160, col, a, 12)
    f.rect(-62, -80, 124, 26, '#ffffff', a * 0.18, 12)
    f.text(ch, 0, 36, 104, txt, a, MONO, True)
    c.restore()


def books(f, x, base, n, a, w=150):
    """Pile de livres (n tranches)."""
    cols = (SPARK, CAPITAL, EARTH, RED, MUTED)
    for i in range(int(n)):
        off = 10 * math.sin(i * 1.7)
        f.rect(x - w/2 + off, base - (i + 1) * 30, w, 26, cols[i % 5], a, 5)
    fr = n - int(n)
    if fr > 0:
        i = int(n)
        f.rect(x - w/2 + 10 * math.sin(i * 1.7), base - (i + 1) * 30, w, 26, cols[i % 5], a * fr, 5)


def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')
    c = f.c

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.8, 30.2))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Combien en 50 ans ?', W/2, 296, 46, SPARK, ha)

    # S1 — accroche (0–4) : une plume écrit dès la première image
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        words(f, 'Avant 1450, en Europe :', 400, 52, 0.05, MUTED, t_out=o)
        words(f, 'chaque livre', 520, 92, 0.3, INK, t_out=o)
        words(f, 'copié à la main.', 640, 92, 1.2, SPARK, t_out=o)
        fr = seg(t, 0.0, 4.0)
        page(f, W/2, 1110, 520, 640, fo, fr)
        n = 9; i = min(n - 1, int(fr * n)); p = fr * n - i
        qx = W/2 - 260 + 36 + (520 - 72) * p
        qy = 1110 - 320 + 50 + i * (640 - 80) / n
        quill(f, qx + 6, qy - 4, 120, fo)

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.0:
        o1 = 7.4
        g1 = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'Un copiste,', 470, 96, 4.2, INK, t_out=o1)
            words(f, '2 ou 3 pages par jour.', 590, 80, 5.0, SPARK, t_out=o1)
            for k in range(3):
                t0 = 4.6 + k * 0.8
                aa = g1 * ease(seg(t, t0, t0 + 0.3))
                page(f, W/2 - 300 + k * 300, 1050, 240, 320, aa, seg(t, t0, t0 + 0.8), (k - 1) * 0.06)
            f.text('pages', W/2, 1300, 40, MUTED, g1 * ease(seg(t, 5.6, 5.9)), MONO, False)
        o2 = 10.7
        g2 = ease(seg(t, 7.6, 8.0)) * (1 - seg(t, o2, o2 + 0.3))
        if g2 > 0:
            words(f, 'Ton intuition :', 500, 72, 7.7, MUTED, t_out=o2)
            words(f, 'la machine a tout fait.', 620, 80, 8.1, INK, t_out=o2)
            d = 0.5 + 0.5 * math.sin((t - 8.0) * 3.0)
            press(f, W/2, 1120, 1.25, g2, d)

    # S3 — la question (10.9–13.6)
    if 10.9 <= t < 13.6:
        words(f, 'Combien de livres', 820, 100, 11.0, INK, t_out=12.5)
        words(f, 'en 50 ans ?', 950, 116, 11.4, SPARK, t_out=12.5)

    # S4 — la preuve (13.5–30)
    if 13.4 <= t < 30.0:
        # A : une journée, copiste contre presse (13.6–21.3)
        oa = 21.3
        ga = ease(seg(t, 13.5, 13.9)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Une journée de travail.', 430, 76, 13.6, INK, t_out=oa)
            p = ease_io(seg(t, 14.6, 19.6))
            # soleil qui traverse le ciel (la journée passe)
            sx = lerp(160, 920, p); sy = 600 - 90 * math.sin(math.pi * p)
            f.circle(sx, sy, 34, SPARK, ga * 0.9)
            f.line([(120, 640), (960, 640)], LINE, ga, 3)
            # colonnes
            base = 1250
            f.text('copiste', 290, 760, 46, MUTED, ga, DISPLAY, True)
            f.text('presse', 790, 760, 46, MUTED, ga, DISPLAY, True)
            nc = 3 * p
            books(f, 290, base, nc, ga, 160)
            np_ = 13 * p
            books(f, 790, base, np_, ga, 200)
            f.line([(80, base + 8), (1000, base + 8)], MUTED, ga * 0.6, 3)
            a2 = ga * ease(seg(t, 14.6, 14.9))
            c.save(); c.translate(290, 1380); s = bump(t, 19.6, 0.15); c.scale(s, s)
            f.text(f'{int(round(nc))}', 0, 0, 100, INK, a2, MONO, True); c.restore()
            val = int(round(3600 * p / 10.0)) * 10
            c.save(); c.translate(790, 1380); s = bump(t, 19.6, 0.15); c.scale(s, s)
            f.text(fmt_int(val), 0, 0, 100, SPARK, a2, MONO, True); c.restore()
            f.text('pages', W/2, 1460, 40, MUTED, a2, MONO, False)
            f.text('presse : jusqu’à 3 600 selon les estimations hautes', W/2, 1530, 28, MUTED,
                   a2 * 0.9 * ease(seg(t, 19.8, 20.1)), MONO, False)
        # B : les éditions s'empilent, 1450 -> 1500 (21.5–29.6)
        gb = ease(seg(t, 21.5, 21.9)) * (1 - seg(t, 29.4, 29.8))
        if gb > 0:
            words(f, 'Les presses se multiplient.', 430, 70, 21.6, INK, t_out=29.4)
            p = ease_io(seg(t, 22.4, 27.4))
            yr = int(round(lerp(1450, 1500, p)))
            c.save(); c.translate(W/2, 640); s = bump(t, 27.4, 0.12); c.scale(s, s)
            f.text(str(yr), 0, 0, 120, INK, gb, MONO, True); c.restore()
            # frise
            f.line([(140, 720), (940, 720)], LINE, gb, 6)
            f.line([(140, 720), (140 + 800 * p, 720)], SPARK, gb, 6)
            # piles qui montent
            for k in range(5):
                h = clamp(p * 5 - k) * (6 + k * 3.2)
                books(f, 190 + k * 175, 1250, h, gb, 130)
            f.line([(80, 1258), (1000, 1258)], MUTED, gb * 0.6, 3)
            ed = int(round(30000 * p / 100.0)) * 100
            a3 = gb * ease(seg(t, 22.4, 22.7))
            f.text(f'≈ {fmt_int(ed)}', W/2, 1390, 100, SPARK, a3, MONO, True)
            f.text('éditions différentes', W/2, 1470, 46, INK, a3, DISPLAY, True)
            f.text('recensement de la British Library (ISTC)', W/2, 1530, 28, MUTED, a3 * 0.9, MONO, False)

    # S5 — la réponse (30–36)
    if 29.9 <= t < 36.0:
        o = 35.6
        words(f, 'Environ', 620, 90, 30.0, INK, t_out=o)
        a = ease(seg(t, 30.3, 30.6)) * (1 - seg(t, o, o + 0.3))
        big_center(f, '20', 920, 300, SPARK, a, bump(t, 30.3, 0.18))
        words(f, 'millions de livres', 1090, 80, 31.0, INK, t_out=o)
        words(f, 'imprimés avant 1500.', 1200, 64, 31.8, MUTED, t_out=o)
        words(f, 'En 50 ans à peine.', 1360, 56, 33.2, SPARK, t_out=o)

    # S6 — le retournement (36–48.4)
    if 36.0 <= t < 48.4:
        words(f, 'Le secret ?', 900, 150, 36.1, SPARK, t_out=37.9)
        # A : la presse existait déjà, pour le raisin (38.1–42.6)
        oa = 42.6
        ga = ease(seg(t, 38.1, 38.5)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Pas la presse :', 440, 84, 38.2, INK, t_out=oa)
            words(f, 'on l’utilisait pour le vin.', 550, 70, 38.8, SPARK, t_out=oa)
            d = 0.5 + 0.5 * math.sin((t - 38.5) * 2.6)
            press(f, W/2, 1080, 1.3, ga, d)
            # grappe écrasée + jus
            for k in range(7):
                gx = W/2 - 90 + (k % 4) * 60 + (30 if k >= 4 else 0)
                gy = 1080 + 20 - (k // 4) * 40 - (1 - d) * 20
                f.circle(gx, gy, 24 * (1 - 0.35 * d), GRAPE, ga)
            jy = 1080 + 145
            f.rect(W/2 - 160, jy, 320, 14 + 40 * d, GRAPE, ga * 0.7, 6)
            f.text('pressoir à vis : bien avant Gutenberg', W/2, 1500, 34, MUTED, ga * ease(seg(t, 39.6, 39.9)), MONO, False)
        # B : des lettres en métal, réutilisables (42.9–47.9)
        ob = 47.9
        gb = ease(seg(t, 42.8, 43.2)) * (1 - seg(t, ob, ob + 0.3))
        if gb > 0:
            words(f, 'Des lettres en métal', 440, 80, 42.9, INK, t_out=ob)
            words(f, 'qu’on réutilise.', 550, 80, 43.5, SPARK, t_out=ob)
            src = 'CHIEN'; dst = 'NICHE'
            XS = [W/2 - 2 * 160 + k * 160 for k in range(5)]
            m = ease_io(seg(t, 45.2, 46.2))
            used = [False] * 5
            for k, ch in enumerate(src):
                j = [i for i, d in enumerate(dst) if d == ch and not used[i]][0]; used[j] = True
                x = lerp(XS[k], XS[j], m)
                lift = -90 * math.sin(math.pi * m)
                t0 = 43.6 + k * 0.15
                tblock(f, x, 940 + lift, ch, gb * ease(seg(t, t0, t0 + 0.25)), bump(t, t0, 0.15))
            word = src if m < 0.5 else dst
            pa = gb * ease(seg(t, 44.4, 44.7)) * (1 - 0.8 * math.sin(math.pi * m))
            f.rect(W/2 - 330, 1110, 660, 150, PAPER, pa, 12)
            f.text(word, W/2, 1222, 110, INKB, pa, MONO, True)
            f.text('Mêmes lettres, autre mot.', W/2, 1360, 50, EARTH, gb * ease(seg(t, 46.3, 46.6)))
            f.text('fondues en série dans un moule à main', W/2, 1480, 32, MUTED,
                   gb * 0.9 * ease(seg(t, 44.0, 44.3)), MONO, False)

    # S7 — l'escalade (48–56.4) : l'idée était déjà en Chine
    if 48.0 <= t < 56.4:
        o = 55.9
        ga = ease(seg(t, 48.1, 48.4)) * (1 - seg(t, o, o + 0.3))
        if ga > 0:
            words(f, 'L’idée existait déjà,', 430, 80, 48.1, INK, t_out=o)
            words(f, 'en Chine.', 540, 90, 48.7, SPARK, t_out=o)
            # caractères en argile qui tombent en place
            for k in range(4):
                t0 = 49.4 + k * 0.3
                aa = ga * ease(seg(t, t0, t0 + 0.3))
                dy = -80 * (1 - ease(seg(t, t0, t0 + 0.35)))
                x = W/2 - 255 + k * 170
                c.save(); c.translate(x, 860 + dy)
                f.rect(-70, -70, 140, 140, CLAY, aa, 14)
                f.rect(-70, -70, 140, 24, '#ffffff', aa * 0.15, 14)
                # motif abstrait (pas un vrai caractère)
                for r in range(3):
                    ww = 36 + 18 * ((k + r) % 3)
                    f.rect(-ww, -42 + r * 32, 2 * ww, 12, DEEP, aa, 5)
                f.circle(-30 + k * 20, 40, 9, DEEP, aa)
                c.restore()
            a1 = ga * ease(seg(t, 50.8, 51.1))
            f.text('Bi Sheng, vers 1040 :', W/2, 1060, 62, INK, a1)
            f.text('des lettres en argile cuite.', W/2, 1140, 54, MUTED, a1)
            a2 = ga * ease(seg(t, 52.6, 52.9))
            c.save(); c.translate(W/2, 1320); s = bump(t, 52.6, 0.18); c.scale(s, s)
            f.text('400 ans', 0, 0, 120, SPARK, a2, MONO, True); c.restore()
            f.text('avant Gutenberg.', W/2, 1420, 60, INK, a2)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        a = ease(seg(t, 56.1, 56.4))
        tblock(f, W/2, 640, 'A', a, bump(t, 56.1, 0.15) * 1.3, METAL, DEEP)
        words(f, 'Le génie : une lettre', 900, 84, 56.3, INK)
        words(f, 'qu’on réutilise.', 1020, 96, 57.6, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(240, 1160, 600, 150, OCEAN, a, 28)
        pa = 0.5 + 0.5 * math.sin((t - 60) * 3)
        f.rect(240, 1160, 600, 150, SPARK, a * 0.25 * pa, 28)
        f.text('Abonne-toi.', W/2, 1255, 62, INK, a)


def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    ev += [(0.15, pop(440, 0.09)), (1.2, ding(880, amp=0.18))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (12.5, 29.6, 47.9, 55.9)]
    ev += [(11.0, pop(520))]
    ev += [(15.0, rise(4.4, 300, 900, 0.07)), (19.6, clink(1500))]
    ev += [(27.4, ding(784, amp=0.2))]
    ev += [(30.3, ding(1046, amp=0.28)), (36.1, pop(300, 0.15))]
    ev += [(45.2, pop(520, 0.12)), (46.3, ding(784, amp=0.22))]
    ev += [(52.6, pop(440, 0.12))]
    ev += [(56.3, pop(440)), (60.0, ding(784, amp=0.22))]
    return ev
