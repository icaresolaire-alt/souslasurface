"""L'effet de simple exposition : on aime ce qu'on a déjà vu. Même structure que le pilote.

Sources :
- Tour Eiffel : JSTOR Daily, E. Zarevich, 17 févr. 2023, « The Artists Who Hated the Eiffel Tower » (lettre de
  protestation publiée le 14 février 1887 ; Meissonier, Garnier, Bouguereau, Gounod…) ; History.com,
  N. K. Nittle, « How the Eiffel Tower Survived » (maj 17 août 2026 : lettre dans Le Temps, « the useless and
  monstrous Eiffel Tower », Maupassant, Garnier ; permis de 20 ans ; construite pour l'Exposition de 1889) ;
  toureiffel.paris « The artists who protested the Eiffel Tower » (une quarantaine de signataires, Le Temps,
  « useless and monstrous », Maupassant, Gounod, Garnier ; droits pour 20 ans).
- Zajonc 1968 (« Attitudinal effects of mere exposure ») : Atticus Li, « Mere exposure effect » (mots turcs
  inventés « iktitaf », « biwojni », « afworbu », de 1 à 25 présentations, « bon ou mauvais ? » ; idéogrammes
  chinois ; photos de visages) ; Changing Minds « Mere exposure » (idéogrammes montrés de 1 à 25 fois : plus
  vus, sens jugé plus positif) ; Wikipedia « Mere-exposure effect » (symboles déjà vus jugés plus positifs).
  Barres affichées en schéma, sans valeur.
- 208 expériences : Bornstein, Psychological Bulletin 106(2), 1989, p. 265-289, d'après Atticus Li (« 208
  separate experiments », 1968-1987) et Wikipedia (« A meta-analysis of 208 experiments … robust and reliable »).
- Mécanisme : Wikipedia (Zajonc : un stimulus nouveau provoque d'abord méfiance et évitement, chaque exposition
  suivante moins de peur ; l'exposition répétée augmente la fluidité perceptive, qui augmente l'affect positif).
- Miroir : Mita, Dermer et Knight, JPSP 35(8), 1977, p. 597-601 : Fstoppers (33 femmes et une amie proche
  chacune ; elles préfèrent leur image miroir, leurs amies la vraie photo) ; Gizmodo, R. Gonzalez, 22 oct. 2013
  et Psychology Today, sept. 2022 (concordants).
- Plafond : Wikipedia (effet maximal en 10 à 20 présentations, puis l'appréciation peut baisser, courbe en U
  inversé ; exemple de la chanson) ; Changing Minds (Miller 1976 : au-delà de 200 expositions, réactions
  négatives). Courbe affichée en schéma.
- Visages, mots qui défilent et courbes illustratifs.
"""
import math
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro (ep044 précédent).
COVER = dict(tag='Psychologie', l1='Pourquoi tu finis par aimer', l2='ce que tu détestais')

SKIN = '#e9c9a3'


def tower(f, cx, base, h, a, prog=1.0, col=SPARK, wd=7):
    """Tour Eiffel stylisée, tracée de bas en haut selon prog (0 à 1)."""
    if a <= 0 or prog <= 0: return
    top = base - h
    def x_at(y, side):
        # profil courbe : large en bas, fin en haut
        u = (base - y) / h
        half = h * 0.34 * (1 - u) ** 2.2 + h * 0.012
        return cx + side * half
    ymax = base - h * prog
    n = 40
    for side in (-1, 1):
        pts = []
        for i in range(n + 1):
            y = base - h * i / n
            if y < ymax: break
            pts.append((x_at(y, side), y))
        if len(pts) > 1:
            f.line(pts, col, a, wd)
    # plateformes
    for u, extra in ((0.17, 0.05), (0.42, 0.03), (0.78, 0.015)):
        y = base - h * u
        if y >= ymax:
            f.line([(x_at(y, -1) - h * extra, y), (x_at(y, 1) + h * extra, y)], col, a, wd + 2)
    # arche
    if prog > 0.15:
        c = f.c; c.save(); c.translate(cx, base); c.scale(h * 0.2, h * 0.12)
        c.arc_negative(0, 0, 1, 0, math.pi); c.restore()
        c.set_line_width(wd); f.color(col, a); c.stroke()
    # croisillons
    for k in range(10):
        y1 = base - h * (0.05 + 0.07 * k); y2 = y1 - h * 0.07
        if y2 < ymax or k > 9: break
        f.line([(x_at(y1, -1), y1), (x_at(y2, 1), y2)], col, a * 0.55, wd * 0.5)
        f.line([(x_at(y1, 1), y1), (x_at(y2, -1), y2)], col, a * 0.55, wd * 0.5)
    if prog >= 1:
        f.line([(cx, top), (cx, top - h * 0.06)], col, a, wd * 0.7)


def face(f, x, y, r, a, flip=1.0, col=SKIN, ring=None):
    """Visage asymétrique (mèche, sourcil, grain de beauté) ; flip de -1 à 1 = miroir."""
    if a <= 0: return
    c = f.c
    c.save(); c.translate(x, y); c.scale(flip if abs(flip) > 0.02 else 0.02, 1)
    if ring:
        f.circle(0, 0, r + 12, ring, a * 0.9)
    f.circle(0, 0, r, col, a)
    # mèche de cheveux d'un seul côté
    c.move_to(-r * 0.95, -r * 0.2)
    c.curve_to(-r * 0.9, -r * 1.25, r * 0.6, -r * 1.25, r * 0.95, -r * 0.35)
    c.curve_to(r * 0.4, -r * 0.75, -r * 0.2, -r * 0.55, -r * 0.95, -r * 0.2)
    f.color('#5a3a26', a); c.fill()
    for s in (-1, 1):
        f.circle(s * r * 0.36, -r * 0.08, r * 0.08, DEEP, a)
    # sourcil levé d'un côté
    f.line([(-r * 0.5, -r * 0.3), (-r * 0.22, -r * 0.34)], DEEP, a, max(3, r * 0.06))
    f.line([(r * 0.22, -r * 0.42), (r * 0.5, -r * 0.5)], DEEP, a, max(3, r * 0.06))
    # sourire en coin
    f.line([(-r * 0.3, r * 0.38), (0, r * 0.45), (r * 0.32, r * 0.3)], '#7a3b35', a, max(3, r * 0.07))
    # grain de beauté
    f.circle(r * 0.5, r * 0.15, r * 0.05, '#6b4430', a)
    c.restore()


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


def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')
    c = f.c

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.8, 30.2))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Pourquoi on finit par aimer ?', W/2, 296, 44, SPARK, ha)

    # S1 — accroche (0–4) : la tour se dessine dès la première image
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        words(f, 'Paris a détesté', 460, 80, 0.05, INK, t_out=o)
        words(f, 'la tour Eiffel.', 575, 88, 1.0, SPARK, t_out=o)
        tower(f, W/2, 1450, 700, fo, ease_io(seg(t, 0.0, 2.6)))

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.0:
        o1 = 7.4
        g1 = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, '« Inutile', 460, 92, 4.2, INK, t_out=o1)
            words(f, 'et monstrueuse »', 570, 92, 4.6, RED, t_out=o1)
            # page de journal
            jy = 780 + 20 * (1 - ease(seg(t, 4.4, 4.9)))
            f.rect(240, jy, 600, 520, INK, g1 * 0.92, 10)
            f.text('LE TEMPS', W/2, jy + 90, 66, DEEP, g1, DISPLAY, True)
            f.line([(280, jy + 120), (800, jy + 120)], DEEP, g1, 4)
            for k in range(7):
                ww = 520 if k % 3 else 380
                f.rect(280, jy + 160 + 46 * k, ww * ease(seg(t, 5.0 + 0.1 * k, 5.4 + 0.1 * k)), 18, MUTED, g1, 6)
            f.text('14 février 1887', W/2, 1400, 52, SPARK, g1 * ease(seg(t, 5.4, 5.7)), MONO, True)
            f.text('Maupassant, Garnier, Gounod…', W/2, 1480, 38, MUTED, g1 * ease(seg(t, 5.9, 6.2)), MONO, False)
        o2 = 10.7
        g2 = ease(seg(t, 7.6, 8.0)) * (1 - seg(t, o2, o2 + 0.3))
        if g2 > 0:
            words(f, 'Aujourd’hui,', 460, 76, 7.7, MUTED, t_out=o2)
            words(f, 'c’est le symbole de Paris.', 570, 70, 8.1, SPARK, t_out=o2)
            tower(f, W/2, 1450, 640, g2, 1.0)
            for k in range(14):  # petits éclats tout autour
                ang = k / 14 * 2 * math.pi + t * 0.4
                rr = 380 + 30 * math.sin(t * 3 + k)
                f.circle(W/2 + rr * math.cos(ang), 1130 + rr * 0.8 * math.sin(ang), 8, SPARK,
                         g2 * ease(seg(t, 8.6, 9.0)) * (0.5 + 0.5 * math.sin(t * 4 + k)))

    # S3 — la question (10.9–13.6)
    if 10.9 <= t < 13.6:
        words(f, 'Pourquoi on finit', 820, 84, 11.0, INK, t_out=12.5)
        words(f, 'par l’aimer ?', 940, 100, 11.4, SPARK, t_out=12.5)

    # S4 — la preuve (13.5–30)
    if 13.4 <= t < 30.0:
        # A : des mots inventés, montrés plus ou moins souvent (13.6–21.6)
        oa = 21.6
        ga = ease(seg(t, 13.5, 13.9)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, '1968. Zajonc montre', 430, 72, 13.6, INK, t_out=oa)
            words(f, 'des mots inventés.', 540, 80, 14.1, SPARK, t_out=oa)
            wl = ['IKTITAF', 'AFWORBU', 'BIWOJNI']
            idx = int(max(0, t - 15.0) * 4) % 3
            flash = 0.55 + 0.45 * math.cos((t - 15.0) * 4 * 2 * math.pi)
            f.rect(160, 760, 760, 220, OCEAN, ga * ease(seg(t, 14.8, 15.1)), 30)
            f.text(wl[idx], W/2, 905, 110, INK, ga * ease(seg(t, 15.0, 15.2)) * flash, MONO, True)
            n = int(1 + 24 * ease_io(seg(t, 15.4, 19.0)))
            f.text(f'vu {n} fois', W/2, 1110, 64, SPARK, ga * ease(seg(t, 15.4, 15.7)), MONO, True)
            words(f, 'Puis : « bon ou mauvais ? »', 1300, 56, 19.4, INK, t_out=oa)
        # B : plus on l'a vu, plus on le juge bon (21.8–29.6)
        gb = ease(seg(t, 21.7, 22.1)) * (1 - seg(t, 29.4, 29.8))
        if gb > 0:
            words(f, 'Plus le mot est vu,', 430, 76, 21.8, INK, t_out=29.3)
            words(f, 'plus il semble « bon ».', 540, 76, 22.3, SPARK, t_out=29.3)
            base = 1300
            data = [('1', 0.25), ('2', 0.35), ('5', 0.5), ('10', 0.68), ('25', 0.9)]
            for i, (lab, v) in enumerate(data):
                ts = 23.0 + 0.5 * i
                x = 230 + 155 * i
                ia = gb * ease(seg(t, ts, ts + 0.3))
                h = 520 * v * ease_io(seg(t, ts, ts + 0.8))
                f.rect(x - 55, base - h, 110, h, SPARK if i == 4 else MUTED, ia, 14)
                f.text(lab, x, base + 64, 50, INK, ia, MONO, True)
            f.line([(140, base), (940, base)], LINE, gb, 6)
            f.text('nombre de fois vu', W/2, 1440, 40, MUTED, gb * ease(seg(t, 25.4, 25.7)), MONO, False)
            f.text('(schéma)', W/2, 1500, 32, MUTED, gb * ease(seg(t, 25.8, 26.1)) * 0.8, MONO, False)

    # S5 — la réponse (30–36)
    if 29.9 <= t < 36.0:
        o = 35.6
        a = ease(seg(t, 30.3, 30.6)) * (1 - seg(t, o, o + 0.3))
        words(f, 'Effet confirmé par', 600, 70, 30.0, MUTED, t_out=o)
        big_center(f, '208', 880, 280, SPARK, a, bump(t, 30.3, 0.18), font=DISPLAY)
        words(f, 'expériences.', 1060, 80, 31.0, INK, t_out=o)
        words(f, 'synthèse de R. Bornstein, 1989', 1200, 38, 32.5, MUTED, t_out=o, font=MONO, bold=False)

    # S6 — le retournement (36–48.4)
    if 36.0 <= t < 48.4:
        words(f, 'Le secret ?', 900, 120, 36.1, SPARK, t_out=37.9)
        # A : le nouveau inquiète, le connu rassure (38.1–42.6)
        oa = 42.6
        ga = ease(seg(t, 38.1, 38.5)) * (1 - seg(t, oa, oa + 0.3))
        if ga > 0:
            words(f, 'Le nouveau', 440, 84, 38.2, INK, t_out=oa)
            words(f, 'inquiète d’abord.', 550, 84, 38.6, RED, t_out=oa)
            # jauge méfiance qui descend à chaque rencontre
            for k in range(5):
                tk = 39.4 + 0.5 * k
                ka = ga * ease(seg(t, tk, tk + 0.25))
                f.circle(250 + 145 * k, 800, 46, SPARK if k == 4 else CAPITAL, ka)
                f.text(str(k + 1), 250 + 145 * k, 818, 46, DEEP if k == 4 else INK, ka, MONO, True)
            lvl = 1 - 0.8 * ease_io(seg(t, 39.4, 41.8))
            f.rect(240, 940, 600, 60, LINE, ga, 30)
            f.rect(240, 940, 600 * lvl, 60, lerp(0, 1, lvl) > 0.5 and RED or EARTH, ga, 30)
            f.text('méfiance', W/2, 1070, 44, MUTED, ga, MONO, False)
            words(f, 'Rien de grave ?', 1230, 64, 40.6, INK, t_out=oa)
            words(f, 'Ton cerveau se détend.', 1330, 64, 41.2, SPARK, t_out=oa)
        # B : le miroir (42.9–47.9)
        ob = 47.9
        gb = ease(seg(t, 42.8, 43.2)) * (1 - seg(t, ob, ob + 0.3))
        if gb > 0:
            words(f, 'Tu préfères ton reflet', 430, 72, 42.9, INK, t_out=ob)
            words(f, 'à ta vraie photo.', 540, 80, 43.4, SPARK, t_out=ob)
            # le visage se retourne comme dans un miroir
            fl = math.cos(math.pi * ease_io(seg(t, 44.2, 45.0)))
            face(f, W/2 - 220, 920, 150, gb, fl, ring=SPARK)
            face(f, W/2 + 220, 920, 150, gb, 1.0, ring=LINE)
            f.text('miroir', W/2 - 220, 1150, 44, SPARK, gb * ease(seg(t, 45.0, 45.3)), MONO, True)
            f.text('photo', W/2 + 220, 1150, 44, MUTED, gb * ease(seg(t, 45.0, 45.3)), MONO, True)
            words(f, 'Tes amis : l’inverse.', 1340, 66, 45.6, INK, t_out=ob)
            f.text('Mita, Dermer et Knight, 1977', W/2, 1460, 34, MUTED, gb * ease(seg(t, 46.0, 46.3)) * 0.85, MONO, False)

    # S7 — l'escalade (48–56.4)
    if 48.0 <= t < 56.4:
        o1 = 51.9
        g1 = ease(seg(t, 48.1, 48.4)) * (1 - seg(t, o1, o1 + 0.3))
        if g1 > 0:
            words(f, 'Pubs, tubes, logos :', 430, 76, 48.1, INK, t_out=o1)
            words(f, 'la répétition paie.', 540, 80, 48.6, SPARK, t_out=o1)
            # un logo qui revient encore et encore
            for i in range(12):
                gx, gy = i % 4, i // 4
                x = W/2 - 330 + 220 * gx; y = 780 + 200 * gy
                tk = 49.1 + 0.15 * i
                la = g1 * ease(seg(t, tk, tk + 0.2))
                f.circle(x, y, 70 * (0.8 + 0.2 * ease(seg(t, tk, tk + 0.25))), OCEAN, la)
                f.text('S', x, y + 30, 88, SPARK, la, DISPLAY, True)
        o2 = 55.9
        g2 = ease(seg(t, 52.1, 52.4)) * (1 - seg(t, o2, o2 + 0.3))
        if g2 > 0:
            words(f, 'Mais trop répété,', 430, 84, 52.2, INK, t_out=o2)
            words(f, 'ça lasse.', 540, 92, 52.7, RED, t_out=o2)
            x0, y0, wd, hh = 160, 1300, 760, 520
            pts = []
            p = seg(t, 53.1, 54.8)
            for i in range(61):
                u = i / 60
                if u > p: break
                v = math.sin(math.pi * u ** 0.75)  # U inversé
                pts.append((x0 + wd * u, y0 - hh * 0.9 * v))
            f.line([(x0, y0), (x0 + wd, y0)], LINE, g2, 6)
            if len(pts) > 1:
                f.line(pts, SPARK, g2, 10)
            f.text('10 à 20 fois : le sommet', W/2, 1420, 42, SPARK, g2 * ease(seg(t, 54.2, 54.5)), MONO, True)
            f.text('nombre de fois vu (schéma)', W/2, 1490, 34, MUTED, g2 * ease(seg(t, 54.6, 54.9)) * 0.85, MONO, False)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        a = ease(seg(t, 56.1, 56.4))
        tower(f, W/2, 900, 380, a, ease_io(seg(t, 56.1, 57.4)), wd=6)
        words(f, 'Tu n’aimes pas ce qui est beau.', 1010, 64, 56.3, INK)
        words(f, 'Tu trouves beau ce que tu connais.', 1110, 56, 57.8, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(240, 1200, 600, 150, OCEAN, a, 28)
        pa = 0.5 + 0.5 * math.sin((t - 60) * 3)
        f.rect(240, 1200, 600, 150, SPARK, a * 0.25 * pa, 28)
        f.text('Abonne-toi.', W/2, 1295, 62, INK, a)


def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    ev += [(0.15, rise(1.2, 300, 900, 0.07))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (12.5, 29.6, 47.9, 55.9)]
    ev += [(11.0, pop(520))]
    ev += [(30.3, ding(1046, amp=0.28)), (36.1, pop(300, 0.15))]
    ev += [(44.2, clink())]
    ev += [(56.3, pop(440)), (60.0, ding(784, amp=0.22))]
    return ev
