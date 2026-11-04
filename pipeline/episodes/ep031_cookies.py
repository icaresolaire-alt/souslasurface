"""Comment les cookies tiers te suivent de site en site. Même structure que le pilote.

Sources :
- Wikipedia « HTTP cookie » (texte lu le 4 nov. 2026) : « Lou Montulli had the idea of using them in web
  communications in June 1994 », employé de Netscape ; « Cookies provided a solution to the problem of reliably
  implementing a virtual shopping cart » ; nom tiré de « magic cookie » (Unix) ; « A third-party cookie belongs
  to a domain different from the one shown in the address bar », typiquement les bannières publicitaires ;
  l'annonceur peut « build up a browsing history of the user across all the websites that have ads from this
  advertiser » ; navigateurs : « Can support cookies as large as 4,096 bytes in size ».
- MacRumors, 24 mars 2020 : Safari (macOS 10.15.4, iOS 13.4) bloque par défaut les cookies tiers,
  « the first mainstream browser to fully block third-party cookies by default ».
- Engadget, 23 avril 2025 : « Google will not make any changes to how third-party cookies work on the Chrome
  browser » ; Engadget, 18 oct. 2025 : Privacy Sandbox abandonné.
- Exemple de numéro « ID 4821 » et noms de sites (boutique.fr, meteo.fr, pub.com…) : illustratifs.
"""
import math
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro (ep030 précédent).
COVER = dict(tag='Tech', l1='Comment une pub', l2='te suit de site en site')


def window(f, x, y, w, h, url, a, url_col=MUTED):
    """Fenêtre de navigateur avec barre d'adresse."""
    if a <= 0: return
    f.rect(x, y, w, h, OCEAN, a, 22)
    f.rect(x, y, w, 64, LINE, a, 22)
    f.rect(x, y + 40, w, 24, LINE, a, 0)
    for k, col in enumerate((RED, SPARK, EARTH)):
        f.circle(x + 30 + k * 26, y + 32, 8, col, a * 0.8)
    f.rect(x + 110, y + 14, w - 130, 36, DEEP, a, 18)
    f.text(url, x + 130, y + 42, 26, url_col, a, MONO, False, 'left')


def pub(f, x, y, w, h, a, glow=0.0):
    """Encart publicitaire venu de pub.com."""
    if a <= 0: return
    f.rect(x, y, w, h, CAPITAL, a, 14)
    if glow > 0:
        f.rect(x, y, w, h, SPARK, a * 0.35 * glow, 14)
    f.text('PUB', x + w / 2, y + h / 2 + 4, min(44, h * 0.4), INK, a)
    f.text('pub.com', x + w / 2, y + h - 14, min(24, h * 0.22), SPARK, a, MONO, False)


def cookie(f, x, y, r, a, label=None):
    """Petit cookie doré (le fichier texte)."""
    if a <= 0: return
    f.circle(x, y, r, SPARK, a)
    for dx, dy in ((-0.35, -0.3), (0.3, -0.1), (-0.1, 0.35), (0.4, 0.4), (-0.45, 0.15)):
        f.circle(x + dx * r, y + dy * r, r * 0.11, '#7a4b12', a)
    if label:
        f.text(label, x, y + r + 46, 34, SPARK, a, MONO, True)


def shoe(f, x, y, s, a, col=SPARK):
    """Basket stylisée, pointe à droite."""
    if a <= 0: return
    c = f.c; c.save(); c.translate(x, y); c.scale(s, s)
    f.color(col, a)
    c.move_to(-70, -30); c.line_to(-20, -30); c.line_to(10, -5); c.curve_to(50, 0, 75, 5, 75, 25)
    c.line_to(-70, 25); c.close_path(); c.fill()
    f.color(INK, a)
    c.rectangle(-72, 25, 149, 10); c.fill()
    c.restore()


def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.8, 30.2))
    f.rect(100, 236, 880, 92, OCEAN, ha * 0.9, 46)
    f.text('Comment la pub te retrouve ?', W/2, 296, 42, SPARK, ha)

    # S1 — accroche (0–4) : la basket apparaît sur un site, puis un autre, puis un autre
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        words(f, 'Tu regardes une basket.', 440, 74, 0.05, INK, t_out=o)
        words(f, 'Elle te suit partout.', 550, 74, 0.7, SPARK, t_out=o)
        for k, (x, y, url, t0) in enumerate(((90, 700, 'boutique.fr', 0.0), (330, 900, 'meteo.fr', 1.2),
                                            (570, 1100, 'foot.fr', 2.0))):
            a = fo * ease(seg(t, t0, t0 + 0.3))
            window(f, x, y, 420, 300, url, a)
            shoe(f, x + 210 + 10 * math.sin(t * 4 + k), y + 190, 1.2 * bump(t, t0, 0.3), a)

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.0:
        o1 = 7.4
        g1 = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'Pourtant, chaque site', 440, 76, 4.2, INK, t_out=o1)
            words(f, 'est fermé aux autres.', 550, 76, 4.7, SPARK, t_out=o1)
            for k, url in enumerate(('boutique.fr', 'meteo.fr', 'foot.fr')):
                y = 720 + k * 250
                a = g1 * ease(seg(t, 4.6 + 0.35 * k, 4.9 + 0.35 * k))
                window(f, 190, y, 700, 200, url, a)
            # murs qui se ferment entre les sites
            for k in range(2):
                y = 935 + k * 250
                p = ease_io(seg(t, 5.8 + 0.3 * k, 6.4 + 0.3 * k))
                f.line([(W/2 - 380 * p, y), (W/2 + 380 * p, y)], RED, g1, 8)
        o2 = 10.7
        g2 = ease(seg(t, 7.6, 8.0)) * (1 - seg(t, o2, o2 + 0.3))
        if g2 > 0:
            words(f, 'Le site météo', 440, 76, 7.7, INK, t_out=o2)
            words(f, 'n’a jamais vu ta boutique.', 550, 70, 8.1, SPARK, t_out=o2)
            window(f, 140, 720, 800, 620, 'meteo.fr', g2)
            f.circle(340, 950, 70 + 4 * math.sin(t * 3), SPARK, g2)
            f.text('14 °C', 340, 1130, 50, INK, g2, MONO, True)
            a = g2 * ease(seg(t, 9.0, 9.3))
            f.rect(560, 820, 330, 420, CAPITAL, a, 16)
            shoe(f, 725, 1030, 1.4 * bump(t, 9.0, 0.3), a)
            f.text('?', 725, 1450, 120, SPARK, g2 * ease(seg(t, 9.6, 9.9)))

    # S3 — la question (10.9–13.6)
    if 10.9 <= t < 13.6:
        words(f, 'Alors comment', 820, 96, 11.0, INK, t_out=12.5)
        words(f, 'la pub te retrouve ?', 950, 90, 11.4, SPARK, t_out=12.5)

    # S4 — la preuve (13.5–30)
    if 13.4 <= t < 30.0:
        # A : sur la boutique, la pub dépose un cookie (13.6–21)
        oa = 21.0
        ga = ease(seg(t, 13.5, 13.9)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Sur la boutique, une pub.', 440, 72, 13.6, INK, t_out=oa)
            words(f, 'Elle vient d’un autre site.', 550, 72, 14.4, SPARK, t_out=oa)
            window(f, 90, 680, 900, 520, 'boutique.fr', ga)
            shoe(f, 330, 960, 2.0, ga, INK)
            pub(f, 620, 760, 320, 400, ga * ease(seg(t, 15.2, 15.5)), seg(t, 15.6, 16.2))
            # le cookie tombe dans le navigateur
            p = ease_io(seg(t, 17.0, 18.4))
            cookie(f, lerp(780, W/2, p), lerp(960, 1340, p), 54, ga * ease(seg(t, 16.8, 17.0)))
            f.text('Il te colle un numéro :', W/2, 1470, 48, INK, ga * ease(seg(t, 18.4, 18.7)))
            f.text('ID 4821', W/2, 1540, 52, SPARK, ga * ease(seg(t, 18.8, 19.1)), MONO, True)
        # B : même pub ailleurs, même numéro, l'historique se remplit (21.3–29.6)
        gb = ease(seg(t, 21.2, 21.6)) * (1 - seg(t, 29.4, 29.8))
        if gb > 0:
            words(f, 'Tu vas sur d’autres sites.', 440, 72, 21.3, INK, t_out=29.4)
            words(f, 'Même pub, même numéro.', 550, 72, 21.9, SPARK, t_out=29.4)
            sites = (('boutique.fr', 21.4), ('meteo.fr', 23.0), ('recettes.fr', 24.6), ('foot.fr', 26.2))
            # fenêtre courante à gauche
            cur = max(i for i, (_, t0) in enumerate(sites) if t >= t0 or i == 0)
            url, t0 = sites[cur]
            ap = gb * ease(seg(t, t0, t0 + 0.3))
            window(f, 70, 700, 470, 560, url, ap)
            pub(f, 150, 830, 310, 300, ap, seg(t, t0 + 0.3, t0 + 0.8))
            # le numéro part vers pub.com
            p = ease_io(seg(t, t0 + 0.6, t0 + 1.3))
            if cur > 0 or t < 23:
                cookie(f, lerp(305, 780, p), lerp(1180, 760, p), 30, gb * (p > 0) * (1 - seg(p, 0.95, 1.0) * 0.6))
            # registre de pub.com
            f.rect(600, 640, 420, 700, LINE, gb, 22)
            f.text('pub.com', 810, 700, 40, SPARK, gb, MONO, True)
            f.text('ID 4821', 810, 760, 36, INK, gb, MONO, True)
            for i, (u, ti) in enumerate(sites):
                ai = gb * ease(seg(t, ti + 1.3, ti + 1.6))
                f.text(u, 650, 860 + i * 90, 36, INK, ai, MONO, False, 'left')
            f.text('Ton historique, chez la pub.', W/2, 1480, 46, SPARK, gb * ease(seg(t, 27.8, 28.1)))

    # S5 — la réponse (30–36)
    if 29.9 <= t < 36.0:
        o = 35.6
        a = ease(seg(t, 30.3, 30.6)) * (1 - seg(t, o, o + 0.3))
        cookie(f, W/2, 600, 90 * bump(t, 30.3, 0.2), a)
        big_center(f, '4 Ko', 1010, 240, SPARK, a, bump(t, 30.3, 0.18), DISPLAY)
        words(f, 'Le coupable : un cookie,', 1170, 64, 31.0, INK, t_out=o)
        words(f, 'un petit texte de 4 Ko au plus.', 1260, 58, 31.6, INK, t_out=o)
        f.text('Juste assez pour un numéro.', W/2, 1400, 40, MUTED, ease(seg(t, 32.8, 33.2)) * a, MONO, False)

    # S6 — le retournement (36–48.4)
    if 36.0 <= t < 48.4:
        words(f, 'Le secret ?', 900, 130, 36.1, INK, t_out=37.9)
        # A : cookie du site contre cookie tiers (38.1–42.6)
        oa = 42.6
        ga = ease(seg(t, 38.1, 38.5)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Ce cookie ne vient pas', 440, 72, 38.2, INK, t_out=oa)
            words(f, 'du site que tu visites.', 550, 72, 38.8, SPARK, t_out=oa)
            window(f, 90, 680, 900, 520, 'boutique.fr', ga)
            shoe(f, 330, 960, 2.0, ga * 0.5, INK)
            pub(f, 620, 760, 320, 400, ga, 0.5 + 0.5 * math.sin(t * 4))
            # flèche vers l'adresse : « pas ce site »
            a1 = ga * ease(seg(t, 39.8, 40.1))
            f.text('pas d’ici', 300, 1290, 40, MUTED, a1, MONO, False)
            f.text('mais d’ici', 780, 1290, 40, SPARK, a1, MONO, True)
            f.text('On l’appelle un cookie tiers.', W/2, 1450, 52, INK, ga * ease(seg(t, 40.8, 41.1)))
        # B : une seule régie, présente sur une foule de sites (42.9–48)
        ob = 47.9
        gb = ease(seg(t, 42.8, 43.2)) * (1 - seg(t, ob, ob + 0.3))
        if gb > 0:
            words(f, 'Et la même pub est', 440, 72, 42.9, INK, t_out=ob)
            words(f, 'sur une foule de sites.', 550, 72, 43.4, SPARK, t_out=ob)
            cx, cy = W/2, 1050
            n = 12
            for i in range(n):
                ang = i / n * 6.283 + 0.26
                x, y = cx + 390 * math.cos(ang), cy + 330 * math.sin(ang)
                ai = gb * ease(seg(t, 43.6 + 0.12 * i, 43.9 + 0.12 * i))
                pl = ease_io(seg(t, 44.0 + 0.12 * i, 44.6 + 0.12 * i))
                f.line([(x, y), (lerp(x, cx, pl), lerp(y, cy, pl))], SPARK, ai * 0.6, 4)
                f.rect(x - 50, y - 36, 100, 72, LINE, ai, 10)
                f.rect(x - 22, y - 12, 44, 30, CAPITAL, ai, 6)
            f.circle(cx, cy, 110 * (1 + 0.04 * math.sin(t * 4)), CAPITAL, gb)
            f.text('pub.com', cx, cy + 12, 40, SPARK, gb, MONO, True)
            f.text('Elle relie tout ce que tu fais.', W/2, 1520, 44, INK, gb * ease(seg(t, 45.8, 46.1)))

    # S7 — l'escalade (48–56.4) : d'où ça vient, où ça va
    if 48.0 <= t < 56.4:
        oa = 51.6
        ga = ease(seg(t, 48.1, 48.4)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Inventé en 1994', 440, 80, 48.1, INK, t_out=oa)
            words(f, 'pour un panier d’achat.', 550, 76, 48.6, SPARK, t_out=oa)
            yr = int(lerp(1990, 1994, ease_io(seg(t, 48.6, 49.6))))
            big_center(f, str(yr), 900, 200, INK, ga)
            # panier
            c = f.c; f.color(SPARK, ga)
            c.move_to(380, 1050); c.line_to(700, 1050); c.line_to(660, 1250); c.line_to(420, 1250); c.close_path(); c.fill()
            f.line([(330, 1000), (380, 1050)], SPARK, ga, 10)
            f.circle(450, 1290, 26, INK, ga); f.circle(630, 1290, 26, INK, ga)
            f.text('Lou Montulli, chez Netscape', W/2, 1440, 42, MUTED, ga * ease(seg(t, 49.6, 49.9)), MONO, False)
        o = 55.9
        gb = ease(seg(t, 51.8, 52.1)) * (1 - seg(t, o, o + 0.3))
        if gb > 0:
            words(f, 'Safari les bloque depuis 2020.', 440, 64, 51.9, INK, t_out=o)
            words(f, 'Chrome les garde.', 550, 76, 52.6, SPARK, t_out=o)
            a1 = gb * ease(seg(t, 52.2, 52.5))
            f.rect(110, 760, 400, 520, LINE, a1, 26)
            f.text('Safari', 310, 850, 54, INK, a1)
            cookie(f, 310, 1030, 80, a1)
            f.line([(220, 940), (400, 1120)], RED, a1 * ease(seg(t, 52.6, 52.9)), 16)
            f.text('bloqués', 310, 1220, 40, EARTH, a1, MONO, True)
            a2 = gb * ease(seg(t, 52.9, 53.2))
            f.rect(570, 760, 400, 520, LINE, a2, 26)
            f.text('Chrome', 770, 850, 54, INK, a2)
            cookie(f, 770, 1030, 80 * bump(t, 53.2, 0.2), a2)
            f.text('autorisés', 770, 1220, 40, RED, a2, MONO, True)
            f.text('Google a renoncé à les supprimer en 2025.', W/2, 1420, 38, MUTED, gb * ease(seg(t, 53.8, 54.1)), MONO, False)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        words(f, 'Ce n’est pas le site qui te suit.', 760, 60, 56.3, INK)
        words(f, 'C’est la pub qu’il affiche.', 870, 72, 57.6, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(240, 1160, 600, 150, OCEAN, a, 28)
        pa = 0.5 + 0.5 * math.sin((t - 60) * 3)
        f.rect(240, 1160, 600, 150, SPARK, a * 0.25 * pa, 28)
        f.text('Abonne-toi.', W/2, 1255, 62, INK, a)


def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    ev += [(0.15, pop(440, 0.09)), (2.0, pop(520, 0.08))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (12.5, 29.6, 47.9, 55.9)]
    ev += [(11.0, pop(520))]
    ev += [(18.8, clink(1500))]
    ev += [(27.8, ding(784, amp=0.2))]
    ev += [(30.3, ding(1046, amp=0.28)), (36.1, pop(300, 0.15))]
    ev += [(40.8, ding(784, amp=0.18))]
    ev += [(49.6, pop(360, 0.12)), (53.2, ding(880, amp=0.18))]
    ev += [(56.3, pop(440)), (60.0, ding(784, amp=0.22))]
    return ev
