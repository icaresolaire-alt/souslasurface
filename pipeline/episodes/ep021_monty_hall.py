"""Le problème de Monty Hall : change de porte et tu doubles tes chances. Même structure que le pilote.

Sources :
- Wikipedia « Monty Hall problem » : énoncé (l'animateur sait où est la voiture, ouvre toujours une porte avec une
  chèvre et propose toujours de changer) ; garder = 1/3, changer = 2/3 ; posé par Steve Selvin (American Statistician,
  1975) ; réponse de Marilyn vos Savant dans « Ask Marilyn », Parade, 1990 ; environ 10 000 lettres, dont près de
  1 000 signées par des docteurs (PhD), la plupart affirmant qu'elle avait tort ; Paul Erdős pas convaincu avant
  une simulation informatique ; version avec un très grand nombre de portes pour l'intuition.
- Science Friday, extrait de « Proof » (A. Vázsonyi et P. Erdős, 1995 : « ça ne devrait faire aucune différence ») ;
  chronique de septembre 1990 et avalanche de lettres, y compris de docteurs.
- National Geographic / Discover (E. Yong) sur Herbranson et Schroeder, J. Comp. Psychol. 124(1), 2010 (non affiché).
- Calcul exact (3 cas équiprobables) et simulation affichée : 1 000 parties tirées au hasard (graine fixe),
  résultats réellement calculés ci-dessous.
"""
import math, random
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro (ep021 -> piano ; ep020 était chill).
COVER = dict(tag='Maths', l1='Le piège des 3 portes :', l2='tu gardes ou tu changes ?')

GREEN = '#6cc070'

# --- simulation réelle : 1 000 parties ---
_rnd = random.Random(21)
SIM = []
for _ in range(1000):
    car = _rnd.randrange(3); pick = _rnd.randrange(3)
    SIM.append(car == pick)          # True : garder gagne ; sinon changer gagne
CUM_KEEP = [0]
for w in SIM: CUM_KEEP.append(CUM_KEEP[-1] + (1 if w else 0))

DX = [240, 540, 840]                  # centres des 3 portes

def car(f, x, y, s, a, col=SPARK):
    if a <= 0: return
    f.rect(x - 70 * s, y - 28 * s, 140 * s, 40 * s, col, a, 14 * s)
    f.rect(x - 40 * s, y - 56 * s, 80 * s, 34 * s, col, a, 12 * s)
    f.rect(x - 30 * s, y - 50 * s, 26 * s, 22 * s, DEEP, a * 0.7, 5 * s)
    f.rect(x + 4 * s, y - 50 * s, 26 * s, 22 * s, DEEP, a * 0.7, 5 * s)
    for dx in (-40, 40):
        f.circle(x + dx * s, y + 14 * s, 17 * s, DEEP, a); f.circle(x + dx * s, y + 14 * s, 8 * s, MUTED, a)

def goat(f, x, y, s, a, col=MUTED):
    if a <= 0: return
    f.rect(x - 50 * s, y - 30 * s, 90 * s, 44 * s, col, a, 20 * s)          # corps
    for dx in (-38, -22, 18, 32):
        f.line([(x + dx * s, y + 8 * s), (x + dx * s, y + 46 * s)], col, a, 8 * s)
    f.line([(x + 30 * s, y - 20 * s), (x + 52 * s, y - 50 * s)], col, a, 16 * s)   # cou
    f.rect(x + 40 * s, y - 70 * s, 42 * s, 28 * s, col, a, 12 * s)         # tête
    f.line([(x + 50 * s, y - 68 * s), (x + 40 * s, y - 94 * s), (x + 30 * s, y - 100 * s)], col, a, 6 * s)  # corne
    f.line([(x + 66 * s, y - 44 * s), (x + 64 * s, y - 30 * s)], col, a, 5 * s)    # barbiche
    f.circle(x + 70 * s, y - 60 * s, 3.5 * s, DEEP, a)

def door(f, x, y, w, h, a, num='', opn=0.0, inside=None, hi=0.0, hi_col=SPARK):
    """Porte centrée en x, base à y. opn : 0 fermée -> 1 ouverte. inside : 'car' / 'goat'."""
    if a <= 0: return
    x0 = x - w / 2; y0 = y - h
    f.rect(x0 - 10, y0 - 10, w + 20, h + 10, LINE, a, 14)
    f.rect(x0, y0, w, h, DEEP, a, 8)
    s = w / 240
    if inside == 'car': car(f, x, y - h * 0.3, s * 1.1, a * opn ** 0.5)
    if inside == 'goat': goat(f, x - 10 * s, y - h * 0.3, s * 1.1, a * opn ** 0.5)
    ww = w * (1 - opn)
    if ww > 1:
        f.rect(x0, y0, ww, h, CAPITAL, a, 8)
        if ww > w * 0.4:
            f.circle(x0 + ww - 26 * s, y - h / 2, 9 * s, SPARK, a)
            if num: f.text(num, x0 + ww / 2, y0 + h * 0.42, 90 * s, INK, a, MONO, True)
    if hi > 0:
        c = f.c; f.color(hi_col, a * hi); c.set_line_width(8)
        c.rectangle(x0 - 16, y0 - 16, w + 32, h + 22); c.stroke()

def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')
    c = f.c

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.8, 30.2))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Garder ou changer ?', W/2, 296, 46, SPARK, ha)

    # S1 — accroche (0–4) : les portes montent dès la première image
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        for i, x in enumerate(DX):
            p = ease(seg(t, 0.0 + i * 0.12, 0.7 + i * 0.12))
            door(f, x, lerp(1900, 1420, p), 220, 340, fo * min(1, p * 3), str(i + 1))
        words(f, 'Change de porte,', 560, 96, 0.15, INK, t_out=o)
        words(f, 'tu doubles', 690, 96, 0.6, INK, t_out=o)
        a = ease(seg(t, 1.2, 1.5)) * fo
        c.save(); c.translate(W/2, 860); s = bump(t, 1.2, 0.2); c.scale(s, s)
        f.text('tes chances.', 0, 0, 120, SPARK, a); c.restore()

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.0:
        ga = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, 10.7, 11.0))
        INS = ['goat', 'car', 'goat']
        # 4–6.8 : une voiture, deux chèvres (portes ouvertes un instant)
        words(f, 'Une voiture,', 520, 88, 4.2, SPARK, t_out=6.6)
        words(f, 'deux chèvres.', 625, 88, 4.6, INK, t_out=6.6)
        opn = ease(seg(t, 4.8, 5.4)) * (1 - ease(seg(t, 6.3, 6.8)))
        # 6.9– : tu choisis la 1, l'animateur ouvre la 3 (chèvre)
        words(f, 'Tu choisis la porte 1.', 520, 72, 6.9, INK, t_out=10.6)
        words(f, 'L’animateur ouvre la 3.', 610, 72, 7.9, INK, t_out=10.6)
        for i, x in enumerate(DX):
            o_i = opn
            if i == 2: o_i = max(o_i, ease(seg(t, 8.3, 8.9)))
            hi = ease(seg(t, 7.1, 7.4)) if i == 0 else 0
            door(f, x, 1240, 240, 380, ga, str(i + 1), o_i, INS[i], hi)
        a = ga * ease(seg(t, 9.0, 9.3))
        f.text('Ton intuition :', W/2, 1360, 50, MUTED, a, bold=False)
        c.save(); c.translate(W/2, 1480); s = bump(t, 9.2); c.scale(s, s)
        f.text('50 / 50', 0, 0, 110, INK, a * ease(seg(t, 9.2, 9.5)), MONO, True); c.restore()

    # S3 — la question (10.9–13.6)
    if 10.9 <= t < 13.6:
        words(f, 'Tu gardes', 820, 110, 11.0, INK, t_out=12.5)
        words(f, 'ou tu changes ?', 960, 110, 11.4, SPARK, t_out=12.5)

    # S4 — la preuve (13.5–30)
    if 13.4 <= t < 30.0:
        # 4a : les 3 cas possibles (13.5–21.6)
        ga = ease(seg(t, 13.5, 13.9)) * (1 - seg(t, 21.3, 21.6))
        if ga > 0:
            words(f, 'Tu prends la porte 1.', 420, 70, 13.6, INK, t_out=21.3)
            words(f, 'La voiture peut être…', 505, 70, 14.0, MUTED, t_out=21.3)
            f.text('GARDER', 690, 640, 32, MUTED, ga, MONO, True)
            f.text('CHANGER', 900, 640, 32, MUTED, ga, MONO, True)
            for r in range(3):
                t0 = 14.8 + r * 1.7
                ra = ga * ease(seg(t, t0, t0 + 0.35))
                y = 820 + r * 250
                f.rect(80, y - 190, 920, 220, OCEAN, ra * 0.6, 24)
                for i in range(3):
                    x = 140 + i * 140
                    ins = 'car' if i == r else 'goat'
                    door(f, x, y, 110, 165, ra, '', 1.0, ins, 1.0 if i == 0 else 0)
                keep_win = (r == 0)
                ka = ra * ease(seg(t, t0 + 0.6, t0 + 0.9))
                f.text('gagné' if keep_win else 'perdu', 690, y - 50, 54, GREEN if keep_win else RED, ka)
                f.text('perdu' if keep_win else 'gagné', 900, y - 50, 54, RED if keep_win else GREEN, ka)
            a = ga * ease(seg(t, 19.6, 19.9))
            f.text('Garder : 1 fois sur 3.', W/2, 1450, 52, INK, a)
            f.text('Changer : 2 fois sur 3.', W/2, 1525, 52, SPARK, a)
        # 4b : simulation de 1 000 parties (21.7–29.8)
        ga = ease(seg(t, 21.7, 22.1)) * (1 - seg(t, 29.4, 29.8))
        if ga > 0:
            words(f, 'On rejoue', 430, 80, 21.8, INK, t_out=29.4)
            words(f, '1 000 fois.', 530, 80, 22.2, SPARK, t_out=29.4)
            n = int(round(1000 * ease_io(seg(t, 22.8, 27.6))))
            k = CUM_KEEP[n]; ch = n - k
            base = 1320; maxh = 620
            for j, (lab, v, col) in enumerate((('GARDER', k, MUTED), ('CHANGER', ch, SPARK))):
                x = 230 + j * 380
                h = maxh * v / 700
                f.rect(x, base - h, 240, h, col, ga, 14)
                f.text(fmt_int(v), x + 120, base - h - 30, 64, col, ga, MONO, True)
                f.text(lab, x + 120, base + 60, 36, INK, ga, MONO, True)
            f.line([(150, base), (930, base)], MUTED, ga, 4)
            f.text(f'parties : {fmt_int(n)}', W/2, 1470, 34, MUTED, ga * 0.9, MONO, False)

    # S5 — la réponse (30–36)
    if 29.9 <= t < 36.0:
        o = 33.0
        a = ease(seg(t, 30.3, 30.6)) * (1 - seg(t, o, o + 0.3))
        words(f, 'Si tu changes, tu gagnes', 560, 72, 30.0, INK, t_out=o)
        c.save(); c.translate(W/2, 880); s = bump(t, 30.3, 0.18); c.scale(s, s)
        f.text('2 fois sur 3', 0, 0, 150, SPARK, a); c.restore()
        o2 = 35.6
        words(f, 'Si tu gardes :', 620, 90, 33.2, MUTED, t_out=o2)
        a = ease(seg(t, 33.7, 34.0)) * (1 - seg(t, o2, o2 + 0.3))
        big_center(f, '1 sur 3', 830, 140, INK, a, bump(t, 33.7, 0.12))

    # S6 — le retournement : le premier choix reste à 1/3 (36–48.4)
    if 36.0 <= t < 48.4:
        words(f, 'Pourquoi ?', 900, 150, 36.1, SPARK, t_out=37.9)
        ga = ease(seg(t, 38.1, 38.5)) * (1 - seg(t, 47.9, 48.3))
        if ga > 0:
            y = 1180
            opn3 = ease(seg(t, 42.6, 43.2))
            for i, x in enumerate(DX):
                door(f, x, y, 220, 340, ga, str(i + 1), opn3 if i == 2 else 0, 'goat' if i == 2 else None,
                     1.0 if i == 0 else 0)
            # 38–42.4 : 1/3 contre 2/3
            o = 42.3
            words(f, 'Ton choix : 1 chance sur 3.', 440, 64, 38.3, INK, t_out=o)
            words(f, 'Les deux autres : 2 sur 3.', 530, 64, 39.6, SPARK, t_out=o)
            ba = ga * ease(seg(t, 39.8, 40.2))
            f.text('1/3', DX[0], 1290, 64, INK, ba * (1 - seg(t, 42.3, 42.6)), MONO, True)
            # accolade dorée autour des portes 2 et 3, qui reste
            bx0, bx1 = DX[1] - 130, DX[2] + 130
            f.line([(bx0, 1230), (bx0, 1260), (bx1, 1260), (bx1, 1230)], SPARK, ba, 7)
            frac = '2/3' if t < 44.3 else ''
            f.text(frac, (bx0 + bx1) / 2, 1340, 64, SPARK, ba * (1 - seg(t, 44.0, 44.3)), MONO, True)
            # 42.4–48 : l'animateur sait, il ouvre une chèvre, les 2/3 se reportent
            o = 47.9
            words(f, 'Il sait où est la voiture.', 440, 64, 42.4, INK, t_out=o)
            words(f, 'Il n’ouvre jamais la bonne.', 530, 64, 43.4, INK, t_out=o)
            pa = ga * ease(seg(t, 44.4, 44.8))
            c.save(); c.translate(DX[1], 1350); s = bump(t, 44.4, 0.25); c.scale(s, s)
            f.text('2/3', 0, 0, 90, SPARK, pa, MONO, True); c.restore()
            f.line([(DX[2], 1300), (DX[1] + 70, 1320)], SPARK, pa * 0.8, 5, [12, 10])
            a = ga * ease(seg(t, 45.2, 45.5))
            f.text('Les 2/3 passent', W/2, 1450, 60, INK, a)
            f.text('sur la porte 2.', W/2, 1525, 60, SPARK, a)

    # S7 — l'escalade : 100 portes, puis 1990 (48–56.4)
    if 48.0 <= t < 56.4:
        o = 52.6
        ga = ease(seg(t, 48.1, 48.4)) * (1 - seg(t, o, o + 0.3))
        if ga > 0:
            words(f, 'Avec 100 portes ?', 440, 84, 48.1, INK, t_out=o)
            opn = ease_io(seg(t, 49.4, 51.0))
            for k in range(100):
                r, cidx = divmod(k, 10)
                x = 165 + cidx * 83; y = 680 + r * 78
                keep = k in (0, 63)
                shut = 1.0 if keep else 1 - clamp(opn * 100 - (k * 0.9))
                col = SPARK if k == 0 else (INK if k == 63 and opn > 0.95 else CAPITAL)
                f.rect(x, y, 62 * 1, 64, col if shut > 0.02 else LINE, ga * (0.25 + 0.75 * shut), 6)
            a = ga * ease(seg(t, 50.9, 51.2))
            f.text('98 chèvres ouvertes.', W/2, 1520, 54, MUTED, a)
            a2 = ga * ease(seg(t, 51.4, 51.7))
            f.circle(165 + 3 * 83 + 31, 680 + 6 * 78 + 32, 54, SPARK, a2 * 0.9, 6)
        o2 = 55.9
        ga = ease(seg(t, 52.8, 53.1)) * (1 - seg(t, o2, o2 + 0.3))
        if ga > 0:
            words(f, 'En 1990,', 560, 90, 52.9, INK, t_out=o2)
            words(f, 'près de 1 000 docteurs', 700, 76, 53.3, INK, t_out=o2)
            words(f, 'ont écrit : « Faux ! »', 800, 76, 53.8, RED, t_out=o2)
            a = ga * ease(seg(t, 54.6, 54.9))
            f.text('Ils avaient tort.', W/2, 980, 80, SPARK, a)
            f.text('Parade, « Ask Marilyn », 1990', W/2, 1510, 30, MUTED, ga * 0.9, MONO, False)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        a = ease(seg(t, 56.1, 56.4))
        c.save(); c.translate(W/2, 640); s = bump(t, 56.1, 0.12); c.scale(s, s)
        door(f, 0, 110, 160, 240, a, '', ease(seg(t, 56.4, 57.2)), 'car')
        c.restore()
        words(f, 'Une porte ouverte', 860, 72, 56.3, INK)
        words(f, 'est une information.', 970, 80, 57.6, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(240, 1100, 600, 150, OCEAN, a, 28)
        pa = 0.5 + 0.5 * math.sin((t - 60) * 3)
        f.rect(240, 1100, 600, 150, SPARK, a * 0.25 * pa, 28)
        f.text('Abonne-toi.', W/2, 1195, 62, INK, a)

def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    ev += [(0.15, pop(440, 0.09)), (1.2, clink(1900))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (12.5, 29.6, 47.9, 55.9)]
    ev += [(8.3, pop(300, 0.15)), (11.0, pop(520))]
    ev += [(19.6, ding(784, amp=0.2)), (23.0, rise(1.2, 300, 900, 0.08))]
    ev += [(30.3, ding(1046, amp=0.28)), (36.1, pop(300, 0.15))]
    ev += [(44.4, ding(988, amp=0.24)), (49.4, rise(1.2, 300, 900, 0.08))]
    ev += [(56.3, pop(440)), (60.0, ding(784, amp=0.22))]
    return ev
