"""Vrai ou faux : 4 choses que tout le monde croit (téléphone, loterie, diamants, plastique)."""
import math, sys
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
COVER = dict(tag='Vrai ou faux', l1='4 choses que tout', l2='le monde croit')

# (début, fin) de chaque affirmation dans le temps du script
BLOCKS = [(5.0, 19.0), (19.0, 33.0), (33.0, 47.0), (47.0, 58.0)]
VERDICTS = [('PAS PROUVÉ', MUTED), ('VRAI', EARTH), ('PLUTÔT VRAI', EARTH), ('FAUX', RED)]
STAMP_AT = [13.4, 26.0, 41.5, 53.0]

def stamp(f, text, col, x, y, t, t0, size=88):
    p = seg(t, t0, t0 + 0.35)
    if p <= 0: return
    c = f.c; c.save(); c.translate(x, y); c.rotate(-0.12)
    s = lerp(1.6, 1.0, ease(p)); c.scale(s, s)
    w = f.width(text, size) + 70
    f.rect(-w / 2, -size * 0.78, w, size * 1.3, DEEP, 0.92 * ease(p), 8)
    c.set_line_width(10); f.color(col, ease(p)); c.rectangle(-w / 2, -size * 0.78, w, size * 1.3); c.stroke()
    f.text(text, 0, size * 0.32, size, col, ease(p))
    c.restore()

def claim(f, text, t, a0, a1):
    """L'affirmation entre guillemets, en haut, pendant tout le bloc."""
    a = ease(seg(t, a0, a0 + 0.4)) * (1 - seg(t, a1 - 0.4, a1))
    if a <= 0: return
    f.rect(70, 300, 940, 210, OCEAN, a * 0.95, 28)
    f.text('ON DIT QUE…', W / 2, 352, 30, SPARK, a, MONO, True)
    f.wrap('« ' + text + ' »', W / 2, 420, 46, 860, INK, a)

def scoreboard(f, t):
    """Les verdicts déjà rendus, en petites pastilles sous le bandeau."""
    a = ease(seg(t, 5.0, 5.5)) * (1 - seg(t, 57.6, 58.0))
    if a <= 0: return
    for i in range(4):
        x = W / 2 + (i - 1.5) * 120; y = 245
        done = t >= STAMP_AT[i] + 0.3
        col = VERDICTS[i][1] if done else LINE
        f.circle(x, y, 22, col, a)
        f.text(str(i + 1), x, y, 24, DEEP if done else MUTED, a, MONO, True, 'center', 'middle')

def phone(f, x, y, a):
    c = f.c; w, h = 300, 560
    f.color(INK, a); c.set_line_width(10)
    r = 46; x0, y0 = x - w / 2, y - h / 2
    c.new_sub_path()
    c.arc(x0 + w - r, y0 + r, r, -math.pi / 2, 0); c.arc(x0 + w - r, y0 + h - r, r, 0, math.pi / 2)
    c.arc(x0 + r, y0 + h - r, r, math.pi / 2, math.pi); c.arc(x0 + r, y0 + r, r, math.pi, 1.5 * math.pi)
    c.close_path(); c.stroke()
    f.rect(x - 50, y0 + 22, 100, 14, INK, a, 7)

def mic(f, x, y, col, a, s=1.0):
    f.rect(x - 22 * s, y - 50 * s, 44 * s, 76 * s, col, a, 22 * s)
    f.color(col, a); f.c.set_line_width(7 * s)
    f.c.new_sub_path(); f.c.arc(x, y - 4 * s, 40 * s, 0.15, math.pi - 0.15); f.c.stroke()
    f.line([(x, y + 36 * s), (x, y + 58 * s)], col, a, 7 * s)

def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')
    scoreboard(f, t)

    # ---------- Accroche (0–5)
    if t < 5.3:
        o = 4.8
        words(f, '4 choses que', 640, 96, 0.1, INK, t_out=o)
        words(f, 'tout le monde croit.', 760, 96, 0.5, INK, t_out=o)
        a = ease(seg(t, 1.8, 2.2)) * (1 - seg(t, o, o + 0.3))
        flip = int(t * 2.2) % 2 == 0
        big_center(f, 'VRAI ?' if flip else 'FAUX ?', 1040, 150, EARTH if flip else RED, a, 1.0, DISPLAY)
        words(f, 'On vérifie.', 1260, 70, 3.2, SPARK, t_out=o)

    # ---------- 1. Le téléphone (5–19)
    a0, a1 = BLOCKS[0]
    if a0 <= t < a1:
        claim(f, 'Ton téléphone écoute tes conversations pour te cibler en pub.', t, a0, a1)
        a = ease(seg(t, 5.6, 6.0)) * (1 - seg(t, a1 - 0.4, a1))
        phone(f, W / 2, 880, a)
        pulse = 0.5 + 0.5 * math.sin(t * 6)
        on = t < 9.5
        mic(f, W / 2, 880, RED if on else MUTED, a)
        if on:
            for k in range(3):
                f.circle(W / 2, 870, 80 + 40 * k + 20 * pulse, RED, a * (0.35 - 0.1 * k), 4)
        if t >= 9.5:
            f.line([(W / 2 - 90, 790), (W / 2 + 90, 970)], RED, a * ease(seg(t, 9.5, 9.8)), 12)
        words(f, 'Plus de 17 000 applis testées :', 1250, 46, 8.0, INK, t_out=a1 - 0.4, bold=False)
        words(f, 'aucune n’allumait le micro en cachette.', 1320, 46, 8.8, INK, t_out=a1 - 0.4)
        words(f, 'Mais tes clics en disent déjà assez.', 1420, 44, 15.2, SPARK, t_out=a1 - 0.4)
        stamp(f, *VERDICTS[0], W / 2, 1110, t, STAMP_AT[0], 76)
        f.text('Northeastern University, 2018 (Android)', W / 2, 1530, 26, MUTED, a * seg(t, 8.5, 9), bold=False)

    # ---------- 2. La loterie (19–33)
    a0, a1 = BLOCKS[1]
    if a0 <= t < a1:
        claim(f, 'Au Loto, on te rend à peine la moitié de ta mise.', t, a0, a1)
        a = ease(seg(t, 19.6, 20.0)) * (1 - seg(t, a1 - 0.4, a1))
        n_back = int(54 * ease_io(seg(t, 21.0, 24.0)))
        for i in range(100):
            r, col_ = divmod(i, 10)
            x = W / 2 + (col_ - 4.5) * 74; y = 640 + r * 62
            back = i < n_back
            f.circle(x, y, 26, SPARK if back else LINE, a)
        f.text('100 € misés', W / 2, 590, 40, MUTED, a, bold=False)
        big_center(f, f'{n_back} €', 1340, 120, SPARK, a, bump(t, 24.0, 0.15))
        words(f, 'reviennent aux joueurs, en moyenne.', 1420, 44, 24.4, INK, t_out=a1 - 0.4)
        stamp(f, *VERDICTS[1], W / 2, 980, t, STAMP_AT[1])
        words(f, 'La loi impose entre 50 et 60 %.', 1500, 40, 28.0, MUTED, t_out=a1 - 0.4, bold=False)
        f.text('Taux Loto FDJ : 54,35 % depuis mai 2026', W / 2, 1560, 26, MUTED, a * seg(t, 24.5, 25), bold=False)

    # ---------- 3. Les diamants (33–47)
    a0, a1 = BLOCKS[2]
    if a0 <= t < a1:
        claim(f, 'Les diamants sont chers parce qu’ils sont rares.', t, a0, a1)
        a = ease(seg(t, 33.6, 34.0)) * (1 - seg(t, a1 - 0.4, a1))
        cx, cy, R = W / 2, 860, 230
        p = 0.8 * ease_io(seg(t, 34.5, 36.5))
        f.circle(cx, cy, R, LINE, a)
        if p > 0:
            f.color(SPARK, a); f.c.move_to(cx, cy)
            f.c.arc(cx, cy, R, -math.pi / 2, -math.pi / 2 + 2 * math.pi * p); f.c.close_path(); f.c.fill()
        big_center(f, f'{int(round(p * 100))} %', cy + 30, 96, DEEP if p > 0.3 else INK, a)
        words(f, 'Une seule entreprise, De Beers,', 1180, 46, 36.6, INK, t_out=a1 - 0.4)
        words(f, 'contrôlait près de 80 % des diamants bruts.', 1250, 44, 37.4, INK, t_out=a1 - 0.4, bold=False)
        words(f, '1947 : « A diamond is forever ».', 1360, 50, 39.6, SPARK, t_out=a1 - 0.4)
        words(f, 'Un slogan publicitaire.', 1430, 44, 40.4, INK, t_out=a1 - 0.4, bold=False)
        stamp(f, *VERDICTS[2], W / 2, 1530, t, STAMP_AT[2], 64)
        f.text('Rareté organisée au XXe siècle (Stern NYU, cas De Beers)', W / 2, 600, 26, MUTED, a * seg(t, 36.6, 37), bold=False)

    # ---------- 4. Le plastique (47–58)
    a0, a1 = BLOCKS[3]
    if a0 <= t < a1:
        claim(f, 'Le plastique que tu tries est recyclé.', t, a0, a1)
        a = ease(seg(t, 47.6, 48.0)) * (1 - seg(t, a1 - 0.4, a1))
        n_rec = int(9 * ease_io(seg(t, 49.0, 50.5)))
        for i in range(100):
            r, col_ = divmod(i, 10)
            x = W / 2 + (col_ - 4.5) * 74; y = 620 + r * 64
            col = SPARK if i < n_rec else LINE
            f.rect(x - 14, y - 18, 28, 44, col, a, 6); f.rect(x - 6, y - 30, 12, 14, col, a, 3)
        big_center(f, f'{n_rec} %', 1330, 120, SPARK, a, bump(t, 50.5, 0.15))
        words(f, 'du plastique est recyclé dans le monde.', 1410, 44, 50.8, INK, t_out=a1 - 0.4)
        words(f, 'Le reste : décharge, incinération, nature.', 1480, 40, 51.8, MUTED, t_out=a1 - 0.4, bold=False)
        stamp(f, *VERDICTS[3], W / 2, 960, t, STAMP_AT[3])
        f.text('OCDE, Global Plastics Outlook 2022', W / 2, 1560, 26, MUTED, a * seg(t, 51, 51.5), bold=False)

    # ---------- Chute (58–66)
    if t >= 58.0:
        words(f, 'Une phrase choc', 720, 76, 58.2)
        words(f, 'n’est pas une preuve.', 830, 76, 58.8, SPARK)
        a = ease(seg(t, 61.0, 61.4))
        f.rect(240, 1000, 600, 150, OCEAN, a, 28)
        f.text('Abonne-toi.', W / 2, 1095, 62, INK, a)

def sfx_events():
    from sound import pop, ding, whoosh
    ev = [(0.1, pop(440)), (1.8, pop(520))]
    for (b0, _b1), st in zip(BLOCKS, STAMP_AT):
        ev += [(b0, whoosh(0.5, 0.15)), (st, ding(784, amp=0.25))]
    ev += [(24.0, pop(600)), (50.5, pop(600)), (58.2, whoosh(0.5, 0.15)), (61.0, ding(659, amp=0.2))]
    return ev
