"""Le biais d'ancrage : un chiffre tiré au hasard change ta réponse. Même structure que le pilote.

Sources :
- A. Tversky et D. Kahneman, « Judgment under Uncertainty: Heuristics and Biases », Science 185 (4157), 1974,
  p. 1124-1131 : roue de la fortune truquée pour s'arrêter sur 10 ou sur 65 ; question : pourcentage de pays
  africains à l'ONU ; estimations médianes 25 % (roue sur 10) et 45 % (roue sur 65) ; explication
  « ancrage et ajustement » : on part d'une valeur de départ et on ajuste trop peu.
  Repris par Wikipedia « Anchoring effect » et readthesequences.com « Anchoring and Adjustment » (médianes 25 et 45).
- B. Englich, T. Mussweiler et F. Strack, « Playing Dice With Criminal Sentences », Personality and Social
  Psychology Bulletin 32 (2), 2006 : juges allemands expérimentés, même dossier de vol à l'étalage, paire de dés
  truqués donnant 3 ou 9 ; peines moyennes d'environ 5 mois contre 8 mois. Repris par D. Kahneman,
  « Thinking, Fast and Slow », 2011 (chap. 11) et Quinn Emanuel, « Nobel Prize-Winning Insights for Trial
  Lawyers », sept. 2020.
- Aucune réponse individuelle affichée : seules les valeurs publiées (médianes, moyennes) sont montrées.
"""
import math
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro (ep022 -> electro ; ep021 était piano).
COVER = dict(tag='Psychologie', l1='Un dé truqué a changé', l2='la peine de vrais juges')

NSEC = 20                    # secteurs de la roue : 0, 5, 10, ..., 95


def wheel(f, x, y, r, phi, a, hi=None):
    """Roue de la fortune centrée en (x, y), tournée de phi degrés (sens horaire). Pointeur en haut."""
    if a <= 0: return
    c = f.c
    f.circle(x, y, r + 14, LINE, a)
    step = 360 / NSEC
    for i in range(NSEC):
        a0 = math.radians(-90 + phi + i * step - step / 2)
        a1 = a0 + math.radians(step)
        c.move_to(x, y); c.arc(x, y, r, a0, a1); c.close_path()
        f.color(CAPITAL if i % 2 == 0 else OCEAN, a); c.fill()
    for i in range(NSEC):
        ang = math.radians(-90 + phi + i * step)
        c.save(); c.translate(x + r * 0.8 * math.cos(ang), y + r * 0.8 * math.sin(ang)); c.rotate(ang + math.pi / 2)
        lab = str(i * 5)
        col = SPARK if (hi is not None and lab == hi) else INK
        f.text(lab, 0, r * 0.045, r * 0.13, col, a, MONO, True)
        c.restore()
    f.circle(x, y, r * 0.16, DEEP, a); f.circle(x, y, r * 0.07, SPARK, a)
    # pointeur
    c.move_to(x - r * 0.1, y - r - 30); c.line_to(x + r * 0.1, y - r - 30); c.line_to(x, y - r + 22); c.close_path()
    f.color(SPARK, a); c.fill()


def spin(t, t0, t1, target, turns=3, start=None):
    """Angle de la roue : tourne puis s'arrête sur le secteur `target` (valeur 0..95)."""
    i = target // 5
    end = -i * 360 / NSEC
    p = seg(t, t0, t1)
    e = 1 - (1 - p) ** 3
    if start is None: start = end - 360 * turns
    return lerp(start, end, e)


def die(f, x, y, s, n, a, col=INK):
    """Dé carré centré en (x, y), côté s, face n."""
    if a <= 0: return
    f.rect(x - s / 2, y - s / 2, s, s, col, a, s * 0.16)
    P = {1: [(0, 0)], 2: [(-1, -1), (1, 1)], 3: [(-1, -1), (0, 0), (1, 1)],
         4: [(-1, -1), (1, -1), (-1, 1), (1, 1)], 5: [(-1, -1), (1, -1), (0, 0), (-1, 1), (1, 1)],
         6: [(-1, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (1, 1)]}
    for dx, dy in P[n]:
        f.circle(x + dx * s * 0.27, y + dy * s * 0.27, s * 0.085, DEEP, a)


def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')
    c = f.c

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.8, 30.2))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('La roue compte-t-elle ?', W/2, 296, 46, SPARK, ha)

    # S1 — accroche (0–4) : la roue tourne dès la première image
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        p = ease(seg(t, 0.0, 0.6))
        wheel(f, W/2, lerp(1700, 1180, p), 300, -t * 260, fo * min(1, p * 2))
        words(f, 'Un chiffre au hasard', 520, 88, 0.15, INK, t_out=o)
        a = ease(seg(t, 1.0, 1.3)) * fo
        c.save(); c.translate(W/2, 660); s = bump(t, 1.0, 0.2); c.scale(s, s)
        f.text('change ta réponse.', 0, 0, 96, SPARK, a); c.restore()

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.0:
        ga = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, 10.7, 11.0))
        words(f, 'Une expérience de 1974.', 470, 70, 4.2, MUTED, t_out=6.9)
        # la roue s'arrête sur 10, puis sur 65
        if t < 7.2:
            phi = spin(t, 4.3, 5.9, 10); hi = '10' if t > 5.9 else None
        else:
            phi = spin(t, 7.2, 8.6, 65, 2, spin(7.2, 4.3, 5.9, 10)); hi = '65' if t > 8.6 else None
        wa = ga * (1 - seg(t, 9.0, 9.3))
        wheel(f, W/2, 1080, 280, phi, wa, hi)
        a = wa * ease(seg(t, 5.9, 6.2))
        f.text('Elle tombe sur 10…', W/2, 600, 76, INK, a * (1 - seg(t, 7.0, 7.2)))
        a = wa * ease(seg(t, 8.6, 8.9))
        f.text('… ou sur 65.', W/2, 600, 76, SPARK, a)
        # puis la question
        words(f, 'Puis :', 560, 70, 9.2, MUTED, t_out=10.7)
        words(f, 'quel % des pays de l’ONU', 700, 72, 9.4, INK, t_out=10.7)
        words(f, 'sont africains ?', 800, 72, 9.8, INK, t_out=10.7)
        a = ga * ease(seg(t, 9.6, 9.9))
        f.text('Rien à voir avec la roue.', W/2, 1000, 50, MUTED, a, bold=False)

    # S3 — la question (10.9–13.6)
    if 10.9 <= t < 13.6:
        words(f, 'La roue change-t-elle', 820, 92, 11.0, INK, t_out=12.5)
        words(f, 'la réponse ?', 950, 110, 11.4, SPARK, t_out=12.5)

    # S4 — la preuve (13.5–30)
    if 13.4 <= t < 30.0:
        ga = ease(seg(t, 13.5, 13.9)) * (1 - seg(t, 29.4, 29.8))
        if ga > 0:
            words(f, 'Deux groupes.', 430, 80, 13.6, INK, t_out=29.4)
            words(f, 'Même question.', 530, 80, 14.1, MUTED, t_out=29.4)
            XS = (290, 790)
            for j, (val, col) in enumerate(((10, INK), (65, SPARK))):
                x = XS[j]
                t0 = 14.6 + j * 0.5
                wa = ga * ease(seg(t, t0, t0 + 0.4))
                phi = spin(t, t0, t0 + 2.2, val, 3)
                wheel(f, x, 780, 130, phi, wa, str(val) if t > t0 + 2.2 else None)
                f.text(f'roue sur {val}', x, 990, 40, MUTED, wa, MONO, True)
            # barres : réponses médianes
            base = 1400; maxh = 290
            f.line([(120, base), (960, base)], MUTED, ga * ease(seg(t, 17.6, 18.0)), 4)
            for j, (val, col) in enumerate(((25, INK), (45, SPARK))):
                x = XS[j]
                t0 = 18.0 + j * 1.4
                p = ease_io(seg(t, t0, t0 + 2.4))
                v = val * p
                h = maxh * v / 50
                ba = ga * ease(seg(t, t0, t0 + 0.3))
                f.rect(x - 110, base - h, 220, h, col if j else CAPITAL, ba, 14)
                f.text(f'{int(round(v))} %', x, base - h - 28, 78, col, ba, MONO, True)
            a = ga * ease(seg(t, 23.6, 24.0))
            f.text('réponse médiane', W/2, 1470, 36, MUTED, a, MONO, False)
            # le même savoir : pulsation des deux barres et rappel
            a = ga * ease(seg(t, 25.0, 25.4))
            f.text('Seule la roue a changé.', W/2, 1540, 52, INK, a)

    # S5 — la réponse (30–36)
    if 29.9 <= t < 36.0:
        o = 33.0
        a = ease(seg(t, 30.3, 30.6)) * (1 - seg(t, o, o + 0.3))
        words(f, 'La roue sur 65 ajoute', 560, 76, 30.0, INK, t_out=o)
        c.save(); c.translate(W/2, 900); s = bump(t, 30.3, 0.18); c.scale(s, s)
        f.text('+20 points', 0, 0, 128, SPARK, a, MONO, True); c.restore()
        o2 = 35.6
        words(f, '25 % devient', 620, 90, 33.2, MUTED, t_out=o2)
        a = ease(seg(t, 33.7, 34.0)) * (1 - seg(t, o2, o2 + 0.3))
        big_center(f, '45 %', 860, 170, SPARK, a, bump(t, 33.7, 0.12))

    # S6 — le retournement : ancrage et ajustement (36–48.4)
    if 36.0 <= t < 48.4:
        words(f, 'Pourquoi ?', 900, 150, 36.1, SPARK, t_out=37.9)
        ga = ease(seg(t, 38.1, 38.5)) * (1 - seg(t, 47.9, 48.3))
        if ga > 0:
            o = 42.6
            words(f, 'Ton cerveau part', 440, 72, 38.3, INK, t_out=o)
            words(f, 'du chiffre qu’il voit.', 530, 72, 38.8, INK, t_out=o)
            words(f, 'Puis il ajuste…', 440, 72, 42.8, INK, t_out=47.9)
            words(f, 'mais trop peu.', 530, 80, 43.6, SPARK, t_out=47.9)
            # droite graduée 0–100
            y = 1000; x0, x1 = 120, 960
            X = lambda v: lerp(x0, x1, v / 100)
            la = ga * ease(seg(t, 38.6, 39.0))
            f.line([(x0, y), (x1, y)], MUTED, la, 5)
            for v in range(0, 101, 10):
                f.line([(X(v), y - 14), (X(v), y + 14)], MUTED, la, 3)
            f.text('0', X(0), y + 70, 36, MUTED, la, MONO, False)
            f.text('100', X(100), y + 70, 36, MUTED, la, MONO, False)
            # ancres
            for j, (anc, ans, col, yy) in enumerate(((10, 25, INK, -1), (65, 45, SPARK, 1))):
                t0 = 39.6 + j * 0.8
                aa = ga * ease(seg(t, t0, t0 + 0.3))
                c.save(); c.translate(X(anc), y); s = bump(t, t0, 0.3); c.scale(s, s)
                f.circle(0, 0, 18, col, aa); c.restore()
                f.text(f'roue {anc}', X(anc), y + yy * 210 + (30 if yy > 0 else 0), 38, col, aa, MONO, True)
                # ajustement : flèche qui avance puis s'arrête trop tôt
                p = ease(seg(t, 44.2 + j * 0.4, 45.8 + j * 0.4))
                if p > 0:
                    xa, xb = X(anc), lerp(X(anc), X(ans), p)
                    yl = y + yy * 50
                    f.line([(xa, yl), (xb, yl)], col, ga, 7)
                    d = 1 if ans > anc else -1
                    f.line([(xb - d * 22, yl - 16), (xb, yl), (xb - d * 22, yl + 16)], col, ga, 7)
                    if p > 0.98:
                        f.text(f'{ans} %', xb, yl + yy * 75 + (24 if yy > 0 else -6), 50, col, ga, MONO, True)
            a = ga * ease(seg(t, 46.2, 46.5))
            c.save(); c.translate(W/2, 1420); s = bump(t, 46.2, 0.15); c.scale(s, s)
            f.text('L’ancrage.', 0, 0, 96, SPARK, a); c.restore()

    # S7 — l'escalade : même des juges (48–56.4)
    if 48.0 <= t < 56.4:
        o = 55.9
        ga = ease(seg(t, 48.1, 48.4)) * (1 - seg(t, o, o + 0.3))
        if ga > 0:
            words(f, 'Même de vrais juges.', 430, 80, 48.1, INK, t_out=o)
            words(f, 'Dés truqués : 3 ou 9.', 530, 66, 49.0, MUTED, t_out=o)
            XS = (290, 790)
            for j, (d1, d2, tot, mois, col) in enumerate(((1, 2, 3, 5, INK), (4, 5, 9, 8, SPARK))):
                x = XS[j]
                t0 = 49.4 + j * 0.4
                da = ga * ease(seg(t, t0, t0 + 0.3))
                rot = (1 - ease(seg(t, t0, t0 + 0.7))) * 2.5
                for k, n in enumerate((d1, d2)):
                    c.save(); c.translate(x - 70 + k * 140, 720); c.rotate(rot * (1 if k else -1))
                    die(f, 0, 0, 110, n, da, INK); c.restore()
                f.text(f'= {tot}', x, 860, 64, col, da * ease(seg(t, t0 + 0.7, t0 + 1.0)), MONO, True)
                # peine
                t1 = 51.2 + j * 0.6
                p = ease_io(seg(t, t1, t1 + 1.4))
                pa = ga * ease(seg(t, t1, t1 + 0.3))
                h = 370 * (mois * p) / 8
                f.rect(x - 110, 1380 - h, 220, h, col if j else CAPITAL, pa, 14)
                f.text(f'{int(round(mois * p))} mois', x, 1380 - h - 26, 64, col, pa, MONO, True)
            f.line([(120, 1380), (960, 1380)], MUTED, ga * ease(seg(t, 51.0, 51.3)), 4)
            a = ga * ease(seg(t, 53.4, 53.7))
            f.text('Même dossier. Peine moyenne.', W/2, 1450, 42, INK, a, bold=False)
            f.text('Englich, Mussweiler, Strack, 2006', W/2, 1520, 30, MUTED, ga * 0.9, MONO, False)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        a = ease(seg(t, 56.1, 56.4))
        c.save(); c.translate(W/2, 620); s = bump(t, 56.1, 0.12); c.scale(s, s)
        wheel(f, 0, 0, 120, spin(t, 56.1, 57.6, 65, 2), a, '65' if t > 57.6 else None)
        c.restore()
        words(f, 'Le premier chiffre vu', 880, 76, 56.3, INK)
        words(f, 'décide à ta place.', 990, 84, 57.6, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(240, 1120, 600, 150, OCEAN, a, 28)
        pa = 0.5 + 0.5 * math.sin((t - 60) * 3)
        f.rect(240, 1120, 600, 150, SPARK, a * 0.25 * pa, 28)
        f.text('Abonne-toi.', W/2, 1215, 62, INK, a)


def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    ev += [(0.15, pop(440, 0.09)), (1.0, clink(1900))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (12.5, 29.6, 47.9, 55.9)]
    ev += [(5.9, pop(300, 0.15)), (8.6, pop(520)), (11.0, pop(520))]
    ev += [(20.0, rise(1.2, 300, 900, 0.08)), (23.6, ding(784, amp=0.2))]
    ev += [(30.3, ding(1046, amp=0.28)), (36.1, pop(300, 0.15))]
    ev += [(46.2, ding(988, amp=0.24)), (51.2, rise(1.2, 300, 900, 0.08))]
    ev += [(56.3, pop(440)), (60.0, ding(784, amp=0.22))]
    return ev
