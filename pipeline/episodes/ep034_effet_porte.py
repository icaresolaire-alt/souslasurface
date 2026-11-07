"""Pourquoi tu oublies ce que tu venais chercher en passant une porte (« effet de la porte »). Même structure que le pilote.

Sources :
- Radvansky, Krawietz et Tamplin, « Walking through doorways causes forgetting: Further explorations »,
  Quarterly Journal of Experimental Psychology 64(8), 1632-1645, 2011 :
  * Université de Notre Dame, communiqué « Walking through doorways causes forgetting, new research shows »
    (provost.nd.edu) : trois expériences, environnements réels et virtuels, étudiants ; objets pris sur une
    table et cachés dans des boîtes, traversée d'une pièce ou passage d'une porte sur la même distance ;
    « Entering or exiting through a doorway serves as an 'event boundary' in the mind, which separates
    episodes of activity and files them away » ; retour dans la pièce d'origine : « no improvements in memory ».
  * BPS Research Digest, C. Jarrett, 2 nov. 2011, « How walking through a doorway increases forgetting » :
    environnement virtuel de 55 pièces, objet échangé de table en table ; « event boundary » / mise à jour du
    « event model » ; « Performance was no better when back in the original room » ; pire dans une 3e pièce.
  * About memory (archive.memory-key.com), « Walking through doorways causes forgetting » : expérience en
    vraies salles, 60 étudiants ; retour dans la pièce d'origine sans avantage ; « it was the number of new
    rooms entered that appears to be important ».
- Nuance : McFadyen, Nolan, Pinocy, Buteri et Baumann, « Doorways do not always cause forgetting: a multimodal
  investigation », BMC Psychology 9:41, 8 mars 2021 (PMC7938580) : « we observed no significant effect of
  doorways on forgetting » sans tâche annexe ; « under working memory load, memory was more susceptible to
  interference after moving through doorways » (tâche : compter à rebours).
- Barres de l'expérience affichées comme schéma, sans pourcentage (chiffres non recoupés par deux sources).
"""
import math
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro (ep033 précédent).
COVER = dict(tag='Psychologie', l1='Pourquoi tu oublies tout', l2='en passant une porte')

WOOD = '#6b4f3a'
FRAME = '#b9c7cf'
WALL = '#3b5a6e'
SKY = '#9fd3ff'


def door(f, x, yb, a, k=1.0, s=1.0, glow=0.0):
    """Porte vue de face, bas au sol yb. k = ouverture (0 fermée, 1 ouverte)."""
    if a <= 0: return
    w, h = 220 * s, 420 * s
    x0, y0 = x - w / 2, yb - h
    if glow > 0:
        f.rect(x0 - 30 * s, y0 - 30 * s, w + 60 * s, h + 30 * s, SPARK, a * glow * 0.25, 20 * s)
    f.rect(x0, y0, w, h, '#05101a', a)                 # ouverture sombre
    f.color(SKY, a * 0.18 * k); f.c.rectangle(x0, y0, w, h); f.c.fill()
    # battant (rétréci en perspective quand il s'ouvre)
    pw = w * (1 - 0.78 * k)
    c = f.c; f.color(WOOD, a)
    c.move_to(x0, y0); c.line_to(x0 + pw, y0 + 26 * s * k); c.line_to(x0 + pw, yb - 10 * s * k)
    c.line_to(x0, yb); c.close_path(); c.fill()
    f.circle(x0 + pw - 24 * s * (1 - k * 0.6), yb - h / 2, 9 * s, SPARK, a)
    # chambranle
    f.line([(x0 - 10 * s, yb), (x0 - 10 * s, y0 - 10 * s), (x0 + w + 10 * s, y0 - 10 * s), (x0 + w + 10 * s, yb)],
           FRAME, a, 14 * s)


def person(f, x, yb, a, s=1.0, t=0.0, walking=False):
    """Silhouette simple, pieds en yb."""
    if a <= 0: return
    bob = 6 * s * abs(math.sin(t * 7)) if walking else 0
    f.circle(x, yb - 300 * s - bob, 44 * s, INK, a)
    f.rect(x - 46 * s, yb - 245 * s - bob, 92 * s, 150 * s, INK, a, 30 * s)
    sw = 0.35 * math.sin(t * 7) if walking else 0
    for sg in (1, -1):
        f.line([(x, yb - 100 * s - bob), (x + sg * 60 * s * sw, yb)], INK, a, 26 * s)


def bubble(f, x, y, a, txt, col=INK, size=44, w=None):
    if a <= 0: return
    ww = w or f.width(txt, size) + 70
    f.rect(x - ww / 2, y - 60, ww, 100, OCEAN, a, 40)
    f.rect(x - ww / 2, y - 60, ww, 100, SPARK, a * 0.18, 40)
    f.circle(x - 20, y + 60, 14, OCEAN, a); f.circle(x - 34, y + 90, 8, OCEAN, a)
    f.text(txt, x, y + 6, size, col, a)


def stopwatch(f, x, y, r, a, v, vmax=3.0):
    if a <= 0: return
    f.circle(x, y, r, LINE, a, 18)
    k = clamp(v / vmax)
    c = f.c; f.color(SPARK, a); c.set_line_width(18)
    c.new_sub_path(); c.arc(x, y, r, -math.pi / 2, -math.pi / 2 + 2 * math.pi * k); c.stroke()
    f.rect(x - 22, y - r - 46, 44, 26, FRAME, a, 6)
    f.text(f'{v:.1f}'.replace('.', ',') + ' s', x, y + 26, 76, INK, a, MONO, True)


def plan(f, y, a, k, with_door, label, t):
    """Vue de dessus : couloir de 760 px, avec ou sans mur + porte au milieu. k = avancée 0..1."""
    if a <= 0: return
    x0, x1, h = 160, 920, 200
    f.rect(x0, y, x1 - x0, h, LINE, a * 0.7, 18)
    f.line([(x0, y), (x1, y), (x1, y + h), (x0, y + h), (x0, y)], WALL, a, 10)
    if with_door:
        xm = (x0 + x1) / 2
        f.line([(xm, y), (xm, y + 60)], WALL, a, 14)
        f.line([(xm, y + h - 60), (xm, y + h)], WALL, a, 14)
        f.line([(xm, y + 60), (xm + 60, y + 90)], WOOD, a, 8)
    # tables
    f.rect(x0 + 30, y + 70, 60, 60, WOOD, a, 8)
    f.rect(x1 - 90, y + 70, 60, 60, WOOD, a, 8)
    px = lerp(x0 + 120, x1 - 120, ease_io(k))
    f.line([(x0 + 120, y + h / 2), (px, y + h / 2)], SPARK, a * 0.5, 4, [10, 12])
    f.circle(px, y + h / 2, 26, INK, a)
    f.rect(px + 14, y + h / 2 - 46, 30, 30, SPARK, a, 6)       # l'objet porté (caché dans une boîte)
    f.text(label, x0, y - 22, 36, MUTED, a, MONO, True, 'left')


def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.8, 30.2))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Pourquoi la porte ?', W / 2, 296, 44, SPARK, ha)

    # S1 — accroche (0–4) : on passe la porte, la pensée s'efface
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        words(f, 'Tu passes une porte.', 470, 76, 0.05, INK, t_out=o)
        words(f, 'Et tu as oublié pourquoi.', 580, 70, 0.7, SPARK, t_out=o)
        yb = 1450
        door(f, 640, yb, fo, ease(seg(t, 0.0, 0.8)), 1.0)
        px = lerp(180, 900, ease_io(seg(t, 0.2, 3.4)))
        person(f, px, yb, fo, 0.9, t, True)
        k = seg(t, 2.0, 2.4)
        bubble(f, px + 30, 820, fo * (1 - k), 'les clés', INK)
        bubble(f, px + 30, 820, fo * k, '?', SPARK, 70, 150)

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.0:
        o1 = 7.4
        g1 = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'Tu le savais', 470, 80, 4.2, INK, t_out=o1)
            words(f, 'il y a 3 secondes.', 580, 76, 4.6, SPARK, t_out=o1)
            stopwatch(f, W / 2, 1060, 230, g1, 3.0 * ease_io(seg(t, 4.8, 6.8)))
        o2 = 10.7
        g2 = ease(seg(t, 7.6, 8.0)) * (1 - seg(t, o2, o2 + 0.3))
        if g2 > 0:
            words(f, 'Rien ne s’est passé.', 470, 76, 7.7, INK, t_out=o2)
            words(f, 'Juste un seuil.', 580, 80, 8.2, SPARK, t_out=o2)
            door(f, W / 2, 1450, g2, 1.0, 1.25, 0.5 + 0.5 * math.sin(t * 4))

    # S3 — la question (10.9–13.6)
    if 10.9 <= t < 13.6:
        words(f, 'Pourquoi une porte', 820, 90, 11.0, INK, t_out=12.5)
        words(f, 'te fait oublier ?', 950, 90, 11.4, SPARK, t_out=12.5)

    # S4 — la preuve (13.5–30)
    if 13.4 <= t < 30.0:
        oa = 21.0
        ga = ease(seg(t, 13.5, 13.9)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Notre Dame, 2011.', 440, 76, 13.6, INK, t_out=oa)
            words(f, 'Des étudiants portent', 550, 70, 14.1, SPARK, t_out=oa)
            words(f, 'des objets cachés.', 640, 70, 14.4, SPARK, t_out=oa)
            k = seg(t, 15.4, 19.4)
            plan(f, 830, ga * ease(seg(t, 15.0, 15.4)), k, False, 'même pièce', t)
            plan(f, 1180, ga * ease(seg(t, 15.2, 15.6)), k, True, 'avec une porte', t)
            f.text('Même distance.', W / 2, 1520, 54, INK, ga * ease(seg(t, 19.0, 19.4)))
        gb = ease(seg(t, 21.2, 21.6)) * (1 - seg(t, 29.4, 29.8))
        if gb > 0:
            words(f, 'Puis on teste', 440, 76, 21.3, INK, t_out=29.4)
            words(f, 'leur mémoire.', 550, 76, 21.7, SPARK, t_out=29.4)
            yb = 1330; hmax = 520
            h1 = 0.32 * hmax * ease_io(seg(t, 22.6, 23.8))
            h2 = 1.0 * hmax * ease_io(seg(t, 24.2, 26.2))
            f.line([(150, yb), (930, yb)], LINE, gb, 4)
            f.rect(220, yb - h1, 260, h1, MUTED, gb, 14)
            f.rect(600, yb - h2, 260, h2, SPARK, gb, 14)
            f.text('même pièce', 350, yb + 55, 36, MUTED, gb, MONO, True)
            f.text('après la porte', 730, yb + 55, 36, INK, gb, MONO, True)
            f.text('oublis', 140, yb - hmax - 20, 34, MUTED, gb * ease(seg(t, 22.4, 22.8)), MONO, False, 'left')
            f.text('Plus d’oublis', W / 2, 1490, 54, SPARK, gb * ease(seg(t, 26.4, 26.8)))
            f.text('schéma simplifié', W / 2, 1545, 30, MUTED, gb * ease(seg(t, 26.4, 26.8)), MONO, False)

    # S5 — la réponse (30–36)
    if 29.9 <= t < 36.0:
        o = 35.6
        a = ease(seg(t, 30.3, 30.6)) * (1 - seg(t, o, o + 0.3))
        words(f, 'La seule différence :', 620, 66, 30.1, INK, t_out=o)
        big_center(f, '1 porte', 850, 170, SPARK, a, bump(t, 30.3, 0.15))
        g = ease(seg(t, 31.8, 32.2)) * a
        door(f, W / 2, 1360, g, ease(seg(t, 32.0, 33.0)), 0.8, 0.6)
        f.text('En virtuel comme en vraies salles.', W / 2, 1500, 42, MUTED, g * ease(seg(t, 32.6, 33.0)), DISPLAY, True)

    # S6 — le retournement (36–48.4)
    if 36.0 <= t < 48.4:
        words(f, 'Le secret ?', 900, 130, 36.1, INK, t_out=37.9)
        oa = 42.8
        ga = ease(seg(t, 38.1, 38.5)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Ton cerveau découpe', 440, 74, 38.2, INK, t_out=oa)
            words(f, 'ta vie en épisodes.', 550, 74, 38.7, SPARK, t_out=oa)
            # bande de 3 épisodes ; la porte = la coupure ; l'épisode précédent est rangé
            k = 2 * ease_io(seg(t, 39.4, 41.6))
            names = ['cuisine', 'couloir', 'chambre']
            for i, nm in enumerate(names):
                cur = k
                x = W / 2 - 120 + (i - cur) * 290
                dim = 1.0 if abs(i - cur) < 0.5 else 0.35
                gi = ga * ease(seg(t, 39.0 + i * 0.15, 39.4 + i * 0.15))
                f.rect(x, 860, 240, 360, OCEAN, gi, 18)
                f.rect(x, 860, 240, 360, SPARK if dim == 1.0 else LINE, gi * (0.35 if dim == 1.0 else 0.6), 18)
                f.text(nm, x + 120, 1060, 38, INK, gi * dim, MONO, True)
                if i < 2:
                    f.rect(x + 248, 900, 34, 280, WOOD, gi * 0.9, 6)
            f.text('Chaque porte tourne la page.', W / 2, 1420, 48, INK, ga * ease(seg(t, 40.8, 41.2)))
            f.text('L’épisode d’avant est rangé.', W / 2, 1490, 44, MUTED, ga * ease(seg(t, 41.2, 41.6)))
        ob = 47.9
        gb = ease(seg(t, 42.9, 43.3)) * (1 - seg(t, ob, ob + 0.3))
        if gb > 0:
            words(f, 'Revenir dans la pièce', 440, 74, 43.0, INK, t_out=ob)
            words(f, 'n’aide même pas.', 550, 76, 43.5, SPARK, t_out=ob)
            # trois pièces : A -> B -> retour A
            xs = [270, 540, 810]
            for i, (x, nm) in enumerate(zip(xs[:2], ['pièce 1', 'pièce 2'])):
                f.rect(x - 120, 800, 240, 300, LINE, gb * 0.8, 18)
                f.text(nm, x, 1150, 34, MUTED, gb, MONO, True)
            f.rect(xs[2] - 120, 800, 240, 300, LINE, gb * 0.8, 18)
            f.text('pièce 1', xs[2], 1150, 34, MUTED, gb, MONO, True)
            p = ease_io(seg(t, 44.0, 46.0))
            px = lerp(xs[0], xs[2], p)
            f.circle(px, 950, 30, INK, gb)
            f.line([(xs[0], 1010), (px, 1010)], SPARK, gb * 0.6, 5, [10, 12])
            f.text('retour', xs[2], 760, 34, SPARK, gb * ease(seg(t, 45.6, 46.0)), MONO, True)
            f.text('Pas mieux qu’à côté.', W / 2, 1380, 50, INK, gb * ease(seg(t, 46.0, 46.4)))
            f.text('Ce n’est pas le décor. C’est la coupure.', W / 2, 1450, 40, MUTED, gb * ease(seg(t, 46.3, 46.7)))

    # S7 — l'escalade (48–56.4) : la nuance de 2021
    if 48.0 <= t < 56.4:
        oa = 52.0
        ga = ease(seg(t, 48.1, 48.4)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Une étude de 2021', 440, 74, 48.1, INK, t_out=oa)
            words(f, 'nuance l’effet.', 550, 76, 48.6, SPARK, t_out=oa)
            door(f, W / 2, 1300, ga, 1.0, 0.9)
            person(f, lerp(300, 800, ease_io(seg(t, 49.2, 51.4))), 1300, ga, 0.75, t, True)
            bubble(f, lerp(330, 830, ease_io(seg(t, 49.2, 51.4))), 820, ga, 'les clés', INK)
            f.text('Tête libre : pas d’effet net.', W / 2, 1460, 50, INK, ga * ease(seg(t, 50.4, 50.8)))
        o = 55.9
        gb = ease(seg(t, 52.2, 52.5)) * (1 - seg(t, o, o + 0.3))
        if gb > 0:
            words(f, 'L’oubli surgit quand', 440, 74, 52.3, INK, t_out=o)
            words(f, 'ta tête est chargée.', 550, 74, 52.7, SPARK, t_out=o)
            person(f, W / 2 - 200, 1380, gb, 0.85, t, True)
            items = ['mail', 'appel', 'courses', 'rendez-vous']
            for i, it in enumerate(items):
                gi = gb * ease(seg(t, 53.0 + i * 0.25, 53.3 + i * 0.25))
                f.rect(560, 780 + i * 120, 400, 90, OCEAN, gi, 30)
                f.text(it, 760, 840 + i * 120, 40, INK, gi, MONO, True)
            f.text('Ex. : compter à rebours en marchant', W / 2, 1490, 38, MUTED, gb * ease(seg(t, 54.2, 54.5)))

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        words(f, 'Ce n’est pas ta mémoire qui lâche.', 760, 54, 56.3, INK)
        words(f, 'C’est la porte qui tourne la page.', 870, 60, 57.6, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(240, 1160, 600, 150, OCEAN, a, 28)
        pa = 0.5 + 0.5 * math.sin((t - 60) * 3)
        f.rect(240, 1160, 600, 150, SPARK, a * 0.25 * pa, 28)
        f.text('Abonne-toi.', W / 2, 1255, 62, INK, a)


def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    ev += [(0.15, pop(440, 0.09))]
    ev += [(2.0, clink(900))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (12.5, 29.6, 47.9, 55.9)]
    ev += [(11.0, pop(520))]
    ev += [(26.4, ding(784, amp=0.2))]
    ev += [(30.3, ding(1046, amp=0.28)), (36.1, pop(300, 0.15))]
    ev += [(40.8, ding(784, amp=0.18))]
    ev += [(46.0, ding(880, amp=0.18))]
    ev += [(56.3, pop(440)), (60.0, ding(784, amp=0.22))]
    return ev
