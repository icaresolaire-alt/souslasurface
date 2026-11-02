"""Internet passe sous la mer : les câbles sous-marins. Même structure que le pilote.

Sources :
- Part des données internationales : Engadget, W. Shanklin, 5 juin 2026, « How the Internet Crosses Oceans »
  (« About 99 percent of international internet traffic uses these undersea cables », d'après ONU Info) ;
  Le Figaro Nautisme, 16 mars 2026 (« L'Union internationale des télécommunications rappelle que les câbles
  sous-marins transportent plus de 99 % des échanges internationaux de données ») ; Brussels Times,
  18 février 2025 (ONU : 99 %). Mental Floss (2015, mis à jour 2023, d'après la NOAA) : plus de 95 %.
- Nombre de câbles : TeleGeography, « How Many Submarine Cables Are There, Anyway? », 23 sept. 2026
  (607 systèmes en service, 102 en projet). Longueur : ICPC, fiche presse (environ 1,7 million de km en 2025 ;
  FAQ mai 2026 : environ 1,8 million) et BGR, 9 mars 2026 (1,7 million de km). Tour de la Terre 40 075 km
  -> 1,7 M / 40 075 = 42 tours.
- Épaisseur : Engadget 2026 (« roughly as thick as a garden hose », fibres « no thicker than a human hair ») ;
  Figaro Nautisme 2026, d'après TeleGeography (tuyau d'arrosage, fibres de l'épaisseur d'un cheveu).
- MAREA : 6 600 km entre Virginia Beach et Bilbao (Next INpact « MAREA : 6 600 km de fibre optique pour
  relier Virginia Beach et Bilbao » ; DatacenterDynamics, 2017, câble Microsoft et Facebook terminé).
- Pannes : ICPC FAQ, mai 2026 (« approximately 150–200 submarine telecommunications cable faults occur
  globally each year. Around 70–80% are caused by accidental human activity, such as commercial fishing
  activity and ships' anchors ») ; Engadget 2026 (150 à 200 incidents par an, environ 80 % d'origine humaine,
  ancres ou chalutiers) ; Submarine Networks, 2025 (environ 200 pannes par an, 86 % pêche et ancres).
  Requins : Mental Floss, d'après l'ICPC (« fish bites » : moins de 1 % des pannes de l'histoire du secteur).
- Satellite géostationnaire : 35 786 km d'altitude (36 000 km arrondi) ; trajet sol -> satellite -> sol
  au moins 72 000 km. Lumière dans la fibre : environ 200 000 km/s -> 6 600 km en 33 ms (calcul).
"""
import math
from lib import *
from kinetic import words, bump, big_center
from worldmap import WorldMap, ROUTE_SHANGHAI_ROTTERDAM

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro (ep028 précédent).
COVER = dict(tag='Tech', l1='Ton internet passe', l2='sous la mer')

WORLD = WorldMap(lon=(-180, 180), lat=(-58, 78), x=40, y=760, w=1000)
ATL = WorldMap(lon=(-84, 6), lat=(22, 58), x=40, y=760, w=1000)

MAREA = [(-75.98, 36.85), (-70, 38.3), (-60, 40.3), (-45, 42.6), (-30, 44.6), (-18, 45.3), (-8, 44.6), (-2.93, 43.4)]
# Tracés simplifiés de grands axes de câbles (lon, lat), tous en mer
CABLES = [
    [(-74, 40.4), (-60, 41.5), (-40, 46), (-20, 49), (-5.6, 50.1)],
    MAREA,
    [(-80.1, 26.5), (-70, 22.5), (-55, 14), (-45, 5), (-38.5, -3.7)],
    [(-38.5, -3.7), (-30, 10), (-22, 28), (-9.3, 38.7)],
    [(-9.3, 38.7), (-14, 30), (-20, 15), (-15, 5), (0, -2), (10, -10), (13, -22), (17.9, -33.5)],
    [(-38.5, -3.7), (-20, -8), (0, -10), (13.2, -8.8)],
    list(reversed(ROUTE_SHANGHAI_ROTTERDAM)),
    [(-118.3, 33.6), (-135, 30), (-158, 21.3), (-179.9, 28)],
    [(-124, 44), (-150, 46), (-179.9, 42)],
    [(179.9, 28), (160, 30), (141, 35)],
    [(179.9, 42), (160, 40), (141, 36)],
    [(151.5, -34), (158, -20), (158, -8), (147, 10), (140, 30)],
    [(103.8, 1.3), (108, 6), (113, 15), (120, 20), (122, 30.8)],
    [(55, 25.5), (58, 22), (65, 16), (72.8, 18.9)],
]


def cables(f, M, p, a, col=SPARK, width=3):
    for i, c in enumerate(CABLES):
        q = clamp(p * 1.6 - i * 0.045)
        M.route(f, c, ease_io(q), a, col, width, ghost=False)


def satellite(f, x, y, a, s=1.0):
    if a <= 0: return
    f.rect(x - 22 * s, y - 16 * s, 44 * s, 32 * s, INK, a, 6)
    f.rect(x - 92 * s, y - 12 * s, 60 * s, 24 * s, CAPITAL, a, 3)
    f.rect(x + 32 * s, y - 12 * s, 60 * s, 24 * s, CAPITAL, a, 3)
    f.line([(x - 32 * s, y), (x - 22 * s, y)], INK, a, 3)
    f.line([(x + 22 * s, y), (x + 32 * s, y)], INK, a, 3)


def ship(f, x, y, a):
    if a <= 0: return
    c = f.c; f.color(CAPITAL, a)
    c.move_to(x - 110, y); c.line_to(x + 110, y); c.line_to(x + 85, y + 50); c.line_to(x - 90, y + 50); c.close_path(); c.fill()
    f.rect(x + 20, y - 60, 60, 60, INK, a * 0.85, 6)


def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.8, 30.2))
    f.rect(120, 236, 840, 92, OCEAN, ha * 0.9, 46)
    f.text('Quelle part passe sous la mer ?', W/2, 296, 42, SPARK, ha)

    # S1 — accroche (0–4) : les câbles s'allument sur la carte du monde
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        WORLD.draw(f, fo)
        cables(f, WORLD, seg(t, 0.0, 3.6), fo)
        words(f, 'Ton message pour New York', 470, 70, 0.05, INK, t_out=o)
        words(f, 'ne passe pas par le ciel.', 580, 70, 0.7, INK, t_out=o)
        words(f, 'Il passe sous la mer.', 1300, 84, 1.6, SPARK, t_out=o)

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.0:
        o1 = 7.4
        g1 = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'Ton intuition :', 470, 72, 4.2, MUTED, t_out=o1)
            words(f, 'l’espace, les satellites.', 580, 76, 4.7, INK, t_out=o1)
            # la Terre et un satellite qui tourne
            f.circle(W/2, 1080, 170, EARTH, g1 * 0.85)
            ang = -math.pi / 2 + 0.9 * math.sin((t - 4) * 0.8)
            satellite(f, W/2 + 330 * math.cos(ang), 1080 + 330 * math.sin(ang), g1, 0.8)
            f.circle(W/2, 1080, 330, LINE, g1 * 0.0)
        o2 = 10.7
        g2 = ease(seg(t, 7.6, 8.0)) * (1 - seg(t, o2, o2 + 0.3))
        if g2 > 0:
            words(f, 'En vrai :', 470, 72, 7.7, MUTED, t_out=o2)
            words(f, 'un câble au fond de l’océan.', 580, 72, 8.2, INK, t_out=o2)
            # coupe : surface, eau, fond, câble qui s'allume
            ys, yb = 760, 1300
            f.rect(60, ys, 960, yb - ys, OCEAN, g2 * 0.9, 20)
            wave = [(60 + i * 12, ys + 6 * math.sin(i * 0.5 + t * 3)) for i in range(81)]
            f.line(wave, MUTED, g2, 3)
            f.rect(60, yb, 960, 70, '#2a2a22', g2, 10)
            p = ease_io(seg(t, 8.6, 10.2))
            f.line([(80, yb - 6), (80 + 920 * p, yb - 6)], SPARK, g2, 8)
            f.circle(80 + 920 * p, yb - 6, 12, INK, g2 * (p > 0.02))

    # S3 — la question (10.9–13.6)
    if 10.9 <= t < 13.6:
        words(f, 'Quelle part d’internet', 820, 90, 11.0, INK, t_out=12.5)
        words(f, 'passe sous la mer ?', 950, 96, 11.4, SPARK, t_out=12.5)

    # S4 — la preuve (13.5–30)
    if 13.4 <= t < 30.0:
        # A : MAREA, Virginia Beach -> Bilbao (13.6–21)
        oa = 21.0
        ga = ease(seg(t, 13.5, 13.9)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Un vrai câble : MAREA.', 440, 76, 13.6, INK, t_out=oa)
            words(f, 'États-Unis → Espagne', 550, 64, 14.2, SPARK, t_out=oa)
            ATL.draw(f, ga)
            p = ease_io(seg(t, 15.0, 19.0))
            ATL.route(f, MAREA, p, ga, SPARK, 7)
            ATL.port(f, -75.98, 36.85, 'Virginia Beach', ga, SPARK, 12, 34, 54)
            ATL.port(f, -2.93, 43.26, 'Bilbao', ga * ease(seg(t, 18.6, 19.0)), SPARK, 12, 34, -26)
            x, y = ATL.point_on(MAREA, p)
            f.circle(x, y, 18, INK, ga * (0.5 + 0.5 * math.sin(t * 12)) * (p < 1))
            f.text(fmt_int(6600 * p) + ' km', W/2, 1380, 84, INK, ga * ease(seg(t, 15.0, 15.3)), MONO, True)
            f.text('traversés par la lumière en 0,03 s', W/2, 1470, 42, MUTED, ga * ease(seg(t, 18.8, 19.1)), MONO, False)
        # B : tous les câbles du monde (21.3–29.6)
        gb = ease(seg(t, 21.2, 21.6)) * (1 - seg(t, 29.4, 29.8))
        if gb > 0:
            words(f, 'Et il y en a', 440, 80, 21.3, INK, t_out=29.4)
            words(f, 'des centaines.', 550, 80, 21.8, SPARK, t_out=29.4)
            WORLD.draw(f, gb)
            p = seg(t, 22.4, 27.0)
            cables(f, WORLD, p, gb)
            f.text(fmt_int(607 * ease_io(p)), W/2, 690, 96, INK, gb * ease(seg(t, 22.4, 22.7)), MONO, True)
            f.text('câbles en service', W/2, 1240, 42, MUTED, gb * ease(seg(t, 22.6, 22.9)), MONO, False)
            f.text('1,7 million de km', W/2, 1360, 72, SPARK, gb * ease(seg(t, 25.4, 25.8)), MONO, True)
            f.text('tracés simplifiés', W/2, 1440, 30, MUTED, gb * ease(seg(t, 23.0, 23.3)), MONO, False)

    # S5 — la réponse (30–36)
    if 29.9 <= t < 36.0:
        o = 35.6
        a = ease(seg(t, 30.3, 30.6)) * (1 - seg(t, o, o + 0.3))
        big_center(f, '99 %', 820, 240, SPARK, a, bump(t, 30.3, 0.18))
        words(f, 'des données entre pays', 1000, 72, 31.0, INK, t_out=o)
        words(f, 'passent par ces câbles.', 1100, 72, 31.6, INK, t_out=o)
        f.text('Estimation ONU et UIT, 2025-2026', W/2, 1300, 34, MUTED, ease(seg(t, 32.6, 33.0)) * a, MONO, False)

    # S6 — le retournement (36–48.4)
    if 36.0 <= t < 48.4:
        words(f, 'Pourquoi pas', 820, 120, 36.1, INK, t_out=37.9)
        words(f, 'les satellites ?', 960, 120, 36.6, SPARK, t_out=37.9)
        # A : la distance (38.1–42.6)
        oa = 42.6
        ga = ease(seg(t, 38.1, 38.5)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Un satellite classique', 440, 76, 38.2, INK, t_out=oa)
            words(f, 'tourne à 36 000 km.', 550, 76, 38.7, SPARK, t_out=oa)
            gx0, gx1, gy = 200, 880, 1250
            sx, sy = W/2, 720
            f.rect(80, gy, 920, 14, EARTH, ga, 7)
            satellite(f, sx, sy, ga * ease(seg(t, 39.0, 39.3)), 0.8)
            p1 = ease_io(seg(t, 39.4, 40.4)); p2 = ease_io(seg(t, 40.4, 41.4))
            f.line([(gx0, gy), (lerp(gx0, sx, p1), lerp(gy, sy + 20, p1))], RED, ga, 5)
            if p2 > 0: f.line([(sx, sy + 20), (lerp(sx, gx1, p2), lerp(sy + 20, gy, p2))], RED, ga, 5)
            f.text('72 000 km', W/2, 960, 56, RED, ga * ease(seg(t, 41.0, 41.3)), MONO, True)
            p3 = ease_io(seg(t, 40.0, 41.2))
            f.line([(gx0, gy + 50), (lerp(gx0, gx1, p3), gy + 50)], SPARK, ga, 8)
            f.circle(gx0, gy, 12, INK, ga); f.circle(gx1, gy, 12, INK, ga)
            f.text('câble : 6 600 km', W/2, gy + 130, 52, SPARK, ga * ease(seg(t, 41.0, 41.3)), MONO, True)
        # B : dans le câble (42.9–48)
        ob = 47.9
        gb = ease(seg(t, 42.8, 43.2)) * (1 - seg(t, ob, ob + 0.3))
        if gb > 0:
            words(f, 'Le câble : épais comme', 440, 76, 42.9, INK, t_out=ob)
            words(f, 'un tuyau d’arrosage.', 550, 76, 43.4, SPARK, t_out=ob)
            cx, cy = W/2, 960
            g = ease(seg(t, 43.6, 44.4))
            f.circle(cx, cy, 230 * g, CAPITAL, gb)
            f.circle(cx, cy, 190 * g, OCEAN, gb)
            f.circle(cx, cy, 120 * g, LINE, gb)
            for k in range(8):
                ang = k * math.pi / 4
                fx, fy = cx + 60 * math.cos(ang) * g, cy + 60 * math.sin(ang) * g
                pulse = 0.5 + 0.5 * math.sin(t * 9 + k * 1.3)
                f.circle(fx, fy, 14 * g, SPARK, gb * ease(seg(t, 44.6, 45.0)) * (0.4 + 0.6 * pulse))
            f.text('Dedans : des fils de verre', W/2, 1330, 50, INK, gb * ease(seg(t, 45.2, 45.5)))
            f.text('fins comme un cheveu.', W/2, 1400, 50, SPARK, gb * ease(seg(t, 45.2, 45.5)))
            f.text('Tes données y voyagent en lumière.', W/2, 1480, 38, MUTED, gb * ease(seg(t, 46.0, 46.3)), MONO, False)

    # S7 — l'escalade (48–56.4) : 42 tours de la Terre, et les pannes
    if 48.0 <= t < 56.4:
        oa = 51.6
        ga = ease(seg(t, 48.1, 48.4)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Mis bout à bout :', 560, 72, 48.1, INK, t_out=oa)
            n = 42 * ease_io(seg(t, 48.6, 50.4))
            big_center(f, str(int(round(n))), 820, 220, SPARK, ga, bump(t, 50.4, 0.15))
            words(f, 'fois le tour de la Terre.', 1000, 64, 49.0, INK, t_out=oa)
            for k in range(int(n)):
                ang = k / 42 * 2 * math.pi
                f.circle(W/2 + 330 * math.cos(ang), 1260 + 120 * math.sin(ang), 7, SPARK, ga * 0.8)
        o = 55.9
        gb = ease(seg(t, 51.8, 52.1)) * (1 - seg(t, o, o + 0.3))
        if gb > 0:
            words(f, '150 à 200 pannes par an.', 440, 64, 51.9, INK, t_out=o)
            words(f, 'Surtout chalutiers et ancres.', 540, 64, 52.5, SPARK, t_out=o)
            ys, yb = 760, 1200
            f.rect(60, ys, 960, yb - ys, OCEAN, gb * 0.9, 20)
            f.rect(60, yb, 960, 60, '#2a2a22', gb, 10)
            f.line([(80, yb - 6), (1000, yb - 6)], SPARK, gb, 6)
            px = lerp(220, 640, ease_io(seg(t, 52.4, 54.0)))
            ship(f, px, ys - 50, gb)
            ax, ay = px - 60, yb - 24
            f.line([(px - 100, ys), (ax, ay)], MUTED, gb, 3)
            f.rect(ax - 16, ay - 16, 32, 32, MUTED, gb, 4)
            if t > 54.0:
                f.circle(ax, yb - 6, 26 * (0.6 + 0.4 * math.sin(t * 10)), RED, gb * 0.8)
            f.text('Les requins ? Moins de 1 %.', W/2, 1400, 50, MUTED, gb * ease(seg(t, 54.0, 54.3)))

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        a = ease(seg(t, 56.1, 56.4))
        words(f, 'Internet n’est pas dans le ciel.', 760, 64, 56.3, INK)
        words(f, 'Il dort au fond de la mer.', 870, 72, 57.6, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(240, 1160, 600, 150, OCEAN, a, 28)
        pa = 0.5 + 0.5 * math.sin((t - 60) * 3)
        f.rect(240, 1160, 600, 150, SPARK, a * 0.25 * pa, 28)
        f.text('Abonne-toi.', W/2, 1255, 62, INK, a)


def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    ev += [(0.15, pop(440, 0.09)), (1.6, ding(880, amp=0.18))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (12.5, 29.6, 47.9, 55.9)]
    ev += [(11.0, pop(520))]
    ev += [(19.0, clink(1500))]
    ev += [(22.4, rise(4.6, 300, 900, 0.07)), (27.0, ding(784, amp=0.2))]
    ev += [(30.3, ding(1046, amp=0.28)), (36.1, pop(300, 0.15))]
    ev += [(41.0, ding(784, amp=0.18))]
    ev += [(50.4, ding(880, amp=0.18)), (54.0, pop(360, 0.12))]
    ev += [(56.3, pop(440)), (60.0, ding(784, amp=0.22))]
    return ev
