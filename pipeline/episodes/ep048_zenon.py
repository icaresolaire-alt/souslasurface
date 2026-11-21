"""Le paradoxe d'Achille et de la tortue (Zénon d'Élée). Même structure que le pilote.

Note : SUJETS.md parlait du « lièvre et de la tortue » ; chez Zénon c'est Achille contre la tortue
(le lièvre est chez La Fontaine). On garde la version de Zénon.

Sources :
- Zénon d'Élée, né vers 490 av. J.-C., penseur du Ve siècle av. J.-C., connu pour ses paradoxes ;
  arguments rapportés par Aristote, Physique VI 9 (239b14-18 : « the slowest runner never will be
  overtaken by the fastest ») : Stanford Encyclopedia of Philosophy, « Zeno of Elea » ; Mathwords,
  « Zeno's Paradoxes » (« Zeno of Elea (c. 490–430 BCE) »). « Près de 2 500 ans » : arrondi.
- Dichotomie (aller à mi-chemin, puis à mi-chemin du reste…) : SEP (« what moves must reach the half-way
  point earlier than the end ») ; Wikipedia « 1/2 + 1/4 + 1/8 + 1/16 + ⋯ ».
- 1/2 + 1/4 + 1/8 + … = 1, série utilisée pour représenter la dichotomie et Achille : Wikipedia
  « 1/2 + 1/4 + 1/8 + 1/16 + ⋯ » (« The sum of the series is 1 ») ; Mathwords (« converges to exactly 1 »).
- Résolution par les séries convergentes / la notion de limite : Mathwords (« resolved by the modern concept
  of convergent infinite series ») ; Wikipedia (« sometimes considered to resolve », réserve
  philosophique, d'où « les maths répondent » et non « fin du débat »).
- Exemple chiffré (Achille 10 m/s, tortue 1 m/s, 90 m d'avance) : illustratif, comme ceux de Mathwords
  (9 m, 10 m/s et 1 m/s) et de Wikipedia (10 m). Aristote ne donne pas d'avance. Calculs : écarts 90, 9,
  0,9, 0,09 m ; temps 9 + 0,9 + 0,09 + … = 10 s ; rattrapage à 100 m (10 s × 10 m/s ; 90 + 10 × 1).
"""
import math
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro (ep047 précédent).
COVER = dict(tag='Maths', l1='Pourquoi Achille ne rattrape', l2='jamais la tortue (en théorie)')

X0, X1 = 140, 940          # piste : 0 m à 110 m
def mx(m): return X0 + (X1 - X0) * m / 110.0


def achille(f, x, y, a, s=1.0):
    if a <= 0: return
    f.circle(x, y - 70 * s, 26 * s, SPARK, a)
    f.rect(x - 20 * s, y - 44 * s, 40 * s, 44 * s, SPARK, a, 12 * s)
    f.text('A', x, y - 61 * s, 30 * s, DEEP, a, DISPLAY, True)


def tortue(f, x, y, a, s=1.0):
    if a <= 0: return
    c = f.c
    f.circle(x + 34 * s, y - 16 * s, 11 * s, EARTH, a)
    f.color(EARTH, a)
    c.save(); c.translate(x, y); c.scale(1, 0.75)
    c.arc(0, 0, 34 * s, math.pi, 2 * math.pi); c.close_path(); c.fill(); c.restore()
    f.color('#2f6e55', a)
    c.save(); c.translate(x, y - 8 * s); c.scale(1, 0.6)
    c.arc(0, 0, 18 * s, math.pi, 2 * math.pi); c.close_path(); c.fill(); c.restore()


def track(f, y, a, ticks=True):
    if a <= 0: return
    f.line([(X0, y), (X1, y)], LINE, a, 6)
    if ticks:
        for m in (0, 50, 100):
            f.line([(mx(m), y - 10), (mx(m), y + 10)], MUTED, a, 3)
            f.text(f'{m} m', mx(m), y + 52, 30, MUTED, a, MONO, False)


def race_pos(u):
    """Étapes de Zénon : u ∈ [0, n] → (pos Achille, pos tortue). Étape k : Achille va là où était la tortue."""
    k = int(u); r = u - k
    pa = 100 - 100 * 0.1 ** k          # 0, 90, 99, 99.9…
    pt = 100 - 10 * 0.1 ** k           # 90, 99, 99.9…
    na = 100 - 100 * 0.1 ** (k + 1); nt = 100 - 10 * 0.1 ** (k + 1)
    e = ease_io(r)
    return lerp(pa, na, e), lerp(pt, nt, e)


GAPS = ['90 m', '9 m', '0,9 m', '0,09 m', '0,009 m', '0,0009 m']
TIMES = ['9', '0,9', '0,09', '0,009']


def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')
    c = f.c

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.8, 30.2))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Où est l’erreur ?', W/2, 296, 46, SPARK, ha)

    # S1 — accroche (0–4) : Achille court dès la première image
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        words(f, 'Achille ne rattrapera', 440, 84, 0.05, INK, t_out=o)
        words(f, 'jamais la tortue.', 550, 92, 0.5, SPARK, t_out=o)
        track(f, 1100, fo, ticks=False)
        xa = mx(10 + 60 * ease_io(seg(t, 0, 3.8))); xt = mx(80 + 6 * seg(t, 0, 3.8))
        achille(f, xa, 1100, fo, 1.3)
        tortue(f, xt, 1100, fo, 1.3)
        f.text('C’est prouvé.', W/2, 1400, 64, RED, fo * ease(seg(t, 2.2, 2.5)), DISPLAY, True)

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.0:
        o1 = 7.6
        g1 = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'Un paradoxe vieux de', 440, 76, 4.2, INK, t_out=o1)
            words(f, 'près de 2 500 ans.', 550, 84, 4.6, SPARK, t_out=o1)
            f.rect(240, 760, 600, 420, OCEAN, g1 * 0.9, 30)
            # colonne grecque stylisée
            ca = g1 * ease(seg(t, 5.0, 5.4))
            f.rect(420, 810, 240, 36, MUTED, ca, 6)
            for i in range(4):
                f.rect(445 + i * 52, 850, 34, 230 * ease(seg(t, 5.1 + 0.1 * i, 5.6 + 0.1 * i)), MUTED, ca, 4)
            f.rect(420, 1084, 240, 36, MUTED, ca, 6)
            f.text('Zénon d’Élée', W/2, 1290, 64, INK, g1 * ease(seg(t, 5.8, 6.1)), DISPLAY, True)
            f.text('né vers 490 av. J.-C.', W/2, 1370, 44, MUTED, g1 * ease(seg(t, 6.3, 6.6)), MONO, True)
        o2 = 10.7
        g2 = ease(seg(t, 7.8, 8.2)) * (1 - seg(t, o2, o2 + 0.3))
        if g2 > 0:
            words(f, 'Évidemment faux.', 520, 96, 7.9, INK, t_out=o2)
            words(f, 'Mais prouve-le.', 650, 96, 8.7, SPARK, t_out=o2)
            track(f, 1150, g2, ticks=False)
            u = seg(t, 8.2, 10.6)
            achille(f, mx(20 + 85 * u), 1150, g2, 1.3)
            tortue(f, mx(80 + 8.5 * u), 1150, g2, 1.3)
            f.text('?', mx(92), 980, 90, RED, g2 * ease(seg(t, 9.6, 9.9)), DISPLAY, True)

    # S3 — la question (10.9–13.6)
    if 10.9 <= t < 13.6:
        words(f, 'Où est', 820, 116, 11.0, INK, t_out=12.5)
        words(f, 'l’erreur ?', 950, 116, 11.4, SPARK, t_out=12.5)

    # S4 — la preuve (13.5–30)
    if 13.4 <= t < 30.0:
        # A : les étapes de Zénon (13.6–22.4)
        oa = 22.4
        ga = ease(seg(t, 13.5, 13.9)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'La tortue part', 430, 80, 13.6, INK, t_out=oa)
            words(f, 'avec 90 m d’avance.', 540, 80, 14.0, SPARK, t_out=oa)
            f.text('Achille : 10 m/s   Tortue : 1 m/s', W/2, 660, 36, MUTED,
                   ga * ease(seg(t, 14.6, 14.9)), MONO, False)
            track(f, 960, ga)
            # étapes : 0→1 de 15.6 à 17.4, puis plus vite
            starts = [15.4, 17.3, 18.7, 19.8, 20.7]
            k = 0; u = 0.0
            for i, s0 in enumerate(starts):
                if t >= s0:
                    k = i; u = i + seg(t, s0, s0 + (1.6 if i == 0 else 1.0))
            if t < starts[0]: u = 0.0
            pa, pt = race_pos(u)
            achille(f, mx(pa), 960, ga, 1.1)
            tortue(f, mx(pt), 960, ga, 1.1)
            # zoom : loupe sur la zone d'arrivée
            za = ga * ease(seg(t, 18.6, 19.0))
            if za > 0:
                f.rect(140, 1060, 800, 140, OCEAN, za * 0.9, 24)
                f.text('Achille arrive où était la tortue…', W/2, 1145, 38, INK, za, DISPLAY, True)
            ki = min(k, len(GAPS) - 2) if t >= starts[0] else -1
            gap = GAPS[ki + 1] if ki >= 0 and u - k > 0.6 else GAPS[max(ki, 0)]
            f.text('étape ' + str(max(k + 1, 1) if t >= starts[0] else 0), W/2, 1300, 44, MUTED,
                   ga * ease(seg(t, 15.4, 15.7)), MONO, True)
            f.text('écart : ' + gap, W/2, 1400, 70, SPARK,
                   ga * ease(seg(t, 15.4, 15.7)) * (0.8 + 0.2 * bump(t, starts[min(k, 4)] + 1.0, 1.0)), MONO, True)
            f.text('…elle a déjà avancé.', W/2, 1500, 44, RED, ga * ease(seg(t, 19.2, 19.5)), DISPLAY, True)
        # B : une infinité d'étapes (22.6–29.6)
        gb = ease(seg(t, 22.5, 22.9)) * (1 - seg(t, 29.4, 29.8))
        if gb > 0:
            words(f, 'Une infinité', 430, 92, 22.6, INK, t_out=29.3)
            words(f, 'd’étapes.', 545, 92, 23.0, SPARK, t_out=29.3)
            words(f, 'Donc… jamais ?', 680, 64, 23.8, RED, t_out=29.3)
            # temps de chaque étape, qui s'empilent
            for i, s in enumerate(TIMES):
                ts = 24.6 + 0.8 * i
                ra = gb * ease(seg(t, ts, ts + 0.3))
                y = 840 + i * 120
                f.rect(190, y - 66, 700, 100, OCEAN, ra * 0.9, 22)
                f.text(('+ ' if i else '') + s + ' s', W/2, y + 6, 54, INK, ra, MONO, True)
            f.text('+ …', W/2, 1340, 54, MUTED, gb * ease(seg(t, 27.8, 28.1)), MONO, True)
            tot = 10 - 10 * 0.1 ** clamp((t - 24.6) / 0.8 + 1, 0, 6)
            f.text(f'{tot:.4f} s'.replace('.', ','), W/2, 1480, 72, SPARK,
                   gb * ease(seg(t, 24.6, 24.9)), MONO, True)

    # S5 — la réponse (30–36)
    if 29.9 <= t < 36.0:
        o = 35.6
        a = ease(seg(t, 30.3, 30.6)) * (1 - seg(t, o, o + 0.3))
        words(f, 'Le total ne dépasse jamais', 580, 64, 30.0, MUTED, t_out=o)
        big_center(f, '10 s', 880, 280, SPARK, a, bump(t, 30.3, 0.18), font=DISPLAY)
        f.rect(190, 1080, 700, 130, OCEAN, a * ease(seg(t, 32.0, 32.3)) * 0.9, 28)
        words(f, 'Il la double à 100 m.', 1170, 60, 32.2, INK, t_out=o)
        track(f, 1380, a * ease(seg(t, 33.0, 33.3)), ticks=False)
        u = seg(t, 33.2, 35.4)
        achille(f, mx(60 + 50 * u), 1380, a * ease(seg(t, 33.0, 33.3)))
        tortue(f, mx(96 + 5 * u), 1380, a * ease(seg(t, 33.0, 33.3)))

    # S6 — le retournement (36–48.4)
    if 36.0 <= t < 48.4:
        words(f, 'Le secret ?', 900, 120, 36.1, SPARK, t_out=37.9)
        # A : le carré qui se remplit, 1/2 + 1/4 + … = 1 (38.1–43.4)
        oa = 43.4
        ga = ease(seg(t, 38.1, 38.5)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Des morceaux de plus en', 430, 72, 38.2, INK, t_out=oa)
            words(f, 'plus petits ne font pas l’infini.', 530, 64, 38.6, SPARK, t_out=oa)
            S = 600; x, y, w, h = W/2 - S/2, 660, S, S
            f.rect(x, y, S, S, OCEAN, ga, 8)
            labels = ['1/2', '1/4', '1/8', '1/16', '1/32', '1/64', '1/128', '', '', '']
            rx, ry, rw, rh = x, y, w, h
            for i in range(10):
                ts = 39.2 + 0.42 * i
                pa = ga * ease(seg(t, ts, ts + 0.3))
                if i % 2 == 0:
                    pw, ph = rw / 2, rh; px, py = rx, ry; rx += pw; rw -= pw
                else:
                    pw, ph = rw, rh / 2; px, py = rx, ry; ry += ph; rh -= ph
                col = SPARK if i % 2 == 0 else EARTH
                f.rect(px + 3, py + 3, max(pw - 6, 1), max(ph - 6, 1), col, pa * 0.9, 6)
                if labels[i] and i < 5:
                    f.text(labels[i], px + pw / 2, py + ph / 2 + 14, 44 - 6 * i, DEEP, pa, MONO, True)
            f.text('1/2 + 1/4 + 1/8 + … = 1', W/2, 1400, 54, SPARK, ga * ease(seg(t, 42.4, 42.7)), MONO, True)
        # B : une durée finie (43.6–47.9)
        ob = 47.9
        gb = ease(seg(t, 43.5, 43.9)) * (1 - seg(t, ob, ob + 0.3))
        if gb > 0:
            words(f, 'Infini d’étapes,', 440, 92, 43.6, INK, t_out=ob)
            words(f, 'durée finie.', 555, 92, 44.1, SPARK, t_out=ob)
            # barres de temps qui rétrécissent et s'arrêtent net sur un mur
            xs = 140; L = 760
            acc = 0.0
            for i in range(8):
                ts = 44.6 + 0.3 * i
                pa = gb * ease(seg(t, ts, ts + 0.25))
                ln = L * 0.9 * 0.1 ** i if i < 3 else max(L * 0.9 * 0.1 ** i, 3)
                f.rect(xs + acc, 820, ln * pa, 120, SPARK if i % 2 == 0 else EARTH, gb, 6)
                acc += ln
            f.line([(xs + L, 790), (xs + L, 970)], RED, gb * ease(seg(t, 45.4, 45.7)), 8)
            f.text('10 s', xs + L, 1030, 46, RED, gb * ease(seg(t, 45.4, 45.7)), MONO, True)
            f.text('Les maths appellent ça', W/2, 1240, 54, INK, gb * ease(seg(t, 46.0, 46.3)), DISPLAY, True)
            f.text('une limite.', W/2, 1340, 84, SPARK, gb * ease(seg(t, 46.5, 46.8)) * bump(t, 46.5, 0.12),
                   DISPLAY, True)

    # S7 — l'escalade (48–56.4) : la dichotomie, chacun de tes pas
    if 48.0 <= t < 56.4:
        o1 = 55.9
        g1 = ease(seg(t, 48.1, 48.4)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'Pour traverser ta chambre,', 430, 70, 48.1, INK, t_out=o1)
            words(f, 'fais d’abord la moitié.', 530, 70, 48.7, SPARK, t_out=o1)
            # pièce vue de dessus : porte à droite
            f.rect(140, 720, 800, 420, OCEAN, g1 * 0.9, 20)
            f.rect(900, 840, 40, 180, SPARK, g1 * ease(seg(t, 49.0, 49.3)), 8)
            n = clamp((t - 49.6) / 0.75, 0, 7)
            k = int(n); r = n - k
            p = 1 - 0.5 ** k; pn = 1 - 0.5 ** (k + 1)
            pos = lerp(p, pn, ease_io(r)) if t >= 49.6 else 0
            x = 200 + 680 * pos
            for j in range(1, min(k + 1, 6) + 1):
                xx = 200 + 680 * (1 - 0.5 ** j)
                f.line([(xx, 1090), (xx, 1120)], MUTED, g1, 3)
            f.circle(x, 930, 34, INK, g1)
            fr = ['1/2', '3/4', '7/8', '15/16', '31/32', '63/64', '127/128', '255/256']
            f.text('fait : ' + fr[min(k, 7)] if t >= 50.2 else '', W/2, 1260, 62, SPARK, g1, MONO, True)
            f.text('puis la moitié du reste…', W/2, 1360, 46, MUTED, g1 * ease(seg(t, 50.4, 50.7)), DISPLAY, True)
            f.text('Et tu arrives quand même.', W/2, 1480, 54, INK, g1 * ease(seg(t, 53.4, 53.7)), DISPLAY, True)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        a = ease(seg(t, 56.1, 56.4))
        track(f, 820, a, ticks=False)
        u = seg(t, 56.1, 59.5)
        achille(f, mx(40 + 70 * ease_io(u)), 820, a, 1.2)
        tortue(f, mx(88 + 6 * u), 820, a, 1.2)
        words(f, 'Une infinité d’étapes', 1030, 66, 56.3, INK)
        words(f, 'peut tenir en 10 secondes.', 1120, 62, 57.8, SPARK)
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
    ev += [(46.5, clink())]
    ev += [(56.3, pop(440)), (60.0, ding(784, amp=0.22))]
    return ev
