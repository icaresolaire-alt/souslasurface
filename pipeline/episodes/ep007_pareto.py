"""La loi de Pareto (80/20). Même structure que le pilote (ep001)."""
import math, numpy as np
from lib import *
from kinetic import words, bump, big_center
from worldmap import WorldMap

TOTAL = 66.0
COVER = dict(tag='Maths', l1='20 % des causes', l2='font 80 % des effets', big='80/20')

# 100 clients : décroissance exponentielle calée pour que les 20 premiers fassent 80 % (r^20 = 1/4 en limite)
N = 100
R = 0.92274
VAL = np.array([R ** i for i in range(N)]); VAL = VAL / VAL.sum()
TOP20 = VAL[:20].sum()                       # 0,800
ORDER = np.random.default_rng(7).permutation(N)   # position initiale (désordonnée) de chaque client trié
BX0, BW, BBASE, BMAX = 70, 9.4, 1330, 600     # barres : x départ, pas, base, hauteur max
def bar_h(i): return max(5, BMAX * VAL[i] / VAL[0])

def bars(f, t, a, sort_p=0.0, lit=0, grow=1.0, equal=False):
    for i in range(N):
        stag = clamp(sort_p * 1.6 - (i / N) * 0.6)
        pos = lerp(ORDER[i], i, ease_io(stag))
        x = BX0 + pos * BW
        h = (230 if equal else bar_h(i)) * grow
        col = SPARK if i < lit else CAPITAL
        f.rect(x + 1, BBASE - h, BW - 2, h, col, a, 2)

# carte d'Italie corrigée de la latitude (sinon trop large)
class LatMap(WorldMap):
    def xy(self, lon, lat):
        return self.x + (lon - self.lon0) * self.k * 0.74, self.y + (self.lat1 - lat) * self.k
ITALY = LatMap(lon=(6.0, 19.0), lat=(36.5, 47.2), x=W/2 - 13 * 46 * 0.74 / 2, y=450, w=13 * 46)
ITALY.w = ITALY.w * 0.74

def person(f, x, y, s, col, a):
    f.circle(x, y - s * 0.9, s * 0.42, col, a)
    f.rect(x - s * 0.5, y - s * 0.4, s, s * 1.0, col, a, s * 0.4)

def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.6, 30.0))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Les 20 meilleurs ?', W/2, 296, 46, SPARK, ha)

    # S1 — accroche (0–4) : les barres poussent dès la première image
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        for i in range(N):
            g = ease(seg(t, 0.0 + ORDER[i] * 0.012, 0.6 + ORDER[i] * 0.012))
            x = BX0 + ORDER[i] * BW; h = bar_h(i) * 0.55 * g
            col = SPARK if (i < 20 and t > 2.6) else CAPITAL
            f.rect(x + 1, 1480 - h, BW - 2, h, col, fo, 2)
        words(f, '20 % de tes clients', 520, 80, 0.15, INK, t_out=o)
        words(f, 'font souvent', 640, 80, 0.75, INK, t_out=o)
        words(f, '80 % de tes ventes.', 760, 92, 1.3, SPARK, t_out=o)
        words(f, 'Et ça marche presque partout.', 900, 54, 2.3, MUTED, t_out=o, bold=False)

    # S2 — enjeu : l'intuition de l'égalité (4–12)
    if 4.0 <= t < 12.6:
        ga = ease(seg(t, 4.1, 4.5)) * (1 - seg(t, 12.0, 12.4))
        bars(f, t, ga, 0.0, 0, ease(seg(t, 4.2, 5.4)), equal=True)
        words(f, '100 clients.', 640, 120, 4.3, INK, t_out=6.4)
        words(f, 'Ton intuition :', 560, 60, 6.6, MUTED, t_out=12.0, bold=False)
        words(f, 'chacun pèse pareil.', 670, 76, 7.0, INK, t_out=12.0)
        a = ease(seg(t, 8.8, 9.1)) * ga
        f.text('les 20 premiers', W/2, 840, 48, MUTED, a, bold=False)
        big_center(f, '= 20 %', 970, 120, INK, a, bump(t, 8.8))
        # les 20 premiers s'éclairent légèrement pour montrer l'idée
        la = ease(seg(t, 9.0, 9.5)) * ga
        for i in range(20):
            f.rect(BX0 + ORDER[i] * BW + 1, BBASE - 230, BW - 2, 230, MUTED, la * 0.9, 2)

    # S3 — la question (12.2–14.6)
    if 12.2 <= t < 14.9:
        words(f, 'Combien rapportent', 820, 96, 12.4, INK, t_out=14.4)
        words(f, 'les 20 meilleurs ?', 950, 104, 12.9, SPARK, t_out=14.4)

    # S4 — la preuve : barres réelles, tri, puis les 20 premiers en doré (14.4–30)
    if 14.4 <= t < 30.2:
        ga = ease(seg(t, 14.5, 14.9)) * (1 - seg(t, 29.6, 30.0))
        grow = ease(seg(t, 14.6, 15.8))
        sp = seg(t, 16.6, 20.4)
        k = int(20 * seg(t, 21.0, 26.0)) if t < 26.0 else 20
        bars(f, t, ga, sp, k, grow)
        f.line([(BX0, BBASE + 4), (BX0 + N * BW, BBASE + 4)], LINE, ga, 3)
        words(f, 'Ce que rapporte chaque client', 470, 46, 14.7, MUTED, t_out=20.6, bold=False)
        words(f, 'On les trie.', 600, 96, 16.4, INK, t_out=20.6)
        if t >= 20.6:
            share = VAL[:k].sum() if k > 0 else 0.0
            ca = ease(seg(t, 20.7, 21.0)) * ga
            f.text(f'les {k} premiers' if k > 1 else ('le premier' if k == 1 else 'les premiers'), W/2, 470, 50, MUTED, ca, bold=False)
            big_center(f, f'{int(round(share * 100))} %', 620, 130, SPARK, ca, bump(t, 26.0, 0.2))
        # accolades sous les barres
        ba = ease(seg(t, 26.6, 27.0)) * ga
        x20 = BX0 + 20 * BW
        f.line([(BX0 + 2, BBASE + 30), (x20 - 2, BBASE + 30)], SPARK, ba, 5)
        f.text('20 clients', BX0, BBASE + 90, 42, SPARK, ba, DISPLAY, True, 'left')
        f.text('80 %', BX0, BBASE + 150, 48, SPARK, ba, MONO, True, 'left')
        bb = ease(seg(t, 27.4, 27.8)) * ga
        f.line([(x20 + 4, BBASE + 30), (BX0 + N * BW - 2, BBASE + 30)], MUTED, bb, 5)
        f.text('les 80 autres', BX0 + N * BW, BBASE + 90, 42, MUTED, bb, DISPLAY, True, 'right')
        f.text('20 %', BX0 + N * BW, BBASE + 150, 48, MUTED, bb, MONO, True, 'right')
        f.text('Exemple illustratif', W/2, 1540, 28, MUTED, ga * ease(seg(t, 15.0, 15.4)), bold=False)

    # S5 — la réponse (30–35.4)
    if 29.9 <= t < 35.4:
        a = ease(seg(t, 30.0, 30.3)) * (1 - seg(t, 34.8, 35.2))
        v = 0.80 * ease(seg(t, 30.0, 31.2))
        big_center(f, f'{int(round(v * 100))} %', 860, 260, SPARK, a, bump(t, 31.2, 0.12))
        words(f, 'des ventes', 1000, 72, 31.4, INK, t_out=34.8)
        words(f, 'avec 20 % des clients.', 1100, 66, 32.0, INK, t_out=34.8)
        words(f, 'C’est la loi de Pareto.', 1260, 58, 33.0, MUTED, t_out=34.8, bold=False)

    # S6 — le retournement : l'origine (35–48)
    if 35.0 <= t < 48.4:
        words(f, 'Pourquoi', 820, 130, 35.1, INK, t_out=37.1)
        words(f, '« Pareto » ?', 960, 120, 35.5, SPARK, t_out=37.1)
        ga = ease(seg(t, 37.3, 37.8)) * (1 - seg(t, 47.9, 48.3))
        if ga > 0:
            c = f.c; c.save()
            z = 1 + 0.06 * seg(t, 37.3, 47.9); cx, cy = W/2, ITALY.y + ITALY.h / 2
            c.translate(cx, cy); c.scale(z, z); c.translate(-cx, -cy)
            ITALY.draw(f, ga)
            c.restore()
            f.rect(ITALY.x - 6, ITALY.y - 6, ITALY.w + 12, ITALY.h + 12, LINE, 0, 0)
            words(f, 'Italie, 1906.', 420, 60, 37.6, MUTED, t_out=47.9, bold=False)
            words(f, 'L’économiste Vilfredo Pareto', 1000, 50, 38.4, INK, t_out=47.9)
            words(f, 'remarque :', 1060, 50, 39.0, INK, t_out=47.9)
            # 10 personnes, 2 en doré
            for j in range(10):
                pa = ease(seg(t, 39.6 + j * 0.06, 39.9 + j * 0.06)) * ga
                gold = j < 2 and t > 40.6
                sc = 1 + (0.08 * math.sin((t - 40.6) * 5) if gold else 0)
                person(f, 150 + j * 87, 1215, 44 * sc, SPARK if gold else CAPITAL, pa)
            a1 = ease(seg(t, 40.6, 40.9)) * ga
            f.text('environ 20 % des habitants', W/2, 1330, 46, SPARK, a1)
            a2 = ease(seg(t, 41.4, 41.7)) * ga
            f.text('possèdent 80 % des terres.', W/2, 1392, 46, SPARK, a2)
            words(f, 'Le même déséquilibre', 1480, 44, 44.2, INK, t_out=47.9, bold=False)
            words(f, 'se retrouve dans d’autres pays.', 1536, 44, 44.6, INK, t_out=47.9, bold=False)

    # S7 — l'escalade : partout (48–56)
    if 48.0 <= t < 56.4:
        out = 1 - seg(t, 55.9, 56.3)
        words(f, 'On le retrouve partout.', 480, 70, 48.1, INK, t_out=55.9)
        a = ease(seg(t, 48.8, 49.1)) * out
        f.rect(110, 560, 860, 230, OCEAN, a, 28)
        f.text('Microsoft, 2002', W/2, 625, 38, MUTED, a, bold=False)
        f.text('20 % des bugs', W/2, 695, 54, INK, a)
        f.text('causent 80 % des erreurs.', W/2, 760, 54, SPARK, a)
        items = ['les ventes', 'les richesses', 'les plaintes', 'ton temps']
        for i, s in enumerate(items):
            ia = ease(seg(t, 50.4 + i * 0.5, 50.7 + i * 0.5)) * out
            x = 290 + (i % 2) * 500; y = 910 + (i // 2) * 110
            f.rect(x - 220, y - 62, 440, 88, OCEAN, ia, 44)
            f.text(s, x, y - 4, 44, INK, ia)
        words(f, 'Parfois 70/30, parfois 90/10.', 1240, 50, 52.8, MUTED, t_out=55.9, bold=False)
        words(f, 'Un ordre de grandeur,', 1340, 56, 53.6, INK, t_out=55.9)
        words(f, 'pas une loi exacte.', 1410, 56, 54.0, INK, t_out=55.9)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        words(f, 'Tout ne se vaut pas.', 720, 76, 56.3)
        words(f, 'Trouve tes 20 %.', 830, 76, 57.4, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(140, 1000, 800, 170, OCEAN, a, 28)
        f.text('Abonne-toi.', W/2, 1105, 64, INK, a)
        f.text('Contenu éducatif, pas un conseil financier.', W/2, 1300, 30, MUTED, a, bold=False)

def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    for t0, n in ((0.15, 4), (0.75, 2), (1.3, 4), (2.3, 4)):
        for i in range(n): ev.append((t0 + i * 0.11, pop(420 + 40 * i, 0.09)))
    ev += [(2.6, ding(880, amp=0.18))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (3.9, 12.1, 14.4, 29.7, 34.9, 47.9, 55.9)]
    ev += [(4.3, pop(330)), (4.4, pop(392)), (6.6, pop(392)), (7.0, pop(440)), (8.8, ding(660, amp=0.2))]
    ev += [(12.4, pop(330)), (12.9, pop(440))]
    x = 14.6
    while x < 15.8: ev.append((x, tick())); x += 0.06
    ev += [(16.4, pop(392)), (16.6, rise(3.8, 200, 700, 0.06))]
    x = 16.6
    while x < 20.4: ev.append((x, tick())); x += 0.1
    for i in range(20): ev.append((21.0 + i * 0.25, pop(380 + i * 22, 0.1)))
    ev += [(26.0, ding(1175, amp=0.3)), (26.6, clink(1900)), (27.4, clink(1500))]
    ev += [(30.0, rise(1.2, 300, 1046, 0.1)), (31.2, ding(1046, amp=0.28)), (35.1, pop(300, 0.15)), (35.5, pop(450, 0.15))]
    for j in range(10): ev.append((39.6 + j * 0.06, pop(500 + j * 20, 0.08)))
    ev += [(40.6, ding(880, amp=0.22)), (41.4, ding(1046, amp=0.22))]
    ev += [(48.8, ding(784, amp=0.2))]
    for i in range(4): ev.append((50.4 + i * 0.5, pop(500 + i * 60)))
    ev += [(53.6, pop(392)), (56.3, pop(440)), (57.4, pop(550)), (60.0, ding(784, amp=0.22))]
    return ev
