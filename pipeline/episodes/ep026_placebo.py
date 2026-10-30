"""L'effet placebo : une fausse pilule soulage mieux quand elle est chère. Même structure que le pilote.

Sources :
- Waber, Shiv, Carmon et Ariely, « Commercial Features of Placebo and Therapeutic Efficacy »,
  JAMA 2008 (lettre, 5 mars 2008). Stanford GSB Insights « The Behavioral Impact of a Higher Price »
  (1er mars 2008) : petites décharges électriques au poignet ; 2,50 $ la pilule contre 10 cents ;
  « 85 % » ont eu moins mal avec la pilule chère « contre 61 % » avec la pilule soldée.
  News-Medical, « Costly placebo works better than cheap one » (6 mars 2008) : 82 participants,
  brochure 2,50 $ ou 10 cents, 85 % contre 61 %.
- Levine, Gordon et Fields, « The mechanism of placebo analgesia », The Lancet 1978;2(8091):654-7
  (PubMed 80579) : douleur après extraction de dents de sagesse ; la naloxone (qui bloque les opioïdes
  du corps) augmente la douleur des patients soulagés par placebo ; « la libération d'endorphines
  sert d'intermédiaire à l'analgésie placebo ».
- Kaptchuk et al., PLoS ONE, 22 déc. 2010. Harvard Gazette / HMS « Placebos work, even without deception » :
  80 patients atteints du syndrome de l'intestin irritable, flacon marqué « placebo », 3 semaines ;
  soulagement suffisant pour 59 % contre 35 % sans traitement.
- Nuance affichée : l'effet porte surtout sur ce qu'on ressent (douleur, inconfort) ; il ne guérit pas
  une maladie (Kaptchuk, Harvard Gazette ; consensus des revues sur le placebo).
"""
import math
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro (ep025 précédent).
COVER = dict(tag='Science', l1='Une fausse pilule soulage', l2='mieux quand elle est chère')

PILL_A = '#f2f2ee'
PILL_B = '#d8584a'
PILL_C = '#5b8fd8'
BRAIN = '#c98aa0'


def pill(f, x, y, s, a, rot=0.0, cb=PILL_B, split=0.0):
    """Gélule vue de côté ; split > 0 ouvre les deux moitiés."""
    if a <= 0: return
    c = f.c; c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    w, h = 220, 90
    d = split * 70
    c.save(); c.rectangle(-w/2 - 10 - d, -h, w/2 + 10, 2 * h); c.clip()
    c.translate(-d, 0); f.rect(-w/2, -h/2, w, h, PILL_A, a, h/2); c.restore()
    c.save(); c.rectangle(0 + d, -h, w/2 + 10, 2 * h); c.clip()
    c.translate(d, 0); f.rect(-w/2, -h/2, w, h, cb, a, h/2); c.restore()
    f.rect(-w/2 + 30 - d, -h/2 + 14, w/2 - 40, 14, '#ffffff', a * 0.35, 7)
    c.restore()


def bolt(f, x, y, s, a):
    if a <= 0: return
    c = f.c; c.save(); c.translate(x, y); c.scale(s, s)
    f.color(SPARK, a); c.new_sub_path()
    pts = [(10, -60), (-26, 6), (-2, 6), (-12, 60), (26, -8), (2, -8), (14, -60)]
    c.move_to(*pts[0])
    for p in pts[1:]: c.line_to(*p)
    c.close_path(); c.fill(); c.restore()


def tag(f, x, y, txt, col, a, s=1.0):
    """Étiquette de prix."""
    if a <= 0: return
    c = f.c; c.save(); c.translate(x, y); c.scale(s, s)
    f.rect(-140, -50, 280, 100, col, a, 18)
    f.circle(-112, 0, 9, DEEP, a)
    f.text(txt, 14, 17, 48, DEEP, a, MONO, True)
    c.restore()


def bar(f, x, base, w, hmax, p, col, a, label, val):
    if a <= 0: return
    h = hmax * p
    f.rect(x - w/2, base - hmax, w, hmax, LINE, a * 0.5, 14)
    if h > 1: f.rect(x - w/2, base - h, w, h, col, a, 14)
    f.text(val, x, base - h - 24, 72, col if col != CAPITAL else INK, a, MONO, True)
    f.text(label, x, base + 60, 40, MUTED, a, DISPLAY, True)


def brain(f, x, y, s, a, glow=0.0):
    if a <= 0: return
    c = f.c; c.save(); c.translate(x, y); c.scale(s, s)
    if glow > 0: f.circle(0, 0, 190, SPARK, a * 0.25 * glow)
    for (dx, dy, r) in ((-70, -20, 80), (0, -55, 85), (75, -20, 80), (-40, 40, 70), (45, 40, 70)):
        f.circle(dx, dy, r, BRAIN, a)
    for (dx, dy, r) in ((-70, -20, 80), (0, -55, 85), (75, -20, 80), (-40, 40, 70), (45, 40, 70)):
        f.circle(dx, dy, r * 0.6, '#ffffff', a * 0.08)
    f.line([(0, -120), (0, 100)], DEEP, a * 0.5, 5)
    c.restore()


def gauge(f, x, y, w, level, a, label='douleur'):
    """Jauge horizontale de douleur (0..1)."""
    if a <= 0: return
    f.rect(x - w/2, y, w, 44, LINE, a, 22)
    col = RED if level > 0.5 else SPARK
    if level > 0.02: f.rect(x - w/2, y, w * level, 44, col, a, 22)
    f.text(label, x, y - 22, 36, MUTED, a, MONO, False)


def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')
    c = f.c

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.8, 30.2))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Le prix change la douleur ?', W/2, 296, 44, SPARK, ha)

    # S1 — accroche (0–4) : une gélule tombe et rebondit dès la première image
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        words(f, 'Une fausse pilule', 470, 92, 0.05, INK, t_out=o)
        words(f, 'soulage mieux', 590, 92, 0.6, INK, t_out=o)
        words(f, 'quand elle est chère.', 710, 84, 1.3, SPARK, t_out=o)
        p = seg(t, 0.0, 1.0)
        yb = 1150 - 420 * (1 - p) ** 2 if p < 1 else 1150 - 60 * abs(math.sin((t - 1.0) * 4)) * math.exp(-(t - 1.0) * 2)
        pill(f, W/2, yb, 1.5, fo, -0.25 + 0.5 * p)
        tag(f, W/2 + 230, 1330, '2,50 $', SPARK, fo * ease(seg(t, 1.8, 2.1)), bump(t, 1.8, 0.2))

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.0:
        o1 = 7.4
        g1 = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'Dedans :', 470, 90, 4.2, MUTED, t_out=o1)
            words(f, 'rien du tout.', 590, 100, 4.7, INK, t_out=o1)
            sp = ease_io(seg(t, 5.2, 6.0))
            pill(f, W/2, 1050, 1.6, g1, 0.0, PILL_B, sp)
            for k in range(14):
                ang = k * 2.4; r = 40 + 160 * sp * ((k % 5) / 5 + 0.2)
                f.rect(W/2 + r * math.cos(ang) - 7, 1050 + 140 * sp + r * 0.3 * math.sin(ang) - 7,
                       14, 14, '#ffffff', g1 * sp * 0.8, 3)
            f.text('du sucre, de l’amidon', W/2, 1340, 40, MUTED, g1 * ease(seg(t, 6.0, 6.3)), MONO, False)
        o2 = 10.7
        g2 = ease(seg(t, 7.6, 8.0)) * (1 - seg(t, o2, o2 + 0.3))
        if g2 > 0:
            words(f, 'Ton intuition :', 500, 72, 7.7, MUTED, t_out=o2)
            words(f, 'le prix ne change rien.', 620, 80, 8.1, INK, t_out=o2)
            wob = 0.06 * math.sin((t - 8) * 4)
            pill(f, W/2 - 220, 1060, 1.1, g2, wob)
            pill(f, W/2 + 220, 1060, 1.1, g2, -wob)
            f.text('=', W/2, 1090, 120, INK, g2 * ease(seg(t, 8.6, 8.9)), MONO, True)

    # S3 — la question (10.9–13.6)
    if 10.9 <= t < 13.6:
        words(f, 'Le prix peut-il', 820, 100, 11.0, INK, t_out=12.5)
        words(f, 'changer la douleur ?', 950, 96, 11.4, SPARK, t_out=12.5)

    # S4 — la preuve (13.5–30)
    if 13.4 <= t < 30.0:
        # A : l'expérience (13.6–21.3)
        oa = 21.3
        ga = ease(seg(t, 13.5, 13.9)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Expérience, 2008 :', 430, 76, 13.6, INK, t_out=oa)
            words(f, '82 volontaires.', 540, 76, 14.2, SPARK, t_out=oa)
            # petites décharges au poignet
            a1 = ga * ease(seg(t, 14.5, 14.8))
            fl = 0.6 + 0.4 * abs(math.sin(t * 9))
            bolt(f, W/2, 790, 1.4 * fl, a1)
            f.text('petites décharges au poignet', W/2, 930, 40, MUTED, a1, MONO, False)
            # deux groupes, même pilule, prix différents
            a2 = ga * ease(seg(t, 16.8, 17.1))
            pill(f, 290, 1140, 0.9, a2, -0.15)
            pill(f, 790, 1140, 0.9, a2, 0.15)
            tag(f, 290, 1290, '2,50 $', SPARK, ga * ease(seg(t, 17.6, 17.9)), bump(t, 17.6, 0.2))
            tag(f, 790, 1290, '0,10 $', MUTED, ga * ease(seg(t, 18.4, 18.7)), bump(t, 18.4, 0.2))
            f.text('Même pilule, sans rien dedans.', W/2, 1450, 46, INK, ga * ease(seg(t, 19.2, 19.5)))
        # B : qui a eu moins mal ? (21.5–29.6)
        gb = ease(seg(t, 21.5, 21.9)) * (1 - seg(t, 29.4, 29.8))
        if gb > 0:
            words(f, 'Qui a eu moins mal ?', 430, 80, 21.6, INK, t_out=29.4)
            p = ease_io(seg(t, 22.6, 27.0))
            base = 1290
            bar(f, 330, base, 230, 680, 0.85 * p, SPARK, gb, 'pilule à 2,50 $', f'{int(round(85 * p))}%')
            bar(f, 750, base, 230, 680, 0.61 * p, CAPITAL, gb, 'pilule à 0,10 $', f'{int(round(61 * p))}%')
            f.text('Waber, Shiv, Carmon, Ariely, JAMA 2008', W/2, 1480, 28, MUTED,
                   gb * 0.9 * ease(seg(t, 23.0, 23.3)), MONO, False)

    # S5 — la réponse (30–36)
    if 29.9 <= t < 36.0:
        o = 35.6
        a = ease(seg(t, 30.3, 30.6)) * (1 - seg(t, o, o + 0.3))
        big_center(f, '85%', 820, 260, SPARK, a, bump(t, 30.3, 0.18))
        words(f, 'ont moins mal', 1000, 84, 31.0, INK, t_out=o)
        words(f, 'avec la pilule « chère ».', 1110, 64, 31.6, INK, t_out=o)
        words(f, 'Soldée : 61 %.', 1290, 64, 33.0, MUTED, t_out=o)

    # S6 — le retournement (36–48.4)
    if 36.0 <= t < 48.4:
        words(f, 'Pourquoi ?', 900, 150, 36.1, SPARK, t_out=37.9)
        # A : le cerveau fabrique ses antidouleurs (38.1–42.6)
        oa = 42.6
        ga = ease(seg(t, 38.1, 38.5)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Ton cerveau fabrique', 440, 80, 38.2, INK, t_out=oa)
            words(f, 'ses propres antidouleurs.', 550, 70, 38.8, SPARK, t_out=oa)
            glow = 0.5 + 0.5 * math.sin((t - 38) * 4)
            brain(f, W/2, 820, 1.0, ga, glow)
            p = seg(t, 39.4, 42.4)
            for k in range(10):
                ph = (t * 0.9 + k / 10) % 1.0
                f.circle(W/2 - 120 + (k % 5) * 60, 960 + ph * 300, 14, SPARK, ga * p * (1 - ph))
            gauge(f, W/2, 1330, 640, 0.9 - 0.6 * ease(seg(t, 39.6, 42.0)), ga * ease(seg(t, 39.2, 39.5)))
            f.text('les endorphines', W/2, 1480, 40, MUTED, ga * ease(seg(t, 40.2, 40.5)), MONO, False)
        # B : bloque-les et la douleur revient (42.9–47.9)
        ob = 47.9
        gb = ease(seg(t, 42.8, 43.2)) * (1 - seg(t, ob, ob + 0.3))
        if gb > 0:
            words(f, 'Bloque-les avec un produit :', 440, 64, 42.9, INK, t_out=ob)
            words(f, 'la douleur revient.', 550, 80, 43.5, SPARK, t_out=ob)
            brain(f, W/2, 820, 1.0, gb)
            blk = ease(seg(t, 44.2, 44.6))
            for k in range(10):
                ph = (t * 0.9 + k / 10) % 1.0
                yy = 960 + ph * 300
                if blk > 0.5 and yy > 1080: continue
                f.circle(W/2 - 120 + (k % 5) * 60, yy, 14, SPARK, gb * (1 - ph))
            c.save(); c.translate(W/2, 1100); s = bump(t, 44.2, 0.2); c.scale(s, s)
            f.rect(-260, -18, 520, 36, RED, gb * blk, 18); c.restore()
            gauge(f, W/2, 1330, 640, 0.3 + 0.55 * ease(seg(t, 44.8, 46.4)), gb)
            f.text('naloxone, dents de sagesse, Lancet 1978', W/2, 1480, 30, MUTED,
                   gb * 0.9 * ease(seg(t, 45.0, 45.3)), MONO, False)

    # S7 — l'escalade (48–56.4) : même en le sachant
    if 48.0 <= t < 56.4:
        o = 55.9
        ga = ease(seg(t, 48.1, 48.4)) * (1 - seg(t, o, o + 0.3))
        if ga > 0:
            words(f, 'Même quand tu sais', 430, 80, 48.1, INK, t_out=o)
            words(f, 'que c’est du vent.', 540, 84, 48.7, SPARK, t_out=o)
            # flacon marqué PLACEBO
            a1 = ga * ease(seg(t, 49.3, 49.6))
            c.save(); c.translate(260, 960); s = bump(t, 49.3, 0.15); c.scale(s, s)
            f.rect(-90, -150, 180, 40, MUTED, a1, 8)
            f.rect(-110, -110, 220, 260, '#d9a35a', a1 * 0.85, 26)
            f.rect(-100, -40, 200, 90, PILL_A, a1, 8)
            f.text('PLACEBO', 0, 20, 38, DEEP, a1, MONO, True)
            c.restore()
            p = ease_io(seg(t, 50.4, 53.0))
            bar(f, 600, 1150, 170, 360, 0.59 * p, SPARK, ga * ease(seg(t, 50.2, 50.5)), 'placebo', f'{int(round(59 * p))}%')
            bar(f, 850, 1150, 170, 360, 0.35 * p, CAPITAL, ga * ease(seg(t, 50.2, 50.5)), 'rien', f'{int(round(35 * p))}%')
            f.text('se sentent soulagés (intestin irritable, Harvard 2010)', W/2, 1330, 28, MUTED,
                   ga * 0.9 * ease(seg(t, 51.0, 51.3)), MONO, False)
            f.text('Ça agit sur ce que tu ressens,', W/2, 1430, 44, INK, ga * ease(seg(t, 53.4, 53.7)))
            f.text('pas sur la maladie elle-même.', W/2, 1495, 44, INK, ga * ease(seg(t, 53.4, 53.7)))

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        a = ease(seg(t, 56.1, 56.4))
        pill(f, W/2, 660, 1.2 * bump(t, 56.1, 0.15), a, 0.08 * math.sin((t - 56) * 2))
        words(f, 'Une partie du remède', 900, 80, 56.3, INK)
        words(f, 'est dans ta tête.', 1020, 96, 57.6, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(240, 1160, 600, 150, OCEAN, a, 28)
        pa = 0.5 + 0.5 * math.sin((t - 60) * 3)
        f.rect(240, 1160, 600, 150, SPARK, a * 0.25 * pa, 28)
        f.text('Abonne-toi.', W/2, 1255, 62, INK, a)


def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    ev += [(0.15, pop(440, 0.09)), (1.8, ding(880, amp=0.18))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (12.5, 29.6, 47.9, 55.9)]
    ev += [(5.2, pop(520, 0.12)), (11.0, pop(520))]
    ev += [(17.6, clink(1500))]
    ev += [(22.8, rise(4.2, 300, 900, 0.07)), (27.0, ding(784, amp=0.2))]
    ev += [(30.3, ding(1046, amp=0.28)), (36.1, pop(300, 0.15))]
    ev += [(44.2, pop(300, 0.14))]
    ev += [(53.0, ding(784, amp=0.2))]
    ev += [(56.3, pop(440)), (60.0, ding(784, amp=0.22))]
    return ev
