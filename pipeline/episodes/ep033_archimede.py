"""Comment flotte un navire de 200 000 tonnes (poussée d'Archimède). Même structure que le pilote.

Sources :
- Principe d'Archimède : OpenStax College Physics via Lumen Learning, « 11.7 Archimedes' Principle »
  (« The buoyant force on an object equals the weight of the fluid it displaces » ; pâte à modeler qui coule
  en boule et flotte en forme de bateau : « Because of its shape, the boat displaces more water than the lump
  and experiences a greater buoyant force. The same is true of steel ships. » ; « If its average density is
  less than that of the surrounding fluid, it will float. » ; table : fer ou acier 7,8, eau de mer 1,025,
  en 10³ kg/m³ ; Archimède ca. 287–212 av. J.-C.).
- Archimède, « Des corps flottants », écrit vers 250 av. J.-C., premier énoncé du principe : Wikipedia
  « On Floating Bodies » (via Wikiwand).
- Pétroliers géants : Strauss Center (Univ. of Texas) « Types of tankers » (VLCC : plus de 200 000 tpl,
  200 000 à 320 000) ; VesselsValue, glossaire « Very Large Crude Carrier » (à partir de 200 000 tpl).
  Affiché : « plus de 200 000 tonnes » ; calcul fait sur 200 000 t.
- Ligne de charge : Wikipedia « Load line (watercraft) » (Samuel Plimsoll ; Merchant Shipping Act 1876 rend la
  marque obligatoire ; marques TF, F, T, S, W, WNA ; eau douce 1 000 kg/m³, eau de mer 1 025 kg/m³ ;
  « the ship will float deeper in freshwater than saltwater ») ; History Hit, 25 juillet 2024, « The Plimsoll
  Line » (Plimsoll député de Derby, « coffin ships », Merchant Shipping Act 1876).
- Calculs : 7,8 / 1,025 = 7,6 ; 200 000 t / 1,025 t/m³ = 195 122 m³ ; racine cubique = 58,0 m ;
  en eau douce 200 000 m³, soit 4 878 m³ de plus (+ 2,5 %).
"""
import math
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro (ep032 précédent).
COVER = dict(tag='Science', l1='Pourquoi un navire en acier', l2='ne coule pas')

WATER = '#1f5f7a'
HULL = '#2c4352'
ANTI = '#a8473a'
STEEL = '#9fb2bd'


def water(f, y, a, t, x0=0, x1=W, y1=1600, col=WATER, amp=8):
    """Surface ondulée de y jusqu'à y1."""
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


def ship(f, x, y, s, a, draft=60):
    """Pétrolier de profil, proue à droite. y = ligne de flottaison, draft = partie immergée (px à s=1)."""
    if a <= 0: return
    c = f.c; c.save(); c.translate(x, y); c.scale(s, s)
    top = -110 + draft          # pont
    bot = draft                 # quille
    # coque
    f.color(HULL, a)
    c.move_to(-300, top); c.line_to(290, top); c.line_to(330, top - 10)
    c.curve_to(320, bot * 0.4, 300, bot, 260, bot); c.line_to(-280, bot)
    c.curve_to(-300, bot, -305, top + 30, -300, top); c.close_path(); c.fill()
    # œuvres vives (sous la flottaison)
    c.save(); c.rectangle(-400, 0, 800, 400); c.clip()
    f.color(ANTI, a)
    c.move_to(-300, top); c.line_to(290, top); c.line_to(330, top - 10)
    c.curve_to(320, bot * 0.4, 300, bot, 260, bot); c.line_to(-280, bot)
    c.curve_to(-300, bot, -305, top + 30, -300, top); c.close_path(); c.fill()
    c.restore()
    # château arrière
    f.rect(-280, top - 120, 110, 120, INK, a, 6)
    f.rect(-270, top - 150, 70, 30, INK, a, 4)
    f.rect(-262, top - 100, 90, 18, OCEAN, a)
    # tuyauterie sur le pont
    f.line([(-150, top - 14), (270, top - 14)], MUTED, a, 6)
    c.restore()


def plimsoll(f, x, y, a, k):
    """Marque de franc-bord simplifiée : cercle barré + échelle TF F T S W."""
    if a <= 0: return
    f.circle(x, y, 70, SPARK, a, 8)
    f.line([(x - 100, y), (x + 100, y)], SPARK, a, 8)
    lab = [('TF', -60), ('F', -40), ('T', -20), ('S', 0), ('W', 20)]
    f.line([(x + 170, y - 70), (x + 170, y + 30)], SPARK, a, 6)
    for i, (s, dy) in enumerate(lab):
        g = a * ease(seg(k, i * 0.15, i * 0.15 + 0.2))
        f.line([(x + 170, y + dy * 2.2 - 20), (x + 250, y + dy * 2.2 - 20)], SPARK, g, 6)
        f.text(s, x + 270, y + dy * 2.2 - 8, 34, INK, g, MONO, True, 'left')


def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.8, 30.2))
    f.rect(120, 236, 840, 92, OCEAN, ha * 0.9, 46)
    f.text('Comment ça flotte ?', W/2, 296, 44, SPARK, ha)

    # S1 — accroche (0–4) : le pétrolier entre, il flotte
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        words(f, 'Plus de 200 000 tonnes', 470, 74, 0.05, INK, t_out=o)
        words(f, 'd’acier. Et ça flotte.', 580, 74, 0.6, SPARK, t_out=o)
        xs = lerp(1500, W/2, ease(seg(t, 0.0, 2.6)))
        ship(f, xs, 1120 + 6 * math.sin(t * 2), 1.25, fo, 60)
        water(f, 1120, fo, t, y1=1560)
        f.text('200 000 t', W/2, 1480, 56, INK, fo * ease(seg(t, 1.6, 2.0)), MONO, True)

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.0:
        o1 = 7.4
        g1 = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'Pourtant, un clou', 470, 76, 4.2, INK, t_out=o1)
            words(f, 'en acier coule.', 580, 76, 4.7, SPARK, t_out=o1)
            f.rect(240, 760, 600, 640, LINE, g1 * 0.6, 24)
            water(f, 860, g1, t, 250, 830, 1390, amp=5)
            p = ease_io(seg(t, 5.0, 6.6))
            ny = lerp(700, 1300, p) if t > 5.0 else 700
            c = f.c; c.save(); c.translate(W/2, ny); c.rotate(0.25 * p)
            f.rect(-8, -90, 16, 180, STEEL, g1, 4)
            f.rect(-34, -98, 68, 16, STEEL, g1, 6)
            c.restore()
            if t > 5.6:
                for i in range(5):
                    by = ny - 120 - ((t - 5.6) * 160 + i * 60) % 300
                    if by > 880: f.circle(W/2 + 20 * math.sin(i + t * 3), by, 8, '#9fd3ff', g1 * 0.6, 3)
        o2 = 10.7
        g2 = ease(seg(t, 7.6, 8.0)) * (1 - seg(t, o2, o2 + 0.3))
        if g2 > 0:
            words(f, 'À volume égal, l’acier', 470, 70, 7.7, INK, t_out=o2)
            words(f, 'pèse 7,6 fois plus lourd.', 575, 70, 8.1, SPARK, t_out=o2)
            yb = 1380; sc = 560 / 7.8
            h1 = 7.8 * sc * ease_io(seg(t, 8.4, 9.6))
            h2 = 1.025 * sc * ease_io(seg(t, 8.6, 9.2))
            f.rect(240, yb - h1, 240, h1, STEEL, g2, 14)
            f.rect(600, yb - h2, 240, h2, WATER, g2, 14)
            f.text('1 m³ d’acier', 360, yb + 55, 36, MUTED, g2, MONO, False)
            f.text('1 m³ d’eau de mer', 720, yb + 55, 36, MUTED, g2, MONO, False)
            f.text(f'{7.8 * ease_io(seg(t, 8.4, 9.6)):.1f}'.replace('.', ',') + ' t', 360, yb - h1 - 22, 48, INK, g2, MONO, True)
            f.text(f'{1.025 * ease_io(seg(t, 8.6, 9.2)):.3f}'.replace('.', ',') + ' t', 720, yb - h2 - 22, 48, INK, g2, MONO, True)

    # S3 — la question (10.9–13.6)
    if 10.9 <= t < 13.6:
        words(f, 'Alors comment', 820, 96, 11.0, INK, t_out=12.5)
        words(f, 'ça flotte ?', 950, 96, 11.4, SPARK, t_out=12.5)

    # S4 — la preuve (13.5–30)
    if 13.4 <= t < 30.0:
        # A : un bloc d'acier coule (13.6–21)
        oa = 21.0
        ga = ease(seg(t, 13.5, 13.9)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Prends un bloc', 440, 76, 13.6, INK, t_out=oa)
            words(f, 'de 1 m³ d’acier.', 550, 76, 14.0, SPARK, t_out=oa)
            f.rect(140, 760, 800, 680, LINE, ga * 0.6, 24)
            water(f, 900, ga, t, 150, 930, 1430, amp=5)
            p = ease_io(seg(t, 15.4, 17.6))
            by = lerp(680, 1220, p)
            f.rect(W/2 - 100, by - 100, 200, 200, STEEL, ga, 10)
            f.text('7,8 t', W/2, by + 16, 48, DEEP, ga, MONO, True)
            # flèches : poids vers le bas, poussée vers le haut (petite)
            if t > 17.8:
                k = ease(seg(t, 17.8, 18.3))
                f.line([(W/2 - 220, by - 60), (W/2 - 220, by + 120)], RED, ga * k, 12)
                f.text('poids 7,8 t', W/2 - 220, by + 170, 34, RED, ga * k, MONO, True)
                f.line([(W/2 + 220, by + 60), (W/2 + 220, by + 60 - 26)], '#9fd3ff', ga * k, 12)
                f.text('poussée 1 t', W/2 + 220, by + 130, 34, '#9fd3ff', ga * k, MONO, True)
            f.text('Il coule.', W/2, 1520, 56, SPARK, ga * ease(seg(t, 18.6, 19.0)))
        # B : le même acier en coque (21.3–29.6)
        gb = ease(seg(t, 21.2, 21.6)) * (1 - seg(t, 29.4, 29.8))
        if gb > 0:
            words(f, 'Aplatis-le en coque', 440, 76, 21.3, INK, t_out=29.4)
            words(f, 'pleine d’air.', 550, 76, 21.8, SPARK, t_out=29.4)
            f.rect(80, 760, 920, 680, LINE, gb * 0.6, 24)
            k = ease_io(seg(t, 22.4, 24.4))            # 0 = bloc, 1 = coque
            wl = 1060                                  # surface
            sink = lerp(-10, 110, ease_io(seg(t, 24.6, 26.4)))   # enfoncement de la coque
            hw = lerp(100, 400, k); hh = lerp(200, 260, k); th = lerp(100, 16, k)
            top = wl + sink - hh
            # coque en U
            c = f.c; f.color(STEEL, gb)
            x0, x1, yb_ = W/2 - hw, W/2 + hw, top + hh
            c.move_to(x0, top); c.line_to(x0, yb_); c.line_to(x1, yb_); c.line_to(x1, top)
            c.line_to(x1 - th, top); c.line_to(x1 - th, yb_ - th); c.line_to(x0 + th, yb_ - th); c.line_to(x0 + th, top)
            c.close_path(); c.fill()
            water(f, wl, gb, t, 90, 990, 1430, amp=4)
            # volume d'eau écarté (hachuré)
            if t > 26.4:
                q = ease(seg(t, 26.4, 26.9))
                f.rect(x0, wl, 2 * hw, yb_ - wl, SPARK, gb * q * 0.35)
                f.text('eau écartée', W/2, wl + (yb_ - wl) / 2 + 14, 40, INK, gb * q, MONO, True)
                f.line([(W/2, 1360), (W/2, 1360 - 70 * q)], '#9fd3ff', gb * q, 14)
            f.text('Même acier. Il flotte.', W/2, 1530, 56, SPARK, gb * ease(seg(t, 27.4, 27.8)))

    # S5 — la réponse (30–36)
    if 29.9 <= t < 36.0:
        o = 35.6
        a = ease(seg(t, 30.3, 30.6)) * (1 - seg(t, o, o + 0.3))
        words(f, 'Pour 200 000 t, il écarte', 640, 62, 30.1, INK, t_out=o)
        big_center(f, '195 000 m³', 860, 150, SPARK, a, bump(t, 30.3, 0.15))
        words(f, 'd’eau de mer.', 990, 66, 30.9, INK, t_out=o)
        g = ease(seg(t, 32.0, 32.4)) * a
        sz = 300 * ease_io(seg(t, 32.0, 33.4))
        f.rect(W/2 - sz/2, 1440 - sz, sz, sz, WATER, g * 0.9, 6)
        f.text('un cube de 58 m de côté', W/2, 1520, 44, MUTED, g, MONO, False)

    # S6 — le retournement (36–48.4)
    if 36.0 <= t < 48.4:
        words(f, 'Le secret ?', 900, 130, 36.1, INK, t_out=37.9)
        # A : l'eau rend ce qu'on lui prend (38.1–42.8)
        oa = 42.8
        ga = ease(seg(t, 38.1, 38.5)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'L’eau pousse vers le haut', 440, 70, 38.2, INK, t_out=oa)
            words(f, 'avec le poids écarté.', 550, 70, 38.7, SPARK, t_out=oa)
            ship(f, W/2, 1000, 1.2, ga, 70)
            water(f, 1000, ga, t, y1=1440)
            n = 7
            for i in range(n):
                x = W/2 - 300 + 600 * i / (n - 1)
                L = 120 * ease(seg(t, 39.4 + i * 0.06, 39.9 + i * 0.06))
                y0 = 1300
                f.line([(x, y0), (x, y0 - L)], '#9fd3ff', ga, 10)
                if L > 20:
                    c = f.c; f.color('#9fd3ff', ga)
                    c.move_to(x, y0 - L - 26); c.line_to(x - 18, y0 - L + 4); c.line_to(x + 18, y0 - L + 4); c.close_path(); c.fill()
            f.text('Archimède, vers 250 av. J.-C.', W/2, 1520, 40, MUTED, ga * ease(seg(t, 40.6, 41.0)), MONO, False)
        # B : un navire, c'est surtout de l'air (43.0–48)
        ob = 47.9
        gb = ease(seg(t, 42.9, 43.3)) * (1 - seg(t, ob, ob + 0.3))
        if gb > 0:
            words(f, 'Un navire, c’est', 440, 76, 43.0, INK, t_out=ob)
            words(f, 'surtout de l’air.', 550, 76, 43.5, SPARK, t_out=ob)
            # coque en coupe : paroi d'acier fine, intérieur vide
            x0, x1, y0, y1 = 200, 880, 760, 1260
            f.rect(x0, y0, x1 - x0, y1 - y0, STEEL, gb, 20)
            k = ease_io(seg(t, 44.0, 45.0))
            f.rect(x0 + 22, y0 + 22, x1 - x0 - 44, (y1 - y0 - 44) * k, OCEAN, gb, 12)
            f.text('air', W/2, y0 + 270, 60, MUTED, gb * k, MONO, True)
            f.text('Acier + air : en moyenne,', W/2, 1380, 46, INK, gb * ease(seg(t, 45.4, 45.7)))
            f.text('moins dense que l’eau.', W/2, 1450, 46, SPARK, gb * ease(seg(t, 45.4, 45.7)))

    # S7 — l'escalade (48–56.4) : rivière ou mer, il ne flotte pas pareil
    if 48.0 <= t < 56.4:
        oa = 52.0
        ga = ease(seg(t, 48.1, 48.4)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'En eau douce, plus légère,', 440, 66, 48.1, INK, t_out=oa)
            words(f, 'il s’enfonce plus.', 545, 74, 48.6, SPARK, t_out=oa)
            k = ease_io(seg(t, 49.4, 50.6))
            ship(f, W/2, 1050, 1.2, ga, lerp(60, 85, k))
            water(f, 1050, ga, t, y1=1440, col=lerp_col(WATER, '#3c8fae', k))
            f.text('mer' if k < 0.5 else 'rivière', W/2, 1400, 44, INK, ga, MONO, True)
            f.text('+ 2,5 % d’eau à écarter', W/2, 1510, 44, MUTED, ga * ease(seg(t, 50.6, 51.0)), MONO, False)
        o = 55.9
        gb = ease(seg(t, 52.2, 52.5)) * (1 - seg(t, o, o + 0.3))
        if gb > 0:
            words(f, 'D’où cette marque', 440, 76, 52.3, INK, t_out=o)
            words(f, 'sur chaque coque.', 550, 76, 52.7, SPARK, t_out=o)
            f.rect(100, 760, 880, 560, HULL, gb, 24)
            plimsoll(f, 400, 1060, gb, seg(t, 53.0, 54.4))
            f.text('Ligne Plimsoll, obligatoire', W/2, 1440, 42, INK, gb * ease(seg(t, 54.0, 54.3)))
            f.text('au Royaume-Uni depuis 1876', W/2, 1505, 42, MUTED, gb * ease(seg(t, 54.0, 54.3)))

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        words(f, 'Un navire ne flotte pas malgré son poids.', 760, 50, 56.3, INK)
        words(f, 'Il flotte grâce à son vide.', 870, 70, 57.6, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(240, 1160, 600, 150, OCEAN, a, 28)
        pa = 0.5 + 0.5 * math.sin((t - 60) * 3)
        f.rect(240, 1160, 600, 150, SPARK, a * 0.25 * pa, 28)
        f.text('Abonne-toi.', W/2, 1255, 62, INK, a)


def lerp_col(c1, c2, k):
    a = hexc(c1); b = hexc(c2)
    return '#%02x%02x%02x' % tuple(int(255 * lerp(a[i], b[i], k)) for i in range(3))


def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    ev += [(0.15, pop(440, 0.09))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (12.5, 29.6, 47.9, 55.9)]
    ev += [(11.0, pop(520))]
    ev += [(17.6, clink(900))]
    ev += [(27.4, ding(784, amp=0.2))]
    ev += [(30.3, ding(1046, amp=0.28)), (36.1, pop(300, 0.15))]
    ev += [(45.4, ding(784, amp=0.18))]
    ev += [(54.0, ding(880, amp=0.18))]
    ev += [(56.3, pop(440)), (60.0, ding(784, amp=0.22))]
    return ev
