"""Comment un code-barres se lit en un bip. Même structure que le pilote.

Sources :
- Structure EAN-13 : Wikipedia « International Article Number » (« 95 areas (also called modules) of equal
  width » ; 3 + 42 + 5 + 42 + 3 ; « A digit is encoded in seven areas, by two black bars and two white spaces ») ;
  grandzebu.net « EAN 13 » (« 12 * 7 + 2 * 3 + 5 = 95 modules », « Each number is coded on 7 modules, each
  comprising 2 bars and two spaces », 30 barres au total) ; Que Choisir, 28 févr. 2006, « Décoder le code-barres »
  (deux barres et deux espaces par chiffre ; 13 chiffres).
- Tables L / R (0 = 0001101 / 1110010) et code complet de l'exemple : Wikipedia (table d'encodage, parité du
  premier chiffre). Code-barres affiché généré exactement d'après ces tables.
- Lecture par la lumière : Orca Scan, « How do barcode scanners work? » (« The black bars absorb the light, while
  the white spaces reflect it ») ; Shopify, « How do barcode scanners work » (cellules photoélectriques, impulsions
  de lumière réfléchie traduites en signal électrique).
- Chiffre de contrôle, poids 1 et 3, modulo 10 : Wikipedia (exemple 400638133393 → somme 89 → 90 - 89 = 1) et
  grandzebu (même méthode, exemple 978020113447 → 6). Un seul chiffre faux change la somme d'un multiple de 1 ou 3
  non divisible par 10 : toujours détecté (calcul).
- Lecture dans les deux sens : Wikipedia (« it does not matter whether the barcode is scanned from the left or from
  the right … parity ») ; Que Choisir (« lecture optique dans n'importe quel sens »). Parité : 0001101 = 3 cases
  noires (impair), 1110010 = 4 (pair).
- Premier article scanné : chewing-gum Wrigley's, 26 juin 1974, supermarché Marsh, Troy (Ohio) : GS1 « Marsh
  holds place of honor » (10 tablettes Juicy Fruit, 67 cents), History.com « This day in history, June 26 »,
  GS1 « How we got here », GS1 UK « The iconic barcode turns 50 ». 52 ans calculés.
- Des milliards de lectures par jour : GS1 « How we got here » (« billions of times every day »), History.com
  (« billions of barcodes scanned daily ») ; GS1 UK 2023 avance 10 milliards (non affiché, chiffre unique).
- Préfixe 300 à 379 = GS1 France, sans indiquer le pays de fabrication : gs1.org/prefixes (« GS1 Prefixes do not
  identify the country of origin ») et Que Choisir (« pas nécessairement celui où il a été fabriqué »).
- Faisceau, signal et paquet de chewing-gum : illustratifs.
"""
import math
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro (ep052 précédent).
COVER = dict(tag='Tech', l1='Comment la caisse lit', l2='ton code-barres en un bip')

L = ['0001101', '0011001', '0010011', '0111101', '0100011',
     '0110001', '0101111', '0111011', '0110111', '0001011']
R = [''.join('1' if b == '0' else '0' for b in x) for x in L]
G = [x[::-1] for x in R]
PAR = ['LLLLLL', 'LLGLGG', 'LLGGLG', 'LLGGGL', 'LGLLGG', 'LGGLLG', 'LGGGLL', 'LGLGLG', 'LGLGGL', 'LGGLGL']

CODE = '4006381333931'  # exemple de Wikipedia, chiffre de contrôle 1


def ean_bits(code):
    d = [int(c) for c in code]
    s = '101'
    for i, p in enumerate(PAR[d[0]]):
        s += (L if p == 'L' else G)[d[1 + i]]
    s += '01010'
    for x in d[7:]:
        s += R[x]
    return s + '101'


BITS = ean_bits(CODE)
assert len(BITS) == 95
GUARD = set(range(3)) | set(range(45, 50)) | set(range(92, 95))


def barcode(f, cx, y, m, h, a, reveal=1.0, digits=True, col=None):
    """Code-barres réel. reveal : part des modules dessinés (de gauche à droite)."""
    if a <= 0: return
    w = 95 * m; x0 = cx - w / 2
    f.rect(x0 - 11 * m, y - 4 * m, w + 22 * m, h + (16 if digits else 8) * m, INK, a, 10)
    n = int(95 * reveal)
    for i in range(n):
        if BITS[i] == '1':
            hh = h + (5 * m if i in GUARD else 0)
            f.rect(x0 + i * m, y, m + 0.5, hh, col or DEEP, a)
    if digits:
        ty = y + h + 11 * m; fs = 9 * m
        f.text(CODE[0], x0 - 6 * m, ty, fs, DEEP, a, MONO, True)
        for k in range(6):
            f.text(CODE[1 + k], x0 + (3 + 7 * k + 3.5) * m, ty, fs, DEEP, a, MONO, True)
            f.text(CODE[7 + k], x0 + (50 + 7 * k + 3.5) * m, ty, fs, DEEP, a, MONO, True)
    return x0


def laser(f, x0, x1, y, a, t):
    if a <= 0: return
    f.line([(x0, y), (x1, y)], RED, a * 0.35, 18)
    f.line([(x0, y), (x1, y)], RED, a, 4)


def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')
    c = f.c

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.8, 30.2))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Comment la caisse lit ?', W/2, 296, 44, SPARK, ha)

    # S1 — accroche (0–4) : le laser balaie dès la première image
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        words(f, 'Bip.', 470, 130, 0.05, SPARK, t_out=o)
        words(f, 'Tu viens de lire 13 chiffres.', 600, 64, 0.6, INK, t_out=o)
        barcode(f, W/2, 820, 8, 360, fo)
        ly = 830 + 340 * (0.5 + 0.5 * math.sin(t * 2.6))
        laser(f, 100, 980, ly, fo * (0.7 + 0.3 * math.sin(t * 20)), t)
        f.text('sans le savoir', W/2, 1400, 48, MUTED, fo * ease(seg(t, 2.2, 2.5)), MONO, True)

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.0:
        o1 = 7.4
        g1 = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'La machine ne voit', 450, 84, 4.2, INK, t_out=o1)
            words(f, 'aucun chiffre.', 565, 92, 4.6, SPARK, t_out=o1)
            # les chiffres s'effacent, il ne reste que des barres
            barcode(f, W/2, 800, 8, 360, g1, digits=False)
            dg = 1 - ease(seg(t, 5.2, 6.2))
            x0 = W/2 - 95 * 4
            for k, ch in enumerate(CODE):
                xx = x0 - 48 + k * 68 + 30
                f.text(ch, xx, 1330 + 40 * (1 - dg), 64, SPARK, g1 * dg, MONO, True)
            f.text('Juste du noir et du blanc.', W/2, 1360, 54, INK, g1 * ease(seg(t, 6.0, 6.3)), DISPLAY, True)
        o2 = 10.7
        g2 = ease(seg(t, 7.6, 8.0)) * (1 - seg(t, o2, o2 + 0.3))
        if g2 > 0:
            words(f, 'Et elle lit même', 450, 84, 7.7, INK, t_out=o2)
            words(f, 'à l’envers.', 565, 96, 8.1, SPARK, t_out=o2)
            rot = math.pi * ease_io(seg(t, 8.5, 9.6))
            c.save(); c.translate(W/2, 1000); c.rotate(rot); c.translate(-W/2, -1000)
            barcode(f, W/2, 820, 8, 320, g2)
            c.restore()
            laser(f, 100, 980, 1000, g2 * ease(seg(t, 9.6, 9.8)), t)
            f.text('Bip.', W/2, 1380, 64, SPARK, g2 * ease(seg(t, 9.8, 10.0)), MONO, True)

    # S3 — la question (10.9–13.6)
    if 10.9 <= t < 13.6:
        words(f, 'Comment', 820, 104, 11.0, INK, t_out=12.5)
        words(f, 'elle lit ?', 945, 116, 11.4, SPARK, t_out=12.5)

    # S4 — la preuve (13.5–30)
    if 13.4 <= t < 30.0:
        # A : la lumière (13.6–21.6)
        oa = 21.6
        ga = ease(seg(t, 13.5, 13.9)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Le blanc renvoie', 430, 76, 13.6, INK, t_out=oa)
            words(f, 'la lumière.', 535, 80, 14.0, SPARK, t_out=oa)
            words(f, 'Le noir l’absorbe.', 650, 72, 16.4, MUTED, t_out=oa)
            m = 8; x0 = W/2 - 95 * m / 2
            barcode(f, W/2, 760, m, 260, ga, digits=False)
            p = ease_io(seg(t, 15.0, 20.6))
            xs = x0 + p * 95 * m
            # faisceau vertical
            f.line([(xs, 740), (xs, 1040)], RED, ga * 0.35, 16)
            f.line([(xs, 740), (xs, 1040)], RED, ga, 3)
            # signal lu
            idx = min(94, int(p * 95))
            pts = []
            base = 1260
            for i in range(idx + 1):
                v = 0 if BITS[i] == '1' else 1
                yy = base - v * 110
                pts += [(x0 + i * m, yy), (x0 + (i + 1) * m, yy)]
            if len(pts) > 1:
                f.line(pts, SPARK, ga, 5)
            f.text('signal : lumière / pas de lumière', W/2, 1380, 40, MUTED,
                   ga * ease(seg(t, 15.4, 15.7)), MONO, False)
            f.text('(schéma)', W/2, 1440, 32, MUTED, ga * ease(seg(t, 15.6, 15.9)) * 0.8, MONO, False)
        # B : 95 cases (21.8–29.6)
        gb = ease(seg(t, 21.7, 22.1)) * (1 - seg(t, 29.4, 29.8))
        if gb > 0:
            words(f, 'Le code est découpé', 430, 80, 21.8, INK, t_out=29.3)
            words(f, 'en cases égales.', 540, 80, 22.3, SPARK, t_out=29.3)
            m = 8; x0 = W/2 - 95 * m / 2
            barcode(f, W/2, 760, m, 300, gb, digits=False)
            p = seg(t, 23.0, 27.0)
            n = int(round(95 * ease_io(p)))
            for i in range(n):
                f.rect(x0 + i * m + 1, 1150, m - 2, 26, SPARK if BITS[i] == '1' else CAPITAL, gb, 2)
            f.text(f'{n}', W/2, 1340, 150, SPARK, gb * ease(seg(t, 23.0, 23.2)), MONO, True)
            f.text('cases, noires ou blanches', W/2, 1440, 48, INK, gb * ease(seg(t, 27.1, 27.4)), DISPLAY, True)

    # S5 — la réponse (30–36)
    if 29.9 <= t < 36.0:
        o = 35.6
        a = ease(seg(t, 30.3, 30.6)) * (1 - seg(t, o, o + 0.3))
        words(f, 'Un chiffre =', 520, 80, 30.0, MUTED, t_out=o)
        big_center(f, '7', 820, 300, SPARK, a, bump(t, 30.3, 0.18), font=DISPLAY)
        words(f, 'cases.', 960, 96, 31.0, INK, t_out=o)
        # zoom : 0001101 = 0
        b = L[0]; s = 92; x0 = W/2 - 7 * s / 2
        za = a * ease(seg(t, 32.0, 32.3))
        f.rect(x0 - 14, 1046, 7 * s + 24, 188, INK, za, 12)
        for i, ch in enumerate(b):
            f.rect(x0 + i * s, 1060, s - 4, 160, DEEP if ch == '1' else INK, za, 6)
            f.text(ch, x0 + i * s + s / 2 - 2, 1290, 44, SPARK if ch == '1' else MUTED,
                   a * ease(seg(t, 32.4 + 0.08 * i, 32.6 + 0.08 * i)), MONO, True)
        f.text('2 barres + 2 espaces = « 0 »', W/2, 1410, 50, INK, a * ease(seg(t, 33.4, 33.7)), DISPLAY, True)

    # S6 — le retournement (36–48.4)
    if 36.0 <= t < 48.4:
        words(f, 'Le secret ?', 900, 116, 36.1, SPARK, t_out=37.9)
        # A : chiffre de contrôle (38.1–43.6)
        oa = 43.6
        ga = ease(seg(t, 38.1, 38.5)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Le dernier chiffre', 430, 80, 38.2, INK, t_out=oa)
            words(f, 'vérifie les autres.', 540, 80, 38.6, SPARK, t_out=oa)
            s = 70; x0 = W/2 - 13 * s / 2 + s / 2
            for k, ch in enumerate(CODE):
                ka = ga * ease(seg(t, 39.0 + 0.04 * k, 39.2 + 0.04 * k))
                last = (k == 12)
                f.rect(x0 + k * s - 30, 700, 60, 90, SPARK if last else OCEAN, ka, 10)
                f.text(ch, x0 + k * s, 768, 56, DEEP if last else INK, ka, MONO, True)
                if not last:
                    f.text('×3' if k % 2 else '×1', x0 + k * s, 850, 30, MUTED,
                           ka * ease(seg(t, 39.8 + 0.04 * k, 40.0 + 0.04 * k)), MONO, True)
            tot = int(89 * ease(seg(t, 40.4, 41.4)))
            f.text(f'total : {tot}', W/2, 1000, 72, INK, ga * ease(seg(t, 40.4, 40.6)), MONO, True)
            f.text('90 − 89 = 1', W/2, 1120, 80, SPARK, ga * ease(seg(t, 41.6, 41.9)), MONO, True)
            f.text('Un chiffre mal lu ?', W/2, 1300, 54, INK, ga * ease(seg(t, 42.0, 42.3)), DISPLAY, True)
            f.text('Le calcul tombe faux. Pas de bip.', W/2, 1380, 50, RED, ga * ease(seg(t, 42.4, 42.7)), DISPLAY, True)
        # B : les deux sens (43.9–47.9)
        ob = 47.9
        gb = ease(seg(t, 43.8, 44.2)) * (1 - seg(t, ob, ob + 0.3))
        if gb > 0:
            words(f, 'Et le sens ?', 430, 84, 43.9, INK, t_out=ob)
            words(f, 'Chaque moitié se trahit.', 545, 70, 44.3, SPARK, t_out=ob)
            s = 70
            for row, (lab, b, nb, yy) in enumerate([('gauche', L[0], 3, 720), ('droite', R[0], 4, 1060)]):
                ra = gb * ease(seg(t, 44.8 + 0.6 * row, 45.1 + 0.6 * row))
                x0 = W/2 - 7 * s / 2
                f.text(lab, W/2, yy - 30, 40, MUTED, ra, MONO, True)
                f.rect(x0 - 12, yy - 12, 7 * s + 20, 144, INK, ra, 10)
                for i, ch in enumerate(b):
                    f.rect(x0 + i * s, yy, s - 4, 120, DEEP if ch == '1' else INK, ra, 6)
                f.text(f'{nb} cases noires : {"impair" if nb % 2 else "pair"}', W/2, yy + 180, 46,
                       SPARK if row == 0 else INK, ra * ease(seg(t, 45.6 + 0.6 * row, 45.9 + 0.6 * row)), DISPLAY, True)
            f.text('La machine sait où est le début.', W/2, 1400, 48, INK, gb * ease(seg(t, 46.4, 46.7)), DISPLAY, True)

    # S7 — l'escalade (48–56.4)
    if 48.0 <= t < 56.4:
        o1 = 52.1
        g1 = ease(seg(t, 48.1, 48.4)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, '26 juin 1974,', 430, 80, 48.1, SPARK, t_out=o1)
            words(f, 'premier bip en caisse.', 540, 72, 48.6, INK, t_out=o1)
            # paquet de chewing-gum qui glisse sous le laser
            px = lerp(-200, W/2, ease(seg(t, 48.8, 49.8)))
            f.rect(px - 210, 760, 420, 240, SPARK, g1, 20)
            f.rect(px - 190, 780, 380, 200, '#f6c862', g1, 14)
            f.text('GUM', px, 900, 70, DEEP, g1, DISPLAY, True)
            laser(f, 120, 960, 880, g1 * ease(seg(t, 49.8, 50.0)) * (0.7 + 0.3 * math.sin(t * 20)), t)
            f.text('Wrigley’s, Troy (Ohio), États-Unis', W/2, 1110, 44, INK, g1 * ease(seg(t, 50.0, 50.3)), DISPLAY, True)
            f.text('Aujourd’hui : des milliards par jour.', W/2, 1240, 50, SPARK, g1 * ease(seg(t, 50.6, 50.9)), DISPLAY, True)
            # bips qui se multiplient
            for i in range(24):
                tk = 50.9 + 0.04 * i
                ba = g1 * ease(seg(t, tk, tk + 0.15)) * 0.8
                f.circle(160 + (i % 12) * 69, 1360 + (i // 12) * 60, 12, SPARK if i % 3 else INK, ba)
        o2 = 55.9
        g2 = ease(seg(t, 52.3, 52.6)) * (1 - seg(t, o2, o2 + 0.3))
        if g2 > 0:
            words(f, 'Ça commence par 3 ?', 430, 76, 52.4, INK, t_out=o2)
            words(f, 'Codé en France.', 540, 84, 52.9, SPARK, t_out=o2)
            for i, ch in enumerate('300 → 379'):
                f.text(ch, W/2 - 4 * 62 + i * 62, 840, 96, SPARK if ch.isdigit() else MUTED,
                       g2 * ease(seg(t, 53.2 + 0.05 * i, 53.4 + 0.05 * i)), MONO, True)
            f.text('Mais pas forcément', W/2, 1060, 60, INK, g2 * ease(seg(t, 54.0, 54.3)), DISPLAY, True)
            f.text('fabriqué en France.', W/2, 1150, 60, RED, g2 * ease(seg(t, 54.3, 54.6)), DISPLAY, True)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        a = ease(seg(t, 56.1, 56.4))
        barcode(f, W/2, 640, 5, 200, a, reveal=ease(seg(t, 56.1, 56.9)))
        words(f, 'Un code-barres n’est pas un dessin.', 1010, 58, 56.3, INK)
        words(f, 'C’est un calcul.', 1110, 72, 57.8, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(240, 1200, 600, 150, OCEAN, a, 28)
        pa = 0.5 + 0.5 * math.sin((t - 60) * 3)
        f.rect(240, 1200, 600, 150, SPARK, a * 0.25 * pa, 28)
        f.text('Abonne-toi.', W/2, 1295, 62, INK, a)


def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    ev += [(0.15, ding(1318, amp=0.18))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (12.5, 29.6, 47.9, 55.9)]
    ev += [(11.0, pop(520))]
    ev += [(30.3, ding(1046, amp=0.28)), (36.1, pop(300, 0.15))]
    ev += [(41.6, clink())]
    ev += [(56.3, pop(440)), (60.0, ding(784, amp=0.22))]
    return ev
