"""Pourquoi le ciel est bleu (et pas violet), et le coucher de soleil orange. Même structure que le pilote.

Sources :
- Wikipedia « Rayleigh scattering » : diffusion inversement proportionnelle à la puissance 4 de la longueur
  d'onde ; premiers articles de Lord Rayleigh sur la couleur du ciel en 1871 ; au crépuscule, la lumière du Soleil
  bas a perdu le bleu diffusé, d'où une teinte jaune à rouge.
- J. Baez / Physics FAQ (UC Riverside) « Why is the sky blue? » : (700/400)^4 ≈ 10 ; le ciel n'est pas violet
  car le Soleil en émet moins (et la haute atmosphère en absorbe) et l'œil y est moins sensible ; coucher de soleil
  rouge car le trajet dans l'air est bien plus long.
- Calcul exact affiché : (700/450)^4 ≈ 5,9 (bleu 450 nm contre rouge 700 nm), (700/400)^4 ≈ 9,4 (violet).
- Wikipedia « Air mass (solar energy) » : masse d'air vers l'horizon ≈ 38 au niveau de la mer (Kasten et Young 37,9).
- NASA SVS 11875 « Curiosity Sees Blue Sunset On Mars » : coucher de soleil bleu filmé le 15 avril 2015, la poussière
  martienne laisse passer le bleu plus efficacement.
- NASA APOD « Martian Sunset » (science.nasa.gov) : la poussière fine donne au ciel martien une teinte rougeâtre et
  diffuse le bleu vers l'avant, d'où une lueur bleutée autour du Soleil couchant.
"""
import math, random, cairo
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro (ep020 -> chill).
COVER = dict(tag='Science', l1='Le ciel devrait être violet.', l2='Pourquoi est-il bleu ?')

BLUE = '#5aa9e6'; VIOLET = '#a184ea'; ORANGE = '#f08a3c'; GREEN = '#6cc070'; OCHRE = '#c48a5a'
SPEC = [(RED, 700), (ORANGE, 600), (GREEN, 530), (BLUE, 450), (VIOLET, 400)]

def sun(f, x, y, r, a, t, col=SPARK, rays=True):
    if a <= 0: return
    if rays:
        for k in range(12):
            ang = k * math.pi / 6 + t * 0.6
            r1 = r + 22; r2 = r + 70 + 14 * math.sin(t * 4 + k)
            f.line([(x + r1 * math.cos(ang), y + r1 * math.sin(ang)),
                    (x + r2 * math.cos(ang), y + r2 * math.sin(ang))], col, a * 0.8, 8)
    f.circle(x, y, r, col, a)

def _photons():
    rnd = random.Random(20); ps = []
    for i in range(170):
        col, lam = SPEC[i % 5]
        p_scat = min(0.95, 0.09 * (700 / lam) ** 4)
        scat = rnd.random() < p_scat
        ps.append(dict(col=col, t0=13.6 + rnd.uniform(0, 5.0), y=rnd.uniform(760, 1340),
                       xs=rnd.uniform(220, 860), ang=rnd.uniform(0, 2 * math.pi), scat=scat))
    return ps
PHOT = _photons()
MOL = [(random.Random(k).uniform(130, 950), random.Random(k + 999).uniform(740, 1360)) for k in range(46)]

def photons(f, t, a):
    if a <= 0: return
    c = f.c; c.save(); c.rectangle(0, 650, W, 760); c.clip()
    for p in PHOT:
        dt = t - p['t0']
        if dt < 0 or dt > 1.6: continue
        x = 60 + dt * 900
        if p['scat'] and x > p['xs']:
            d = x - p['xs']; px = p['xs'] + d * math.cos(p['ang']); py = p['y'] + d * math.sin(p['ang'])
            dx, dy = math.cos(p['ang']), math.sin(p['ang'])
        else:
            px, py, dx, dy = x, p['y'], 1, 0
        fade = 1 - seg(dt, 1.2, 1.6)
        f.line([(px - 50 * dx, py - 50 * dy), (px, py)], p['col'], a * fade, 9)
    c.restore()

def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.8, 30.2))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Pourquoi le ciel est bleu ?', W/2, 296, 46, SPARK, ha)

    # S1 — accroche (0–4) : le Soleil monte dès la première image
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        sy = lerp(1750, 1250, ease(seg(t, 0.0, 1.6)))
        sun(f, W/2, sy, 120, fo * ease(seg(t, 0.0, 0.25)), t)
        words(f, 'Le ciel', 560, 110, 0.15, INK, t_out=o)
        words(f, 'devrait être', 690, 110, 0.5, INK, t_out=o)
        a = ease(seg(t, 1.1, 1.4)) * fo
        c = f.c; c.save(); c.translate(W/2, 860); s = bump(t, 1.1, 0.2); c.scale(s, s)
        f.text('violet.', 0, 0, 160, VIOLET, a); c.restore()

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.0:
        words(f, 'La lumière du Soleil', 480, 84, 4.2, INK, t_out=6.7)
        words(f, 'est blanche.', 590, 84, 4.6, INK, t_out=6.7)
        a = ease(seg(t, 4.4, 4.8)) * (1 - seg(t, 6.6, 6.9))
        # faisceau blanc -> prisme -> spectre
        bx = lerp(60, 470, ease(seg(t, 4.5, 5.2)))
        f.line([(60, 1050), (bx, 1050)], INK, a, 14)
        c = f.c; f.color(CAPITAL, a)
        c.move_to(540, 880); c.line_to(660, 1120); c.line_to(420, 1120); c.close_path(); c.fill()
        sp = ease(seg(t, 5.2, 5.9))
        for i, (col, lam) in enumerate(SPEC):
            ey = 1180 + (i - 2) * 70
            f.line([(560, 1040), (lerp(560, 1000, sp), lerp(1040, ey + 40, sp))], col, a, 12)
        f.text('Toutes les couleurs, mélangées.', W/2, 1420, 48, MUTED, a * ease(seg(t, 5.6, 5.9)), bold=False)
        # l'intuition
        a = ease(seg(t, 6.9, 7.2)) * (1 - seg(t, 8.8, 9.1))
        f.text('Ton intuition :', W/2, 700, 56, MUTED, a, bold=False)
        c.save(); c.translate(W/2, 860); s = bump(t, 6.9); c.scale(s, s)
        f.text('Le ciel reflète', 0, 0, 96, INK, a); f.text('la mer.', 0, 115, 96, BLUE, a)
        c.restore()
        # faux
        a = ease(seg(t, 9.0, 9.3)) * (1 - seg(t, 10.6, 10.9))
        c.save(); c.translate(W/2, 820); c.rotate(-0.08); s = bump(t, 9.0, 0.25); c.scale(s, s)
        f.rect(-230, -110, 460, 150, RED, a * 0.15, 20)
        f.text('FAUX', 0, 10, 120, RED, a, MONO, True); c.restore()
        f.text('Il est bleu même', W/2, 1060, 60, INK, a)
        f.text('au-dessus du désert.', W/2, 1140, 60, INK, a)

    # S3 — la question (10.9–13.6)
    if 10.9 <= t < 13.6:
        words(f, 'Alors pourquoi', 820, 100, 11.0, INK, t_out=12.5)
        words(f, 'est-il bleu ?', 960, 120, 11.4, BLUE, t_out=12.5)

    # S4 — la preuve (13.5–30)
    if 13.4 <= t < 30.0:
        # 4a : les molécules dévient la lumière (13.5–19.4)
        ga = ease(seg(t, 13.5, 13.9)) * (1 - seg(t, 19.2, 19.5))
        if ga > 0:
            words(f, 'L’air est plein', 420, 76, 13.6, INK, t_out=19.2)
            words(f, 'de molécules.', 515, 76, 14.0, INK, t_out=19.2)
            for k, (mx, my) in enumerate(MOL):
                f.circle(mx + 8 * math.sin(t * 1.3 + k), my + 8 * math.cos(t * 1.1 + k), 9, MUTED, ga * 0.6)
            photons(f, t, ga)
            a = ga * ease(seg(t, 16.4, 16.7))
            f.text('Elles font rebondir', W/2, 1470, 56, INK, a)
            f.text('surtout le bleu.', W/2, 1540, 56, BLUE, a)
        # 4b : barres 1/λ⁴ (19.5–25)
        ga = ease(seg(t, 19.5, 19.9)) * (1 - seg(t, 24.9, 25.2))
        if ga > 0:
            words(f, 'Plus l’onde est courte,', 420, 72, 19.6, INK, t_out=24.9)
            words(f, 'plus elle rebondit.', 510, 72, 20.0, SPARK, t_out=24.9)
            base = 1330
            for i, (col, lam) in enumerate(SPEC):
                v = (700 / lam) ** 4
                g = ease_io(seg(t, 20.4 + i * 0.35, 21.4 + i * 0.35))
                x = 160 + i * 160; h = v * 62 * g
                f.rect(x, base - h, 120, h, col, ga, 10)
                f.text(f'{lam} nm', x + 60, base + 50, 30, MUTED, ga, MONO, False)
                if g > 0.95:
                    lab = '×1' if i == 0 else '×' + f'{v:.1f}'.replace('.', ',')
                    f.text(lab, x + 60, base - h - 22, 38, col, ga, MONO, True)
            f.text('diffusion ∝ 1/λ⁴ (Rayleigh, 1871)', W/2, 1480, 30, MUTED, ga * 0.9, MONO, False)
        # 4c : le bleu vient de partout (25–29.8)
        ga = ease(seg(t, 25.1, 25.5)) * (1 - seg(t, 29.4, 29.8))
        if ga > 0:
            words(f, 'Le bleu rebondit', 440, 76, 25.2, INK, t_out=29.4)
            words(f, 'dans tout le ciel.', 535, 76, 25.6, BLUE, t_out=29.4)
            fill = ease(seg(t, 25.6, 28.2))
            f.rect(100, 640, 880, 680, BLUE, ga * 0.45 * fill, 30)
            f.line([(100, 1320), (980, 1320)], MUTED, ga, 4)
            ox, oy = W/2, 1290
            f.circle(ox, oy - 70, 18, INK, ga); f.rect(ox - 16, oy - 50, 32, 50, INK, ga, 12)
            for k in range(14):
                ang = math.pi + (k + 0.5) * math.pi / 14
                ph = ((t - 25.6) * 0.8 + k * 0.37) % 1.0
                if t < 25.6: continue
                r = lerp(600, 90, ph)
                px, py = ox + r * math.cos(ang), oy - 60 + r * math.sin(ang)
                f.line([(px, py), (px - 40 * math.cos(ang), py - 40 * math.sin(ang))], BLUE, ga * (1 - ph * 0.6), 7)

    # S5 — la réponse (30–36)
    if 29.9 <= t < 36.0:
        o = 32.8
        a = ease(seg(t, 30.3, 30.6)) * (1 - seg(t, o, o + 0.3))
        words(f, 'Le bleu rebondit', 560, 80, 30.0, INK, t_out=o)
        c = f.c; c.save(); c.translate(W/2, 860); s = bump(t, 30.3, 0.18); c.scale(s, s)
        f.text('≈ 6×', 0, 0, 240, SPARK, a); c.restore()
        words(f, 'plus que le rouge.', 1020, 80, 30.8, INK, t_out=o)
        o2 = 35.6
        words(f, 'Et le violet ?', 560, 100, 33.0, VIOLET, t_out=o2)
        a = ease(seg(t, 33.6, 33.9)) * (1 - seg(t, o2, o2 + 0.3))
        f.text('Le Soleil en émet moins,', W/2, 760, 64, INK, a)
        a = ease(seg(t, 34.2, 34.5)) * (1 - seg(t, o2, o2 + 0.3))
        f.text('et ton œil le voit mal.', W/2, 860, 64, SPARK, a)

    # S6 — le retournement : le soir, la lumière traverse bien plus d'air (36–48.4)
    if 36.0 <= t < 48.4:
        words(f, 'Et le soir ?', 900, 140, 36.1, ORANGE, t_out=37.9)
        ga = ease(seg(t, 38.1, 38.5)) * (1 - seg(t, 47.9, 48.3))
        if ga > 0:
            CX, CY, R, RA = W/2, 2350, 1000, 1170
            # atmosphère puis Terre
            f.circle(CX, CY, RA, BLUE, ga * 0.18)
            f.circle(CX, CY, R, CAPITAL, ga)
            ox, oy = CX, CY - R
            f.circle(ox, oy - 14, 14, INK, ga)
            if t < 43.0:
                o = 42.6; fa = ga * (1 - seg(t, o, o + 0.3))
                words(f, 'À midi : peu d’air.', 440, 72, 38.3, INK, t_out=o)
                p = ease(seg(t, 38.6, 39.4))
                f.line([(ox, oy - 260), (ox, lerp(oy - 260, oy - 30, p))], INK, fa, 10)
                sun(f, ox, oy - 330, 44, fa, t, rays=False)
                words(f, 'Le soir : bien plus.', 540, 72, 40.0, ORANGE, t_out=o)
                L = math.sqrt(RA ** 2 - R ** 2)
                p = ease(seg(t, 40.3, 41.6))
                x0 = ox + L + 40
                n = 16
                for k in range(n):
                    u0, u1 = k / n, (k + 1) / n
                    if 1 - u1 > p: continue
                    xa, xb = lerp(x0, ox + 30, u0), lerp(x0, ox + 30, min(u1, 1))
                    col = INK if u0 < 0.3 else (SPARK if u0 < 0.6 else ORANGE)
                    f.line([(xa, oy - 14), (xb, oy - 14)], col, fa, 10)
                sun(f, min(W - 40, x0 + 30), oy - 14, 40, fa, t, ORANGE, rays=False)
                n38 = int(lerp(1, 38, ease_io(seg(t, 40.6, 42.0))))
                f.text(f'≈ {n38} fois plus d’air', W/2, 780, 66, SPARK, fa * ease(seg(t, 40.6, 40.9)), MONO, True)
                f.text('schéma non à l’échelle', W/2, 1520, 28, MUTED, fa * 0.8, MONO, False)
            else:
                words(f, 'Le bleu se perd', 520, 84, 43.0, INK, t_out=47.9)
                words(f, 'en route.', 620, 84, 43.4, INK, t_out=47.9)
                a = ga * ease(seg(t, 44.6, 44.9))
                f.text('Il reste l’orange', W/2, 820, 76, ORANGE, a)
                f.text('et le rouge.', W/2, 910, 76, RED, a)
                glow = ease(seg(t, 43.2, 45.0))
                for k in range(6):
                    f.circle(ox, oy - 40, 120 + k * 50, ORANGE, ga * glow * 0.08)
                sun(f, ox, oy - 40, 60, ga * glow, t, ORANGE, rays=False)

    # S7 — l'escalade : sur Mars, c'est l'inverse (48–56.4)
    if 48.0 <= t < 56.4:
        o = 55.9
        words(f, 'Sur Mars,', 440, 84, 48.1, INK, t_out=o)
        words(f, 'c’est l’inverse.', 545, 84, 48.4, SPARK, t_out=o)
        for j, (t0, lab, sky, sc, glow) in enumerate(((48.8, 'Le jour', OCHRE, '#f3e3c3', None),
                                                       (50.2, 'Le soir', '#4a3a3a', '#e8f2ff', BLUE))):
            a = ease(seg(t, t0, t0 + 0.4)) * (1 - seg(t, o, o + 0.3))
            if a <= 0: continue
            x = 110 + j * 450; y = 680
            f.rect(x, y, 410, 440, sky, a, 24)
            f.rect(x, y + 360, 410, 80, '#6b4a33', a, 0)
            sy = y + (150 if j == 0 else 330)
            if glow:
                for k in range(5): f.circle(x + 205, sy, 40 + k * 26, glow, a * 0.16)
            f.circle(x + 205, sy, 30, sc, a)
            f.text(lab, x + 205, y + 520, 52, INK, a)
        a = ease(seg(t, 52.0, 52.3)) * (1 - seg(t, o, o + 0.3))
        f.text('Sa poussière fine', W/2, 1340, 60, INK, a)
        f.text('laisse passer le bleu.', W/2, 1420, 60, BLUE, a)
        f.text('Curiosity, 15 avril 2015 (NASA)', W/2, 1510, 30, MUTED, a * 0.9, MONO, False)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        a = ease(seg(t, 56.1, 56.4))
        c = f.c; c.save(); c.translate(W/2, 620); s = bump(t, 56.1, 0.12); c.scale(s, s)
        sun(f, 0, 0, 80, a, t)
        c.restore()
        words(f, 'L’air n’est pas bleu.', 860, 72, 56.3, INK)
        words(f, 'Il trie la lumière.', 970, 84, 57.6, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(240, 1100, 600, 150, OCEAN, a, 28)
        pa = 0.5 + 0.5 * math.sin((t - 60) * 3)
        f.rect(240, 1100, 600, 150, SPARK, a * 0.25 * pa, 28)
        f.text('Abonne-toi.', W/2, 1195, 62, INK, a)

def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    ev += [(0.15, pop(440, 0.09)), (1.1, clink(1900))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (12.5, 29.6, 47.9, 55.9)]
    ev += [(9.0, pop(300, 0.15)), (11.0, pop(520))]
    ev += [(21.8, ding(784, amp=0.2))]
    ev += [(30.3, ding(1046, amp=0.28)), (36.1, pop(300, 0.15))]
    ev += [(40.6, rise(1.2, 300, 900, 0.08)), (44.6, ding(988, amp=0.24))]
    ev += [(56.3, pop(440)), (60.0, ding(784, amp=0.22))]
    return ev
