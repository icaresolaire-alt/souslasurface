"""Pourquoi on bâille quand quelqu'un bâille. Même structure que le pilote.

Sources :
- 55 % : R. Provine. NPR, R. Krulwich, 24 sept. 2007, « The Quest to Design the Perfect Yawn » (« a medley of
  ordinary yawns on video played to a classroom for five minutes would induce a responsive yawn in 55 percent
  of the audience » ; bouche seule : le taux baisse ; lire sur le bâillement : « roughly the usual rate ») ;
  Reader's Digest (rd.com, maj 11 janv. 2024 : Provine n'a jamais trouvé de bâillement qui fasse bâiller plus de
  55 % des témoins). Concordant : Bartholomew et Cirulli, PLoS ONE 9(3), 2014, e91773 (PMC3954725 ; 328
  personnes, vidéo de 3 min, 222 ont bâillé au moins une fois, 67,7 % ; l'âge n'explique que 8 % ; empathie et
  fatigue non significatives après l'âge) et ScienceDaily, 16 mars 2014 (communiqué Duke).
- Lire ou penser au bâillement suffit : Provine, Tate et Geldmacher 1987 (résumé sur baillement.com/provine5)
  « even reading about or thinking about yawns stimulates them » ; Norscia et Palagi 2011 (PMC3233580) ; BPS
  Research Digest 19 déc. 2011 ; Neuroscience for Kids (faculty.washington.edu/chudler/yawning.html).
- Oxygène : Provine, Tate et Geldmacher, Behavioral and Neural Biology 48, 1987, p. 382-393, « Yawning: No
  effects of 3-5 % CO2, 100 % O2, and exercise » (18 étudiants, 30 min : « Neither 100% O2 nor either of the
  CO2 mixtures influenced the rate of yawning ») ; Neuroscience for Kids et Mental Floss, 12 janv. 2023
  (concordants).
- Lien social : Norscia et Palagi, PLoS ONE 6(12), 2011, e28472 (PMC3233580 ; 109 adultes observés un an en
  situation réelle ; contagion plus forte avec la famille, puis les amis, puis les connaissances, puis les
  inconnus ; délai plus long avec les inconnus) ; BPS Research Digest et National Geographic, 15 déc. 2011
  (concordants, avec la réserve d'A. Gallup : on regarde peut-être plus ses proches). Barres affichées en
  schéma, sans pourcentage. Le lien avec l'empathie est affiché comme discuté (Bartholomew et Cirulli 2014).
- Chiens : Joly-Mascheroni, Senju et Shepherd, Biology Letters 4(5), 2008, p. 446-448 (PMC2610100 : 21 chiens
  sur 29, aucun en condition contrôle, 5 min) ; Live Science, 17 sept. 2008 (21 chiens, 72 %, concordant).
- Enfants : Helt et al., Child Development, 2010, via UConn Today, 15 sept. 2010 (aucun des 20 enfants de 1 an,
  7 sur 20 à 4 ans ; « major jump ... at age four ») ; Norscia et Palagi 2011 (contagion à partir de 4-5 ans).
  Bâillement spontané dès le ventre de la mère : UConn Today ; Neuroscience for Kids.
- Visages, chiens et enfants illustratifs.
"""
import math
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro (ep043 précédent).
COVER = dict(tag='Science', l1='Pourquoi tu bâilles', l2='quand quelqu’un bâille')

SKIN = '#e9c9a3'
SKIN2 = '#c99f78'


def yawn_amt(t, t0, dur=1.8):
    """0 → 1 → 0 : la bouche s'ouvre puis se referme."""
    p = seg(t, t0, t0 + dur)
    return math.sin(math.pi * p) ** 1.4 if 0 < p < 1 else 0.0


def face(f, x, y, r, a, y_amt=0.0, col=SKIN, ring=None):
    """Visage simple ; y_amt = ouverture du bâillement (0 à 1)."""
    if a <= 0: return
    c = f.c
    if ring:
        f.circle(x, y, r + 12, ring, a * 0.9)
    f.circle(x, y, r, col, a)
    # yeux : ouverts (points) ou plissés (traits) pendant le bâillement
    ey = y - r * 0.18
    for s in (-1, 1):
        ex = x + s * r * 0.36
        if y_amt > 0.35:
            f.line([(ex - r * 0.16, ey), (ex + r * 0.16, ey + r * 0.03)], DEEP, a, max(3, r * 0.07))
        else:
            f.circle(ex, ey, r * 0.08, DEEP, a)
    # bouche : ovale qui s'ouvre
    my = y + r * 0.38
    mh = r * (0.04 + 0.5 * y_amt); mw = r * (0.36 - 0.1 * y_amt)
    c.save(); c.translate(x, my + mh * 0.3); c.scale(mw, max(mh, 1))
    c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    f.color('#4a1f22', a); c.fill()


def dog(f, x, y, s, a, col, y_amt=0.0):
    """Tête de chien stylisée : oreilles tombantes, museau qui s'ouvre."""
    if a <= 0: return
    c = f.c
    for k in (-1, 1):
        c.save(); c.translate(x + k * s * 0.62, y - s * 0.05); c.rotate(k * 0.25); c.scale(s * 0.28, s * 0.55)
        c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); f.color(SKIN2 if col == SKIN else col, a * 0.85); c.fill()
    f.circle(x, y, s * 0.62, col, a)
    for k in (-1, 1):
        f.circle(x + k * s * 0.24, y - s * 0.12, s * 0.07, DEEP, a)
    f.circle(x, y + s * 0.18, s * 0.11, DEEP, a)
    if y_amt > 0:
        c.save(); c.translate(x, y + s * 0.38); c.scale(s * 0.18, s * 0.3 * y_amt)
        c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); f.color('#4a1f22', a); c.fill()


def stamp(f, text, col, x, y, t, t0, size=88):
    p = seg(t, t0, t0 + 0.35)
    if p <= 0: return
    c = f.c; c.save(); c.translate(x, y); c.rotate(-0.12)
    s = lerp(1.6, 1.0, ease(p)); c.scale(s, s)
    w = f.width(text, size) + 70
    f.rect(-w / 2, -size * 0.78, w, size * 1.3, DEEP, 0.92 * ease(p), 8)
    c.set_line_width(10); f.color(col, ease(p)); c.rectangle(-w / 2, -size * 0.78, w, size * 1.3); c.stroke()
    f.text(text, 0, size * 0.32, size, col, ease(p))
    c.restore()


# grille de 20 visages pour la classe (11 bâillent = 55 %)
GRID = [(i % 4, i // 4) for i in range(20)]
YAWNERS = [1, 6, 3, 12, 9, 17, 14, 0, 19, 10, 5]  # ordre d'apparition
GRID_T0 = 16.0
GRID_STEP = 0.6


def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')
    c = f.c

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.8, 30.2))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Pourquoi ça se transmet ?', W/2, 296, 46, SPARK, ha)

    # S1 — accroche (0–4) : le visage bâille dès la première image
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        words(f, 'Ce visage va peut-être', 460, 66, 0.05, INK, t_out=o)
        words(f, 'te faire bâiller.', 570, 76, 1.1, SPARK, t_out=o)
        face(f, W/2, 1080, 260 * (0.9 + 0.1 * ease(seg(t, 0, 0.6))), fo, yawn_amt(t, 0.3, 3.2))

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.0:
        o1 = 7.4
        g1 = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'Ton intuition :', 460, 72, 4.2, MUTED, t_out=o1)
            words(f, 'on bâille de fatigue.', 580, 80, 4.7, INK, t_out=o1)
            # petit visage qui s'endort, Z qui montent
            face(f, W/2, 1050, 200, g1, 0.0)
            for k in range(3):
                q = ((t - 5.0) * 0.6 + k / 3) % 1.0
                f.text('z', W/2 + 200 + 60 * q, 880 - 220 * q, 60 + 30 * k, MUTED, g1 * (1 - q) * ease(seg(t, 5.2, 5.6)), MONO, True)
        o2 = 10.7
        g2 = ease(seg(t, 7.6, 8.0)) * (1 - seg(t, o2, o2 + 0.3))
        if g2 > 0:
            words(f, 'Pourtant,', 460, 72, 7.7, MUTED, t_out=o2)
            words(f, 'voir bâiller suffit.', 580, 84, 8.1, SPARK, t_out=o2)
            face(f, W/2 - 200, 1080, 160, g2, yawn_amt(t, 8.4, 1.8))
            face(f, W/2 + 200, 1080, 160, g2, yawn_amt(t, 9.4, 1.8))
            f.text('→', W/2, 1100, 90, SPARK, g2 * ease(seg(t, 9.0, 9.3)), MONO, True)

    # S3 — la question (10.9–13.6)
    if 10.9 <= t < 13.6:
        words(f, 'Pourquoi le bâillement', 820, 80, 11.0, INK, t_out=12.5)
        words(f, 'est contagieux ?', 940, 100, 11.4, SPARK, t_out=12.5)

    # S4 — la preuve (13.5–30)
    if 13.4 <= t < 30.0:
        # A : la classe devant une vidéo de bâillements (13.6–23.6)
        oa = 23.6
        ga = ease(seg(t, 13.5, 13.9)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Une classe.', 430, 84, 13.6, INK, t_out=oa)
            words(f, '5 min de bâillements.', 540, 72, 14.1, SPARK, t_out=oa)
            n = 0
            for idx, (gx, gy) in enumerate(GRID):
                x = W/2 - 330 + 220 * gx; y = 700 + 150 * gy
                fa = ga * ease(seg(t, 14.6 + 0.04 * idx, 15.0 + 0.04 * idx))
                k = YAWNERS.index(idx) if idx in YAWNERS else None
                ya = 0.0; ring = None
                if k is not None:
                    tk = GRID_T0 + GRID_STEP * k
                    if t >= tk:
                        ring = SPARK
                    ya = yawn_amt(t, tk, 1.6) + (0.15 if t >= tk + 1.6 else 0)
                face(f, x, y, 62, fa, ya, ring=ring)
            n = sum(1 for k in range(len(YAWNERS)) if t >= GRID_T0 + GRID_STEP * k)
            pct = int(round(n / 20 * 100))
            f.text(f'{pct} %', W/2, 1500, 90, SPARK, ga * ease(seg(t, 15.8, 16.1)), MONO, True)
        # B : il suffit de lire le mot (23.8–29.6)
        gb = ease(seg(t, 23.7, 24.1)) * (1 - seg(t, 29.4, 29.8))
        if gb > 0:
            words(f, 'Même lire', 430, 90, 23.8, INK, t_out=29.3)
            words(f, 'le mot suffit.', 540, 90, 24.3, SPARK, t_out=29.3)
            word = 'bâillement'
            nch = int(len(word) * seg(t, 25.0, 26.6))
            f.rect(160, 860, 760, 200, OCEAN, gb, 30)
            cur = '|' if (t * 2) % 1 < 0.5 else ' '
            f.text(word[:nch] + cur, W/2, 990, 96, INK, gb, MONO, True)
            face(f, W/2, 1300, 120, gb * ease(seg(t, 26.8, 27.1)), yawn_amt(t, 27.1, 1.8))

    # S5 — la réponse (30–36)
    if 29.9 <= t < 36.0:
        o = 35.6
        a = ease(seg(t, 30.3, 30.6)) * (1 - seg(t, o, o + 0.3))
        words(f, 'Devant une vidéo,', 600, 70, 30.0, MUTED, t_out=o)
        big_center(f, '55 %', 880, 260, SPARK, a, bump(t, 30.3, 0.18), font=DISPLAY)
        words(f, 'bâillent à leur tour.', 1060, 76, 31.0, INK, t_out=o)
        words(f, 'expériences de R. Provine', 1200, 40, 32.5, MUTED, t_out=o, font=MONO, bold=False)

    # S6 — le retournement (36–48.4)
    if 36.0 <= t < 48.4:
        words(f, 'Le manque d’air ?', 900, 110, 36.1, SPARK, t_out=37.9)
        # A : l'oxygène ne change rien (38.1–42.6)
        oa = 42.6
        ga = ease(seg(t, 38.1, 38.5)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, '100 % d’oxygène', 440, 84, 38.2, INK, t_out=oa)
            words(f, 'ou plus de CO2 :', 550, 84, 38.7, INK, t_out=oa)
            # bulles qui montent autour d'un visage
            for k in range(7):
                q = ((t - 38.4) * 0.5 + k / 7) % 1.0
                f.circle(W/2 - 330 + 110 * k, 1400 - 420 * q, 16 + 6 * (k % 3), CAPITAL, ga * (1 - q))
            face(f, W/2, 1050, 170, ga, yawn_amt(t, 39.4, 1.6))
            stamp(f, 'AUCUN EFFET', RED, W/2, 1440, t, 40.6, 74)
        # B : le lien social (42.9–47.9)
        ob = 47.9
        gb = ease(seg(t, 42.8, 43.2)) * (1 - seg(t, ob, ob + 0.3))
        if gb > 0:
            words(f, 'Le secret :', 430, 80, 42.9, MUTED, t_out=ob)
            words(f, 'ton lien avec l’autre.', 540, 80, 43.3, SPARK, t_out=ob)
            rows = [('famille', 1.0), ('amis', 0.78), ('connaissances', 0.5), ('inconnus', 0.3)]
            for i, (lab, v) in enumerate(rows):
                ts = 43.9 + 0.45 * i
                ra = gb * ease(seg(t, ts, ts + 0.3))
                yy = 720 + 165 * i
                w = 560 * v * ease_io(seg(t, ts, ts + 0.8))
                f.text(lab, 110, yy + 62, 44, INK, ra, DISPLAY, True, align='left')
                f.rect(110, yy + 82, w, 46, SPARK if i == 0 else MUTED, ra, 20)
            f.text('plus proche = plus contagieux', W/2, 1440, 40, MUTED, gb * ease(seg(t, 45.8, 46.1)), MONO, False)
            f.text('(lien avec l’empathie discuté)', W/2, 1500, 32, MUTED, gb * ease(seg(t, 46.2, 46.5)) * 0.8, MONO, False)

    # S7 — l'escalade (48–56.4)
    if 48.0 <= t < 56.4:
        o1 = 51.9
        g1 = ease(seg(t, 48.1, 48.4)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'Même ton chien', 430, 84, 48.1, INK, t_out=o1)
            words(f, 'attrape tes bâillements.', 540, 70, 48.6, SPARK, t_out=o1)
            for i in range(29):
                gx, gy = i % 6, i // 6
                x = W/2 - 375 + 150 * gx; y = 730 + 150 * gy
                tk = 49.0 + 0.07 * i
                da = g1 * ease(seg(t, tk, tk + 0.25))
                caught = i < 21 and t >= 50.0 + 0.04 * i
                dog(f, x, y, 52, da, SPARK if caught else LINE, 0.5 if caught else 0.0)
            f.text('21 chiens sur 29', W/2, 1520, 56, SPARK, g1 * ease(seg(t, 50.6, 50.9)), MONO, True)
        o2 = 55.9
        g2 = ease(seg(t, 52.1, 52.4)) * (1 - seg(t, o2, o2 + 0.3))
        if g2 > 0:
            words(f, 'Avant 4 ans,', 430, 84, 52.2, INK, t_out=o2)
            words(f, 'presque jamais.', 540, 84, 52.7, SPARK, t_out=o2)
            base = 1300
            data = [('1 an', 0, 53.3), ('2 ans', 1, 53.7), ('4 ans', 7, 54.1)]
            for i, (lab, v, ts) in enumerate(data):
                x = W/2 - 280 + 280 * i
                ia = g2 * ease(seg(t, ts, ts + 0.3))
                h = 560 * (v / 20) * ease_io(seg(t, ts, ts + 0.7)) * 2.2
                f.rect(x - 80, base - h, 160, h, SPARK if v >= 7 else MUTED, ia, 14)
                f.text(f'{v}/20', x, base - h - 26, 50, SPARK if v >= 7 else INK, ia, MONO, True)
                f.text(lab, x, base + 64, 46, INK, ia, DISPLAY, True)
            f.line([(150, base), (930, base)], LINE, g2, 6)
            f.text('ça s’installe vers 4 ans', W/2, 1500, 40, MUTED, g2 * ease(seg(t, 54.6, 54.9)), MONO, False)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        a = ease(seg(t, 56.1, 56.4))
        face(f, W/2, 760, 130, a, yawn_amt(t, 57.0, 2.0))
        words(f, 'Tu ne bâilles pas', 960, 70, 56.3, INK)
        words(f, 'seul.', 1070, 90, 57.6, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(240, 1180, 600, 150, OCEAN, a, 28)
        pa = 0.5 + 0.5 * math.sin((t - 60) * 3)
        f.rect(240, 1180, 600, 150, SPARK, a * 0.25 * pa, 28)
        f.text('Abonne-toi.', W/2, 1275, 62, INK, a)


def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    ev += [(0.15, rise(1.2, 300, 900, 0.07))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (12.5, 29.6, 47.9, 55.9)]
    ev += [(11.0, pop(520))]
    ev += [(30.3, ding(1046, amp=0.28)), (36.1, pop(300, 0.15))]
    ev += [(40.6, clink())]
    ev += [(56.3, pop(440)), (60.0, ding(784, amp=0.22))]
    return ev
