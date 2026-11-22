"""Pourquoi le lait est toujours au fond du supermarché. Même structure que le pilote.

Le verdict suit les sources : il n'y a pas une seule raison, mais deux (logistique ET ventes).

Sources :
- Hui, Inman, Huang et Suher, « The Effect of In-store Travel Distance on Unplanned Spending:
  Applications to Mobile Promotion Strategies », Journal of Marketing, mars 2013. Suivi des clients par
  puces RFID dans un supermarché américain. NYU Stern (13 mars 2013) : « On average, shoppers travel
  approximately 1,400 feet in a grocery store » (≈ 427 m, affiché « environ 430 m ») ; « Traveling an
  additional 55 feet in the store generates around $1 in additional unplanned spending » (55 pieds
  ≈ 16,8 m, affiché « environ 17 m »). Repris par Drexel LeBow (5 févr. 2013) et Progressive Grocer.
- Logistique : NPR Planet Money (2014, transcript 337034378) : Russ Roberts (Hoover Institution) :
  « The trucks deliver the milk to the back. There's a big refrigerated room there. » ; Rob Olsen
  (acheteur produits laitiers, BJ's) décrit la chaîne du froid (camion froid, chambre froide, rayon).
  Ventes : même émission, « building the basket » ; le consultant Burt Flickinger répond « All of
  the above » ; un porte-parole de Kroger cite les deux raisons. D'où « les deux sont vraies ».
- Escalade : Gilbride, Inman et Stilley, Journal of Marketing (communiqué Notre Dame, 12 juin 2015) :
  les achats imprévus sont plus probables en fin de parcours, et « an unplanned purchase increases the
  probability of another unplanned purchase ». Aucun pourcentage affiché (l'étude n'en donne pas dans
  le communiqué).
- Nuance non affichée : Bell, Corsten et Knox (Wharton, 2009) estiment la part d'achats imprévus plus
  près de 20 % que des 60 à 70 % souvent cités ; on évite donc tout chiffre de part du panier.
"""
import math
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro (ep048 précédent).
COVER = dict(tag='Argent', l1='Pourquoi le lait est', l2='toujours au fond du magasin')

MILK = '#f4f7f2'

# ---------- plan du magasin (vue de dessus) ----------
PX0, PX1 = 150, 930


def store_pts(y0, h):
    """Parcours en serpentin de l'entrée (en bas à gauche) jusqu'au lait (au fond)."""
    top = y0 + h * 0.20; bot = y0 + h * 0.90
    return [(225, y0 + h + 10), (225, top), (375, top), (375, bot), (525, bot),
            (525, top), (675, top), (675, bot), (825, bot), (825, top), (720, y0 + h * 0.13)]


def path_len(pts):
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))


def path_at(pts, u):
    """Points du parcours jusqu'à la fraction u, et position courante."""
    L = path_len(pts) * clamp(u); out = [pts[0]]
    for a, b in zip(pts, pts[1:]):
        d = math.hypot(b[0] - a[0], b[1] - a[1])
        if L >= d: out.append(b); L -= d
        else:
            r = L / d if d else 0
            out.append((lerp(a[0], b[0], r), lerp(a[1], b[1], r))); break
    return out, out[-1]


def store(f, y0, h, a, u=0.0, trail=True, glow=0.0):
    if a <= 0: return
    f.rect(PX0, y0, PX1 - PX0, h, OCEAN, a * 0.95, 22)
    # murs
    f.line([(PX0, y0 + h), (195, y0 + h)], LINE, a, 8)
    f.line([(255, y0 + h), (PX1, y0 + h)], LINE, a, 8)
    f.text('entrée', 225, y0 + h + 52, 30, MUTED, a, MONO, False)
    # rayons
    for x in (300, 450, 600, 750):
        f.rect(x - 28, y0 + h * 0.30, 56, h * 0.52, CAPITAL, a, 10)
    # rayon frais au fond
    f.rect(PX0 + 30, y0 + 16, PX1 - PX0 - 60, h * 0.07, EARTH, a * (0.7 + 0.3 * glow), 10)
    for i in range(9):
        x = PX0 + 70 + i * 80
        f.rect(x, y0 + 22, 30, h * 0.07 - 12, MILK, a, 4)
        f.rect(x + 8, y0 + 18, 14, 8, SPARK, a, 2)
    if u > 0:
        pts, cur = path_at(store_pts(y0, h), u)
        if trail: f.line(pts, SPARK, a * 0.85, 8, dash=[18, 14])
        f.circle(cur[0], cur[1], 22, SPARK, a)
        f.circle(cur[0], cur[1], 10, DEEP, a)


def truck(f, x, y, a, s=1.0):
    """Camion frigorifique vu de dessus, cabine à droite."""
    if a <= 0: return
    f.rect(x, y, 300 * s, 110 * s, INK, a, 12 * s)
    f.rect(x + 300 * s + 8, y + 10 * s, 80 * s, 90 * s, SPARK, a, 14 * s)
    f.text('FROID', x + 150 * s, y + 70 * s, 38 * s, DEEP, a, MONO, True)


def cart(f, x, y, a, fill=0.0, s=1.0):
    if a <= 0: return
    f.line([(x - 120 * s, y - 120 * s), (x - 90 * s, y - 120 * s), (x - 60 * s, y + 20 * s),
            (x + 110 * s, y + 20 * s), (x + 130 * s, y - 80 * s), (x - 78 * s, y - 80 * s)], INK, a, 8 * s)
    cols = [SPARK, EARTH, RED, MILK, SPARK, EARTH, RED, MILK]
    n = int(fill * 8 + 0.001)
    for i in range(n):
        cx = x - 50 * s + (i % 4) * 42 * s; cy = y - 20 * s - (i // 4) * 50 * s
        f.rect(cx, cy - 40 * s, 36 * s, 44 * s, cols[i], a, 6 * s)
    f.circle(x - 40 * s, y + 55 * s, 16 * s, INK, a)
    f.circle(x + 90 * s, y + 55 * s, 16 * s, INK, a)


def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.8, 30.2))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Pourquoi au fond ?', W/2, 296, 46, SPARK, ha)

    # S1 — accroche (0–4) : le client file vers le lait dès la première image
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        words(f, 'Le lait est toujours', 440, 84, 0.05, INK, t_out=o)
        words(f, 'au fond du magasin.', 550, 84, 0.5, SPARK, t_out=o)
        store(f, 760, 640, fo, 0.08 + 0.92 * ease_io(seg(t, 0, 3.7)), trail=True,
              glow=0.5 + 0.5 * math.sin(t * 5))

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.0:
        o1 = 7.6
        g1 = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'Tu viens pour une brique.', 440, 70, 4.2, INK, t_out=o1)
            words(f, 'Tu traverses tout.', 550, 84, 4.9, SPARK, t_out=o1)
            # brique de lait qui grossit
            s = 1 + 0.06 * math.sin((t - 4) * 4)
            ba = g1 * ease(seg(t, 4.6, 5.0))
            c = f.c; c.save(); c.translate(W/2, 1000); c.scale(s, s)
            f.rect(-120, -200, 240, 380, MILK, ba, 18)
            f.rect(-120, -250, 240, 70, MUTED, ba, 12)
            f.rect(-40, -275, 80, 34, SPARK, ba, 8)
            f.rect(-120, -40, 240, 110, '#3d7fb0', ba, 0)
            f.text('LAIT', 0, 40, 72, MILK, ba, DISPLAY, True)
            c.restore()
            f.text('le produit qu’on rachète sans arrêt', W/2, 1340, 42, MUTED,
                   g1 * ease(seg(t, 5.8, 6.1)), DISPLAY, True)
        o2 = 10.7
        g2 = ease(seg(t, 7.8, 8.2)) * (1 - seg(t, o2, o2 + 0.3))
        if g2 > 0:
            words(f, 'Hasard ?', 600, 120, 7.9, INK, t_out=o2)
            words(f, 'Ou piège ?', 760, 120, 8.8, RED, t_out=o2)
            # deux pistes qui clignotent
            for i, lab in enumerate(('pratique', 'calcul')):
                xa = 330 + i * 420
                pa = g2 * ease(seg(t, 9.4 + 0.4 * i, 9.7 + 0.4 * i))
                f.rect(xa - 170, 1000, 340, 140, OCEAN, pa * 0.95, 30)
                f.text(lab, xa, 1088, 56, SPARK if i else INK, pa, DISPLAY, True)

    # S3 — la question (10.9–13.6)
    if 10.9 <= t < 13.6:
        words(f, 'Pourquoi', 820, 120, 11.0, INK, t_out=12.5)
        words(f, 'au fond ?', 950, 120, 11.4, SPARK, t_out=12.5)

    # S4 — la preuve (13.5–30)
    if 13.4 <= t < 30.0:
        # A : des clients suivis à la trace (13.6–22.4)
        oa = 22.4
        ga = ease(seg(t, 13.5, 13.9)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Des chercheurs ont suivi', 430, 70, 13.6, INK, t_out=oa)
            words(f, 'des clients à la trace.', 530, 70, 14.2, SPARK, t_out=oa)
            f.text('puce RFID · supermarché américain · 2013', W/2, 630, 32, MUTED,
                   ga * ease(seg(t, 15.0, 15.3)), MONO, False)
            u = ease_io(seg(t, 15.6, 20.6))
            store(f, 700, 600, ga, max(u, 0.001), trail=True, glow=seg(t, 20.3, 20.8))
            m = 430 * u
            f.text('parcours moyen', W/2, 1425, 40, MUTED, ga * ease(seg(t, 15.6, 15.9)), DISPLAY, True)
            f.text(f'≈ {int(round(m))} m', W/2, 1520, 78, SPARK,
                   ga * ease(seg(t, 15.6, 15.9)) * bump(t, 20.6, 0.15), MONO, True)
        # B : chaque détour (22.6–29.6)
        gb = ease(seg(t, 22.5, 22.9)) * (1 - seg(t, 29.4, 29.8))
        if gb > 0:
            words(f, 'Et chaque mètre', 430, 84, 22.6, INK, t_out=29.3)
            words(f, 'te fait croiser des tentations.', 540, 62, 23.1, SPARK, t_out=29.3)
            # allée : le client avance, les produits s'allument sur son passage
            xs = 160; xe = 920
            x = lerp(xs, xe, ease_io(seg(t, 24.2, 28.6)))
            f.rect(140, 760, 800, 120, CAPITAL, gb, 14)
            f.rect(140, 1180, 800, 120, CAPITAL, gb, 14)
            cols = [SPARK, EARTH, RED, MILK]
            for i in range(10):
                px = 170 + i * 78
                for row, yy in enumerate((780, 1200)):
                    on = 1.0 if x > px + 10 else 0.25
                    f.rect(px, yy, 52, 80, cols[(i + row) % 4], gb * on, 8)
            f.line([(xs, 1030), (x, 1030)], SPARK, gb * 0.85, 8, dash=[18, 14])
            f.circle(x, 1030, 26, SPARK, gb)
            f.circle(x, 1030, 12, DEEP, gb)
            f.text('rayon après rayon…', W/2, 1440, 48, MUTED, gb * ease(seg(t, 25.4, 25.7)), DISPLAY, True)

    # S5 — la réponse (30–36)
    if 29.9 <= t < 36.0:
        o = 35.6
        a = ease(seg(t, 30.3, 30.6)) * (1 - seg(t, o, o + 0.3))
        words(f, 'Tous les 17 m de plus :', 560, 70, 30.0, MUTED, t_out=o)
        big_center(f, '+1 $', 880, 300, SPARK, a, bump(t, 30.3, 0.18), font=DISPLAY)
        f.rect(190, 1010, 700, 130, OCEAN, a * ease(seg(t, 31.8, 32.1)) * 0.9, 28)
        words(f, 'd’achats non prévus.', 1100, 64, 32.0, INK, t_out=o)
        f.text('Journal of Marketing, 2013', W/2, 1260, 36, MUTED, a * ease(seg(t, 33.0, 33.3)), MONO, False)
        # pièces qui tombent
        for i in range(6):
            ts = 32.6 + 0.4 * i
            p = seg(t, ts, ts + 0.5)
            if p > 0:
                f.circle(250 + i * 116, lerp(1300, 1440, ease(p)), 30, SPARK, a * ease(p))
                f.text('$', 250 + i * 116, lerp(1300, 1440, ease(p)) + 12, 34, DEEP, a * ease(p), DISPLAY, True)

    # S6 — le retournement (36–48.4)
    if 36.0 <= t < 48.4:
        words(f, 'Le secret ?', 900, 120, 36.1, SPARK, t_out=37.9)
        # A : le camion livre par l'arrière (38.1–43.4)
        oa = 43.4
        ga = ease(seg(t, 38.1, 38.5)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Il y a aussi', 430, 80, 38.2, INK, t_out=oa)
            words(f, 'un camion.', 540, 92, 38.6, SPARK, t_out=oa)
            # camion qui arrive et se gare contre le mur du fond
            xt = lerp(-420, 300, ease(seg(t, 39.0, 40.4)))
            truck(f, xt, 660, ga)
            # chambre froide derrière le rayon
            ca = ga * ease(seg(t, 40.6, 41.0))
            f.rect(PX0, 820, PX1 - PX0, 170, '#1d4560', ca, 18)
            f.text('chambre froide', W/2, 920, 50, INK, ca, DISPLAY, True)
            store(f, 1000, 420, ga * ease(seg(t, 38.6, 39.0)), 0, glow=seg(t, 41.6, 42.0))
            # flèches : camion → chambre froide → rayon
            for i, (y1, y2, ts) in enumerate(((780, 815, 40.5), (995, 1030, 41.4))):
                pa = ga * ease(seg(t, ts, ts + 0.3))
                f.line([(W/2, y1), (W/2, y2)], SPARK, pa, 8)
            f.text('livré par l’arrière, au froid jusqu’au rayon', W/2, 1540, 38, MUTED,
                   ga * ease(seg(t, 42.0, 42.3)), DISPLAY, True)
        # B : les deux raisons sont vraies (43.6–47.9)
        ob = 47.9
        gb = ease(seg(t, 43.5, 43.9)) * (1 - seg(t, ob, ob + 0.3))
        if gb > 0:
            words(f, 'Les deux', 440, 100, 43.6, INK, t_out=ob)
            words(f, 'sont vraies.', 560, 100, 44.0, SPARK, t_out=ob)
            for i, (lab, sub, col) in enumerate((('Pratique', 'la chaîne du froid', INK),
                                                 ('Rentable', 'le détour fait vendre', SPARK))):
                ts = 44.7 + 0.9 * i
                pa = gb * ease(seg(t, ts, ts + 0.3))
                y = 760 + i * 300
                f.rect(170, y, 740, 240, OCEAN, pa * 0.95, 30)
                f.text(lab, W/2, y + 120, 78, col, pa * bump(t, ts, 0.1), DISPLAY, True)
                f.text(sub, W/2, y + 190, 40, MUTED, pa, DISPLAY, True)

    # S7 — l'escalade (48–56.4) : plus tu restes, plus tu craques
    if 48.0 <= t < 56.4:
        o1 = 55.9
        g1 = ease(seg(t, 48.1, 48.4)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'Et plus tu restes,', 430, 84, 48.1, INK, t_out=o1)
            words(f, 'plus tu craques.', 540, 84, 48.8, SPARK, t_out=o1)
            # horloge qui tourne
            cx, cy, r = 300, 920, 120
            f.circle(cx, cy, r, OCEAN, g1)
            f.circle(cx, cy, r, MUTED, g1, stroke=6)
            ang = -math.pi / 2 + (t - 48.1) * 1.6
            f.line([(cx, cy), (cx + 0.8 * r * math.cos(ang), cy + 0.8 * r * math.sin(ang))], SPARK, g1, 8)
            f.line([(cx, cy), (cx + 0.5 * r * math.cos(ang / 12), cy + 0.5 * r * math.sin(ang / 12))], INK, g1, 8)
            # caddie qui se remplit de plus en plus vite
            fl = seg(t, 49.4, 53.4) ** 1.8
            cart(f, 720, 960, g1, fl, 1.25)
            words(f, 'Un achat imprévu', 1240, 58, 51.6, INK, t_out=o1)
            words(f, 'en appelle un autre.', 1320, 58, 52.1, SPARK, t_out=o1)
            f.text('Journal of Marketing, 2015', W/2, 1430, 34, MUTED, g1 * ease(seg(t, 53.0, 53.3)), MONO, False)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        a = ease(seg(t, 56.1, 56.4))
        store(f, 560, 380, a, 0.05 + 0.95 * ease_io(seg(t, 56.1, 59.6)), trail=True)
        words(f, 'Le lait au fond :', 1060, 72, 56.3, INK)
        words(f, 'pratique, et rentable.', 1150, 72, 57.8, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(240, 1250, 600, 150, OCEAN, a, 28)
        pa = 0.5 + 0.5 * math.sin((t - 60) * 3)
        f.rect(240, 1250, 600, 150, SPARK, a * 0.25 * pa, 28)
        f.text('Abonne-toi.', W/2, 1345, 62, INK, a)


def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    ev += [(0.15, rise(1.2, 300, 900, 0.07))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (12.5, 29.6, 47.9, 55.9)]
    ev += [(11.0, pop(520))]
    ev += [(30.3, ding(1046, amp=0.28)), (36.1, pop(300, 0.15))]
    ev += [(44.0, clink())]
    ev += [(56.3, pop(440)), (60.0, ding(784, amp=0.22))]
    return ev
