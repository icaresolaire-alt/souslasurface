"""Pourquoi un bout de papier vaut 100 € (la valeur de la monnaie). Même structure que le pilote.

Sources :
- Coût de fabrication : Bankenverband (Association des banques allemandes), « What are euro banknotes made
  out of? » : « a euro note only costs an average of eight cents to manufacture » ; « made of pure cotton ».
  Der Tagesspiegel, « Was kostet eigentlich ein Geldschein? » (27 juillet 2015), d'après la BCE : 5 € ≈ 7
  centimes, 10 € ≈ 9 centimes, 500 € au plus 16 centimes ; papier de pure fibre de coton.
  Affiché : « quelques centimes », « ≈ 8 centimes en moyenne ».
- Bretton Woods et 1971 : Federal Reserve History, « Nixon Ends Convertibility of U.S. Dollars to Gold »
  (44 pays, Bretton Woods, 1944 ; dollar convertible en or à 35 $ l'once ; 15 août 1971, fermeture du
  « guichet de l'or ») ; Wikipedia « Nixon shock » (mêmes faits).
- Cours légal : Banque de France, « L'économie en bref : la monnaie » (eeb_monnaie.pdf, 2024) : la banque
  centrale a le monopole d'émission des billets, « qui seule a cours légal ».
- 1923 : Wikipedia « Hyperinflation in the Weimar Republic » (via Wikiwand) : 4,2 marks par dollar en 1914 ;
  « By November 1923, one US dollar was worth 4,210,500,000,000 marks » ; Historisches Museum Basel (4,2
  billions de marks pour un dollar en novembre 1923) ; Schoolmouv et AuCOFFRE (4 200 milliards de marks).
- Monnaie scripturale : Banque de France, eeb_monnaie.pdf : 91 % de la monnaie en circulation en zone euro
  en 2020 (« plus de 90 % ») ; Banque de France, « Eco en bref : masse monétaire » (août 2026) : déc. 2025,
  billets et pièces 1 588 Md€, M3 17 231 Md€, soit 9,2 %. Affiché : 9 euros sur 10 ne sont pas des billets.
"""
import math
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
COVER = dict(tag='Argent', l1='Pourquoi un bout de papier', l2='vaut vraiment 100 €')

NOTE = '#5f9e8a'
GOLD = '#d9a93a'


def note(f, x, y, s, a, rot=0.0, label='100 €', fade=1.0, icon='€'):
    """Billet stylisé."""
    if a <= 0: return
    c = f.c; c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    w, h = 420, 220
    f.rect(-w/2, -h/2, w, h, NOTE, a * fade, 18)
    f.rect(-w/2 + 16, -h/2 + 16, w - 32, h - 32, '#ffffff', a * 0.10, 12)
    f.circle(-w/2 + 90, 0, 62, '#ffffff', a * 0.16)
    f.text(icon, -w/2 + 90, 26, 76, DEEP, a * 0.6, DISPLAY, True)
    f.text(label, 55, 26, 72, DEEP, a, MONO, True)
    c.restore()


def bar(f, x, y, s, a, shine=0.0):
    """Lingot d'or (trapèze)."""
    if a <= 0: return
    c = f.c; c.save(); c.translate(x, y); c.scale(s, s)
    f.color(GOLD, a)
    c.move_to(-150, 70); c.line_to(150, 70); c.line_to(105, -70); c.line_to(-105, -70); c.close_path(); c.fill()
    f.color('#f6d77a', a * 0.8)
    c.move_to(-105, -70); c.line_to(105, -70); c.line_to(90, -45); c.line_to(-90, -45); c.close_path(); c.fill()
    if 0 < shine < 1:
        c.move_to(-150, 70); c.line_to(150, 70); c.line_to(105, -70); c.line_to(-105, -70); c.close_path(); c.clip()
        xx = -190 + 380 * shine
        f.color('#ffffff', a * 0.35)
        c.move_to(xx - 20, 70); c.line_to(xx + 20, 70); c.line_to(xx + 50, -70); c.line_to(xx + 10, -70)
        c.close_path(); c.fill()
    c.restore()


def person(f, x, y, s, a, col=INK, label=''):
    if a <= 0: return
    c = f.c; c.save(); c.translate(x, y); c.scale(s, s)
    f.circle(0, -70, 38, col, a)
    f.rect(-55, -20, 110, 110, col, a, 40)
    c.restore()
    if label: f.text(label, x, y + 140 * s, 34, MUTED, a, DISPLAY, True)


def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')
    c = f.c

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.8, 30.2))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Qui donne sa valeur au billet ?', W/2, 296, 42, SPARK, ha)

    # S1 — accroche (0–4) : le billet tombe et tourne dès la première image
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        words(f, 'Ce billet de 100 €', 470, 88, 0.05, INK, t_out=o)
        words(f, 'coûte quelques centimes', 590, 80, 0.7, INK, t_out=o)
        words(f, 'à fabriquer.', 710, 92, 1.3, SPARK, t_out=o)
        p = seg(t, 0.0, 1.0)
        yb = 1080 - 380 * (1 - p) ** 2
        note(f, W/2, yb, 1.4, fo, -0.15 + 0.15 * p)
        f.text('≈ 8 centimes en moyenne', W/2, 1360, 44, MUTED, fo * ease(seg(t, 2.0, 2.3)), MONO, False)

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.0:
        o1 = 7.4
        g1 = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'C’est du coton', 470, 92, 4.2, INK, t_out=o1)
            words(f, 'et de l’encre.', 590, 92, 4.8, SPARK, t_out=o1)
            note(f, W/2, 1000, 1.5, g1, 0.04 * math.sin((t - 4) * 2), fade=1 - 0.4 * ease(seg(t, 5.4, 6.4)))
            f.text('papier de pure fibre de coton', W/2, 1300, 40, MUTED, g1 * ease(seg(t, 5.6, 5.9)), MONO, False)
        o2 = 10.7
        g2 = ease(seg(t, 7.6, 8.0)) * (1 - seg(t, o2, o2 + 0.3))
        if g2 > 0:
            words(f, 'Ton intuition :', 500, 72, 7.7, MUTED, t_out=o2)
            words(f, 'il y a de l’or derrière.', 630, 84, 8.2, INK, t_out=o2)
            note(f, W/2, 960, 1.0, g2, 0.03 * math.sin((t - 8) * 3))
            bar(f, W/2, 1240, 0.9, g2 * ease(seg(t, 8.9, 9.2)), seg(t, 9.2, 10.2))

    # S3 — la question (10.9–13.6)
    if 10.9 <= t < 13.6:
        words(f, 'Alors, qui lui donne', 820, 96, 11.0, INK, t_out=12.5)
        words(f, 'sa valeur ?', 950, 110, 11.4, SPARK, t_out=12.5)

    # S4 — la preuve (13.5–30)
    if 13.4 <= t < 30.0:
        # A : 1944, le dollar vaut de l'or (13.6–20.6)
        oa = 20.6
        ga = ease(seg(t, 13.5, 13.9)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'En 1944, le dollar', 440, 84, 13.6, INK, t_out=oa)
            words(f, 'est promis en or.', 550, 84, 14.2, SPARK, t_out=oa)
            p = ease_io(seg(t, 15.0, 16.6))
            big_center(f, f'{int(round(35 * p))} $', 840, 150, INK, ga * ease(seg(t, 14.9, 15.2)))
            f.text('=', W/2, 960, 90, MUTED, ga * ease(seg(t, 16.4, 16.7)), MONO, True)
            bar(f, W/2, 1100, 0.9, ga * ease(seg(t, 16.6, 16.9)), seg(t, 17.0, 18.0))
            f.text('1 once d’or (31 g)', W/2, 1270, 44, SPARK, ga * ease(seg(t, 17.0, 17.3)), MONO, True)
            f.text('accords de Bretton Woods, 44 pays', W/2, 1380, 34, MUTED, ga * ease(seg(t, 17.8, 18.1)), MONO, False)
        # B : 15 août 1971, fini (20.8–29.6)
        gb = ease(seg(t, 20.8, 21.2)) * (1 - seg(t, 29.4, 29.8))
        if gb > 0:
            # calendrier qui défile jusqu'à 1971
            p = ease_io(seg(t, 21.2, 23.6))
            year = int(1944 + 27 * p)
            f.rect(290, 400, 500, 360, OCEAN, gb, 30)
            f.rect(290, 400, 500, 90, RED, gb, 30)
            f.rect(290, 460, 500, 30, RED, gb, 0)
            f.text(str(year), W/2, 465, 54, INK, gb, MONO, True)
            day = gb * ease(seg(t, 23.6, 23.9))
            c.save(); c.translate(W/2, 640); s = bump(t, 23.6, 0.2); c.scale(s, s)
            f.text('15 août', 0, 0, 96, INK, day, DISPLAY, True); c.restore()
            words(f, 'Le président Nixon', 900, 76, 24.4, INK, t_out=29.3)
            words(f, 'ferme le guichet de l’or.', 1000, 76, 25.0, SPARK, t_out=29.3)
            ab = gb * ease(seg(t, 25.8, 26.1))
            bar(f, W/2, 1240, 0.8, ab * (1 - 0.6 * seg(t, 26.6, 27.4)))
            k = ease(seg(t, 26.6, 27.2))
            if k > 0:
                f.line([(W/2 - 160, 1150), (W/2 - 160 + 320 * k, 1150 + 180 * k)], RED, ab, 14)
                f.line([(W/2 + 160, 1150), (W/2 + 160 - 320 * k, 1150 + 180 * k)], RED, ab, 14)
            f.text('le dollar ne s’échange plus contre de l’or', W/2, 1420, 34, MUTED,
                   gb * ease(seg(t, 27.4, 27.7)), MONO, False)

    # S5 — la réponse (30–36)
    if 29.9 <= t < 36.0:
        o = 35.6
        a = ease(seg(t, 30.3, 30.6)) * (1 - seg(t, o, o + 0.3))
        big_center(f, '0 g', 820, 260, SPARK, a, bump(t, 30.3, 0.18))
        words(f, 'd’or derrière', 1000, 76, 31.0, INK, t_out=o)
        words(f, 'ton billet.', 1110, 76, 31.5, INK, t_out=o)
        words(f, 'Ton euro ne s’échange', 1280, 60, 33.0, MUTED, t_out=o)
        words(f, 'contre rien du tout.', 1360, 60, 33.4, MUTED, t_out=o)

    # S6 — le retournement (36–48.4)
    if 36.0 <= t < 48.4:
        words(f, 'Le secret ?', 900, 150, 36.1, SPARK, t_out=37.9)
        # A : tout le monde l'accepte (38.1–42.6)
        oa = 42.6
        ga = ease(seg(t, 38.1, 38.5)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Il vaut parce que', 440, 84, 38.2, INK, t_out=oa)
            words(f, 'tout le monde l’accepte.', 550, 78, 38.7, SPARK, t_out=oa)
            xs = (190, 430, 670, 890)
            labs = ('toi', 'boulanger', 'meunier', 'fermier')
            for i, (x, lb) in enumerate(zip(xs, labs)):
                person(f, x, 1000, 0.9, ga * ease(seg(t, 39.2 + 0.15 * i, 39.5 + 0.15 * i)), INK if i else SPARK, lb)
            p = seg(t, 40.0, 42.3) * 3
            i = min(int(p), 2); q = ease_io(p - i)
            nx = xs[i] + (xs[i + 1] - xs[i]) * q
            note(f, nx, 820 - 60 * math.sin(math.pi * q), 0.32, ga * ease(seg(t, 39.8, 40.0)), 0.2 * math.sin(math.pi * q))
            f.text('et l’État lui donne cours légal', W/2, 1300, 38, MUTED, ga * ease(seg(t, 40.6, 40.9)), MONO, False)
        # B : quand la confiance part, 1923 (42.9–47.9)
        ob = 47.9
        gb = ease(seg(t, 42.8, 43.2)) * (1 - seg(t, ob, ob + 0.3))
        if gb > 0:
            words(f, 'Si la confiance part,', 440, 80, 42.9, INK, t_out=ob)
            words(f, 'il ne vaut plus rien.', 550, 80, 43.5, RED, t_out=ob)
            f.text('Allemagne, 1 dollar =', W/2, 760, 50, MUTED, gb * ease(seg(t, 44.0, 44.3)), DISPLAY, True)
            a0 = gb * ease(seg(t, 44.0, 44.3))
            p = seg(t, 44.6, 46.6)
            if p <= 0:
                f.text('1914', W/2, 860, 46, SPARK, a0, MONO, True)
                big_center(f, '4,2 marks', 1010, 96, INK, a0)
            else:
                v = 4.2 * (1e12 / 4.2) ** (p ** 1.6) if p < 1 else 4.2e12
                if v < 1e9: s = fmt_int(v) + ' marks'
                else: s = f'{v/1e9:,.0f}'.replace(',', ' ') + ' milliards'
                f.text('nov. 1923' if p >= 1 else '…', W/2, 860, 46, SPARK, a0, MONO, True)
                big_center(f, s, 1010, 72 if v >= 1e9 else 88, RED if p >= 1 else INK, a0, bump(t, 46.6, 0.15))
                if v >= 1e9: f.text('de marks', W/2, 1090, 46, INK, a0, MONO, True)
            # tas de billets qui grandit
            n = int(1 + 12 * ease(p))
            for k in range(n):
                note(f, W/2 + 40 * math.sin(k * 2.1), 1440 - k * 14, 0.42, gb * 0.95, 0.15 * math.sin(k * 1.7), 'mark', icon='M')

    # S7 — l'escalade (48–56.4) : 9 euros sur 10 ne sont même pas des billets
    if 48.0 <= t < 56.4:
        o = 55.9
        ga = ease(seg(t, 48.1, 48.4)) * (1 - seg(t, o, o + 0.3))
        if ga > 0:
            words(f, 'Et 9 euros sur 10', 430, 84, 48.1, INK, t_out=o)
            words(f, 'ne sont même pas des billets.', 540, 64, 48.9, SPARK, t_out=o)
            for k in range(10):
                col, row = k % 2, k // 2
                x = W/2 - 210 + col * 420; y = 720 + row * 130
                ak = ga * ease(seg(t, 49.8 + 0.08 * k, 50.1 + 0.08 * k))
                q = ease(seg(t, 51.4 + 0.15 * k, 51.8 + 0.15 * k)) if k > 0 else 0.0
                note(f, x, y, 0.5, ak * (1 - q))
                if q > 0:
                    f.rect(x - 105, y - 55, 210, 110, LINE, ak * q, 16)
                    f.text('0101', x, y + 18, 50, SPARK, ak * q, MONO, True)
            f.text('juste des chiffres sur des comptes', W/2, 1440, 38, MUTED,
                   ga * ease(seg(t, 53.4, 53.7)), MONO, False)
            f.text('(zone euro, Banque de France)', W/2, 1500, 30, MUTED,
                   ga * ease(seg(t, 53.4, 53.7)), MONO, False)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        a = ease(seg(t, 56.1, 56.4))
        note(f, W/2, 660, 1.1 * bump(t, 56.1, 0.15), a, 0.05 * math.sin((t - 56) * 2))
        words(f, 'Un billet ne vaut pas son papier.', 900, 60, 56.3, INK)
        words(f, 'Il vaut ce qu’on y croit.', 1010, 74, 57.6, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(240, 1160, 600, 150, OCEAN, a, 28)
        pa = 0.5 + 0.5 * math.sin((t - 60) * 3)
        f.rect(240, 1160, 600, 150, SPARK, a * 0.25 * pa, 28)
        f.text('Abonne-toi.', W/2, 1255, 62, INK, a)


def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    ev += [(0.15, pop(440, 0.09)), (1.9, ding(880, amp=0.18))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (12.5, 29.6, 47.9, 55.9)]
    ev += [(11.0, pop(520))]
    ev += [(16.6, clink(1500))]
    ev += [(23.6, ding(784, amp=0.2))]
    ev += [(30.3, ding(1046, amp=0.28)), (36.1, pop(300, 0.15))]
    ev += [(44.4, rise(2.2, 300, 900, 0.07))]
    ev += [(51.4, ding(784, amp=0.18))]
    ev += [(56.3, pop(440)), (60.0, ding(784, amp=0.22))]
    return ev
