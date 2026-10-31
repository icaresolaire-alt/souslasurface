"""Ce que 100 € de l'an 2000 valent aujourd'hui (inflation). Même structure que le pilote.

Sources :
- INSEE, « L'essentiel sur... l'inflation » (insee.fr/fr/statistiques/4268033, mars 2026) : tableau de
  l'inflation annuelle moyenne (IPC, ensemble des ménages) de 2000 à 2025 ; 2022 +5,2 %, 2023 +4,9 %,
  2024 +2,0 %, 2025 +0,9 %. Produit des 25 hausses 2001-2025 : ×1,512, donc 100 € de 2000 ≈ 151 € de 2025,
  et 100 € n'achètent plus que ≈ 66 € de 2000. Somme simple des hausses : 41,9 % (affiché +42 %).
- Inflationtool, « Value of 2000 Euro (France) today » (d'après l'IPC INSEE) : 100 € de 2000 = 151,33 €
  en 2025, hausse moyenne 1,67 % par an (concordant).
- Taux de conversion fixe 1 € = 6,55957 F (règlement du Conseil, 31 déc. 1998) ; billets et pièces en euros
  le 1er janvier 2002, donc en 2000 on payait encore en francs.
- BCE, communiqué du 8 juillet 2021 (revue stratégique) et Banque de France « La BCE adopte une cible
  d'inflation claire et symétrique de 2 % » : cible de 2 % à moyen terme.
- Calcul : à 2 % par an, ln 2 / ln 1,02 = 35,0 ans pour doubler.
"""
import math
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro (ep026 précédent).
COVER = dict(tag='Argent', l1='Ce que 100 € de l’an 2000', l2='valent vraiment aujourd’hui')

NOTE = '#5f9e8a'
RATES = [1.6, 1.9, 2.1, 2.1, 1.8, 1.7, 1.5, 2.8, 0.1, 1.5, 2.1, 2.0, 0.9, 0.5, 0.0,
         0.2, 1.0, 1.9, 1.1, 0.5, 1.6, 5.2, 4.9, 2.0, 0.9]  # 2001..2025, INSEE
LEVEL = [100.0]
for r in RATES: LEVEL.append(LEVEL[-1] * (1 + r / 100))


def fmt(x, d=0):
    s = f'{x:,.{d}f}'.replace(',', ' ').replace('.', ',')
    return s


def note(f, x, y, s, a, rot=0.0, label='100 €', fade=1.0):
    """Billet stylisé."""
    if a <= 0: return
    c = f.c; c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    w, h = 420, 220
    f.rect(-w/2, -h/2, w, h, NOTE, a * fade, 18)
    f.rect(-w/2 + 16, -h/2 + 16, w - 32, h - 32, '#ffffff', a * 0.10, 12)
    f.circle(-w/2 + 90, 0, 62, '#ffffff', a * 0.16)
    f.text('€', -w/2 + 90, 26, 76, DEEP, a * 0.6, DISPLAY, True)
    f.text(label, 55, 26, 72, DEEP, a, MONO, True)
    c.restore()


def cart(f, x, y, s, a):
    if a <= 0: return
    c = f.c; c.save(); c.translate(x, y); c.scale(s, s)
    f.line([(-190, -120), (-140, -120), (-100, 60), (150, 60), (180, -70), (-125, -70)], INK, a, 12)
    f.circle(-70, 115, 24, INK, a); f.circle(120, 115, 24, INK, a)
    for k, (dx, col) in enumerate(((-60, RED), (10, SPARK), (80, EARTH))):
        f.rect(dx - 30, -130 - (k % 2) * 30, 60, 70 + (k % 2) * 30, col, a, 10)
    c.restore()


def ptag(f, x, y, txt, col, a, s=1.0, w=300):
    if a <= 0: return
    c = f.c; c.save(); c.translate(x, y); c.scale(s, s)
    f.rect(-w/2, -55, w, 110, col, a, 20)
    f.circle(-w/2 + 30, 0, 10, DEEP, a)
    f.text(txt, 14, 20, 60, DEEP, a, MONO, True)
    c.restore()


def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')
    c = f.c

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.8, 30.2))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('100 € de 2000 = ? € aujourd’hui', W/2, 296, 42, SPARK, ha)

    # S1 — accroche (0–4) : un billet tombe et pâlit dès la première image
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        words(f, 'Ton billet de 100 €', 470, 88, 0.05, INK, t_out=o)
        words(f, 'a perdu un tiers', 590, 92, 0.7, INK, t_out=o)
        words(f, 'de sa valeur.', 710, 92, 1.3, SPARK, t_out=o)
        p = seg(t, 0.0, 1.0)
        yb = 1120 - 380 * (1 - p) ** 2
        note(f, W/2, yb, 1.4 - 0.35 * ease(seg(t, 1.8, 3.6)), fo, -0.12 + 0.12 * p,
             fade=1 - 0.5 * ease(seg(t, 1.8, 3.6)))
        f.text('depuis l’an 2000', W/2, 1400, 44, MUTED, fo * ease(seg(t, 2.0, 2.3)), MONO, False)

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.0:
        o1 = 7.4
        g1 = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'Pourtant, le billet', 470, 84, 4.2, INK, t_out=o1)
            words(f, 'n’a pas changé.', 590, 92, 4.8, SPARK, t_out=o1)
            note(f, W/2, 1000, 1.5, g1, 0.04 * math.sin((t - 4) * 2))
            f.text('même papier, même chiffre', W/2, 1300, 40, MUTED, g1 * ease(seg(t, 5.6, 5.9)), MONO, False)
        o2 = 10.7
        g2 = ease(seg(t, 7.6, 8.0)) * (1 - seg(t, o2, o2 + 0.3))
        if g2 > 0:
            words(f, 'Ton intuition :', 500, 72, 7.7, MUTED, t_out=o2)
            words(f, '100 € = 100 €.', 630, 100, 8.2, INK, t_out=o2)
            wob = 0.05 * math.sin((t - 8) * 4)
            note(f, W/2 - 235, 1050, 0.95, g2, wob)
            note(f, W/2 + 235, 1050, 0.95, g2, -wob)
            f.text('en 2000', W/2 - 235, 1230, 40, MUTED, g2, MONO, False)
            f.text('en 2025', W/2 + 235, 1230, 40, MUTED, g2, MONO, False)
            f.text('=', W/2, 1085, 110, INK, g2 * ease(seg(t, 8.8, 9.1)), MONO, True)

    # S3 — la question (10.9–13.6)
    if 10.9 <= t < 13.6:
        words(f, 'Que valent 100 €', 820, 100, 11.0, INK, t_out=12.5)
        words(f, 'de l’an 2000 ?', 950, 100, 11.4, SPARK, t_out=12.5)

    # S4 — la preuve (13.5–30)
    if 13.4 <= t < 30.0:
        # A1 : en 2000, on payait en francs (13.6–17.4)
        oa = 17.4
        ga = ease(seg(t, 13.5, 13.9)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'En 2000, on payait', 440, 80, 13.6, INK, t_out=oa)
            words(f, 'encore en francs.', 550, 80, 14.2, SPARK, t_out=oa)
            note(f, W/2, 850, 1.2, ga * ease(seg(t, 14.6, 14.9)), 0.0)
            p = ease_io(seg(t, 15.2, 16.6))
            f.text(f'= {fmt(655.96 * p, 2)} F', W/2, 1180, 92, INK, ga * ease(seg(t, 15.1, 15.4)), MONO, True)
            f.text('les billets en euros arrivent en 2002', W/2, 1300, 36, MUTED,
                   ga * ease(seg(t, 15.8, 16.1)), MONO, False)
        # A2 : un panier à 100 € (17.6–21.3)
        ob = 21.3
        gb = ease(seg(t, 17.5, 17.9)) * (1 - seg(t, ob, ob + 0.3))
        if gb > 0:
            words(f, 'Prends un panier', 440, 84, 17.6, INK, t_out=ob)
            words(f, 'à 100 € en 2000.', 550, 84, 18.2, SPARK, t_out=ob)
            cart(f, W/2, 960 + 8 * math.sin(t * 3), 1.6, gb * ease(seg(t, 18.6, 18.9)))
            ptag(f, W/2 + 250, 1250, '100 €', SPARK, gb * ease(seg(t, 19.2, 19.5)), bump(t, 19.2, 0.2))
        # B : les années défilent (21.5–29.6)
        gc = ease(seg(t, 21.5, 21.9)) * (1 - seg(t, 29.4, 29.8))
        if gc > 0:
            p = seg(t, 22.4, 27.6)
            n = int(p * 25 + 1e-6)
            frac = p * 25 - n
            year = 2000 + n
            lvl = LEVEL[min(n, 25)] if n >= 25 else LEVEL[n] + (LEVEL[n + 1] - LEVEL[n]) * frac
            f.text(str(year), W/2, 470, 64, MUTED, gc, MONO, True)
            big_center(f, f'{fmt(lvl)} €', 650, 150, SPARK if n >= 25 else INK, gc)
            f.text('le même panier', W/2, 740, 38, MUTED, gc, MONO, False)
            base, x0, step, bw = 1270, 90, 36, 28
            f.line([(x0 - 6, base), (x0 + 25 * step, base)], LINE, gc, 3)
            for i, r in enumerate(RATES):
                q = clamp(p * 25 - i)
                if q <= 0: continue
                h = r * 70 * ease(q)
                col = RED if r >= 4 else SPARK
                f.rect(x0 + i * step, base - h, bw, max(h, 3), col, gc, 6)
            f.text('2001', x0 + 14, base + 50, 28, MUTED, gc, MONO, False)
            f.text('2025', x0 + 24 * step + 14, base + 50, 28, MUTED, gc, MONO, False)
            f.text('2022-2023', x0 + 22 * step, base - 410, 28, RED, gc * ease(seg(t, 26.4, 26.7)), MONO, True)
            f.text('hausse des prix chaque année (INSEE)', W/2, 1400, 32, MUTED,
                   gc * ease(seg(t, 22.6, 22.9)), MONO, False)

    # S5 — la réponse (30–36)
    if 29.9 <= t < 36.0:
        o = 35.6
        a = ease(seg(t, 30.3, 30.6)) * (1 - seg(t, o, o + 0.3))
        big_center(f, '151 €', 820, 230, SPARK, a, bump(t, 30.3, 0.18))
        words(f, 'pour le même panier', 1000, 76, 31.0, INK, t_out=o)
        words(f, 'en 2025.', 1110, 76, 31.5, INK, t_out=o)
        words(f, 'Tes 100 € n’en paient', 1280, 60, 33.0, MUTED, t_out=o)
        words(f, 'que les deux tiers.', 1360, 60, 33.4, MUTED, t_out=o)

    # S6 — le retournement (36–48.4)
    if 36.0 <= t < 48.4:
        words(f, 'Le secret ?', 900, 150, 36.1, SPARK, t_out=37.9)
        # A : additionner ne suffit pas (38.1–42.6)
        oa = 42.6
        ga = ease(seg(t, 38.1, 38.5)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Les hausses', 440, 90, 38.2, INK, t_out=oa)
            words(f, 's’empilent.', 560, 90, 38.7, SPARK, t_out=oa)
            base = 1250
            p1 = ease_io(seg(t, 39.3, 40.6)); p2 = ease_io(seg(t, 40.8, 42.2))
            for (x, v, p, col, lab) in ((330, 42, p1, CAPITAL, 'additionnées'), (750, 51, p2, SPARK, 'en vrai')):
                aa = ga * ease(seg(t, 39.1 if x < 500 else 40.6, 39.4 if x < 500 else 40.9))
                if aa <= 0: continue
                h = 520 * v / 51 * p
                f.rect(x - 115, base - 520, 230, 520, LINE, aa * 0.5, 14)
                if h > 1: f.rect(x - 115, base - h, 230, h, col, aa, 14)
                f.text(f'+{int(round(v * p))} %', x, base - h - 24, 70, INK if col == CAPITAL else SPARK, aa, MONO, True)
                f.text(lab, x, base + 60, 40, MUTED, aa, DISPLAY, True)
        # B : chaque hausse part de prix déjà montés (42.9–47.9)
        ob = 47.9
        gb = ease(seg(t, 42.8, 43.2)) * (1 - seg(t, ob, ob + 0.3))
        if gb > 0:
            words(f, 'Chaque hausse part', 440, 76, 42.9, INK, t_out=ob)
            words(f, 'de prix déjà montés.', 550, 76, 43.5, SPARK, t_out=ob)
            p = seg(t, 44.0, 47.0)
            base = 1330
            for k in range(8):
                q = clamp(p * 8 - k)
                if q <= 0: continue
                h = 120 * (1.22 ** k) * ease(q)
                x = 130 + k * 108
                f.rect(x, base - h, 88, h, SPARK if k == int(p * 8 - 1e-6) else CAPITAL, gb, 10)
                f.rect(x, base - h, 88, min(h, 22 * (1.22 ** k) * 0.6), SPARK, gb * 0.9, 10)
            f.text('hausse sur hausse, année après année', W/2, 1440, 36, MUTED,
                   gb * ease(seg(t, 44.4, 44.7)), MONO, False)

    # S7 — l'escalade (48–56.4) : la BCE vise 2 % par an
    if 48.0 <= t < 56.4:
        o = 55.9
        ga = ease(seg(t, 48.1, 48.4)) * (1 - seg(t, o, o + 0.3))
        if ga > 0:
            words(f, 'La BCE vise 2 % par an.', 430, 72, 48.1, INK, t_out=o)
            words(f, 'Exprès.', 540, 84, 48.9, SPARK, t_out=o)
            p = ease_io(seg(t, 50.0, 53.6))
            gx0, gx1, gy0, gy1 = 150, 930, 1250, 750
            aa = ga * ease(seg(t, 49.8, 50.1))
            f.line([(gx0, gy0), (gx1, gy0)], LINE, aa, 3)
            f.line([(gx0, gy1), (gx1, gy1)], LINE, aa * 0.7, 2, [10, 10])
            pts = []
            N = 60
            for i in range(int(N * p) + 1):
                yrs = 35 * i / N
                v = 1.02 ** yrs
                pts.append((gx0 + (gx1 - gx0) * yrs / 35, gy0 - (gy0 - gy1) * (v - 1)))
            if len(pts) > 1: f.line(pts, SPARK, aa, 8)
            yrs = 35 * p
            f.text(f'{fmt(100 * 1.02 ** yrs)} €', gx0 + 10, gy1 - 30, 56, INK, aa, MONO, True, 'left')
            f.text(f'{int(yrs)} ans', gx1, gy0 + 60, 40, MUTED, aa, MONO, False, 'right')
            f.text('À ce rythme, les prix', W/2, 1420, 48, INK, ga * ease(seg(t, 53.4, 53.7)))
            f.text('doublent en 35 ans.', W/2, 1490, 48, SPARK, ga * ease(seg(t, 53.4, 53.7)))

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        a = ease(seg(t, 56.1, 56.4))
        note(f, W/2, 660, 1.1 * bump(t, 56.1, 0.15), a, 0.05 * math.sin((t - 56) * 2))
        words(f, 'Un billet garde son chiffre,', 900, 66, 56.3, INK)
        words(f, 'pas ce qu’il achète.', 1010, 80, 57.6, SPARK)
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
    ev += [(19.2, clink(1500))]
    ev += [(22.6, rise(5.0, 300, 900, 0.07)), (27.6, ding(784, amp=0.2))]
    ev += [(30.3, ding(1046, amp=0.28)), (36.1, pop(300, 0.15))]
    ev += [(42.2, ding(784, amp=0.18))]
    ev += [(53.6, ding(784, amp=0.2))]
    ev += [(56.3, pop(440)), (60.0, ding(784, amp=0.22))]
    return ev
