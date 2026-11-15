"""Pourquoi tant de navires ont le ventre rouge (peinture antisalissure au cuivre). Même structure que le pilote.

Sources :
- Jalopnik, A. P. Collins, 13 août 2019, « Why So Many Ships Are Red On The Bottom » : à l'époque de la voile,
  revêtement de cuivre ou peinture au plomb contenant des oxydes de cuivre comme biocide ; « That copper in the
  paint gave it its red color » ; « Pretty much any color can be used » ; « red is still popular for the sake
  of tradition ».
- Mental Floss, J. Rossen, 9 sept. 2019 : « The reason is tradition. And worms. » ; « biocides can be mixed with
  virtually any color of paint ».
- SlashGear, 30 août 2025 : l'oxyde de cuivre de la peinture antisalissure est « typically red » ; des peintures
  non rouges existent.
- US Navy, navy.mil, 13 oct. 2016 (ONR, « Barnacle-busting ») : la Navy utilise des peintures au cuivre contre
  les balanes ; elles s'accumulent vite, surtout au port.
- Wikipedia « Copper sheathing » : protection contre le taret (shipworm), les balanes et les algues ; HMS Alarm,
  frégate de 32 canons, entièrement doublée de cuivre en 1761 ; « the Royal Navy set about coppering the bottoms
  of the entire fleet in 1778 ». Concordant : copper.org « Royal Navy Fleet First to Use Copper » (Discover
  Copper, oct. 2004 : « The first wooden ship to be fully sheathed in copper was ... HMS Alarm, in 1761 »),
  Wikipedia « HMS Alarm (1758) » et Soundings, oct. 2025 (« started coppering the entire fleet in 1778 »).
- Schultz, Bendick, Holm et Hertel, « Economic impact of biofouling on a naval surface ship », Biofouling 27(1),
  2011, p. 87-98 (usna.edu) : destroyers classe DDG-51 ; film de vase épais sans coquillages (FR-30) : +10,3 % de
  carburant ; petits organismes durs (FR-60) : +20,4 % ; coût total estimé 56 M$ par an pour toute la classe
  (1 Md$ sur 15 ans), surtout du carburant dû au frottement. Une seule étude (chiffres attribués à l'écran).
- Le taret affiché schématiquement ; organismes et jauge illustratifs (seuls les pourcentages sont chiffrés).
"""
import math
import random
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro (ep041 précédent).
COVER = dict(tag='Mer', l1='Pourquoi tant de navires', l2='ont le ventre rouge')

WATER = '#1f5f7a'
HULL = '#2c4352'
ANTI = '#a8473a'
COPPER = '#c8794a'
SLIME = '#5f8f5a'
SHELL = '#d9d2c0'


def water(f, y, a, t, x0=0, x1=W, y1=1600, col=WATER, amp=8):
    if a <= 0: return
    c = f.c; f.color(col, a * 0.85)
    c.move_to(x0, y1)
    n = 40
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        c.line_to(x, y + amp * math.sin(x / 70 + t * 2.4))
    c.line_to(x1, y1); c.close_path(); c.fill()
    f.color('#9fd3ff', a * 0.35); c.set_line_width(3)
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        yy = y + amp * math.sin(x / 70 + t * 2.4)
        (c.move_to if i == 0 else c.line_to)(x, yy)
    c.stroke()


def hull_path(c, top, bot):
    c.move_to(-300, top); c.line_to(290, top); c.line_to(330, top - 10)
    c.curve_to(320, bot * 0.4, 300, bot, 260, bot); c.line_to(-280, bot)
    c.curve_to(-300, bot, -305, top + 30, -300, top); c.close_path()


def ship(f, x, y, s, a, draft=100, anti=ANTI, wl=0, plates=0.0):
    """Navire de profil, proue à droite. y = repère, wl = ligne de flottaison relative (px)."""
    if a <= 0: return
    c = f.c; c.save(); c.translate(x, y); c.scale(s, s)
    top = -80
    bot = draft
    f.color(HULL, a); hull_path(c, top, bot); c.fill()
    c.save(); c.rectangle(-400, wl, 800, 400); c.clip()
    f.color(anti, a); hull_path(c, top, bot); c.fill()
    if plates > 0:
        # plaques de cuivre qui se posent une à une
        n = 0
        for j in range(3):
            for i in range(14):
                n += 1
                if n / 42 > plates: continue
                f.rect(-290 + i * 41, wl + 4 + j * 22, 37, 18, COPPER, a, 3)
    c.restore()
    f.rect(-280, top - 120, 110, 120, INK, a, 6)
    f.rect(-270, top - 150, 70, 30, INK, a, 4)
    f.rect(-262, top - 100, 90, 18, OCEAN, a)
    f.line([(-150, top - 14), (270, top - 14)], MUTED, a, 6)
    c.restore()


def sailship(f, x, y, s, a, plates):
    """Frégate stylisée : coque en bois, mâts, plaques de cuivre sous l'eau."""
    if a <= 0: return
    c = f.c; c.save(); c.translate(x, y); c.scale(s, s)
    wood = '#6b4a33'
    f.color(wood, a)
    c.move_to(-320, -60); c.line_to(330, -70); c.curve_to(300, 40, 240, 90, 180, 90)
    c.line_to(-230, 90); c.curve_to(-290, 80, -310, 20, -320, -60); c.close_path(); c.fill()
    c.save(); c.rectangle(-400, 0, 800, 200); c.clip()
    n = 0
    for j in range(4):
        for i in range(16):
            n += 1
            if n / 64 > plates: continue
            f.rect(-300 + i * 38, 2 + j * 22, 34, 19, COPPER, a, 3)
    c.restore()
    for mx, h in ((-150, 380), (40, 440), (220, 340)):
        f.line([(mx, -65), (mx, -65 - h)], wood, a, 9)
        f.rect(mx - 90, -65 - h + 40, 180, h * 0.32, INK, a * 0.9, 10)
        f.rect(mx - 75, -65 - h * 0.55, 150, h * 0.3, INK, a * 0.9, 10)
    c.restore()


def barnacle(f, x, y, s, a):
    if a <= 0: return
    c = f.c; f.color(SHELL, a)
    c.move_to(x - 14 * s, y); c.line_to(x - 6 * s, y - 16 * s); c.line_to(x + 6 * s, y - 16 * s)
    c.line_to(x + 14 * s, y); c.close_path(); c.fill()
    f.rect(x - 4 * s, y - 18 * s, 8 * s, 4 * s, DEEP, a, 2)


def weed(f, x, y, h, a, t, k):
    if a <= 0: return
    pts = [(x + 10 * math.sin(t * 2 + k + i * 0.8) * (i / 6), y + h * i / 6) for i in range(7)]
    f.line(pts, SLIME, a, 7)


def worm(f, x, y, a, t, k):
    if a <= 0: return
    pts = [(x + i * 12, y + 8 * math.sin(t * 6 + i + k)) for i in range(7)]
    f.line(pts, '#e8d9b0', a, 9)


def fouling(f, a, t, prog, top=820, bot=1120):
    """Salissures sur une coque vue de près : vase, algues, balanes."""
    r = random.Random(4)
    for k in range(60):
        x = r.uniform(110, 970); y = r.uniform(top + 20, bot - 30)
        kind = r.random()
        p = seg(prog, k / 60 * 0.85, k / 60 * 0.85 + 0.12)
        if p <= 0: continue
        if kind < 0.45:
            f.circle(x, y, 18 * ease(p), SLIME, a * 0.7)
        elif kind < 0.75:
            weed(f, x, bot - 10, 90 * ease(p), a, t, k)
        else:
            barnacle(f, x, y + 10, 1.3 * ease(p), a)


def gauge(f, y, a, val, maxv, label, col):
    if a <= 0: return
    f.rect(140, y, 800, 40, LINE, a, 20)
    f.rect(140, y, 800 * clamp(val / maxv), 40, col, a, 20)
    f.text(label, W/2, y - 30, 48, INK, a)


def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')
    c = f.c

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.8, 30.2))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Pourquoi du rouge ?', W/2, 296, 46, SPARK, ha)

    # S1 — accroche (0–4) : le navire se soulève et montre son ventre rouge
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        words(f, 'Beaucoup de navires', 460, 84, 0.05, INK, t_out=o)
        words(f, 'ont le ventre rouge.', 570, 84, 0.7, SPARK, t_out=o)
        lift = 120 * ease_io(seg(t, 0.0, 2.2))
        ship(f, W/2, 1170 - lift, 1.45, fo)
        water(f, 1170, fo * 0.55, t)

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.0:
        o1 = 7.4
        g1 = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'Une partie', 450, 90, 4.2, INK, t_out=o1)
            words(f, 'que personne ne voit.', 560, 80, 4.7, SPARK, t_out=o1)
            ship(f, W/2, 1040 + 4 * math.sin(t * 2), 1.45, g1)
            water(f, 1040, g1 * 0.6, t)
        o2 = 10.7
        g2 = ease(seg(t, 7.6, 8.0)) * (1 - seg(t, o2, o2 + 0.3))
        if g2 > 0:
            words(f, 'Ton intuition :', 480, 72, 7.7, MUTED, t_out=o2)
            words(f, 'c’est de la déco.', 600, 86, 8.1, INK, t_out=o2)
            # la coque change de couleur comme un nuancier
            cols = [ANTI, '#3f7fa8', '#4a9b7a', '#7a5a9b', ANTI]
            k = int((t - 8.0) * 1.4) % len(cols)
            ship(f, W/2, 1120, 1.3, g2, anti=cols[k], wl=-50)
            water(f, 1060 + 60, g2 * 0.6, t)

    # S3 — la question (10.9–13.6)
    if 10.9 <= t < 13.6:
        words(f, 'Pourquoi peindre', 820, 96, 11.0, INK, t_out=12.5)
        words(f, 'en rouge sous l’eau ?', 950, 96, 11.4, SPARK, t_out=12.5)

    # S4 — la preuve (13.5–30)
    if 13.4 <= t < 30.0:
        # A : sous l'eau, tout s'accroche (13.6–21.6)
        oa = 21.4
        ga = ease(seg(t, 13.5, 13.9)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Sous l’eau,', 430, 90, 13.6, INK, t_out=oa)
            words(f, 'tout s’accroche.', 540, 90, 14.1, SPARK, t_out=oa)
            f.rect(0, 700, W, 900, WATER, ga * 0.5)
            f.rect(80, 800, 920, 340, HULL, ga, 24)
            fouling(f, ga, t, seg(t, 15.0, 20.0), 800, 1140)
            words(f, 'vase, algues, coquillages', 1300, 54, 16.0, MUTED, t_out=oa, bold=False)
            words(f, 'Elles freinent le navire.', 1400, 58, 18.0, INK, t_out=oa)
        # B : la facture en carburant (21.6–29.6)
        gb = ease(seg(t, 21.5, 21.9)) * (1 - seg(t, 29.4, 29.8))
        if gb > 0:
            words(f, 'Carburant en plus :', 440, 84, 21.6, INK, t_out=29.3)
            p1 = ease(seg(t, 22.6, 24.4))
            a1 = gb * ease(seg(t, 22.3, 22.6))
            gauge(f, 720, a1, 10.3 * p1, 25, 'film de vase', SLIME)
            f.text('+' + f'{10.3 * p1:.1f}'.replace('.', ',') + ' %', W/2, 860, 80, SPARK, a1, MONO)
            p2 = ease(seg(t, 25.0, 26.8))
            a2 = gb * ease(seg(t, 24.7, 25.0))
            gauge(f, 1060, a2, 20.4 * p2, 25, 'petits coquillages', SHELL)
            c.save(); c.translate(W/2, 1200); s = bump(t, 26.8, 0.15); c.scale(s, s)
            f.text('+' + f'{20.4 * p2:.1f}'.replace('.', ',') + ' %', 0, 0, 80, SPARK, a2, MONO); c.restore()
            f.text('destroyers US Navy, étude 2011', W/2, 1340, 36, MUTED,
                   gb * ease(seg(t, 27.2, 27.5)), MONO, False)

    # S5 — la réponse (30–36) : le cuivre
    if 29.9 <= t < 36.0:
        o = 35.6
        a = ease(seg(t, 30.3, 30.6)) * (1 - seg(t, o, o + 0.3))
        words(f, 'La parade :', 560, 80, 30.0, INK, t_out=o)
        big_center(f, 'CUIVRE', 840, 210, COPPER, a, bump(t, 30.3, 0.18), DISPLAY)
        words(f, 'Il repousse ce qui s’accroche.', 1020, 60, 31.0, INK, t_out=o)
        words(f, 'Et son oxyde est rouge.', 1130, 70, 32.2, SPARK, t_out=o)
        r = random.Random(9)
        for k in range(10):
            ang = k * math.pi / 5 + t * 0.3
            d = 330 + 120 * ease(seg(t, 31.0, 33.5))
            barnacle(f, W/2 + d * math.cos(ang), 840 + d * 0.22 * math.sin(ang), 1.4,
                     a * (1 - seg(t, 32.0, 34.0)) * 0.9)

    # S6 — le retournement (36–48.4)
    if 36.0 <= t < 48.4:
        words(f, 'Le secret ?', 900, 150, 36.1, SPARK, t_out=37.9)
        # A : 1761, une frégate doublée de cuivre (38.1–42.6)
        oa = 42.6
        ga = ease(seg(t, 38.1, 38.5)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            yr = int(lerp(1700, 1761, ease(seg(t, 38.2, 39.4))))
            big_center(f, str(yr), 470, 130, SPARK, ga, bump(t, 39.4, 0.12))
            words(f, 'Une frégate anglaise,', 590, 64, 38.6, INK, t_out=oa)
            words(f, 'la coque doublée de cuivre.', 670, 64, 39.0, INK, t_out=oa)
            sailship(f, W/2, 1250, 0.9, ga, seg(t, 39.2, 41.4))
            water(f, 1250, ga * 0.5, t, y1=1560)
            for k in range(3):
                bx = 260 + 260 * k + 30 * math.sin(t * 3 + k)
                worm(f, bx, 1430 - 40 * abs(math.sin(t * 2 + k)), ga * 0.9, t, k)
            f.text('le taret ne passe plus', W/2, 1530, 40, MUTED, ga * ease(seg(t, 40.4, 40.7)), MONO, False)
        # B : 1778, toute la flotte ; puis la peinture (42.9–47.9)
        ob = 47.9
        gb = ease(seg(t, 42.8, 43.2)) * (1 - seg(t, ob, ob + 0.3))
        if gb > 0:
            words(f, '1778 : toute', 430, 84, 42.9, INK, t_out=ob)
            words(f, 'la Royal Navy suit.', 540, 84, 43.3, SPARK, t_out=ob)
            words(f, 'Puis le cuivre passe', 1290, 58, 44.8, INK, t_out=ob)
            words(f, 'dans la peinture.', 1370, 58, 45.3, SPARK, t_out=ob)
            words(f, 'Le rouge est resté.', 1470, 50, 46.4, MUTED, t_out=ob)
            # le cuivre en plaques devient peinture : la coque passe du cuivre au rouge
            m = seg(t, 45.0, 46.0)
            ship(f, W/2, 940, 1.35, gb, anti=ANTI, plates=1.0 - m)
            water(f, 940, gb * 0.5, t, y1=1200)

    # S7 — l'escalade (48–56.4) : la facture d'une flotte entière
    if 48.0 <= t < 56.4:
        o = 55.9
        ga = ease(seg(t, 48.1, 48.4)) * (1 - seg(t, o, o + 0.3))
        if ga > 0:
            words(f, 'Pour une seule classe', 430, 72, 48.1, INK, t_out=o)
            words(f, 'de destroyers américains :', 520, 64, 48.6, MUTED, t_out=o)
            prog = ease_io(seg(t, 49.6, 52.6))
            # petite flotte de navires qui apparaissent
            for k in range(12):
                ax = 200 + (k % 4) * 230; ay = 700 + (k // 4) * 120
                ship(f, ax, ay, 0.28, ga * seg(prog, k / 14, k / 14 + 0.1))
            val = int(56 * prog)
            c.save(); c.translate(W/2, 1190); s = bump(t, 52.6, 0.15); c.scale(s, s)
            f.text(f'{val} M$', 0, 0, 170, SPARK, ga, MONO, True); c.restore()
            words(f, 'par an, à cause des salissures', 1300, 50, 52.8, INK, t_out=o)
            f.text('estimation, Schultz et al., Biofouling 2011', W/2, 1390, 32, MUTED,
                   ga * ease(seg(t, 53.2, 53.5)), MONO, False)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        a = ease(seg(t, 56.1, 56.4))
        ship(f, W/2, 690 + 4 * math.sin(t * 2), 0.9, a, wl=-10)
        water(f, 690, a * 0.6, t, 180, 900, 790)
        words(f, 'Ce rouge n’est pas une déco.', 900, 64, 56.3, INK)
        words(f, 'C’est un bouclier de cuivre.', 1010, 70, 57.6, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(240, 1160, 600, 150, OCEAN, a, 28)
        pa = 0.5 + 0.5 * math.sin((t - 60) * 3)
        f.rect(240, 1160, 600, 150, SPARK, a * 0.25 * pa, 28)
        f.text('Abonne-toi.', W/2, 1255, 62, INK, a)


def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    ev += [(0.15, rise(1.2, 300, 900, 0.07))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (12.5, 29.6, 47.9, 55.9)]
    ev += [(11.0, pop(520))]
    ev += [(26.8, ding(784, amp=0.18))]
    ev += [(30.3, ding(1046, amp=0.28)), (36.1, pop(300, 0.15))]
    ev += [(52.6, ding(784, amp=0.18))]
    ev += [(56.3, pop(440)), (60.0, ding(784, amp=0.22))]
    return ev
