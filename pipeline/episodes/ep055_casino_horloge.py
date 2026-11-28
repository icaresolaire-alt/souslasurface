"""Pas d'horloge au casino : le vrai piège est ailleurs (la musique lente). Même structure que le pilote.

Sources :
- Casino.org, C. Levitan, 27 juill. 2026, « Vegas Myths Busted: Casinos Banned Sunlight and Clocks to Trick
  Gamblers » : casinos du Strip des années 1950 aux années 1980 « designed as dark environments with no windows
  or clocks » ; le mythe porte sur la raison ; Bill Friedman (Designing Casinos to Dominate the Competition,
  2000) parle de mythe ; modèle « playground » (Mirage, Bellagio, Wynn) avec lumière naturelle ;
  les horloges : tout le monde en a une en poche.
- Wikipedia « Bill Friedman » : salles en labyrinthe, plafonds bas, sans fenêtre ni horloge, norme du Nevada
  jusqu'au Bellagio (ouvert en 1998), où Roger Thomas adopte la philosophie inverse.
  Mental Floss, N. Keppler, 28 nov. 2024 : le livre de Friedman ne recommande pas explicitement de masquer
  les fenêtres pour dérégler l'horloge interne ; lumière naturelle chez Roger Thomas à partir de la fin des
  années 1990.
- Milliman, « Using Background Music to Affect the Behavior of Supermarket Shoppers », Journal of Marketing 46,
  1982, p. 86-91 : rapporté par Knoferle, Spangenberg, Herrmann et Landwehr, Marketing Letters 23, 2012
  (« slower music [...] decrease pace of in-store traffic flow in a supermarket, thereby leading to greater
  sales » ; « average gross sales increase of 38.2% » ; leur propre essai : 12 %) et par Skeptoid n° 370
  (B. Dunning, 2013 : un supermarché, neuf semaines, 38,2 % ; les clients se souvenaient rarement de la
  musique ; estimations habituelles 10-20 %).
- Wikipedia « Southdale Center » : ouvert le 8 oct. 1956 à Edina (Minnesota), premier centre commercial
  entièrement couvert et climatisé des États-Unis, architecte Victor Gruen. Wikipedia « Gruen transfer » :
  plan volontairement déroutant, le client oublie ce qu'il venait chercher ; Gruen désapprouvait ces
  techniques ; discours de Londres 1978 (« bastard developments »).
"""
import math
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro (ep054 précédent).
COVER = dict(tag='Argent', l1='Pas d’horloge au casino :', l2='le vrai piège est ailleurs')

FELT = '#1f6b4f'
SUN = '#ffd98a'


def clock(f, cx, cy, r, a, t, speed=1.0, crossed=0.0):
    if a <= 0: return
    f.circle(cx, cy, r, OCEAN, a)
    f.circle(cx, cy, r, INK, a, stroke=8)
    for k in range(12):
        an = k * math.pi / 6
        f.line([(cx + 0.8 * r * math.sin(an), cy - 0.8 * r * math.cos(an)),
                (cx + 0.9 * r * math.sin(an), cy - 0.9 * r * math.cos(an))], MUTED, a, 5)
    am = t * speed * 2.0; ah = am / 12 + 1.0
    f.line([(cx, cy), (cx + 0.75 * r * math.sin(am), cy - 0.75 * r * math.cos(am))], INK, a, 7)
    f.line([(cx, cy), (cx + 0.5 * r * math.sin(ah), cy - 0.5 * r * math.cos(ah))], SPARK, a, 10)
    f.circle(cx, cy, 10, SPARK, a)
    if crossed > 0:
        d = r * 1.05 * crossed
        f.line([(cx - r * 1.05, cy - r * 1.05), (cx - r * 1.05 + 2 * d, cy - r * 1.05 + 2 * d)], RED, a, 16)


def window(f, cx, cy, w, h, a, open_=0.0, crossed=0.0):
    if a <= 0: return
    f.rect(cx - w / 2 - 10, cy - h / 2 - 10, w + 20, h + 20, INK, a, 10)
    f.rect(cx - w / 2, cy - h / 2, w, h, DEEP, a, 6)
    if open_ > 0:
        f.rect(cx - w / 2, cy - h / 2, w, h, SUN, a * open_ * 0.85, 6)
        f.circle(cx + w * 0.18, cy - h * 0.15, w * 0.16, '#fff3d0', a * open_)
    f.rect(cx - 5, cy - h / 2, 10, h, INK, a)
    f.rect(cx - w / 2, cy - 5, w, 10, INK, a)
    if crossed > 0:
        s = max(w, h) / 2 + 20
        f.line([(cx - s, cy - s), (cx - s + 2 * s * crossed, cy - s + 2 * s * crossed)], RED, a, 16)


def phone(f, cx, cy, a, t):
    if a <= 0: return
    f.rect(cx - 110, cy - 200, 220, 400, INK, a, 34)
    f.rect(cx - 96, cy - 180, 192, 360, OCEAN, a, 24)
    f.text('18:42', cx, cy + 10, 60, SPARK, a, MONO, True)


def shopper(f, x, y, a, phase, col=INK):
    if a <= 0: return
    f.circle(x, y - 70, 22, col, a)
    f.line([(x, y - 48), (x, y + 10)], col, a, 12)
    sw = 22 * math.sin(phase)
    f.line([(x, y + 10), (x + sw, y + 62)], col, a, 12)
    f.line([(x, y + 10), (x - sw, y + 62)], col, a, 12)
    f.line([(x, y - 30), (x - sw * 0.8, y + 5)], col, a, 10)
    f.line([(x, y - 30), (x + sw * 0.8, y + 5)], col, a, 10)


def shelf(f, x, y, w, a, col=CAPITAL):
    if a <= 0: return
    f.rect(x, y, w, 16, LINE, a, 4)
    for i in range(int(w // 60)):
        f.rect(x + 12 + i * 60, y - 70, 40, 70, (SPARK, EARTH, RED, MUTED)[i % 4], a * 0.85, 6)


def notes(f, x, y, a, t, slow):
    if a <= 0: return
    for k in range(3):
        ph = (t * (0.5 if slow else 1.4) + k / 3) % 1
        nx, ny = x + 60 * k, y - 120 * ph
        f.circle(nx, ny, 14, SPARK, a * (1 - ph))
        f.line([(nx + 12, ny), (nx + 12, ny - 46)], SPARK, a * (1 - ph), 5)


def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')

    # question persistante
    ha = ease(seg(t, 12.8, 13.3)) * (1 - seg(t, 29.8, 30.2))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Le piège, c’est l’horloge ?', W/2, 296, 46, SPARK, ha)

    # S1 — accroche (0–4) : l'horloge tourne puis se fait barrer
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        words(f, 'Au casino :', 440, 84, 0.05, INK, t_out=o)
        words(f, 'pas d’horloge,', 560, 84, 0.45, SPARK, t_out=o)
        words(f, 'pas de fenêtre.', 670, 84, 1.0, SPARK, t_out=o)
        p = ease(seg(t, 0.0, 0.5))
        clock(f, 330, 1030, 170 * (0.6 + 0.4 * p), fo * p, t + 1, speed=3.0, crossed=ease(seg(t, 1.6, 2.1)))
        window(f, 760, 1030, 260, 320, fo * ease(seg(t, 0.4, 0.9)), crossed=ease(seg(t, 2.2, 2.7)))

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.2:
        o1 = 7.6
        g1 = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'On dit que c’est', 440, 80, 4.2, INK, t_out=o1)
            words(f, 'pour te faire', 550, 80, 4.7, INK, t_out=o1)
            words(f, 'oublier l’heure.', 660, 84, 5.2, SPARK, t_out=o1)
            clock(f, W/2, 1060, 200, g1, t, speed=6.0)
        o2 = 10.9
        g2 = ease(seg(t, 7.8, 8.2)) * (1 - seg(t, o2, o2 + 0.3))
        if g2 > 0:
            words(f, 'Et que tu restes', 440, 80, 7.9, INK, t_out=o2)
            words(f, 'à jouer, à acheter…', 550, 76, 8.5, SPARK, t_out=o2)
            # jetons qui s'empilent
            for i in range(8):
                p = ease(seg(t, 8.6 + 0.2 * i, 8.9 + 0.2 * i))
                y = lerp(700, 1300 - 36 * i, p)
                f.rect(W/2 - 110, y, 220, 30, (SPARK, RED)[i % 2], g2 * p, 15)

    # S3 — la question (11–13.8)
    if 11.0 <= t < 13.8:
        words(f, 'Vrai piège', 820, 120, 11.1, INK, t_out=12.7)
        words(f, 'ou mythe ?', 950, 120, 11.5, SPARK, t_out=12.7)

    # S4 — la preuve (13.6–30)
    if 13.5 <= t < 30.0:
        # A : Las Vegas 1950–1980 (13.7–21.6)
        oa = 21.6
        ga = ease(seg(t, 13.6, 14.0)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Las Vegas, 1950 à 1980 :', 430, 66, 13.7, INK, t_out=oa)
            words(f, 'salles sombres, sans fenêtre.', 530, 62, 14.4, SPARK, t_out=oa)
            # labyrinthe de machines qui se remplit
            for r in range(4):
                for c in range(5):
                    k = r * 5 + c
                    p = ease(seg(t, 15.0 + 0.12 * k, 15.3 + 0.12 * k))
                    x = 160 + c * 170 + (60 if r % 2 else 0)
                    y = 720 + r * 150
                    if x > 960: continue
                    f.rect(x - 55, y, 110, 120, LINE, ga * p, 14)
                    f.rect(x - 40, y + 16, 80, 46, SPARK if (int(t * 3) + k) % 4 == 0 else CAPITAL, ga * p, 8)
            f.text('C’était vrai.', W/2, 1380, 64, INK, ga * ease(seg(t, 18.2, 18.5)), DISPLAY, True)
            f.text('un labyrinthe pour te garder', W/2, 1460, 40, MUTED, ga * ease(seg(t, 19.0, 19.3)), DISPLAY, True)
        # B : Bellagio 1998, lumière + téléphone (21.8–29.6)
        ob = 29.4
        gb = ease(seg(t, 21.7, 22.1)) * (1 - seg(t, ob, ob + 0.3))
        if gb > 0:
            words(f, 'Puis le Bellagio, 1998 :', 430, 66, 21.8, INK, t_out=ob)
            words(f, 'la lumière du jour entre.', 530, 66, 22.5, SPARK, t_out=ob)
            window(f, 320, 900, 300, 360, gb, open_=ease_io(seg(t, 23.0, 24.4)))
            pp = ease(seg(t, 25.0, 25.5))
            phone(f, 770, lerp(1000, 900, pp), gb * pp, t)
            f.text('Et l’heure ?', W/2, 1240, 56, INK, gb * ease(seg(t, 25.4, 25.7)), DISPLAY, True)
            f.text('Tu l’as dans ta poche.', W/2, 1330, 56, SPARK, gb * ease(seg(t, 26.2, 26.5)), DISPLAY, True)

    # S5 — la réponse (30–36)
    if 29.9 <= t < 36.0:
        o = 35.6
        a = ease(seg(t, 30.3, 30.6)) * (1 - seg(t, o, o + 0.3))
        words(f, 'Le vrai réglage ?', 470, 70, 30.0, INK, t_out=o)
        words(f, 'La musique lente.', 570, 76, 30.4, SPARK, t_out=o)
        big_center(f, '+38 %', 850, 220, SPARK, a, bump(t, 30.8, 0.18), font=DISPLAY)
        f.rect(150, 990, 780, 230, OCEAN, a * ease(seg(t, 32.2, 32.5)) * 0.9, 28)
        words(f, 'de ventes dans un', 1080, 56, 32.4, INK, t_out=o)
        words(f, 'supermarché testé.', 1160, 56, 32.9, SPARK, t_out=o)
        f.text('Milliman, 1982 · musique lente contre rapide', W/2, 1320, 30, MUTED,
               a * ease(seg(t, 33.6, 33.9)), MONO, False)

    # S6 — le retournement (36–48.4)
    if 36.0 <= t < 48.4:
        words(f, 'Pourquoi ?', 900, 130, 36.1, SPARK, t_out=37.9)
        oa = 43.2
        ga = ease(seg(t, 38.1, 38.5)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Musique lente,', 430, 80, 38.2, INK, t_out=oa)
            words(f, 'tu marches plus lentement.', 530, 64, 38.8, SPARK, t_out=oa)
            # deux allées : rapide en haut, lente en bas
            for row, (y, sp, lab, col) in enumerate(((820, 420, 'rapide', MUTED), (1180, 150, 'lente', SPARK))):
                shelf(f, 120, y - 120, 700, ga)
                x = 160 + ((t - 38.0) * sp) % 640
                shopper(f, x, y, ga, (t - 38.0) * (14 if row == 0 else 5), col)
                notes(f, 850, y - 40, ga, t, slow=(row == 1))
                f.text(lab, 160, y + 110, 36, col, ga, MONO, True, align='left')
            f.text('plus de rayons vus, plus d’achats', W/2, 1420, 42, INK, ga * ease(seg(t, 41.0, 41.3)), DISPLAY, True)
        ob = 47.9
        gb = ease(seg(t, 43.4, 43.8)) * (1 - seg(t, ob, ob + 0.3))
        if gb > 0:
            words(f, 'Le plus fort ?', 430, 84, 43.5, INK, t_out=ob)
            words(f, 'Les clients se souvenaient', 560, 64, 44.2, INK, t_out=ob)
            words(f, 'rarement de la musique.', 650, 64, 44.8, SPARK, t_out=ob)
            p = ease(seg(t, 45.2, 45.6))
            notes(f, W/2 + 220, 1080, gb * p, t, slow=True)
            f.circle(W/2, 1000, 170, MUTED, gb * p * 0.5, stroke=8)
            f.text('?', W/2, 1060, 170, MUTED, gb * p * 0.6, DISPLAY, True)
            f.text('un seul magasin · autres études : environ 10 à 20 %', W/2, 1330, 28, MUTED,
                   gb * ease(seg(t, 46.0, 46.3)), MONO, False)

    # S7 — l'escalade (48–56.4) : le centre commercial
    if 48.0 <= t < 56.4:
        o1 = 55.9
        g1 = ease(seg(t, 48.1, 48.4)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'États-Unis, 1956 :', 430, 70, 48.1, INK, t_out=o1)
            words(f, 'premier mall climatisé.', 520, 70, 48.6, SPARK, t_out=o1)
            # plan qui se dessine, avec un parcours qui serpente
            f.rect(160, 640, 760, 560, LINE, g1 * 0.6, 24)
            for i in range(6):
                p = ease(seg(t, 49.0 + 0.15 * i, 49.4 + 0.15 * i))
                x = 210 + (i % 3) * 240; y = 690 + (i // 3) * 270
                f.rect(x, y, 180, 190, CAPITAL, g1 * p, 14)
            pts = [(190, 1170), (190, 920), (420, 920), (420, 670), (660, 670), (660, 920), (890, 920), (890, 1170)]
            n = 2 + int(6 * ease_io(seg(t, 50.0, 52.4)))
            f.line(pts[:n], SPARK, g1, 8, dash=[18, 14])
            f.text('Plan fait pour qu’on s’y perde :', W/2, 1300, 46, INK, g1 * ease(seg(t, 52.0, 52.3)), DISPLAY, True)
            f.text('l’« effet Gruen ».', W/2, 1380, 54, SPARK, g1 * ease(seg(t, 52.6, 52.9)), DISPLAY, True)
            f.text('Victor Gruen, l’architecte, détestait l’idée.', W/2, 1470, 32, MUTED,
                   g1 * ease(seg(t, 53.4, 53.7)), MONO, False)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        a = ease(seg(t, 56.1, 56.4))
        clock(f, 330, 820, 130, a, t, speed=1.0)
        notes(f, 700, 860, a, t, slow=True)
        words(f, 'On ne te cache pas l’heure.', 1060, 58, 56.3, INK)
        words(f, 'On règle ton rythme.', 1150, 66, 57.8, SPARK)
        a2 = ease(seg(t, 60.0, 60.4))
        f.rect(240, 1320, 600, 150, OCEAN, a2, 28)
        pa = 0.5 + 0.5 * math.sin((t - 60) * 3)
        f.rect(240, 1320, 600, 150, SPARK, a2 * 0.25 * pa, 28)
        f.text('Abonne-toi.', W/2, 1415, 62, INK, a2)


def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    ev += [(0.15, rise(1.2, 300, 900, 0.07))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (12.7, 29.6, 47.9, 55.9)]
    ev += [(11.1, pop(520))]
    ev += [(30.8, ding(1046, amp=0.28)), (36.1, pop(300, 0.15))]
    ev += [(44.2, clink())]
    ev += [(56.3, pop(440)), (60.0, ding(784, amp=0.22))]
    return ev
