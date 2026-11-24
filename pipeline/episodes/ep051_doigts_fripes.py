"""Pourquoi tes doigts fripent dans l'eau. Même structure que le pilote.

Sources :
- Haseleu et al., « Water-induced finger wrinkles do not affect touch acuity or dexterity in handling
  wet objects », PLOS ONE 9(1) e84949, 2014 (MDC Berlin) : « In the 1930s, Lewis and Pickering first
  described the absence of wrinkling in patients with median nerve palsy » ; « the wrinkling test as a
  bedside test of sympathetic nerve function » ; « water-induced skin wrinkling is directly linked to
  vasoconstriction » (Wilder-Smith et Chow) ; peau glabre des doigts, paumes et plantes ; protocole
  30 min dans l'eau à 40 °C ; conclusion : « no significant impact on tactile driven performance or
  dexterity in handling wet or dry objects ». Communiqué MDC du 9 janv. 2014 : 40 volontaires,
  « no advantage to get a better grip of wet or dry objects ».
- NPR, 29 juin 2011 : on sait « since the mid-1930s » que les rides ne se forment pas si les nerfs du
  doigt sont coupés ; hypothèse de Mark Changizi (Brain, Behavior and Evolution, 2011) : des rainures
  comme des pneus pluie, qui évacuent l'eau.
- Scientific American / Nature, 9 janv. 2013 : rides causées par la contraction des vaisseaux sous la
  peau, pas par l'eau qui fait gonfler la peau ; absentes en cas de lésion nerveuse (années 1930).
- Université de Newcastle, communiqué du 9 janv. 2013, et Live Science (C. Q. Choi) : Kareklas, Nettle,
  Smulders, Biology Letters 2013 ; 20 volontaires, 30 min dans l'eau chaude, « 12% faster with the wet
  marbles if their fingers were wrinkled », aucune différence pour les objets secs ; « an active
  process » contrôlé par le système nerveux autonome.
- The Conversation (« Curious Kids ») : plus de 5 min environ, plus vite si l'eau est chaude ; la
  raison n'est pas tranchée. Pas de chiffre de délai affiché à l'écran (une seule source).
"""
import math
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro (ep050 précédent).
COVER = dict(tag='Science', l1='Pourquoi tes doigts', l2='fripent dans l’eau')

SKIN = '#c99272'
SKIN_D = '#a8735a'
NAIL = '#e8c9b4'
WATER = '#1d5a7a'
FOAM = '#eaf1ec'


def finger(f, cx, top, w, h, a, wr=0.0, vessel=None, nail=False):
    """Doigt vu côté pulpe, bout en bas (il trempe). wr = rides (0..1), vessel = largeur des vaisseaux (0..1)."""
    if a <= 0: return
    f.rect(cx - w / 2, top, w, h, SKIN, a, w / 2)
    bot = top + h
    if vessel is not None:
        vw = lerp(4, 16, vessel)
        for dx in (-w * 0.2, w * 0.2):
            pts = [(cx + dx + 10 * math.sin(k * 0.6 + dx), top + w * 0.3 + k * 18) for k in range(int((h - w * 0.55) / 18))]
            f.line(pts, RED, a * 0.85, vw)
    # pli de la phalange
    f.line([(cx - w * 0.3, bot - w * 1.55), (cx + w * 0.3, bot - w * 1.55)], SKIN_D, a * 0.6, 4)
    if wr > 0:
        # rides longitudinales sur la pulpe du bout du doigt
        for i in range(-3, 4):
            x0 = cx + i * w * 0.11
            span = w * (1.15 - 0.05 * abs(i) ** 2)
            pts = []
            for k in range(22):
                y = bot - w * 0.12 - span + k * (span / 21)
                pts.append((x0 + 8 * wr * math.sin(k * 0.9 + i), y))
            f.line(pts, SKIN_D, a * wr, 5)


def water(f, y, a, t, x0=120, x1=960, y1=1500):
    if a <= 0: return
    pts = [(x, y + 8 * math.sin(x * 0.025 - t * 2.5)) for x in range(x0, x1 + 1, 10)]
    c = f.c; f.color(WATER, a * 0.5)
    for i, (x, yy) in enumerate(pts):
        (c.move_to if i == 0 else c.line_to)(x, yy)
    c.line_to(x1, y1); c.line_to(x0, y1); c.close_path(); c.fill()
    f.line(pts, FOAM, a * 0.6, 4)


def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')

    # question persistante
    ha = ease(seg(t, 12.8, 13.3)) * (1 - seg(t, 29.8, 30.2))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Qui plisse tes doigts ?', W/2, 296, 46, SPARK, ha)

    # S1 — accroche (0–4) : un doigt plonge et se ride dès la première image
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        words(f, 'Ce n’est pas l’eau', 440, 80, 0.05, INK, t_out=o)
        words(f, 'qui fripe tes doigts.', 550, 80, 0.6, SPARK, t_out=o)
        u = ease_io(seg(t, 0, 2.0))
        finger(f, W/2, lerp(620, 800, u), 200, 600, fo, wr=ease(seg(t, 1.8, 3.6)))
        water(f, 1180, fo, t)

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.2:
        o1 = 7.6
        g1 = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'On croit que la peau', 440, 76, 4.2, INK, t_out=o1)
            words(f, 'boit l’eau et gonfle.', 550, 76, 4.9, SPARK, t_out=o1)
            # éponge qui gonfle
            s = 1 + 0.25 * ease_io(seg(t, 5.2, 7.2))
            f.rect(W/2 - 170 * s, 1050 - 110 * s, 340 * s, 220 * s, SPARK, g1 * 0.85, 30)
            for i in range(9):
                f.circle(W/2 - 110 * s + (i % 3) * 110 * s, 990 - 0 * s + (i // 3) * 60 * s, 14 * s, OCEAN, g1 * 0.6)
            f.text('comme une éponge', W/2, 1330, 44, MUTED, g1 * ease(seg(t, 5.8, 6.1)), DISPLAY, True)
        o2 = 10.9
        g2 = ease(seg(t, 7.8, 8.2)) * (1 - seg(t, o2, o2 + 0.3))
        if g2 > 0:
            words(f, 'Une éponge gonflée', 440, 80, 7.9, INK, t_out=o2)
            words(f, 'reste lisse.', 550, 80, 8.5, RED, t_out=o2)
            f.rect(W/2 - 210, 940, 420, 270, SPARK, g2 * 0.85, 34)
            f.text('lisse', W/2, 1090, 60, OCEAN, g2, DISPLAY, True)
            p = ease(seg(t, 9.2, 9.6))
            f.text('Ton doigt, lui, se ride.', W/2, 1340, 52, INK, g2 * p, DISPLAY, True)

    # S3 — la question (11–13.8)
    if 11.0 <= t < 13.8:
        words(f, 'Alors qui', 820, 120, 11.1, INK, t_out=12.7)
        words(f, 'les plisse ?', 950, 120, 11.5, SPARK, t_out=12.7)

    # S4 — la preuve (13.6–30)
    if 13.5 <= t < 30.0:
        # A : nerf coupé = doigt lisse (13.7–21.6)
        oa = 21.6
        ga = ease(seg(t, 13.6, 14.0)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Indice : un doigt', 430, 72, 13.7, INK, t_out=oa)
            words(f, 'au nerf abîmé reste lisse.', 530, 64, 14.4, SPARK, t_out=oa)
            wr = ease(seg(t, 16.0, 18.6))
            finger(f, 340, 760, 180, 560, ga, wr=wr)
            finger(f, 740, 760, 180, 560, ga, wr=0.0)
            water(f, 1120, ga, t, y1=1360)
            # nerf : trait doré coupé
            na = ga * ease(seg(t, 15.0, 15.4))
            f.line([(340, 690), (340, 1200)], SPARK, na, 6)
            f.line([(740, 690), (740, 900)], SPARK, na, 6)
            f.line([(740, 950), (740, 1200)], SPARK, na * 0.4, 6, dash=[8, 10])
            f.line([(715, 910), (765, 940)], RED, na, 8)
            f.line([(715, 940), (765, 910)], RED, na, 8)
            f.text('nerf intact', 340, 1420, 38, INK, na, DISPLAY, True)
            f.text('nerf abîmé', 740, 1420, 38, RED, na, DISPLAY, True)
            f.text('observé dès les années 1930', W/2, 1510, 36, MUTED,
                   ga * ease(seg(t, 18.4, 18.7)), DISPLAY, True)
        # B : les vaisseaux se serrent (21.8–29.6)
        ob = 29.4
        gb = ease(seg(t, 21.7, 22.1)) * (1 - seg(t, ob, ob + 0.3))
        if gb > 0:
            words(f, 'Le nerf donne un ordre :', 430, 70, 21.8, INK, t_out=ob)
            words(f, 'les vaisseaux se serrent.', 540, 70, 22.5, SPARK, t_out=ob)
            u = ease_io(seg(t, 23.6, 27.0))
            wbody = lerp(220, 196, u)
            finger(f, W/2, 720, wbody, 640, gb, wr=ease(seg(t, 25.0, 28.0)), vessel=1 - u, nail=False)
            ya = 1440
            f.text('le bout du doigt dégonfle', W/2, ya, 44, MUTED, gb * ease(seg(t, 24.6, 24.9)), DISPLAY, True)
            f.text('la peau se plisse', W/2, ya + 64, 48, SPARK,
                   gb * ease(seg(t, 26.6, 26.9)) * bump(t, 26.6, 0.1), DISPLAY, True)

    # S5 — la réponse (30–36)
    if 29.9 <= t < 36.0:
        o = 35.6
        a = ease(seg(t, 30.3, 30.6)) * (1 - seg(t, o, o + 0.3))
        words(f, 'Ce qui plisse tes doigts,', 560, 68, 30.0, MUTED, t_out=o)
        big_center(f, 'tes nerfs', 860, 200, SPARK, a, bump(t, 30.6, 0.18), font=DISPLAY)
        f.rect(150, 1040, 780, 230, OCEAN, a * ease(seg(t, 32.2, 32.5)) * 0.9, 28)
        words(f, 'Les médecins s’en servent', 1130, 54, 32.4, INK, t_out=o)
        words(f, 'pour tester les nerfs.', 1210, 54, 32.9, SPARK, t_out=o)
        f.text('Haseleu et al., PLOS ONE 2014', W/2, 1360, 32, MUTED, a * ease(seg(t, 33.6, 33.9)), MONO, False)

    # S6 — le retournement (36–48.4) : des pneus pluie ?
    if 36.0 <= t < 48.4:
        words(f, 'Pourquoi ?', 900, 130, 36.1, SPARK, t_out=37.9)
        oa = 43.2
        ga = ease(seg(t, 38.1, 38.5)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Une idée : des pneus pluie.', 430, 66, 38.2, INK, t_out=oa)
            words(f, 'Les rides évacuent l’eau.', 530, 66, 38.9, SPARK, t_out=oa)
            # pneu vu de face avec rainures, gouttes chassées
            cx, cy = W/2, 1040
            f.rect(cx - 170, cy - 260, 340, 520, '#2a2f36', ga, 60)
            for i in range(-2, 3):
                pts = [(cx + i * 60 + 14 * math.sin(k * 0.8), cy - 240 + k * 24) for k in range(21)]
                f.line(pts, DEEP, ga, 12)
            for i in range(10):
                p = seg(t, 39.6 + 0.25 * i, 40.8 + 0.25 * i)
                if 0 < p < 1:
                    side = -1 if i % 2 else 1
                    f.circle(cx + side * (60 + 260 * p), cy + 180 - 60 * p + 40 * math.sin(i), 14 * (1 - 0.4 * p),
                             FOAM, ga * (1 - p))
            f.text('Mark Changizi, 2011', W/2, 1420, 34, MUTED, ga * ease(seg(t, 40.4, 40.7)), MONO, False)
        ob = 47.9
        gb = ease(seg(t, 43.4, 43.8)) * (1 - seg(t, ob, ob + 0.3))
        if gb > 0:
            words(f, 'Test : des billes mouillées.', 430, 66, 43.5, INK, t_out=ob)
            words(f, 'Doigts fripés :', 530, 66, 44.1, INK, t_out=ob)
            big_center(f, '12 % plus vite', 820, 130, SPARK, gb * ease(seg(t, 44.6, 44.9)), bump(t, 44.6, 0.16), font=DISPLAY)
            # billes qui passent d'un bol à l'autre
            for i in range(6):
                p = ease_io(seg(t, 45.0 + 0.35 * i, 45.8 + 0.35 * i))
                x = lerp(300, 780, p); y = 1120 - 160 * math.sin(math.pi * p)
                f.circle(x, y, 26, '#7fb7d6', gb * 0.95)
            f.rect(200, 1150, 200, 60, OCEAN, gb, 20)
            f.rect(680, 1150, 200, 60, OCEAN, gb, 20)
            f.text('objets secs : aucune différence', W/2, 1330, 42, MUTED,
                   gb * ease(seg(t, 46.0, 46.3)), DISPLAY, True)
            f.text('Newcastle, 2013 · 20 volontaires', W/2, 1420, 32, MUTED,
                   gb * ease(seg(t, 46.4, 46.7)), MONO, False)

    # S7 — l'escalade (48–56.4) : la contre-étude
    if 48.0 <= t < 56.4:
        o1 = 55.9
        g1 = ease(seg(t, 48.1, 48.4)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'Mais en 2014,', 430, 76, 48.1, INK, t_out=o1)
            words(f, '40 volontaires refont le test.', 530, 60, 48.7, SPARK, t_out=o1)
            # deux barres qui montent : lisses vs fripés, identiques
            p = ease_io(seg(t, 49.6, 51.8))
            base = 1300
            for x, lab in ((360, 'lisses'), (720, 'fripés')):
                hgt = 420 * p
                f.rect(x - 90, base - hgt, 180, hgt, SPARK if lab == 'fripés' else INK, g1 * 0.9, 16)
                f.text(lab, x, base + 60, 42, INK, g1, DISPLAY, True)
            f.text('=', W/2, base - 180, 110, SPARK, g1 * ease(seg(t, 51.8, 52.1)), DISPLAY, True)
            f.text('aucune différence', W/2, 1440, 50, INK, g1 * ease(seg(t, 52.2, 52.5)), DISPLAY, True)
            f.text('Le débat reste ouvert.', W/2, 1520, 44, SPARK,
                   g1 * ease(seg(t, 53.4, 53.7)) * bump(t, 53.4, 0.1), DISPLAY, True)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        a = ease(seg(t, 56.1, 56.4))
        finger(f, W/2, 470, 170, 540, a, wr=ease(seg(t, 56.4, 58.6)))
        water(f, 900, a, t, y1=1080)
        words(f, 'Tes doigts ne prennent pas l’eau.', 1180, 52, 56.3, INK)
        words(f, 'Ils obéissent à tes nerfs.', 1260, 64, 57.8, SPARK)
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
    ev += [(30.6, ding(1046, amp=0.28)), (36.1, pop(300, 0.15))]
    ev += [(44.6, clink())]
    ev += [(56.3, pop(440)), (60.0, ding(784, amp=0.22))]
    return ev
