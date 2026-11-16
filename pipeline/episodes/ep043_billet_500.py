"""Pourquoi on n'imprime plus le billet de 500 €. Même structure que le pilote.

Sources :
- BCE, communiqué du 4 mai 2016 « ECB ends production and issuance of €500 banknote » (repris en entier par
  cashessentials.org, 5 mai 2016) : arrêt définitif de la production, « taking into account concerns that this
  banknote could facilitate illicit activities » ; le billet « will remain legal tender », « will always retain
  its value » et peut être échangé auprès des banques centrales nationales « for an unlimited period of time ».
- La finance pour tous (IEFP), 10 janv. 2019 : fin de l'émission le 27 janvier 2019 (Allemagne et Autriche
  jusqu'au 26 avril 2019), cours légal « pendant une période illimitée », billets « soupçonnés de faciliter des
  activités illégales ». Concordant : Wikipedia « 500 euro note » (27 janv. 2019 pour 17 banques centrales sur 19,
  26 avril 2019 pour les deux autres).
- Poids : P. Sands, World Economic Forum, 24 févr. 2016 (« In €500 notes, the equivalent value is 2.2kg ») ;
  Slate.fr « Très prisés du crime organisé, les gros billets sont de plus en plus décriés » (2016 : « un million
  d'euros en coupures de 500 pèse 2,2 kg ») ; La Libre Belgique, 8 févr. 2020 (2,2 kilos, d'après Febelfin).
  Nombres de billets calculés : 1 000 000 / 500 = 2 000 ; 1 000 000 / 20 = 50 000.
- Royaume-Uni 2010 : CNBC, 13 mai 2010 « UK Stops Supplying 500 Notes to Fight Crime » (« More than 90 percent
  of the demand for these notes in the UK came from criminals, according to the agency », SOCA) ; concordant :
  Police Professional « Ninety per cent of 500 euro notes are linked to crime », Business Standard 20 mai 2010.
- En circulation : Banque de France, « Chiffres clés sur les billets et les pièces 2025 » (publié août 2026 :
  émissions nettes de billets de 500 en zone euro 105,2 Md€ fin 2025, contre 119,0 Md€ fin 2024) ; Wikipedia
  « 500 euro note », tableau d'après la BCE (210 367 338 billets en déc. 2025 ; pic de 613 559 542 en déc. 2015).
  Concordant pour le pic : WEF 2016 (« €300bn of €500 notes have been issued », soit environ 600 millions).
- Billets, piles et mallette dessinés de façon illustrative.
"""
import math
import random
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro (ep042 précédent).
COVER = dict(tag='Argent', l1='Pourquoi on n’imprime plus', l2='le billet de 500 €')

PURPLE = '#8d6bb8'
PURPLE_D = '#5e4685'
BLUE20 = '#4f86c6'
BLUE20_D = '#33608f'
CASE = '#6b4a33'


def note(f, x, y, s, a, val='500', col=PURPLE, dark=PURPLE_D, rot=0.0):
    """Billet stylisé centré en (x, y), largeur 320*s (proportions 160 x 82 mm)."""
    if a <= 0: return
    c = f.c; c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    w, h = 320, 164
    f.rect(-w/2, -h/2, w, h, col, a, 10)
    f.rect(-w/2 + 12, -h/2 + 12, w - 24, h - 24, dark, a * 0.55, 6)
    f.circle(-w/2 + 80, 0, 46, col, a * 0.9)
    f.text(val, w/2 - 24, h/2 - 26, 64, INK, a, MONO, True, align='right')
    f.text('€', -w/2 + 80, 18, 54, INK, a * 0.9)
    c.restore()


def pile(f, x, ybot, n, a, col, dark, w=150, step=2.0, label=None):
    """Pile de billets vue de profil, n tranches."""
    if a <= 0 or n <= 0: return
    for i in range(int(n)):
        yy = ybot - i * step
        f.rect(x - w/2, yy - step, w, step, col if i % 2 else dark, a)
    f.rect(x - w/2, ybot - n * step - 4, w, 6, INK, a * 0.6, 2)


def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')
    c = f.c

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.8, 30.2))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Pourquoi l’arrêter ?', W/2, 296, 46, SPARK, ha)

    # S1 — accroche (0–4) : le billet arrive, un tampon « FIN » tombe
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        words(f, 'Le billet de 500 €', 460, 86, 0.05, INK, t_out=o)
        words(f, 'n’est plus imprimé.', 570, 86, 0.7, SPARK, t_out=o)
        sx = lerp(-300, W/2, ease(seg(t, 0.0, 1.0)))
        note(f, sx, 1000, 2.3, fo, rot=-0.05 * (1 - ease(seg(t, 0, 1.0))))
        sa = fo * ease(seg(t, 2.0, 2.2))
        if sa > 0:
            c.save(); c.translate(W/2, 1000); c.rotate(-0.18)
            s = bump(t, 2.0, 0.3); c.scale(s, s)
            c.set_line_width(10); f.color(RED, sa)
            c.rectangle(-210, -80, 420, 160); c.stroke()
            f.text('FIN', 0, 40, 120, RED, sa); c.restore()

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.0:
        o1 = 7.4
        g1 = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'Pourtant,', 450, 90, 4.2, INK, t_out=o1)
            words(f, 'il vaut toujours 500 €.', 560, 80, 4.7, SPARK, t_out=o1)
            note(f, W/2, 1000 + 8 * math.sin(t * 2), 2.2, g1)
            f.text('toujours valable', W/2, 1300, 44, MUTED, g1 * ease(seg(t, 5.6, 5.9)), MONO, False)
        o2 = 10.7
        g2 = ease(seg(t, 7.6, 8.0)) * (1 - seg(t, o2, o2 + 0.3))
        if g2 > 0:
            words(f, 'Ton intuition :', 480, 72, 7.7, MUTED, t_out=o2)
            words(f, 'trop de faux billets.', 600, 80, 8.1, INK, t_out=o2)
            for k in range(3):
                ang = -0.25 + 0.25 * k + 0.04 * math.sin(t * 2 + k)
                note(f, 300 + 240 * k, 1000 + 30 * (k % 2), 1.3, g2 * ease(seg(t, 8.4 + 0.3 * k, 8.7 + 0.3 * k)), rot=ang)
            f.text('?', W/2, 1300, 120, SPARK, g2 * ease(seg(t, 9.4, 9.7)))

    # S3 — la question (10.9–13.6)
    if 10.9 <= t < 13.6:
        words(f, 'Alors pourquoi', 820, 96, 11.0, INK, t_out=12.5)
        words(f, 'l’avoir arrêté ?', 950, 96, 11.4, SPARK, t_out=12.5)

    # S4 — la preuve (13.5–30)
    if 13.4 <= t < 30.0:
        # A : un million d'euros, deux piles (13.6–21.6)
        oa = 21.4
        ga = ease(seg(t, 13.5, 13.9)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Un million d’euros.', 430, 90, 13.6, INK, t_out=oa)
            p20 = ease_io(seg(t, 14.8, 18.0))
            p500 = ease_io(seg(t, 15.4, 17.0))
            ybot = 1330
            # billets de 20 : pile 25 fois plus haute (50 000 contre 2 000)
            pile(f, 320, ybot, 250 * p20, ga, BLUE20, BLUE20_D, w=200, step=2.4)
            pile(f, 760, ybot, 10 * p500, ga, PURPLE, PURPLE_D, w=200, step=2.4)
            f.text(fmt_int(50000 * p20), 320, 1420, 56, INK, ga, MONO)
            f.text('billets de 20 €', 320, 1480, 36, MUTED, ga, MONO, False)
            c.save(); c.translate(760, 1420); s = bump(t, 17.0, 0.15); c.scale(s, s)
            f.text(fmt_int(2000 * p500), 0, 0, 56, SPARK, ga, MONO); c.restore()
            f.text('billets de 500 €', 760, 1480, 36, MUTED, ga, MONO, False)
            words(f, '25 fois moins de billets.', 560, 58, 18.6, SPARK, t_out=oa)
        # B : tout tient dans un coin de mallette (21.6–29.6)
        gb = ease(seg(t, 21.5, 21.9)) * (1 - seg(t, 29.4, 29.8))
        if gb > 0:
            words(f, 'En billets de 500,', 440, 84, 21.6, INK, t_out=29.3)
            words(f, 'ça tient dans un coin.', 550, 76, 22.2, SPARK, t_out=29.3)
            # mallette ouverte
            f.rect(160, 760, 760, 480, CASE, gb, 26)
            f.rect(190, 790, 700, 420, DEEP, gb, 16)
            f.rect(470, 720, 140, 50, CASE, gb, 14)
            # liasses qui tombent dans un coin
            for k in range(4):
                p = ease(seg(t, 23.0 + 0.6 * k, 23.5 + 0.6 * k))
                yy = lerp(640, 1150 - 16 * k, p)
                note(f, 330, yy, 0.62, gb * seg(t, 23.0 + 0.6 * k, 23.1 + 0.6 * k), val='500' if k == 3 else '')
            words(f, 'Le reste : vide.', 1320, 54, 26.0, MUTED, t_out=29.3, bold=False)
            f.text('1 million = 2 000 billets', W/2, 1420, 40, INK, gb * ease(seg(t, 26.8, 27.1)), MONO, False)

    # S5 — la réponse (30–36) : 2,2 kg
    if 29.9 <= t < 36.0:
        o = 35.6
        a = ease(seg(t, 30.3, 30.6)) * (1 - seg(t, o, o + 0.3))
        words(f, 'Un million d’euros pèse', 560, 72, 30.0, INK, t_out=o)
        big_center(f, '2,2 kg', 840, 220, SPARK, a, bump(t, 30.3, 0.18))
        words(f, 'Ça tient dans un sac à main.', 1030, 64, 31.2, INK, t_out=o)
        # balance qui oscille
        sw = 0.08 * math.sin((t - 30) * 3) * (1 - seg(t, 31, 34))
        c.save(); c.translate(W/2, 1250); c.rotate(sw); c.scale(1.5, 1.5)
        f.line([(-260, 0), (260, 0)], MUTED, a, 8)
        f.rect(-330, 10, 140, 16, MUTED, a, 6); f.rect(190, 10, 140, 16, MUTED, a, 6)
        note(f, -260, -20, 0.4, a)
        f.rect(210, -80, 100, 90, MUTED, a * 0.8, 10)
        f.text('kg', 260, -22, 40, DEEP, a)
        c.restore()
        f.line([(W/2, 1250), (W/2, 1480)], MUTED, a, 10)

    # S6 — le retournement (36–48.4)
    if 36.0 <= t < 48.4:
        words(f, 'Le secret ?', 900, 150, 36.1, SPARK, t_out=37.9)
        # A : Royaume-Uni, 2010 (38.1–42.6)
        oa = 42.6
        ga = ease(seg(t, 38.1, 38.5)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Royaume-Uni, 2010.', 450, 76, 38.2, INK, t_out=oa)
            words(f, 'Qui achète ces billets ?', 550, 64, 38.7, MUTED, t_out=oa)
            # 10 silhouettes, 9 s'allument
            for k in range(10):
                x = 165 + (k % 5) * 187; y = 820 + (k // 5) * 260
                hot = k < 9 and t > 39.6 + 0.12 * k
                col = RED if hot else MUTED
                f.circle(x, y, 38, col, ga)
                f.rect(x - 52, y + 48, 104, 120, col, ga, 40)
            c.save(); c.translate(W/2, 1460); s = bump(t, 40.8, 0.15); c.scale(s, s)
            f.text('plus de 90 %', 0, 0, 90, SPARK, ga * ease(seg(t, 40.8, 41.0)), MONO); c.restore()
            f.text('de la demande : des criminels', W/2, 1540, 38, INK, ga * ease(seg(t, 41.0, 41.3)), MONO, False)
        # B : la BCE tranche (42.9–47.9)
        ob = 47.9
        gb = ease(seg(t, 42.8, 43.2)) * (1 - seg(t, ob, ob + 0.3))
        if gb > 0:
            words(f, 'Petit, léger, précieux :', 430, 76, 42.9, INK, t_out=ob)
            words(f, 'parfait pour cacher.', 530, 76, 43.4, SPARK, t_out=ob)
            yr = int(lerp(2010, 2016, ease(seg(t, 44.4, 45.2))))
            big_center(f, str(yr), 820, 150, SPARK, gb, bump(t, 45.2, 0.12))
            words(f, 'La BCE arrête l’impression.', 1010, 58, 45.3, INK, t_out=ob)
            words(f, 'Dernières émissions : 2019.', 1110, 52, 46.2, MUTED, t_out=ob)
            # le billet se couvre d'un voile
            na = gb * ease(seg(t, 43.4, 43.8))
            note(f, W/2, 1330, 1.0, na)
            f.rect(W/2 - 160, 1248, 320 * ease(seg(t, 45.3, 46.6)), 164, DEEP, na * 0.75, 10)

    # S7 — l'escalade (48–56.4) : ceux qui restent cachés quelque part
    if 48.0 <= t < 56.4:
        o = 55.9
        ga = ease(seg(t, 48.1, 48.4)) * (1 - seg(t, o, o + 0.3))
        if ga > 0:
            words(f, 'Mais ils n’ont pas disparu.', 430, 70, 48.1, INK, t_out=o)
            words(f, 'Billets de 500 en circulation :', 520, 50, 48.6, MUTED, t_out=o, bold=False)
            prog = ease_io(seg(t, 49.6, 52.6))
            val = lerp(614, 210, prog)
            yr = int(lerp(2015, 2025, prog))
            # barre qui descend
            f.rect(240, 700, 600, 70, LINE, ga, 35)
            f.rect(240, 700, 600 * val / 614, 70, PURPLE, ga, 35)
            f.text(str(yr), W/2, 860, 60, MUTED, ga, MONO)
            c.save(); c.translate(W/2, 1080); s = bump(t, 52.6, 0.15); c.scale(s, s)
            f.text(f'{int(val)} millions', 0, 0, 130, SPARK, ga, MONO, True); c.restore()
            words(f, 'Soit 105 milliards d’euros.', 1240, 58, 53.0, INK, t_out=o)
            f.text('fin 2025, Banque de France / BCE', W/2, 1330, 32, MUTED,
                   ga * ease(seg(t, 53.4, 53.7)), MONO, False)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        a = ease(seg(t, 56.1, 56.4))
        note(f, W/2, 680 + 6 * math.sin(t * 2), 1.4, a)
        words(f, 'Son problème : pas sa valeur.', 900, 62, 56.3, INK)
        words(f, 'Sa taille.', 1010, 84, 57.6, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(240, 1160, 600, 150, OCEAN, a, 28)
        pa = 0.5 + 0.5 * math.sin((t - 60) * 3)
        f.rect(240, 1160, 600, 150, SPARK, a * 0.25 * pa, 28)
        f.text('Abonne-toi.', W/2, 1255, 62, INK, a)


def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    ev += [(0.15, rise(1.2, 300, 900, 0.07)), (2.0, pop(260, 0.18))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (12.5, 29.6, 47.9, 55.9)]
    ev += [(11.0, pop(520))]
    ev += [(17.0, ding(784, amp=0.18))]
    ev += [(30.3, ding(1046, amp=0.28)), (36.1, pop(300, 0.15))]
    ev += [(40.8, ding(784, amp=0.18))]
    ev += [(52.6, ding(784, amp=0.18))]
    ev += [(56.3, pop(440)), (60.0, ding(784, amp=0.22))]
    return ev
