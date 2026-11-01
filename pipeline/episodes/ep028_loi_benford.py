"""La loi de Benford : pourquoi près d'un nombre sur trois commence par 1. Même structure que le pilote.

Sources :
- Wikipedia « Benford's law » : P(d) = log10(1 + 1/d) ; 1 en tête dans 30,1 % des cas, 9 dans 4,6 % ;
  chiffres répartis uniformément = 11,1 % chacun. Newcomb 1881 : dans les tables de logarithmes, les
  premières pages (nombres commençant par 1) bien plus usées. Benford 1938, « The Law of Anomalous Numbers »,
  20 domaines, 20 229 observations (surfaces de 335 rivières, 3 259 populations, 104 constantes physiques,
  1 800 masses moléculaires...). Ne s'applique pas aux données sur un seul ordre de grandeur (tailles,
  numéros de téléphone, prix psychologiques). Varian 1972 : les gens qui inventent des chiffres les
  répartissent de façon trop uniforme.
- TU Darmstadt, module « Benford's Law - Historical Approach » : Newcomb 1881, American Journal of
  Mathematics (premières pages des tables plus usées) ; Benford, 20 contextes, environ 20 000 données.
- Law Times, 28 juillet 2014, « Benford's law a key weapon for detecting fraud » : 20 listes, 20 229
  données ; Nigrini (thèse 1992) propose l'usage par le fisc américain ; utilisé par les auditeurs
  (logiciels IDEA, ACL), l'agence du revenu du Canada s'en sert comme outil parmi d'autres ;
  « Analytics never proves a fraud » : un signal d'alerte, pas une preuve.
- Calcul (escalade du retournement) : ville à +10 % par an, de 1 000 à 2 000 hab. = ln 2 / ln 1,1 = 7,3 ans ;
  de 9 000 à 10 000 = ln(10/9) / ln 1,1 = 1,1 an ; de 1 000 à 10 000 = 24,2 ans.
"""
import math
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro (ep027 précédent).
COVER = dict(tag='Maths', l1='Pourquoi tant de nombres', l2='commencent par un 1')

BEN = [math.log10(1 + 1 / d) for d in range(1, 10)]  # 0,301 ... 0,046


def bars(f, vals, x0, base, a, hmax=520, col=SPARK, bw=74, step=98, labels=True, hi=None):
    """Histogramme des 9 premiers chiffres."""
    if a <= 0: return
    f.line([(x0 - 10, base), (x0 + 8 * step + bw + 10, base)], LINE, a, 3)
    for i, v in enumerate(vals):
        h = hmax * v / 0.301
        x = x0 + i * step
        c = col if not callable(col) else col(i)
        if h > 1: f.rect(x, base - h, bw, h, c, a, 10)
        if labels:
            f.text(str(i + 1), x + bw / 2, base + 62, 48, SPARK if hi == i else MUTED, a, MONO, True)


def page(f, x, y, d, wear, a):
    """Page d'une table de logarithmes, plus ou moins usée."""
    if a <= 0: return
    f.rect(x - 42, y - 150, 84, 300, INK, a * (0.92 - 0.45 * wear), 8)
    for k in range(7):
        f.rect(x - 28, y - 120 + k * 36, 56, 8, DEEP, a * 0.35, 3)
    # traces de doigts
    rnd = [(0.3, 0.2), (-0.4, 0.6), (0.1, -0.5), (-0.2, -0.1), (0.4, 0.8), (-0.3, -0.8)]
    for k, (u, v) in enumerate(rnd[:int(round(wear * 6))]):
        f.circle(x + u * 40, y + v * 120, 22, '#6b5a40', a * 0.55)
    f.text(str(d), x, y + 220, 52, SPARK if d == 1 else MUTED, a, MONO, True)


def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')
    c = f.c

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.8, 30.2))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Combien commencent par 1 ?', W/2, 296, 44, SPARK, ha)

    # S1 — accroche (0–4) : des chiffres tombent, le 1 grossit
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        words(f, 'Dans la vraie vie,', 470, 84, 0.05, INK, t_out=o)
        words(f, 'les nombres adorent', 590, 84, 0.6, INK, t_out=o)
        words(f, 'commencer par 1.', 710, 92, 1.2, SPARK, t_out=o)
        for d in range(1, 10):
            p = seg(t, 0.05 * d, 0.05 * d + 0.9)
            x = 140 + (d - 1) * 100
            y = 1180 - 300 * (1 - ease(p))
            s = 1.0 + (0.9 * ease(seg(t, 1.8, 3.2)) if d == 1 else 0)
            col = SPARK if d == 1 else MUTED
            cc = f.c; cc.save(); cc.translate(x, y); cc.scale(s, s)
            f.text(str(d), 0, 0, 80, col, fo * ease(p) * (1 - 0.5 * (d != 1) * ease(seg(t, 1.8, 3.2))), MONO, True)
            cc.restore()

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.0:
        o1 = 7.4
        g1 = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'Factures, villes,', 470, 84, 4.2, INK, t_out=o1)
            words(f, 'rivières, molécules…', 590, 84, 4.7, SPARK, t_out=o1)
            for k, s in enumerate(('1 284 €', '3 917 hab.', '172 km', '96,40 €', '2 731', '18 000 t')):
                aa = g1 * ease(seg(t, 5.2 + 0.2 * k, 5.5 + 0.2 * k))
                x = W/2 + (-230 if k % 2 == 0 else 230)
                y = 880 + (k // 2) * 160 + 10 * math.sin(t * 2 + k)
                f.text(s, x, y, 56, INK, aa, MONO, True)
        o2 = 10.7
        g2 = ease(seg(t, 7.6, 8.0)) * (1 - seg(t, o2, o2 + 0.3))
        if g2 > 0:
            words(f, 'Ton intuition :', 470, 72, 7.7, MUTED, t_out=o2)
            words(f, 'chaque chiffre a sa chance.', 590, 72, 8.2, INK, t_out=o2)
            p = ease_io(seg(t, 8.6, 9.6))
            bars(f, [0.111 * p] * 9, 128, 1230, g2, hmax=520, col=CAPITAL)
            f.text('1 sur 9 = 11 % chacun', W/2, 1420, 44, MUTED, g2 * ease(seg(t, 9.4, 9.7)), MONO, True)

    # S3 — la question (10.9–13.6)
    if 10.9 <= t < 13.6:
        words(f, 'Combien de nombres', 820, 96, 11.0, INK, t_out=12.5)
        words(f, 'commencent par 1 ?', 950, 96, 11.4, SPARK, t_out=12.5)

    # S4 — la preuve (13.5–30)
    if 13.4 <= t < 30.0:
        # A : Newcomb 1881, les pages usées (13.6–21)
        oa = 21.0
        ga = ease(seg(t, 13.5, 13.9)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, '1881. Un astronome', 440, 80, 13.6, INK, t_out=oa)
            words(f, 'remarque un détail.', 550, 80, 14.2, SPARK, t_out=oa)
            f.text('sa table de logarithmes', W/2, 660, 40, MUTED, ga * ease(seg(t, 14.8, 15.1)), MONO, False)
            for d in range(1, 10):
                wear = BEN[d - 1] / 0.301 * ease(seg(t, 16.0, 18.0))
                page(f, 140 + (d - 1) * 100, 1000, d, wear, ga * ease(seg(t, 15.0 + 0.08 * d, 15.3 + 0.08 * d)))
            words(f, 'Les pages des nombres en 1', 1360, 52, 18.2, INK, t_out=oa)
            words(f, 'sont les plus usées.', 1440, 52, 18.7, SPARK, t_out=oa)
        # B : Benford 1938, 20 229 nombres (21.3–29.6)
        gb = ease(seg(t, 21.2, 21.6)) * (1 - seg(t, 29.4, 29.8))
        if gb > 0:
            words(f, '1938. Frank Benford', 440, 80, 21.3, INK, t_out=29.4)
            words(f, 'compte tout.', 550, 80, 21.9, SPARK, t_out=29.4)
            p = ease_io(seg(t, 22.6, 27.6))
            f.text(fmt_int(20229 * p), W/2, 700, 96, INK, gb * ease(seg(t, 22.4, 22.7)), MONO, True)
            cats = ('rivières', 'villes', 'constantes physiques', 'masses moléculaires', 'adresses')
            k = min(4, int(seg(t, 22.6, 27.6) * 5))
            f.text(cats[k], W/2, 780, 40, MUTED, gb * ease(seg(t, 22.6, 22.9)), MONO, False)
            bars(f, [v * p for v in BEN], 128, 1300, gb * ease(seg(t, 22.6, 22.9)), hmax=420,
                 col=lambda i: SPARK if i == 0 else CAPITAL, hi=0)
            f.text('nombres relevés dans 20 domaines', W/2, 1450, 34, MUTED,
                   gb * ease(seg(t, 23.0, 23.3)), MONO, False)

    # S5 — la réponse (30–36)
    if 29.9 <= t < 36.0:
        o = 35.6
        a = ease(seg(t, 30.3, 30.6)) * (1 - seg(t, o, o + 0.3))
        big_center(f, '30 %', 820, 240, SPARK, a, bump(t, 30.3, 0.18))
        words(f, 'commencent par 1.', 1000, 80, 31.0, INK, t_out=o)
        words(f, 'Par 9 ?', 1220, 64, 32.6, MUTED, t_out=o)
        words(f, 'moins de 5 %.', 1310, 64, 33.2, INK, t_out=o)

    # S6 — le retournement (36–48.4)
    if 36.0 <= t < 48.4:
        words(f, 'Le secret ?', 900, 150, 36.1, SPARK, t_out=37.9)
        # A : passer de 1 à 2 = doubler ; de 9 à 10 = +11 % (38.1–42.6)
        oa = 42.6
        ga = ease(seg(t, 38.1, 38.5)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Pour quitter le 1,', 440, 84, 38.2, INK, t_out=oa)
            words(f, 'il faut doubler.', 560, 84, 38.8, SPARK, t_out=oa)
            # règle logarithmique
            x0, x1, y = 110, 970, 1000
            aa = ga * ease(seg(t, 39.2, 39.5))
            f.line([(x0, y), (x1, y)], LINE, aa, 4)
            for d in range(1, 11):
                x = x0 + (x1 - x0) * math.log10(d)
                f.line([(x, y - 22), (x, y + 22)], MUTED, aa, 3)
                if d <= 5 or d == 10:
                    f.text(str(d), x, y + 80, 40 if d > 1 else 52, SPARK if d == 1 else MUTED, aa, MONO, True)
            p1 = ease_io(seg(t, 39.6, 40.6))
            xa = x0 + (x1 - x0) * math.log10(2)
            f.rect(x0, y - 60, (xa - x0) * p1, 36, SPARK, aa, 10)
            f.text('×2', (x0 + xa) / 2, y - 90, 48, SPARK, aa * ease(seg(t, 40.4, 40.7)), MONO, True)
            p2 = ease_io(seg(t, 41.0, 41.6))
            x9 = x0 + (x1 - x0) * math.log10(9)
            f.rect(x9, y - 60, (x1 - x9) * p2, 36, RED, aa, 10)
            f.text('+11 %', (x9 + x1) / 2 - 20, y - 90, 44, RED, aa * ease(seg(t, 41.4, 41.7)), MONO, True)
            f.text('de 9 à 10 : un petit pas de +11 %', W/2, 1300, 44, MUTED, ga * ease(seg(t, 41.4, 41.7)), MONO, False)
        # B : une ville qui grandit de 10 % par an (42.9–48)
        ob = 47.9
        gb = ease(seg(t, 42.8, 43.2)) * (1 - seg(t, ob, ob + 0.3))
        if gb > 0:
            words(f, 'Une ville grandit', 440, 80, 42.9, INK, t_out=ob)
            words(f, 'de 10 % par an.', 550, 80, 43.4, SPARK, t_out=ob)
            p = seg(t, 44.0, 47.0)
            yrs = 24.16 * p
            pop = 1000 * 1.1 ** yrs
            f.text(f'{fmt_int(min(pop, 9999))} hab.', W/2, 720, 84, INK, gb, MONO, True)
            f.text(f'an {int(yrs)}', W/2, 790, 38, MUTED, gb, MONO, False)
            # années passées sur chaque premier chiffre
            spent = []
            for d in range(1, 10):
                lo, hi = math.log(d) / math.log(1.1), math.log(d + 1) / math.log(1.1)
                spent.append(clamp(yrs - lo, 0, hi - lo))
            bars(f, [s / 7.27 * 0.301 for s in spent], 128, 1260, gb, hmax=360,
                 col=lambda i: SPARK if i == 0 else CAPITAL, hi=0)
            f.text('7 ans sur le 1, 1 an sur le 9', W/2, 1440, 40, SPARK,
                   gb * ease(seg(t, 46.6, 46.9)), MONO, True)

    # S7 — l'escalade (48–56.4) : les chiffres inventés se trahissent
    if 48.0 <= t < 56.4:
        o = 55.9
        ga = ease(seg(t, 48.1, 48.4)) * (1 - seg(t, o, o + 0.3))
        if ga > 0:
            words(f, 'Des chiffres inventés ?', 430, 72, 48.1, INK, t_out=o)
            words(f, 'Trop bien répartis.', 540, 80, 48.8, RED, t_out=o)
            p = ease_io(seg(t, 49.6, 51.0))
            q = ease_io(seg(t, 50.6, 52.0))
            aa = ga * ease(seg(t, 49.5, 49.8))
            base, hmax = 1150, 360
            f.line([(110, base), (970, base)], LINE, aa, 3)
            for i in range(9):
                x = 128 + i * 98
                h1 = hmax * BEN[i] / 0.301 * p
                h2 = hmax * 0.111 / 0.301 * q
                if h1 > 1: f.rect(x, base - h1, 36, h1, SPARK, aa, 8)
                if h2 > 1: f.rect(x + 38, base - h2, 36, h2, RED, aa, 8)
                f.text(str(i + 1), x + 37, base + 56, 40, MUTED, aa, MONO, True)
            f.rect(250, 1240, 30, 30, SPARK, aa, 6); f.text('vrais', 300, 1266, 36, INK, aa, MONO, False, 'left')
            f.rect(600, 1240, 30, 30, RED, aa * ease(seg(t, 50.6, 50.9)), 6)
            f.text('inventés', 650, 1266, 36, INK, aa * ease(seg(t, 50.6, 50.9)), MONO, False, 'left')
            f.text('Auditeurs et fisc s’en servent', W/2, 1400, 46, INK, ga * ease(seg(t, 52.6, 52.9)))
            f.text('comme signal d’alerte.', W/2, 1470, 46, SPARK, ga * ease(seg(t, 52.6, 52.9)))

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        a = ease(seg(t, 56.1, 56.4))
        big_center(f, '1', 700, 260, SPARK, a, bump(t, 56.1, 0.15))
        words(f, 'Les vrais nombres aiment le 1.', 900, 62, 56.3, INK)
        words(f, 'Les faux, eux, se trahissent.', 1010, 70, 57.6, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(240, 1160, 600, 150, OCEAN, a, 28)
        pa = 0.5 + 0.5 * math.sin((t - 60) * 3)
        f.rect(240, 1160, 600, 150, SPARK, a * 0.25 * pa, 28)
        f.text('Abonne-toi.', W/2, 1255, 62, INK, a)


def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    ev += [(0.15, pop(440, 0.09)), (1.9, ding(880, amp=0.18))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (12.5, 29.6, 47.9, 55.9)]
    ev += [(11.0, pop(520))]
    ev += [(18.2, clink(1500))]
    ev += [(22.6, rise(5.0, 300, 900, 0.07)), (27.6, ding(784, amp=0.2))]
    ev += [(30.3, ding(1046, amp=0.28)), (36.1, pop(300, 0.15))]
    ev += [(46.6, ding(784, amp=0.18))]
    ev += [(50.6, pop(360, 0.12))]
    ev += [(56.3, pop(440)), (60.0, ding(784, amp=0.22))]
    return ev
