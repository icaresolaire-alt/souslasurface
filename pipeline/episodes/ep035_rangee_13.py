"""Pourquoi ton avion n'a pas de rangée 13 (et autres chiffres maudits). Même structure que le pilote.

Sources :
- Lufthansa, cité par SlashGear (15 août 2025, « This Well-Known Airline Skips Row 13 - Here's Why ») :
  « Next to row 13, we exclude row 17 on our aircraft as well », le 17 portant malheur « in countries such as
  Italy and Brazil » ; et par Staffordshire Live (site Lufthansa : « In some countries, for example Italy and
  Brazil, the typical unlucky number is 17 and not 13 »).
- Euronews via Yahoo UK, 21 mars 2023, « Which airlines skip row 13 and where does the superstition come from? » :
  Ryanair, Air France, Singapore Airlines, Cathay Pacific, Qatar, Emirates, KLM, Iberia sautent la rangée 13
  sur certains avions ; Judas 13e convive de la Cène ; XVII anagramme de VIXI (« j'ai vécu ») ; en chinois,
  « quatre » se prononce presque comme « mort ». Concordant : Staffordshire Live (Ryanair, Air France, Iberia ;
  British Airways, easyJet, Delta, American gardent une rangée 13).
- Immeubles : Wikipedia « Thirteenth floor » (Wikiwand) : en 2002, Dilip Rangnekar d'Otis estime que 85 % des
  immeubles de 13 étages ou plus équipés d'ascenseurs Otis n'ont pas d'étage nommé 13 ; le 13e devient « 14 ».
  Concordant : Boing Boing, 21 juillet 2026 (« the button marked 14 opens onto the actual thirteenth floor »).
  Affiché comme estimation.
- Gallup, 2007, « Thirteen Percent of Americans Bothered to Stay on Hotels' 13th Floor »
  (news.gallup.com/poll/26887), repris par Boing Boing 2026.
- Plan de cabine affiché schématique (numéros seuls, aucun modèle d'avion précis).
"""
import math
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro (ep034 précédent).
COVER = dict(tag='Histoire', l1='Pourquoi ton avion', l2='n’a pas de rangée 13')

SEAT = '#2f4f66'


def seat_row(f, y, num, a, col=SEAT, numcol=MUTED, glow=0.0, s=1.0, cx=W / 2):
    """Une rangée de 6 sièges (3 + allée + 3) centrée en cx, numéro dans l'allée."""
    if a <= 0: return
    sw, gap, aisle = 92 * s, 12 * s, 120 * s
    h = 74 * s
    if glow > 0:
        f.rect(cx - 3 * (sw + gap) - aisle / 2 - 20 * s, y - 10 * s, 6 * (sw + gap) + aisle + 40 * s, h + 20 * s,
               SPARK, a * glow * 0.3, 18 * s)
    for side in (-1, 1):
        for i in range(3):
            if side < 0:
                x = cx - aisle / 2 - (i + 1) * (sw + gap) + gap
            else:
                x = cx + aisle / 2 + i * (sw + gap)
            f.rect(x, y, sw - gap, h, col, a, 14 * s)
            f.rect(x, y, sw - gap, 14 * s, INK, a * 0.12, 6 * s)
    f.text(str(num), cx, y + h * 0.68, 40 * s, numcol, a, MONO, True)


def cabin(f, y0, nums, a, t, scroll=0.0, hl=None, mark=None, s=1.0, y_min=0, y_max=2000):
    """Liste de rangées défilantes. hl = numéro surligné, mark = numéro à barrer (rangée fantôme)."""
    if a <= 0: return
    step = 104 * s
    for i, n in enumerate(nums):
        y = y0 + i * step - scroll
        if y < y_min or y > y_max: continue
        fade = clamp((y - y_min) / 80) * clamp((y_max - y) / 80)
        if n == mark:
            f.line([(W / 2 - 330 * s, y + 37 * s), (W / 2 + 330 * s, y + 37 * s)], RED, a * fade * 0.8, 4, [14, 14])
            f.text('13', W / 2, y + 52 * s, 44 * s, RED, a * fade, MONO, True)
            continue
        g = (0.5 + 0.5 * math.sin(t * 5)) if n == hl else 0
        seat_row(f, y, n, a * fade, SEAT, SPARK if n == hl else MUTED, g, s)


def chip(f, x, y, txt, a, col=INK, size=40, bg=OCEAN):
    if a <= 0: return
    w = f.width(txt, size) + 60
    f.rect(x - w / 2, y - 50, w, 76, bg, a, 38)
    f.text(txt, x, y + 2, size, col, a)


def building(f, cx, yb, a, k, t):
    """Immeuble de 16 étages, ascenseur : boutons sans 13."""
    if a <= 0: return
    fl = 16; fh = 52; w = 300
    x0 = cx - w / 2
    nshow = int(fl * ease_io(k) + 0.999)
    for i in range(nshow):
        y = yb - (i + 1) * fh
        f.rect(x0, y, w, fh - 6, OCEAN, a, 6)
        for j in range(4):
            f.rect(x0 + 24 + j * 68, y + 12, 40, fh - 30, SPARK if (i * 7 + j) % 5 == 0 else LINE, a * 0.8, 4)
        lab = i + 1 if i < 12 else i + 2
        col = SPARK if i == 12 else MUTED
        f.text(str(lab), x0 - 50, y + 34, 30, col, a, MONO, True)
    if nshow >= 13:
        y13 = yb - 13 * fh
        g = ease(seg(k, 0.85, 1.0))
        f.line([(x0 + w + 20, y13 + 22), (x0 + w + 90, y13 + 22)], SPARK, a * g, 5)
        f.text('le vrai 13e', x0 + w + 100, y13 + 34, 34, SPARK, a * g, DISPLAY, True, 'left')


def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.8, 30.2))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Où est la rangée 13 ?', W / 2, 296, 44, SPARK, ha)

    # S1 — accroche (0–4) : la cabine défile, 12 puis 14
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        words(f, 'Dans ton avion,', 440, 76, 0.05, INK, t_out=o)
        words(f, 'il manque une rangée.', 550, 72, 0.6, SPARK, t_out=o)
        sc = 420 * ease_io(seg(t, 0.0, 3.0))
        cabin(f, 1080, [9, 10, 11, 12, 14, 15, 16, 18], fo * ease(seg(t, 0.0, 0.4)), t, sc,
              hl=14 if t > 2.4 else None, y_min=680, y_max=1560)

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.0:
        o1 = 7.4
        g1 = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'Après la 12,', 440, 80, 4.2, INK, t_out=o1)
            words(f, 'on passe à la 14.', 550, 80, 4.7, SPARK, t_out=o1)
            seat_row(f, 860, 12, g1 * ease(seg(t, 5.0, 5.4)))
            k = ease(seg(t, 5.6, 6.2))
            f.text('13 ?', W / 2, 1040, 70, RED, g1 * k, MONO, True)
            seat_row(f, 1110, 14, g1 * ease(seg(t, 6.0, 6.4)), numcol=SPARK)
        o2 = 10.7
        g2 = ease(seg(t, 7.6, 8.0)) * (1 - seg(t, o2, o2 + 0.3))
        if g2 > 0:
            words(f, 'Aucun siège retiré.', 470, 76, 7.7, INK, t_out=o2)
            words(f, 'Juste un numéro.', 580, 80, 8.2, SPARK, t_out=o2)
            p = 0.5 + 0.5 * math.sin(t * 3)
            seat_row(f, 920, 14, g2, s=1.3, numcol=SPARK, glow=p)
            f.text('= la 13e rangée', W / 2, 1200, 56, INK, g2 * ease(seg(t, 9.0, 9.4)))

    # S3 — la question (10.9–13.6)
    if 10.9 <= t < 13.6:
        words(f, 'Où est passée', 820, 90, 11.0, INK, t_out=12.5)
        words(f, 'la rangée 13 ?', 950, 90, 11.4, SPARK, t_out=12.5)

    # S4 — la preuve (13.5–30)
    if 13.4 <= t < 30.0:
        oa = 21.4
        ga = ease(seg(t, 13.5, 13.9)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Lufthansa l’assume :', 440, 74, 13.6, INK, t_out=oa)
            words(f, 'pas de 13, pas de 17.', 550, 74, 14.1, SPARK, t_out=oa)
            sc = 640 * ease_io(seg(t, 15.0, 19.6))
            cabin(f, 760, list(range(10, 13)) + [13] + list(range(14, 17)) + [17] + list(range(18, 23)),
                  ga, t, sc, mark=None, y_min=680, y_max=1560)
            # rangées fantômes 13 et 17 barrées
            for n, i in ((13, 3), (17, 7)):
                y = 760 + i * 104 - sc
                if 680 < y < 1560:
                    fade = clamp((y - 680) / 80) * clamp((1560 - y) / 80)
                    f.rect(W / 2 - 340, y, 680, 74, DEEP, ga * fade, 14)
                    f.line([(W / 2 - 330, y + 37), (W / 2 + 330, y + 37)], RED, ga * fade * 0.8, 4, [14, 14])
                    f.rect(W / 2 - 60, y + 8, 120, 58, DEEP, ga * fade, 10)
                    f.text(str(n), W / 2, y + 52, 44, RED, ga * fade, MONO, True)
            f.text('Le 17 porte malheur en Italie et au Brésil.', W / 2, 1520, 38, MUTED,
                   ga * ease(seg(t, 19.0, 19.4)))
        gb = ease(seg(t, 21.6, 22.0)) * (1 - seg(t, 29.4, 29.8))
        if gb > 0:
            words(f, 'Et elle n’est pas seule,', 440, 70, 21.7, INK, t_out=29.4)
            words(f, 'sur certains avions :', 540, 70, 22.2, SPARK, t_out=29.4)
            names = ['Air France', 'Ryanair', 'KLM', 'Iberia', 'Emirates', 'Qatar', 'Singapore', 'Cathay Pacific']
            for i, nm in enumerate(names):
                gi = gb * ease(seg(t, 23.0 + i * 0.35, 23.3 + i * 0.35))
                x = 300 if i % 2 == 0 else 780
                y = 760 + (i // 2) * 130
                chip(f, x, y, nm, gi, INK, 40)
            g2 = gb * ease(seg(t, 26.4, 26.8))
            f.text('D’autres la gardent :', W / 2, 1360, 44, MUTED, g2)
            f.text('easyJet, British Airways, Delta.', W / 2, 1430, 44, INK, g2)

    # S5 — la réponse (30–36)
    if 29.9 <= t < 36.0:
        o = 35.6
        a = ease(seg(t, 30.3, 30.6)) * (1 - seg(t, o, o + 0.3))
        words(f, 'La rangée 13 est toujours là.', 560, 62, 30.1, INK, t_out=o)
        words(f, 'Elle s’appelle', 680, 62, 30.8, INK, t_out=o)
        big_center(f, '14', 980, 300, SPARK, a, bump(t, 31.6, 0.15))
        g = a * ease(seg(t, 32.4, 32.8))
        f.text('Tu t’y assois peut-être sans le savoir.', W / 2, 1300, 42, MUTED, g, DISPLAY, True)

    # S6 — le retournement (36–48.4) : chaque pays son chiffre maudit
    if 36.0 <= t < 48.4:
        words(f, 'Pourquoi ?', 900, 130, 36.1, INK, t_out=37.9)
        oa = 42.6
        ga = ease(seg(t, 38.1, 38.5)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Le 13 arrive', 440, 76, 38.2, INK, t_out=oa)
            words(f, 'juste après le 12 parfait.', 550, 66, 38.7, SPARK, t_out=oa)
            # 12 points en cercle, puis le 13e de trop
            cx, cy, r = W / 2 - 60, 1050, 270
            for i in range(12):
                gi = ga * ease(seg(t, 39.2 + i * 0.07, 39.4 + i * 0.07))
                ang = -math.pi / 2 + i * 2 * math.pi / 12
                f.circle(cx + r * math.cos(ang), cy + r * math.sin(ang), 30, INK, gi)
            f.text('12 mois · 12 heures', cx, cy + 12, 30, MUTED, ga * ease(seg(t, 40.0, 40.4)), MONO, True)
            g13 = ga * ease(seg(t, 40.6, 41.0))
            f.circle(cx + r + 150, cy - 120, 30, RED, g13)
            f.text('13', cx + r + 150, cy - 170, 40, RED, g13, MONO, True)
            f.text('Judas, 13e à table à la Cène.', W / 2, 1450, 44, INK, ga * ease(seg(t, 41.2, 41.6)))
        ob = 47.9
        gb = ease(seg(t, 42.8, 43.2)) * (1 - seg(t, ob, ob + 0.3))
        if gb > 0:
            words(f, 'Chaque pays a', 440, 76, 42.9, INK, t_out=ob)
            words(f, 'son chiffre maudit.', 550, 76, 43.4, SPARK, t_out=ob)
            # bloc Italie : XVII -> VIXI
            g1 = gb * ease(seg(t, 44.0, 44.4))
            f.rect(110, 700, 860, 330, OCEAN, g1, 26)
            f.text('Italie', 160, 770, 40, MUTED, g1, DISPLAY, True, 'left')
            k = ease_io(seg(t, 44.6, 45.8))
            letters_a = 'XVII'; letters_b = 'VIXI'
            # positions : X V I I  ->  V I X I
            perm = [2, 0, 1, 3]   # où va chaque lettre de XVII
            for i, ch in enumerate(letters_a):
                x = lerp(330 + i * 140, 330 + perm[i] * 140, k)
                f.text(ch, x, 930, 110, SPARK if k > 0.95 else INK, g1, MONO, True)
            f.text('= « j’ai vécu »', 720, 1000, 36, INK, g1 * ease(seg(t, 45.9, 46.2)), DISPLAY, True, 'left')
            # bloc Chine : 4
            g2 = gb * ease(seg(t, 46.2, 46.6))
            f.rect(110, 1080, 860, 260, OCEAN, g2, 26)
            f.text('Chine', 160, 1150, 40, MUTED, g2, DISPLAY, True, 'left')
            f.text('4', 330, 1290, 130, SPARK, g2, MONO, True)
            f.text('se prononce', 470, 1230, 40, INK, g2, DISPLAY, True, 'left')
            f.text('presque comme « mort ».', 470, 1290, 40, INK, g2, DISPLAY, True, 'left')

    # S7 — l'escalade (48–56.4) : les immeubles
    if 48.0 <= t < 56.4:
        oa = 52.3
        ga = ease(seg(t, 48.1, 48.4)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Les immeubles aussi.', 440, 76, 48.1, INK, t_out=oa)
            building(f, 330, 1470, ga, seg(t, 48.6, 51.0), t)
            g = ga * ease(seg(t, 49.4, 49.8))
            f.text('85 %', 800, 1100, 120, SPARK, g, MONO, True)
            f.text('des immeubles', 800, 1170, 36, INK, g, DISPLAY, True)
            f.text('sans étage « 13 »', 800, 1220, 36, INK, g, DISPLAY, True)
            f.text('estimation Otis,', 800, 1290, 30, MUTED, g, MONO, False)
            f.text('ascenseurs, 2002', 800, 1330, 30, MUTED, g, MONO, False)
        o = 55.9
        gb = ease(seg(t, 52.5, 52.8)) * (1 - seg(t, o, o + 0.3))
        if gb > 0:
            words(f, 'Et ça marche :', 440, 76, 52.6, INK, t_out=o)
            n = int(round(13 * ease_io(seg(t, 53.0, 54.4))))
            big_center(f, f'{n} %', 820, 200, SPARK, gb, bump(t, 54.4, 0.12))
            words(f, 'des Américains seraient gênés', 1000, 50, 53.4, INK, t_out=o)
            words(f, 'de dormir au 13e étage.', 1070, 50, 53.8, INK, t_out=o)
            f.text('Gallup, 2007', W / 2, 1170, 32, MUTED, gb * ease(seg(t, 54.2, 54.5)), MONO, False)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        words(f, 'Le 13 n’a jamais disparu.', 760, 62, 56.3, INK)
        words(f, 'On lui a juste changé de nom.', 870, 60, 57.6, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(240, 1160, 600, 150, OCEAN, a, 28)
        pa = 0.5 + 0.5 * math.sin((t - 60) * 3)
        f.rect(240, 1160, 600, 150, SPARK, a * 0.25 * pa, 28)
        f.text('Abonne-toi.', W / 2, 1255, 62, INK, a)


def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    ev += [(0.15, pop(440, 0.09))]
    ev += [(2.4, clink(900))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (12.5, 29.6, 47.9, 55.9)]
    ev += [(11.0, pop(520))]
    ev += [(19.0, ding(784, amp=0.2))]
    ev += [(31.6, ding(1046, amp=0.28)), (36.1, pop(300, 0.15))]
    ev += [(45.8, ding(784, amp=0.18))]
    ev += [(54.4, ding(880, amp=0.18))]
    ev += [(56.3, pop(440)), (60.0, ding(784, amp=0.22))]
    return ev
