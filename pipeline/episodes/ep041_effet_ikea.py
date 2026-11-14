"""L'effet IKEA : on aime plus ce qu'on a monté soi-même. Même structure que le pilote.

Sources :
- Étude : M. Norton, D. Mochon, D. Ariely, « The IKEA effect: When labor leads to love », document de travail
  Harvard Business School 2011 (n° 11-091), publié dans Journal of Consumer Psychology 22(3), 2012, p. 453-460.
  Wikipedia « IKEA effect » (trois études publiées en 2011) ; QUT / The Conversation, Mortimer, Mathmann et
  Grimmer, 31 mai 2021.
- Boîte de rangement IKEA (Kassett) : enchère moyenne 0,48 $ pour la boîte déjà montée contre 0,78 $ pour ceux
  qui l'ont montée, enchère plafonnée à 1 $ : Priceonomics, 26 févr. 2014 (« the mean valuation in the
  pre-assembly group was $0.48, the self-assembly group... ($0.78) ») ; Atticus Li, « IKEA effect » (mêmes
  chiffres). « 63 % de plus » : Wikipedia et Silicon Canals, 17 août 2026. Calcul : 0,78 / 0,48 = 1,625.
- Origami : les créateurs paient environ cinq fois plus pour leur origami que les autres : Wikipedia (« about
  five times more »), Silicon Canals (« roughly five times higher ») ; LifeLabs Learning (0,23 $ contre 0,05 $,
  enchères de 0 à 100 cents). Les créateurs jugent leur origami presque aussi précieux que celui d'un expert :
  Wikipedia et QUT (« almost equal in value to the expert origami »).
- L'effet disparaît si la tâche n'est pas finie ou si l'objet est détruit : Wikipedia (« when participants built
  and then destroyed their creations, or failed to complete them, the IKEA effect dissipated »), QUT,
  Priceonomics. Nuance non affichée : la réplication de Sarstedt et al. (2017) ne retrouve pas l'effet de
  l'inachèvement, mais confirme celui de la destruction.
- Non affiché : l'histoire des préparations pour gâteau avec un œuf frais, que QUT juge très exagérée.
- La dernière idée (tes idées, tes projets) est un conseil, pas un résultat d'étude.
"""
import math
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro (ep040 précédent).
COVER = dict(tag='Psychologie', l1='Pourquoi tu aimes plus', l2='le meuble que tu as monté')

WOOD = '#c8a173'
WOOD2 = '#a27c52'
WOOD3 = '#e0c298'
PAPER = '#eaf1ec'
PAPER2 = '#b9c8c2'


def poly(f, pts, col, a):
    if a <= 0: return
    c = f.c; f.color(col, a)
    for i, (x, y) in enumerate(pts):
        (c.move_to if i == 0 else c.line_to)(x, y)
    c.close_path(); c.fill()


def box(f, x, y, s, a, p=1.0, fall=0.0):
    """Caisse en bois vue de trois quarts ; (x, y) = coin bas avant ; p = montage (0 = en kit, 1 = montée).
    fall > 0 : les panneaux se détachent et tombent."""
    if a <= 0: return
    d = s * 0.45
    # trois panneaux : côté, dessus, face ; chacun arrive d'une direction différente
    parts = [
        ('side', WOOD2, (260, -40), 0.0),
        ('top', WOOD3, (0, -360), 0.25),
        ('front', WOOD, (-280, 60), 0.5),
    ]
    for name, col, (dx, dy), lag in parts:
        q = ease(seg(p, lag * 0.8, lag * 0.8 + 0.5))
        ox, oy = dx * (1 - q), dy * (1 - q)
        if fall > 0:
            k = {'side': 1, 'top': -1, 'front': 0.4}[name]
            ox += 140 * k * fall; oy += 120 * fall * fall * (1.2 if name == 'top' else 0.8)
        aa = a * (0.35 + 0.65 * q)
        if name == 'front':
            pts = [(x, y), (x + s, y), (x + s, y - s), (x, y - s)]
        elif name == 'side':
            pts = [(x + s, y), (x + s + d, y - d), (x + s + d, y - s - d), (x + s, y - s)]
        else:
            pts = [(x, y - s), (x + s, y - s), (x + s + d, y - s - d), (x + d, y - s - d)]
        pts = [(px + ox, py + oy) for (px, py) in pts]
        poly(f, pts, col, aa)
        if name == 'front':
            # poignée découpée
            cx = x + s / 2 + ox; cy = y - s * 0.62 + oy
            f.rect(cx - s * 0.16, cy - s * 0.05, s * 0.32, s * 0.1, DEEP, aa * 0.8, s * 0.05)


def bar(f, x, base, w, hmax, frac, col, a, label, value):
    if a <= 0: return
    h = hmax * frac
    f.rect(x - w / 2, base - h, w, h, col, a, 14)
    f.text(value, x, base - h - 30, 66, col, a, MONO, True)
    f.text(label, x, base + 62, 40, INK, a, DISPLAY, True)


def crane(f, x, y, s, a, col=PAPER, col2=PAPER2, wob=0.0):
    """Grue en origami stylisée (triangles), wob = défauts de pliage."""
    if a <= 0: return
    j = lambda k: wob * 18 * math.sin(k * 2.3 + 1)
    poly(f, [(x - s, y - s * 0.1 + j(1)), (x, y + s * 0.25), (x - s * 0.15, y - s * 0.75 + j(2))], col, a)
    poly(f, [(x + s, y - s * 0.2 + j(3)), (x, y + s * 0.25), (x + s * 0.12, y - s * 0.8 + j(4))], col2, a)
    poly(f, [(x - s * 0.6, y + s * 0.1), (x + s * 0.6, y + s * 0.1), (x, y + s * 0.45 + j(5))], col2, a)
    poly(f, [(x + s * 0.55, y + s * 0.12), (x + s * 0.95 + j(6), y - s * 0.55), (x + s * 0.7, y + s * 0.12)], col, a)


def heart(f, x, y, r, a, fill):
    """Cœur dont le remplissage doré monte de 0 à 1."""
    if a <= 0: return
    c = f.c

    def path():
        c.new_path(); c.move_to(x, y + r * 0.9)
        c.curve_to(x - r * 1.6, y - r * 0.1, x - r * 0.8, y - r * 1.3, x, y - r * 0.45)
        c.curve_to(x + r * 0.8, y - r * 1.3, x + r * 1.6, y - r * 0.1, x, y + r * 0.9)
        c.close_path()
    path(); f.color(LINE, a); c.fill()
    c.save(); path(); c.clip()
    top = y + r * 0.9 - (r * 2.1) * fill
    f.rect(x - r * 2, top, r * 4, r * 3, SPARK, a, 0)
    c.restore()
    path(); f.color(SPARK, a); c.set_line_width(6); c.stroke()


def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')
    c = f.c

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.8, 30.2))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Combien vaut ta boîte ?', W/2, 296, 46, SPARK, ha)

    # S1 — accroche (0–4) : la caisse se monte dès la première image
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        words(f, 'Ce que tu montes toi-même,', 460, 66, 0.05, INK, t_out=o)
        words(f, 'tu le crois plus précieux.', 570, 66, 1.2, SPARK, t_out=o)
        box(f, W/2 - 230, 1350, 400, fo, p=0.15 + 0.85 * seg(t, 0.0, 3.0))

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.0:
        o1 = 7.4
        g1 = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'Même boîte.', 470, 90, 4.2, INK, t_out=o1)
            words(f, 'Même bois.', 580, 90, 4.8, SPARK, t_out=o1)
            for k in range(2):
                bb = g1 * ease(seg(t, 4.6 + 0.4 * k, 5.0 + 0.4 * k))
                box(f, 150 + 450 * k, 1300 + 10 * math.sin(t * 2 + k), 280, bb)
            f.text('=', W/2 + 20, 1170, 120, SPARK, g1 * ease(seg(t, 5.6, 5.9)), MONO, True)
        o2 = 10.7
        g2 = ease(seg(t, 7.6, 8.0)) * (1 - seg(t, o2, o2 + 0.3))
        if g2 > 0:
            words(f, 'Ton intuition :', 480, 72, 7.7, MUTED, t_out=o2)
            words(f, 'elles valent', 600, 84, 8.1, INK, t_out=o2)
            words(f, 'le même prix.', 710, 84, 8.6, SPARK, t_out=o2)
            ab = g2 * ease(seg(t, 8.6, 8.9))
            box(f, W/2 - 200, 1340, 340, ab)
            f.text('? $', W/2 + 340, 1100, 90, SPARK, ab * (0.6 + 0.4 * math.sin(t * 4)), MONO, True)

    # S3 — la question (10.9–13.6)
    if 10.9 <= t < 13.6:
        words(f, 'Et si tu l’avais', 820, 96, 11.0, INK, t_out=12.5)
        words(f, 'montée toi-même ?', 950, 100, 11.4, SPARK, t_out=12.5)

    # S4 — la preuve (13.5–30)
    if 13.4 <= t < 30.0:
        # A : l'expérience de la boîte IKEA (13.6–21.4)
        oa = 21.4
        ga = ease(seg(t, 13.5, 13.9)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Harvard, 2011.', 430, 84, 13.6, INK, t_out=oa)
            words(f, 'Une boîte IKEA aux enchères.', 530, 62, 14.1, SPARK, t_out=oa)
            # petite boîte qui se monte à droite pendant le test
            base = 1290
            g = ease_io(seg(t, 15.4, 18.0))
            v1 = 0.48 * g; v2 = 0.78 * ease_io(seg(t, 16.4, 19.2))
            ba = ga * ease(seg(t, 15.0, 15.4))
            hmax = 560
            bar(f, 330, base, 220, hmax, v1, MUTED, ba, 'déjà montée',
                f'{v1:.2f} $'.replace('.', ','))
            bar(f, 750, base, 220, hmax, v2, SPARK, ba, 'montée soi-même',
                f'{v2:.2f} $'.replace('.', ','))
            f.line([(150, base), (930, base)], LINE, ba, 6)
            f.line([(150, base - hmax), (930, base - hmax)], LINE, ba * 0.6, 3, dash=[14, 12])
            f.text('enchère max : 1 $', 150, base - hmax - 16, 30, MUTED, ba, MONO, False, align='left')
            words(f, 'enchère moyenne, même boîte', 1460, 40, 18.6, MUTED, t_out=oa, font=MONO, bold=False)
        # B : les origamis (21.6–29.6)
        gb = ease(seg(t, 21.5, 21.9)) * (1 - seg(t, 29.4, 29.8))
        if gb > 0:
            words(f, 'Même test', 430, 90, 21.6, INK, t_out=29.3)
            words(f, 'avec des origamis.', 540, 84, 22.1, SPARK, t_out=29.3)
            ca = gb * ease(seg(t, 22.8, 23.2))
            crane(f, 330, 800 + 10 * math.sin(t * 2), 150, ca, wob=0.7)
            crane(f, 750, 800 + 10 * math.sin(t * 2 + 1), 150, ca, wob=0.7)
            base = 1330
            u = ease_io(seg(t, 24.0, 26.4))
            hmax = 1200
            bar(f, 330, base, 200, hmax, 0.23 * u, SPARK, ca, 'son créateur', f'{0.23 * u:.2f} $'.replace('.', ','))
            bar(f, 750, base, 200, hmax, 0.05 * u, MUTED, ca, 'les autres', f'{0.05 * u:.2f} $'.replace('.', ','))
            f.line([(150, base), (930, base)], LINE, ca, 6)
            f.text('presque 5 fois plus', W/2, 1490, 50, SPARK, gb * ease(seg(t, 26.6, 26.9)), MONO, True)

    # S5 — la réponse (30–36)
    if 29.9 <= t < 36.0:
        o = 35.6
        a = ease(seg(t, 30.3, 30.6)) * (1 - seg(t, o, o + 0.3))
        words(f, 'Pour la même boîte :', 600, 70, 30.0, MUTED, t_out=o)
        big_center(f, '+63 %', 880, 260, SPARK, a, bump(t, 30.3, 0.18), font=DISPLAY)
        words(f, 'si tu l’as montée.', 1060, 80, 31.0, INK, t_out=o)
        words(f, '0,78 $ contre 0,48 $', 1200, 44, 32.5, MUTED, t_out=o, font=MONO, bold=False)

    # S6 — le retournement (36–48.4)
    if 36.0 <= t < 48.4:
        words(f, 'Pourquoi ?', 900, 150, 36.1, SPARK, t_out=37.9)
        # A : l'effort devient de l'attachement (38.1–42.6)
        oa = 42.6
        ga = ease(seg(t, 38.1, 38.5)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Ton effort', 440, 90, 38.2, INK, t_out=oa)
            words(f, 'devient de l’amour.', 550, 84, 38.7, SPARK, t_out=oa)
            fill = ease_io(seg(t, 39.2, 41.8))
            # gouttes d'effort qui montent vers le cœur
            for k in range(5):
                q = ((t - 38.5) * 0.9 + k / 5) % 1.0
                f.circle(W/2 - 280 + 140 * k, 1420 - 360 * q, 12, INK, ga * (1 - q) * 0.7)
            heart(f, W/2, 960, 170 * bump(t, 41.8, 0.1), ga, fill)
        # B : seulement si tu finis (42.9–47.9)
        ob = 47.9
        gb = ease(seg(t, 42.8, 43.2)) * (1 - seg(t, ob, ob + 0.3))
        if gb > 0:
            words(f, 'Mais seulement', 440, 84, 42.9, INK, t_out=ob)
            words(f, 'si tu la finis.', 550, 90, 43.4, SPARK, t_out=ob)
            fall = ease(seg(t, 45.0, 46.2))
            box(f, W/2 - 200, 1180, 320, gb * (1 - 0.7 * fall), p=0.7, fall=fall)
            f.text('détruite ou pas finie :', W/2, 1440, 42, MUTED, gb * ease(seg(t, 45.6, 45.9)), MONO, False)
            f.text('l’effet disparaît', W/2, 1510, 52, RED, gb * ease(seg(t, 46.0, 46.3)), MONO, True)

    # S7 — l'escalade (48–56.4)
    if 48.0 <= t < 56.4:
        o1 = 51.9
        g1 = ease(seg(t, 48.1, 48.4)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'Ton origami raté', 430, 84, 48.1, INK, t_out=o1)
            words(f, '≈ celui d’un expert.', 540, 84, 48.7, SPARK, t_out=o1)
            ca = g1 * ease(seg(t, 49.0, 49.3))
            crane(f, 290, 1000, 170, ca, wob=1.0)
            crane(f, 790, 1000, 170, ca, SPARK, '#c99232', wob=0.0)
            f.text('≈', W/2 + 10, 1030, 120, INK, ca * ease(seg(t, 49.6, 49.9)), MONO, True)
            f.text('toi', 290, 1300, 46, INK, ca, DISPLAY, True)
            f.text('un expert', 790, 1300, 46, INK, ca, DISPLAY, True)
            f.text('selon les créateurs', W/2, 1420, 38, MUTED, ca * ease(seg(t, 50.0, 50.3)), MONO, False)
        o2 = 55.9
        g2 = ease(seg(t, 52.1, 52.4)) * (1 - seg(t, o2, o2 + 0.3))
        if g2 > 0:
            words(f, 'Méfie-toi aussi', 430, 84, 52.2, INK, t_out=o2)
            words(f, 'de tes idées.', 540, 84, 52.7, SPARK, t_out=o2)
            items = [('ton projet', 53.2), ('ton plan', 53.8), ('ton code', 54.4)]
            for i, (lab, ts) in enumerate(items):
                ia = g2 * ease(seg(t, ts, ts + 0.3))
                yy = 820 + 190 * i
                x0 = W/2 - 280 + 60 * (1 - ease(seg(t, ts, ts + 0.3)))
                f.rect(x0, yy, 560, 130, OCEAN, ia, 30)
                f.circle(x0 + 70, yy + 65, 22 * bump(t, ts, 0.3), SPARK, ia)
                f.text(lab, x0 + 120, yy + 82, 52, INK, ia, DISPLAY, True, align='left')

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        a = ease(seg(t, 56.1, 56.4))
        box(f, W/2 - 140, 840, 230, a)
        words(f, 'Ce que tu construis,', 960, 66, 56.3, INK)
        words(f, 'tu le surestimes.', 1060, 74, 57.6, SPARK)
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
    ev += [(19.2, clink())]
    ev += [(30.3, ding(1046, amp=0.28)), (36.1, pop(300, 0.15))]
    ev += [(45.0, pop(260, 0.15))]
    ev += [(56.3, pop(440)), (60.0, ding(784, amp=0.22))]
    return ev
