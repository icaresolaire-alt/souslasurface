"""Le biais du survivant : les impacts de balles sur les avions revenus. Même structure que le pilote.

Sources :
- W. Allen Wallis, « The Statistical Research Group, 1942–1945 », JASA 1980 (cité par T. Taylor,
  Conversable Economist, 31 déc. 2020) : SRG basé à Columbia pendant la Seconde Guerre mondiale (Wald, Friedman,
  Savage...) ; l'armée était encline à protéger les parties qui montraient le plus d'impacts sur les avions revenus ;
  Wald suppose les impacts répartis uniformément ; manuscrit de 1943 « A Method of Estimating Plane Vulnerability
  Based on Damage of Survivors », publié en 1980.
- B. Casselman, « The Legend of Abraham Wald », AMS Feature Column, juin 2016 : SRG formé à l'été 1942 ;
  mémorandums de Wald vers 1943 sur la vulnérabilité des avions à partir des survivants ; les dialogues et les
  schémas d'impacts popularisés sont des reconstitutions (d'où « schéma simplifié » à l'écran, et aucun chiffre
  d'impacts inventé).
"""
import math, random, cairo
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro (ep018 -> guitare).
COVER = dict(tag='Psychologie', l1='Ces impacts de balles', l2='montrent le mauvais endroit')

METAL = '#5d7a8c'

def poly(f, pts, col, a):
    c = f.c; f.color(col, a)
    for i, (x, y) in enumerate(pts): (c.move_to if i == 0 else c.line_to)(x, y)
    c.close_path(); c.fill()

ENGINES = (-300, -150, 150, 300)

def plane(f, x, y, s, a, rot=0.0, eng_col=None):
    """Bombardier vu de dessus, nez vers le haut. Envergure ≈ 960 × s."""
    if a <= 0 or s <= 0: return
    c = f.c; c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    poly(f, [(-480, -10), (-60, -70), (60, -70), (480, -10), (470, 30), (60, 10), (-60, 10), (-470, 30)], METAL, a)
    poly(f, [(-190, 250), (-40, 220), (40, 220), (190, 250), (185, 285), (-185, 285)], METAL, a)
    f.rect(-45, -320, 90, 640, METAL, a, 45)
    f.rect(-28, -290, 56, 60, DEEP, a * 0.8, 20)   # cockpit
    ec = eng_col or '#7f98a8'
    for ex in ENGINES:
        f.rect(ex - 26, -140, 52, 150, ec, a, 24)
        f.rect(ex - 40, -150, 80, 10, INK, a * 0.5, 5)  # hélice
    c.restore()

def _holes():
    rnd = random.Random(18); pts = []
    while len(pts) < 70:
        z = rnd.random()
        if z < 0.55:   # ailes, hors moteurs
            x = rnd.uniform(-460, 460); y = rnd.uniform(-40, 15)
            if abs(x) < 70 or any(abs(x - e) < 45 for e in ENGINES): continue
            if y < -10 - 60 * (1 - abs(x) / 480): pass
        elif z < 0.85:  # fuselage, hors cockpit
            x = rnd.uniform(-30, 30); y = rnd.uniform(-180, 300)
        else:           # empennage
            x = rnd.uniform(-170, 170); y = rnd.uniform(235, 278)
        pts.append((x, y))
    return pts
HOLES = _holes()

def holes(f, x, y, s, a, n, rot=0.0):
    if a <= 0 or n <= 0: return
    c = f.c; c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    for i, (hx, hy) in enumerate(HOLES[:int(n)]):
        f.circle(hx, hy, 11, RED, a)
        f.circle(hx, hy, 5, DEEP, a)
    c.restore()

def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.8, 30.2))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Où faut-il blinder l’avion ?', W/2, 296, 46, SPARK, ha)

    # S1 — accroche (0–4) : l'avion arrive, les impacts surgissent
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        words(f, 'Ces impacts de balles', 470, 84, 0.15, INK, t_out=o)
        words(f, 'montrent', 580, 104, 0.6, INK, t_out=o)
        words(f, 'le mauvais endroit.', 700, 104, 1.0, SPARK, t_out=o)
        py = lerp(1700, 1150, ease(seg(t, 0.0, 1.4)))
        plane(f, W/2, py, 0.9, fo * ease(seg(t, 0.0, 0.3)))
        holes(f, W/2, py, 0.9, fo, 70 * seg(t, 1.2, 3.2))

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.0:
        words(f, 'Seconde Guerre mondiale.', 520, 76, 4.2, MUTED, t_out=6.7)
        words(f, 'Les bombardiers', 640, 92, 4.6, INK, t_out=6.7)
        words(f, 'rentrent criblés.', 750, 92, 5.0, RED, t_out=6.7)
        a = ease(seg(t, 4.4, 4.8)) * (1 - seg(t, 6.6, 6.9))
        px = lerp(-300, W/2, ease(seg(t, 4.4, 5.6)))
        plane(f, px, 1180, 0.62, a)
        holes(f, px, 1180, 0.62, a, 70)
        # le blindage pèse
        words(f, 'Le blindage est lourd.', 560, 80, 6.9, INK, t_out=8.8)
        words(f, 'Impossible de tout couvrir.', 680, 64, 7.4, SPARK, t_out=8.8)
        a = ease(seg(t, 7.0, 7.3)) * (1 - seg(t, 8.7, 9.0))
        sink = ease_io(seg(t, 7.6, 8.4))
        f.rect(340, 900 + sink * 120, 400, 160, METAL, a, 20)
        f.text('BLINDAGE', W/2, 1000 + sink * 120, 54, INK, a, MONO, True)
        f.line([(240, 1220), (840, 1220)], LINE, a, 8)
        f.text('= moins de bombes, moins d’essence', W/2, 1330, 40, MUTED, a * ease(seg(t, 7.9, 8.2)), MONO, False)
        a = ease(seg(t, 9.0, 9.3)) * (1 - seg(t, 10.6, 10.9))
        f.text('Ton intuition :', W/2, 700, 56, MUTED, a, bold=False)
        c = f.c; c.save(); c.translate(W/2, 860); s = bump(t, 9.0); c.scale(s, s)
        f.text('Blinder là où', 0, 0, 96, INK, a); f.text('il y a des trous.', 0, 110, 96, INK, a)
        c.restore()

    # S3 — la question (10.9–13.5)
    if 10.9 <= t < 13.6:
        words(f, 'Alors, où faut-il', 820, 100, 11.0, INK, t_out=12.5)
        words(f, 'blinder ?', 960, 120, 11.4, SPARK, t_out=12.5)

    # S4 — la preuve : on compte les impacts zone par zone (13.5–30)
    if 13.4 <= t < 30.0:
        ga = ease(seg(t, 13.5, 13.9)) * (1 - seg(t, 29.4, 29.8))
        words(f, 'On compte les impacts', 420, 70, 13.6, INK, t_out=19.4)
        words(f, 'sur les avions revenus.', 510, 70, 14.0, SPARK, t_out=19.4)
        PX, PY, S = W/2, 1020, 0.92
        hl = ease(seg(t, 21.6, 22.1))
        eng = SPARK if hl > 0.5 else None
        plane(f, PX, PY, S, ga, eng_col=eng)
        holes(f, PX, PY, S, ga, 70 * ease_io(seg(t, 14.6, 19.2)))
        # étiquettes de zones
        def tag(txt, x, y, t0, col=INK):
            a = ga * ease(seg(t, t0, t0 + 0.3))
            c = f.c; c.save(); c.translate(x, y); s = bump(t, t0, 0.12); c.scale(s, s)
            f.text(txt, 0, 0, 46, col, a, align='center'); c.restore()
        tag('Ailes : plein', 260, 1135, 19.6, RED)
        tag('Fuselage : plein', 820, 1135, 20.1, RED)
        tag('Queue : plein', 540, 1400, 20.6, RED)
        words(f, 'Et sur les moteurs ?', 440, 76, 19.6, INK, t_out=25.0)
        a = ga * ease(seg(t, 22.0, 22.3))
        c = f.c; c.save(); c.translate(W/2, 600); s = bump(t, 22.0, 0.16); c.scale(s, s)
        f.text('Presque rien.', 0, 0, 84, SPARK, a); c.restore()
        words(f, 'Les moteurs seraient solides ?', 440, 62, 25.2, INK, t_out=29.4)
        f.text('schéma simplifié', W/2, 1520, 28, MUTED, ga * 0.8, MONO, False)

    # S5 — la réponse (30–35.4)
    if 29.9 <= t < 35.4:
        o = 34.8
        words(f, 'Abraham Wald, 1943 :', 560, 66, 30.0, MUTED, t_out=o)
        a = ease(seg(t, 30.5, 30.8)) * (1 - seg(t, o, o + 0.3))
        c = f.c; c.save(); c.translate(W/2, 760); s = bump(t, 30.5, 0.16); c.scale(s, s)
        f.text('Blinder là où', 0, 0, 104, INK, a)
        f.text('il n’y a', 0, 140, 130, SPARK, a)
        f.text('PAS de trous.', 0, 290, 130, SPARK, a)
        c.restore()
        words(f, 'Statistical Research Group, Columbia', 1300, 32, 32.0, MUTED, t_out=o, font=MONO, bold=False)

    # S6 — le retournement : les avions touchés au moteur ne rentrent pas (35–48.4)
    if 35.0 <= t < 48.4:
        words(f, 'Pourquoi ?', 900, 140, 35.1, INK, t_out=37.1)
        ga = ease(seg(t, 37.3, 37.7)) * (1 - seg(t, 47.9, 48.3))
        if ga > 0 and t < 43.0:
            o = 42.6
            words(f, 'Touché au moteur ?', 440, 80, 37.4, INK, t_out=o)
            words(f, 'Il ne rentre pas.', 540, 80, 39.6, RED, t_out=o)
            fa = ga * (1 - seg(t, o, o + 0.3))
            f.line([(120, 680), (960, 680)], SPARK, fa * 0.7, 4, dash=[18, 14])
            f.text('BASE', 960, 660, 30, SPARK, fa, MONO, True, align='right')
            for i, x in enumerate((210, 430, 650, 870)):
                hit_engine = i in (1, 2)
                fly = ease_io(seg(t, 37.6 + i * 0.15, 41.6 + i * 0.15))
                if not hit_engine:
                    y = lerp(1450, 800, fly); rot = 0.0; aa = fa
                else:
                    yh = lerp(1450, 800, min(fly, 0.42))
                    fall = seg(t, 39.2 + i * 0.15, 41.4 + i * 0.15)
                    y = yh + 500 * fall * fall; rot = (1 if i == 1 else -1) * 1.4 * fall
                    aa = fa * (1 - fall)
                plane(f, x, y, 0.2, aa, rot, eng_col=RED if hit_engine and t > 38.9 + i * 0.15 else None)
                holes(f, x, y, 0.2, aa, 30 if not hit_engine else 0, rot)
                if hit_engine:
                    fl = seg(t, 38.9 + i * 0.15, 39.3 + i * 0.15)
                    if 0 < fl < 1: f.circle(x, y - 10, 40 + 60 * fl, SPARK, fa * (1 - fl) * 0.8)
        if t >= 42.6:
            words(f, 'Tu n’as vu', 560, 92, 42.9, INK, t_out=47.9)
            words(f, 'que les survivants.', 670, 92, 43.3, SPARK, t_out=47.9)
            a = ease(seg(t, 44.8, 45.1)) * (1 - seg(t, 47.9, 48.3))
            c = f.c; c.save(); c.translate(W/2, 960); s = bump(t, 44.8, 0.14); c.scale(s, s)
            f.rect(-420, -80, 840, 220, OCEAN, a, 32)
            f.text('Le biais', 0, -5, 76, INK, a)
            f.text('du survivant.', 0, 95, 76, SPARK, a)
            c.restore()

    # S7 — l'escalade : le biais est partout (48–56.4)
    if 48.0 <= t < 56.4:
        words(f, '« Avant, on construisait', 450, 66, 48.1, INK, t_out=51.9)
        words(f, 'plus solide. »', 540, 66, 48.6, INK, t_out=51.9)
        a = ease(seg(t, 48.4, 48.7)) * (1 - seg(t, 51.8, 52.1))
        for i, (x, h) in enumerate(((200, 330), (360, 280), (540, 380), (720, 300), (880, 350))):
            standing = i in (0, 2, 4)
            if standing:
                f.rect(x - 65, 1300 - h, 130, h, METAL, a, 6)
                for r in range(int(h // 70)):
                    f.rect(x - 40, 1300 - h + 25 + r * 70, 25, 32, SPARK, a * 0.6, 3)
                    f.rect(x + 15, 1300 - h + 25 + r * 70, 25, 32, SPARK, a * 0.6, 3)
            else:
                gone = ease(seg(t, 49.4, 50.2))
                f.rect(x - 65, 1300 - h, 130, h, LINE, a * (1 - gone) + a * 0.25 * gone, 6)
                f.line([(x - 65, 1300 - h), (x + 65, 1300 - h), (x + 65, 1300), (x - 65, 1300), (x - 65, 1300 - h)],
                       MUTED, a * gone, 3, dash=[12, 10])
        f.line([(120, 1300), (960, 1300)], MUTED, a, 4)
        a2 = ease(seg(t, 50.2, 50.5)) * (1 - seg(t, 51.8, 52.1))
        f.text('Les fragiles sont tombés.', W/2, 1420, 56, SPARK, a2)
        # les réussites qu'on raconte
        words(f, 'Le milliardaire sans diplôme ?', 450, 62, 52.2, INK, t_out=55.9)
        a = ease(seg(t, 52.4, 52.7)) * (1 - seg(t, 55.9, 56.3))
        for k in range(40):
            cx = 190 + (k % 8) * 100; cy = 720 + (k // 8) * 120
            win = k == 19
            fade = 1 if win else 1 - 0.8 * ease(seg(t, 53.4, 54.2))
            col = SPARK if win else INK
            f.circle(cx, cy - 22, 18, col, a * fade)
            f.rect(cx - 26, cy, 52, 46, col, a * fade, 20)
        a3 = ease(seg(t, 54.0, 54.3)) * (1 - seg(t, 55.9, 56.3))
        f.text('Ceux qui ont échoué', W/2, 1400, 58, INK, a3)
        f.text('ne font pas de livres.', W/2, 1475, 58, SPARK, a3)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        a = ease(seg(t, 56.1, 56.4))
        c = f.c; c.save(); c.translate(W/2, 600); s = bump(t, 56.1, 0.12); c.scale(s, s)
        f.circle(0, 0, 110, SPARK, a, stroke=18)
        f.text('?', 0, 50, 150, SPARK, a); c.restore()
        words(f, 'Avant d’écouter les gagnants,', 840, 64, 56.3, INK)
        words(f, 'demande-toi qui manque.', 940, 76, 57.6, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(240, 1060, 600, 150, OCEAN, a, 28)
        pa = 0.5 + 0.5 * math.sin((t - 60) * 3)
        f.rect(240, 1060, 600, 150, SPARK, a * 0.25 * pa, 28)
        f.text('Abonne-toi.', W/2, 1155, 62, INK, a)

def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    ev += [(0.15, pop(440, 0.09)), (1.3, clink(1900))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (12.5, 29.6, 47.9, 55.9)]
    ev += [(11.0, pop(520))]
    ev += [(22.0, ding(784, amp=0.2))]
    ev += [(30.5, ding(1046, amp=0.28)), (35.1, pop(300, 0.15))]
    ev += [(39.2, pop(220, 0.12)), (44.8, ding(988, amp=0.24))]
    ev += [(56.3, pop(440)), (60.0, ding(784, amp=0.22))]
    return ev
