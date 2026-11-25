"""L'effet de leurre : l'offre que personne n'achète te fait payer plus. Même structure que le pilote.

Sources :
- Wikipedia « Decoy effect » : exemple de Dan Ariely (Predictably Irrational, ch. 1), « a true case used by
  The Economist » : web 59 $, papier 125 $, papier + web 125 $ ; avec les trois offres 16 % web, 0 % papier,
  84 % papier + web ; sans l'offre papier seul 68 % web, 32 % papier + web. Article fondateur : Huber, Payne,
  Puto, « Adding Asymmetrically Dominated Alternatives », Journal of Consumer Research 9(1), 1982, p. 90-98.
  Réserves : Yang et Lynn 2014, Frederick, Lee et Baskin 2014 (« The Limits of Attraction », JMR) ; Huber,
  Payne et Puto 2014 (« Let's Be Honest About the Attraction Effect ») : l'effet dépend des conditions.
- The Conversation, « The decoy effect: how you are influenced to choose without really knowing it » :
  Ariely « tested the options on 100 of his students » ; 68 % puis 16 % pour l'offre web, 84 % pour le combo ;
  Huber, Payne et Puto, conférence 1981, publication 1982.
- Cartes de restaurant : Mental Floss (J. Hullinger, 2016, « They use expensive decoys » : un plat très cher
  en haut de la carte « makes everything else seem reasonably priced ») et Lafayette Magazine 2018
  (« The Power of Nudge » : le plateau à 109 $ « could be a so-called decoy » à côté de celui à 55 $).
  Carte affichée à l'écran : illustrative.
"""
import math
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro (ep051 précédent).
COVER = dict(tag='Psychologie', l1='L’offre que personne n’achète', l2='te fait payer plus cher')

PAPER = '#d9cfb8'


def card(f, cx, cy, title, price, a, hl=False, dim=False, w=290, h=300):
    if a <= 0: return
    col = SPARK if hl else (LINE if dim else OCEAN)
    f.rect(cx - w / 2, cy - h / 2, w, h, col, a * (0.95 if not dim else 0.8), 26)
    if not hl:
        f.rect(cx - w / 2 + 4, cy - h / 2 + 4, w - 8, h - 8, OCEAN if not dim else DEEP, a, 23)
    tc = OCEAN if hl else (MUTED if dim else INK)
    lines = title.split('\n')
    for i, s in enumerate(lines):
        f.text(s, cx, cy - 52 + i * 48 - 24 * (len(lines) - 1), 42, tc, a, DISPLAY, True)
    f.text(price, cx, cy + 90, 72, OCEAN if hl else SPARK, a, DISPLAY, True)


def bar(f, x, base, pct, a, col, lab, hmax=380, w=170):
    if a <= 0: return
    hgt = hmax * pct / 100
    f.rect(x - w / 2, base - hgt, w, max(hgt, 4), col, a * 0.92, 14)
    f.text(f'{int(round(pct))} %', x, base - hgt - 24, 60, INK, a, DISPLAY, True)
    f.text(lab, x, base + 56, 38, MUTED, a, DISPLAY, True)


def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')

    # question persistante
    ha = ease(seg(t, 12.8, 13.3)) * (1 - seg(t, 29.8, 30.2))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('L’offre inutile compte-t-elle ?', W/2, 296, 44, SPARK, ha)

    # S1 — accroche (0–4) : trois offres tombent dès la première image
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        words(f, 'L’offre que personne', 440, 80, 0.05, INK, t_out=o)
        words(f, 'n’achète te fait', 550, 80, 0.55, INK, t_out=o)
        words(f, 'payer plus cher.', 660, 80, 1.0, SPARK, t_out=o)
        for i, (ttl, pr) in enumerate((('Offre 1', '59'), ('Offre 2', '125'), ('Offre 3', '125'))):
            p = ease(seg(t, 0.1 + 0.35 * i, 0.8 + 0.35 * i))
            card(f, 210 + 330 * i, lerp(820, 1060, p), ttl, pr, fo * p, hl=(i == 2 and t > 2.4), w=280, h=260)

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.2:
        o1 = 7.6
        g1 = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'Tu crois choisir', 440, 80, 4.2, INK, t_out=o1)
            words(f, 'selon ce que tu veux.', 550, 76, 4.8, SPARK, t_out=o1)
            # étiquette de prix qui se balance
            ang = 0.25 * math.sin((t - 4) * 2.2)
            cx, cy = W/2, 960
            f.line([(cx, 720), (cx + 260 * math.sin(ang), 720 + 260 * math.cos(ang))], MUTED, g1, 4)
            tx, ty = cx + 260 * math.sin(ang), 720 + 260 * math.cos(ang)
            f.rect(tx - 160, ty, 320, 200, SPARK, g1 * 0.92, 24)
            f.text('le prix', tx, ty + 125, 64, OCEAN, g1, DISPLAY, True)
        o2 = 10.9
        g2 = ease(seg(t, 7.8, 8.2)) * (1 - seg(t, o2, o2 + 0.3))
        if g2 > 0:
            words(f, 'Une offre en plus,', 440, 80, 7.9, INK, t_out=o2)
            words(f, 'que personne ne veut ?', 550, 72, 8.5, MUTED, t_out=o2)
            card(f, 360, 1000, 'Offre A', '?', g2)
            card(f, 720, 1000, 'Offre B', '?', g2)
            p = ease(seg(t, 9.0, 9.5))
            f.text('Ça ne devrait rien changer.', W/2, 1330, 52, INK, g2 * p, DISPLAY, True)

    # S3 — la question (11–13.8)
    if 11.0 <= t < 13.8:
        words(f, 'Vraiment', 820, 120, 11.1, INK, t_out=12.7)
        words(f, 'rien ?', 950, 130, 11.5, SPARK, t_out=12.7)

    # S4 — la preuve (13.6–30)
    if 13.5 <= t < 30.0:
        # A : deux offres (13.7–21.6)
        oa = 21.6
        ga = ease(seg(t, 13.6, 14.0)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Dan Ariely, 100 étudiants.', 430, 64, 13.7, INK, t_out=oa)
            words(f, 'Deux abonnements :', 530, 70, 14.4, SPARK, t_out=oa)
            ca = ga * ease(seg(t, 15.0, 15.4))
            card(f, 360, 760, 'Web', '59 $', ca, w=300, h=250)
            card(f, 720, 760, 'Papier\n+ web', '125 $', ca, w=300, h=250)
            p = ease_io(seg(t, 16.4, 18.6))
            bar(f, 360, 1360, 68 * p, ga * ease(seg(t, 16.2, 16.5)), INK, 'web')
            bar(f, 720, 1360, 32 * p, ga * ease(seg(t, 16.2, 16.5)), SPARK, 'papier + web')
            f.text('la plupart prennent le moins cher', W/2, 1510, 40, MUTED,
                   ga * ease(seg(t, 19.0, 19.3)), DISPLAY, True)
        # B : on ajoute le leurre (21.8–29.6)
        ob = 29.4
        gb = ease(seg(t, 21.7, 22.1)) * (1 - seg(t, ob, ob + 0.3))
        if gb > 0:
            words(f, 'Il ajoute une 3e offre :', 430, 66, 21.8, INK, t_out=ob)
            words(f, 'papier seul, 125 $.', 530, 72, 22.5, SPARK, t_out=ob)
            card(f, 210, 760, 'Web', '59 $', gb, w=270, h=240)
            pd = ease(seg(t, 23.2, 23.7))
            card(f, 540, lerp(640, 760, pd), 'Papier\nseul', '125 $', gb * pd, dim=True, w=270, h=240)
            card(f, 870, 760, 'Papier\n+ web', '125 $', gb, w=270, h=240)
            p = ease_io(seg(t, 24.4, 27.0))
            ba = gb * ease(seg(t, 22.0, 22.3))
            bar(f, 210, 1360, lerp(68, 16, p), ba, INK, 'web', w=150)
            bar(f, 540, 1360, 0, ba * pd, MUTED, 'papier seul', w=150)
            bar(f, 870, 1360, lerp(32, 84, p), ba, SPARK, 'papier + web', w=150)

    # S5 — la réponse (30–36)
    if 29.9 <= t < 36.0:
        o = 35.6
        a = ease(seg(t, 30.3, 30.6)) * (1 - seg(t, o, o + 0.3))
        words(f, 'Le combo à 125 $ passe', 520, 66, 30.0, MUTED, t_out=o)
        words(f, 'de 32 % à', 610, 66, 30.4, MUTED, t_out=o)
        big_center(f, '84 %', 860, 220, SPARK, a, bump(t, 30.8, 0.18), font=DISPLAY)
        f.rect(150, 1040, 780, 230, OCEAN, a * ease(seg(t, 32.2, 32.5)) * 0.9, 28)
        words(f, 'Et l’offre ajoutée ?', 1130, 56, 32.4, INK, t_out=o)
        words(f, 'Personne ne la prend.', 1210, 56, 32.9, SPARK, t_out=o)
        f.text('exemple d’Ariely, Predictably Irrational', W/2, 1360, 30, MUTED, a * ease(seg(t, 33.6, 33.9)), MONO, False)

    # S6 — le retournement (36–48.4)
    if 36.0 <= t < 48.4:
        words(f, 'Pourquoi ?', 900, 130, 36.1, SPARK, t_out=37.9)
        oa = 43.2
        ga = ease(seg(t, 38.1, 38.5)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Même prix,', 430, 80, 38.2, INK, t_out=oa)
            words(f, 'mais le web en moins.', 530, 72, 38.8, SPARK, t_out=oa)
            card(f, 300, 870, 'Papier\nseul', '125 $', ga, dim=True, w=300, h=260)
            card(f, 780, 870, 'Papier\n+ web', '125 $', ga, hl=t > 40.6, w=300, h=260)
            f.text('<', 540, 900, 110, SPARK, ga * ease(seg(t, 39.8, 40.1)) * bump(t, 39.8, 0.15), DISPLAY, True)
            f.text('Le combo a l’air d’une affaire.', W/2, 1180, 50, INK, ga * ease(seg(t, 40.8, 41.1)), DISPLAY, True)
            f.text('C’est l’effet de leurre.', W/2, 1270, 54, SPARK, ga * ease(seg(t, 41.6, 41.9)), DISPLAY, True)
            f.text('Huber, Payne, Puto, 1982', W/2, 1370, 32, MUTED, ga * ease(seg(t, 42.0, 42.3)), MONO, False)
        ob = 47.9
        gb = ease(seg(t, 43.4, 43.8)) * (1 - seg(t, ob, ob + 0.3))
        if gb > 0:
            words(f, 'Ton cerveau ne sait pas', 430, 70, 43.5, INK, t_out=ob)
            words(f, 'juger un prix seul.', 530, 70, 44.1, INK, t_out=ob)
            words(f, 'Alors il compare.', 680, 84, 45.0, SPARK, t_out=ob)
            # balance qui penche
            tilt = 0.22 * ease_io(seg(t, 45.4, 46.6))
            cx, cy = W/2, 1080
            dx, dy = 300 * math.cos(tilt), 300 * math.sin(tilt)
            f.line([(cx, cy), (cx, 1330)], MUTED, gb, 8)
            f.line([(cx - dx, cy - dy), (cx + dx, cy + dy)], INK, gb, 8)
            f.rect(cx - dx - 90, cy - dy + 20, 180, 110, LINE, gb, 18)
            f.rect(cx + dx - 90, cy + dy + 20, 180, 110, SPARK, gb, 18)
            f.text('leurre', cx - dx, cy - dy + 92, 38, INK, gb, DISPLAY, True)
            f.text('cible', cx + dx, cy + dy + 92, 38, OCEAN, gb, DISPLAY, True)
            f.rect(cx - 140, 1330, 280, 24, MUTED, gb, 12)

    # S7 — l'escalade (48–56.4) : la carte du restaurant
    if 48.0 <= t < 56.4:
        o1 = 55.9
        g1 = ease(seg(t, 48.1, 48.4)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'Au restaurant aussi.', 430, 76, 48.1, INK, t_out=o1)
            words(f, 'Le plat très cher', 530, 72, 48.7, SPARK, t_out=o1)
            words(f, 'sert surtout de repère.', 620, 64, 49.3, SPARK, t_out=o1)
            # carte illustrative
            f.rect(220, 720, 640, 600, PAPER, g1 * 0.95, 24)
            f.text('CARTE', W/2, 800, 40, OCEAN, g1, MONO, True)
            items = (('Plateau royal', '109'), ('Plateau du jour', '55'), ('Assiette', '18'))
            for i, (nm, pr) in enumerate(items):
                p = ease(seg(t, 50.0 + 0.4 * i, 50.4 + 0.4 * i))
                y = 920 + 130 * i
                hl = i == 1 and t > 52.0
                if hl:
                    f.rect(250, y - 62, 580, 92, SPARK, g1 * p * (0.7 + 0.3 * bump(t, 52.0, 0.3)), 18)
                f.text(nm, 290, y, 44, OCEAN, g1 * p, DISPLAY, True, align='left')
                f.text(pr + ' €', 790, y, 46, OCEAN, g1 * p, DISPLAY, True, align='right')
            f.text('le 55 € paraît raisonnable', W/2, 1420, 44, INK, g1 * ease(seg(t, 52.4, 52.7)), DISPLAY, True)
            f.text('carte illustrative · effet variable selon les études', W/2, 1500, 28, MUTED,
                   g1 * ease(seg(t, 53.2, 53.5)), MONO, False)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        a = ease(seg(t, 56.1, 56.4))
        for i in range(3):
            p = ease(seg(t, 56.2 + 0.2 * i, 56.7 + 0.2 * i))
            card(f, 230 + 310 * i, 760, ('Offre 1', 'Leurre', 'Offre 2')[i], ('59', '125', '125')[i],
                 a * p, dim=(i == 1), hl=(i == 2 and t > 58.0), w=260, h=240)
        words(f, 'Tu ne choisis pas un prix.', 1060, 60, 56.3, INK)
        words(f, 'Tu choisis une comparaison.', 1150, 60, 57.8, SPARK)
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
    ev += [(39.8, clink())]
    ev += [(56.3, pop(440)), (60.0, ding(784, amp=0.22))]
    return ev
