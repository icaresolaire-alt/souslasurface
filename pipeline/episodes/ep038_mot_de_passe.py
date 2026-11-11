"""Pourquoi ton mot de passe de 8 caractères tombe en une nuit. Même structure que le pilote.

Sources :
- Vitesse de test : benchmark Hashcat v6.2.6 sur Nvidia RTX 4090 (gist de Chick3nman, 14 oct. 2022,
  gist.github.com/Chick3nman/32e662a5bb63bc4f51b847bb422222fd) : « Hash-Mode 0 (MD5) ... Speed.#1 : 164.1 GH/s ».
- Concordant (ordre de grandeur) : Tom's Hardware, Zhiye Liu, 1er mai 2024, « Nvidia's flagship gaming GPU can
  crack complex passwords in under an hour » (tableau Hive Systems 2024, Hashcat, MD5) : mot de passe de
  8 caractères avec majuscules, minuscules, chiffres et symboles cassé par une RTX 4090 en moins d'une heure
  dans leur scénario ; « 99 years » pour la même carte si le site utilise bcrypt.
  On affiche notre propre calcul, plus prudent (force brute complète) : 11 h.
- Calculs exacts : 95 signes imprimables ASCII.
  95^8 = 6 634 204 312 890 625 ; / 164,1e9 /s = 40 428 s = 11,2 h.
  95^9 → 44 jours ; 95^10 → 11,6 ans ; 95^12 → 104 345 ans (104 ans avec 1 000 cartes).
  26^12 = 95 428 956 661 682 176 = 14,4 fois 95^8.
- Hypothèse affichée à l'écran : la base du site a fuité et les mots de passe y sont hachés en MD5 (rapide).
"""
import math, random
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro (ep037 précédent).
COVER = dict(tag='Tech', l1='Ton mot de passe', l2='tombe en une nuit')

CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#!?$%&@*+=-_'
PWD = 'M7#qL!2x'


def rnd_chars(t, n, seed=0, speed=18):
    r = random.Random(int(t * speed) * 7919 + seed)
    return ''.join(r.choice(CHARS) for _ in range(n))


def field(f, y, s, a, found=0, w=760, size=72):
    """Champ de mot de passe : cases + caractères."""
    if a <= 0: return
    n = len(s)
    cw = w / n
    x0 = W / 2 - w / 2
    f.rect(x0 - 20, y - 70, w + 40, 120, OCEAN, a, 20)
    for i, ch in enumerate(s):
        ok = i < found
        f.rect(x0 + i * cw + 6, y - 56, cw - 12, 92, SPARK if ok else LINE, a * (0.35 if ok else 0.7), 10)
        f.text(ch, x0 + i * cw + cw / 2, y + 12, size, SPARK if ok else INK, a, MONO, True)


def gpu(f, x, y, a, t, s=1.0):
    """Carte graphique stylisée, ventilateurs qui tournent."""
    if a <= 0: return
    c = f.c
    f.rect(x - 220 * s, y - 80 * s, 440 * s, 160 * s, '#1a2f40', a, 18 * s)
    f.rect(x - 220 * s, y + 80 * s, 120 * s, 22 * s, SPARK, a * 0.8, 4)
    for k, dx in enumerate((-105, 105)):
        cx, cy = x + dx * s, y
        f.circle(cx, cy, 62 * s, LINE, a)
        for b in range(5):
            ang = t * 9 + b * 2 * math.pi / 5 + k
            f.line([(cx, cy), (cx + 55 * s * math.cos(ang), cy + 55 * s * math.sin(ang))], MUTED, a, 8 * s)
        f.circle(cx, cy, 14 * s, INK, a)


def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')
    c = f.c

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.8, 30.2))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Comment une nuit suffit ?', W/2, 296, 42, SPARK, ha)

    # S1 — accroche (0–4) : les caractères défilent dès la première image
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        words(f, 'Ton mot de passe', 470, 84, 0.05, INK, t_out=o)
        words(f, 'de 8 caractères ?', 580, 84, 0.4, INK, t_out=o)
        words(f, 'Trouvé en une nuit.', 700, 92, 1.4, SPARK, t_out=o)
        found = int(8 * seg(t, 0.3, 3.4))
        s = PWD[:found] + rnd_chars(t, 8 - found)
        field(f, 1050, s, fo, found)

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.0:
        o1 = 7.4
        g1 = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'Majuscules, chiffres,', 470, 84, 4.2, INK, t_out=o1)
            words(f, 'symboles.', 580, 92, 4.7, SPARK, t_out=o1)
            field(f, 1000, PWD, g1)
            for i, (lab, x) in enumerate((('A–Z', 280), ('0–9', 540), ('#!?', 800))):
                q = g1 * ease(seg(t, 5.2 + 0.4 * i, 5.5 + 0.4 * i))
                c.save(); c.translate(x, 1220); sc = bump(t, 5.2 + 0.4 * i, 0.2); c.scale(sc, sc)
                f.rect(-100, -55, 200, 90, LINE, q, 20)
                f.text(lab, 0, 10, 48, INK, q, MONO, True); c.restore()
        o2 = 10.7
        g2 = ease(seg(t, 7.6, 8.0)) * (1 - seg(t, o2, o2 + 0.3))
        if g2 > 0:
            words(f, 'Ton intuition :', 480, 72, 7.7, MUTED, t_out=o2)
            words(f, 'c’est incassable.', 600, 92, 8.1, SPARK, t_out=o2)
            # cadenas
            la = g2 * ease(seg(t, 8.6, 9.0))
            cy = 1050 + 8 * math.sin(t * 2)
            f.circle(W/2, cy - 120, 100, MUTED, la, 26)
            f.rect(W/2 - 160, cy - 110, 320, 260, SPARK, la, 30)
            f.circle(W/2, cy + 10, 26, DEEP, la)
            f.rect(W/2 - 10, cy + 10, 20, 70, DEEP, la, 6)

    # S3 — la question (10.9–13.6)
    if 10.9 <= t < 13.6:
        words(f, 'Alors comment', 820, 88, 11.0, INK, t_out=12.5)
        words(f, 'une nuit suffit ?', 950, 92, 11.4, SPARK, t_out=12.5)

    # S4 — la preuve (13.5–30)
    if 13.4 <= t < 30.0:
        # A : on compte les combinaisons (13.6–21.2)
        oa = 21.0
        ga = ease(seg(t, 13.5, 13.9)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, '95 signes possibles', 440, 80, 13.6, INK, t_out=oa)
            words(f, 'par case.', 545, 80, 14.0, SPARK, t_out=oa)
            k = int(8 * seg(t, 14.8, 18.4)) + (1 if t >= 14.8 else 0)
            k = min(k, 8)
            cw = 110; x0 = W/2 - 4 * cw
            for i in range(8):
                q = ga * (1.0 if i < k else 0.25)
                f.rect(x0 + i * cw + 6, 700, cw - 12, 100, LINE, q, 10)
                f.text(rnd_chars(t, 1, i) if i < k else '·', x0 + i * cw + cw / 2, 770, 58, INK, q, MONO, True)
                if i < k:
                    f.text('95', x0 + i * cw + cw / 2, 870, 34, SPARK, ga, MONO, True)
            val = 95 ** k if k else 1
            f.text('×'.join(['95'] * max(k, 1)) if k <= 4 else f'95 puissance {k}', W/2, 1000, 44, MUTED, ga * (k > 0), MONO, True)
            f.text(fmt_int(val), W/2, 1130, 64 if k < 8 else 60, SPARK, ga * (k > 0), MONO, True)
            ea = ga * ease(seg(t, 18.6, 18.9))
            c.save(); c.translate(W/2, 1300); sc = bump(t, 18.6, 0.15); c.scale(sc, sc)
            f.text('6 600 000 milliards', 0, 0, 70, INK, ea, DISPLAY, True); c.restore()
            f.text('de combinaisons', W/2, 1380, 48, MUTED, ea, DISPLAY, True)
        # B : la vitesse d'une carte graphique (21.4–29.6)
        gb = ease(seg(t, 21.3, 21.7)) * (1 - seg(t, 29.4, 29.8))
        if gb > 0:
            words(f, 'Une carte graphique', 440, 80, 21.4, INK, t_out=29.3)
            words(f, 'en teste…', 545, 80, 21.9, INK, t_out=29.3)
            gpu(f, W/2, 760, gb, t)
            sp = ease_io(seg(t, 22.6, 25.6))
            f.text(fmt_int(164.1e9 * sp), W/2, 1020, 76, SPARK, gb, MONO, True)
            m1 = gb * ease(seg(t, 25.7, 26.0))
            f.text('164 milliards', W/2, 1160, 70, INK, m1, DISPLAY, True)
            f.text('par seconde', W/2, 1240, 52, MUTED, m1, DISPLAY, True)
            # flux de mots de passe testés
            m2 = gb * ease(seg(t, 26.6, 26.9))
            for j in range(3):
                f.text(rnd_chars(t + j, 8, j, 30), W/2, 1340 + 60 * j, 38, MUTED, m2 * (0.8 - 0.25 * j), MONO, False)

    # S5 — la réponse (30–36)
    if 29.9 <= t < 36.0:
        o = 35.6
        a = ease(seg(t, 30.3, 30.6)) * (1 - seg(t, o, o + 0.3))
        words(f, 'Tout tester prend', 560, 76, 30.0, INK, t_out=o)
        big_center(f, '11 h', 860, 240, SPARK, a, bump(t, 30.3, 0.18))
        words(f, 'Une nuit.', 1040, 84, 31.2, INK, t_out=o)
        na = a * ease(seg(t, 32.4, 32.7))
        f.text('si la base du site a fuité', W/2, 1240, 40, MUTED, na, DISPLAY, True)
        f.text('protégée en MD5, 1 carte RTX 4090', W/2, 1300, 34, MUTED, na, MONO, False)

    # S6 — le retournement (36–48.4)
    if 36.0 <= t < 48.4:
        words(f, 'Le secret ?', 900, 150, 36.1, SPARK, t_out=37.9)
        # A : chaque caractère en plus multiplie par 95 (38.1–42.6)
        oa = 42.6
        ga = ease(seg(t, 38.1, 38.5)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Un caractère de plus', 440, 80, 38.2, INK, t_out=oa)
            words(f, 'multiplie par 95.', 550, 88, 38.7, SPARK, t_out=oa)
            rows = [('8', '11 h', 0.08), ('9', '44 jours', 0.3), ('10', '11,6 ans', 1.0)]
            for i, (n, lab, frac) in enumerate(rows):
                q = ga * ease(seg(t, 39.3 + 0.9 * i, 39.6 + 0.9 * i))
                y = 760 + 190 * i
                f.text(f'{n} car.', 150, y + 20, 44, INK, q, MONO, True, 'left')
                grow = ease(seg(t, 39.3 + 0.9 * i, 40.0 + 0.9 * i))
                f.rect(360, y - 30, max(20, 580 * frac * grow), 60, SPARK if i == 2 else MUTED, q, 10)
                f.text(lab, 360, y + 95, 44, SPARK if i == 2 else INK, q, MONO, True, 'left')
        # B : 12 minuscules battent 8 signes variés (42.9–47.9)
        ob = 47.9
        gb = ease(seg(t, 42.8, 43.2)) * (1 - seg(t, ob, ob + 0.3))
        if gb > 0:
            words(f, 'La longueur bat', 440, 88, 42.9, INK, t_out=ob)
            words(f, 'les symboles.', 550, 92, 43.4, SPARK, t_out=ob)
            q1 = gb * ease(seg(t, 44.0, 44.3))
            f.text('M7#qL!2x', W/2, 760, 64, INK, q1, MONO, True)
            f.text('8 signes variés', W/2, 830, 36, MUTED, q1, MONO, False)
            q2 = gb * ease(seg(t, 45.0, 45.3))
            f.text('chatbleuroux', W/2, 980, 64, SPARK, q2, MONO, True)
            f.text('12 minuscules', W/2, 1050, 36, MUTED, q2, MONO, False)
            q3 = ease(seg(t, 46.0, 46.3))
            c.save(); c.translate(W/2, 1240); sc = bump(t, 46.0, 0.15); c.scale(sc, sc)
            f.text('14 fois plus long à casser', 0, 0, 58, INK, gb * q3, DISPLAY, True); c.restore()

    # S7 — l'escalade (48–56.4) : 12 caractères variés
    if 48.0 <= t < 56.4:
        o = 55.9
        ga = ease(seg(t, 48.1, 48.4)) * (1 - seg(t, o, o + 0.3))
        if ga > 0:
            words(f, 'Et 12 signes variés ?', 440, 84, 48.1, INK, t_out=o)
            # compteur d'années
            yr = 104000 * ease_io(seg(t, 49.0, 52.0))
            f.text(fmt_int(yr), W/2, 760, 130, SPARK, ga, MONO, True)
            f.text('ans', W/2, 860, 60, INK, ga, DISPLAY, True)
            aa = ga * ease(seg(t, 52.4, 52.7))
            f.text('Avec 1 000 cartes ?', W/2, 1060, 56, INK, aa, DISPLAY, True)
            gpu(f, W/2, 1220, aa, t, 0.5)
            ab = ga * ease(seg(t, 53.4, 53.7))
            c.save(); c.translate(W/2, 1430); sc = bump(t, 53.4, 0.15); c.scale(sc, sc)
            f.text('encore 104 ans', 0, 0, 72, SPARK, ab, DISPLAY, True); c.restore()

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        a = ease(seg(t, 56.1, 56.4))
        s = rnd_chars(t, 12, 3, 8)
        field(f, 650, s, a, 0, 900, 58)
        words(f, 'Un symbole de plus aide.', 920, 72, 56.3, INK)
        words(f, 'Un caractère de plus protège.', 1030, 68, 57.6, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(240, 1160, 600, 150, OCEAN, a, 28)
        pa = 0.5 + 0.5 * math.sin((t - 60) * 3)
        f.rect(240, 1160, 600, 150, SPARK, a * 0.25 * pa, 28)
        f.text('Abonne-toi.', W/2, 1255, 62, INK, a)


def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    ev += [(0.15, rise(1.2, 300, 900, 0.07))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (12.5, 29.6, 47.9, 55.9)]
    ev += [(11.0, pop(520))]
    ev += [(18.6, ding(784, amp=0.18))]
    ev += [(30.3, ding(1046, amp=0.28)), (36.1, pop(300, 0.15))]
    ev += [(53.4, ding(784, amp=0.18))]
    ev += [(56.3, pop(440)), (60.0, ding(784, amp=0.22))]
    return ev
