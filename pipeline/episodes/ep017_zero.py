"""Le nombre zéro est plus jeune que le Colisée. Même structure que le pilote.

Sources :
- MacTutor (Univ. St Andrews), biographie de Brahmagupta : le Brahmasphutasiddhanta est écrit en 628 ;
  zéro défini comme un nombre moins lui-même ; a + 0 = a ; a × 0 = 0.
- History of Information (historyofinformation.com/detail.php?id=181) : en 628, Brahmagupta écrit le
  Brahmasphutasiddhanta, qui montre une bonne compréhension du rôle mathématique du zéro.
- MacTutor, « A history of Zero » : signe babylonien pour une place vide vers 400 av. J.-C. (pas un nombre) ;
  Fibonacci décrit les neuf chiffres indiens et le signe 0 dans le Liber abaci.
- Rutgers (d'après Neugebauer) : le signe zéro babylonien est en usage au moins vers 300 av. J.-C. ;
  M. Suri (UMBC) : « vers 300 av. J.-C. », et aucune de ces civilisations ne voyait le zéro comme un nombre.
- Italia.it (site officiel du tourisme italien) : Colisée inauguré en 80 apr. J.-C. par Titus.
- MacTutor, biographie de Fibonacci et York University (MATH 1700) : Liber abaci, 1202.
"""
import math
from lib import *
from kinetic import words, bump, big_center

TOTAL = 66.0
# Musique : choisie automatiquement d'après le numéro (ep017 -> electro).
COVER = dict(tag='Histoire', l1='Le nombre zéro est plus', l2='jeune que le Colisée')

STONE = '#c9a77a'

def colisee(f, x, y, w, h, a, rise=1.0):
    """Façade simplifiée : trois étages d'arches, qui monte depuis le bas."""
    if a <= 0: return
    c = f.c; c.save(); c.translate(x, y + (1 - rise) * 120)
    f.rect(-w/2, -h, w, h, STONE, a * 0.22, 10)
    f.rect(-w/2, -h, w, h * 0.10, STONE, a * 0.55, 6)
    n = 7; tier = h * 0.30
    for row in range(3):
        y0 = -row * tier
        for k in range(n):
            ax = -w/2 + (k + 0.5) * w / n
            aw = w / n * 0.55; ah = tier * 0.62
            f.rect(ax - aw/2, y0 - ah - 10, aw, ah, DEEP, a * 0.9, aw / 2)
        f.line([(-w/2, y0 - tier + 4), (w/2, y0 - tier + 4)], STONE, a * 0.8, 4)
    f.line([(-w/2, 0), (w/2, 0)], STONE, a, 5)
    c.restore()

def draw(f, t):
    f.t = t
    f.chrome(t, TOTAL, 'SOUS LA SURFACE', '')

    # question persistante
    ha = ease(seg(t, 12.6, 13.1)) * (1 - seg(t, 29.8, 30.2))
    f.rect(140, 236, 800, 92, OCEAN, ha * 0.9, 46)
    f.text('Depuis quand existe le zéro ?', W/2, 296, 46, SPARK, ha)

    # S1 — accroche (0–4) : le Colisée qui monte dès la première image
    if t < 4.3:
        o = 3.9; fo = 1 - seg(t, o, o + 0.3)
        words(f, 'Le nombre zéro est', 470, 88, 0.15, INK, t_out=o)
        words(f, 'plus jeune', 580, 104, 0.6, INK, t_out=o)
        words(f, 'que le Colisée.', 700, 104, 1.0, SPARK, t_out=o)
        colisee(f, W/2, 1330, 760, 420, fo * ease(seg(t, 0.0, 0.4)), ease_io(seg(t, 0.0, 1.6)))
        a = ease(seg(t, 2.2, 2.5)) * fo
        c = f.c; c.save(); c.translate(W/2, 1450); s = bump(t, 2.2, 0.12); c.scale(s, s)
        f.text('inauguré en l’an 80', 0, 0, 44, MUTED, a, MONO, True); c.restore()

    # S2 — enjeu (4–11)
    if 4.0 <= t < 11.0:
        words(f, 'Les Romains', 560, 92, 4.2, INK, t_out=6.7)
        words(f, 'comptaient sans zéro.', 670, 80, 4.6, SPARK, t_out=6.7)
        a = ease(seg(t, 5.0, 5.3)) * (1 - seg(t, 6.6, 6.9))
        big_center(f, 'MMXXVI', 960, 150, INK, a, bump(t, 5.0, 0.12), DISPLAY)
        a2 = ease(seg(t, 5.6, 5.9)) * (1 - seg(t, 6.6, 6.9))
        f.text('= 2026', W/2, 1100, 70, MUTED, a2, MONO, True)
        # aucun symbole pour « rien »
        words(f, 'Pour écrire « rien » ?', 560, 80, 6.9, INK, t_out=8.8)
        a = ease(seg(t, 7.1, 7.4)) * (1 - seg(t, 8.7, 9.0))
        for i, ch in enumerate('IVXLCDM'):
            ai = a * ease(seg(t, 7.1 + i * 0.08, 7.4 + i * 0.08))
            f.text(ch, 165 + i * 125, 900, 96, INK, ai, DISPLAY, True)
        a3 = ease(seg(t, 7.9, 8.2)) * (1 - seg(t, 8.7, 9.0))
        f.text('Aucun symbole.', W/2, 1100, 72, RED, a3)
        a = ease(seg(t, 9.0, 9.3)) * (1 - seg(t, 10.6, 10.9))
        f.text('Ton intuition :', W/2, 700, 56, MUTED, a, bold=False)
        c = f.c; c.save(); c.translate(W/2, 860); s = bump(t, 9.0); c.scale(s, s)
        f.text('Le zéro a toujours', 0, 0, 96, INK, a); f.text('existé.', 0, 110, 96, INK, a)
        c.restore()

    # S3 — la question (10.9–13.5)
    if 10.9 <= t < 13.6:
        words(f, 'Alors, depuis quand', 820, 100, 11.0, INK, t_out=12.5)
        words(f, 'existe le zéro ?', 960, 104, 11.4, SPARK, t_out=12.5)

    # S4 — la preuve : frise chronologique (13.5–30)
    if 13.4 <= t < 30.0:
        ga = ease(seg(t, 13.5, 13.9)) * (1 - seg(t, 29.4, 29.8))
        words(f, 'Remontons le temps.', 450, 72, 13.6, INK, t_out=29.4)
        LX = 220; y0, y1 = 590, 1390
        grow = ease_io(seg(t, 14.0, 14.8))
        f.line([(LX, y0), (LX, y0 + (y1 - y0) * grow)], LINE, ga, 8)
        # trajet du curseur
        yb, yr_, yi = 700, 1010, 1330   # positions de la frise (pas à l'échelle)
        p1 = ease_io(seg(t, 14.8, 15.6)); p2 = ease_io(seg(t, 19.6, 20.6)); p3 = ease_io(seg(t, 24.0, 25.4))
        cy = lerp(y0, yb, p1)
        cy = lerp(cy, yr_, p2); cy = lerp(cy, yi, p3)
        if t > 14.8:
            f.line([(LX, y0), (LX, cy)], SPARK, ga * 0.9, 8)
            f.circle(LX, cy, 20, SPARK, ga)
            f.circle(LX, cy, 34, SPARK, ga * 0.25 * (0.5 + 0.5 * math.sin(t * 5)))
        # Babylone
        ab = ga * ease(seg(t, 15.5, 15.8))
        f.circle(LX, yb, 12, INK, ab)
        f.text('Babylone', 280, yb - 30, 56, INK, ab, align='left')
        f.text('vers 300 av. J.-C.', 280, yb + 20, 34, MUTED, ab, MONO, True, align='left')
        a = ga * ease(seg(t, 16.4, 16.7))
        f.text('Un signe pour « case vide ».', 280, yb + 80, 42, INK, a, bold=False, align='left')
        a = ga * ease(seg(t, 17.6, 17.9))
        c = f.c; c.save(); c.translate(280, yb + 136); s = bump(t, 17.6, 0.12); c.scale(s, s)
        f.text('Pas encore un nombre.', 0, 0, 42, SPARK, a, align='left'); c.restore()
        # Rome
        ar = ga * ease(seg(t, 20.5, 20.8))
        f.circle(LX, yr_, 12, INK, ar)
        f.text('Rome', 280, yr_ - 30, 56, INK, ar, align='left')
        f.text('an 80 : le Colisée', 280, yr_ + 20, 34, MUTED, ar, MONO, True, align='left')
        a = ga * ease(seg(t, 21.6, 21.9))
        c = f.c; c.save(); c.translate(280, yr_ + 80); s = bump(t, 21.6, 0.12); c.scale(s, s)
        f.text('Toujours pas de zéro.', 0, 0, 42, RED, a, align='left'); c.restore()
        # le point d'arrivée inconnu
        ai = ga * ease(seg(t, 25.3, 25.6))
        f.circle(LX, yi, 12, INK, ai)
        c = f.c; c.save(); c.translate(280, yi + 18); s = bump(t, 25.3, 0.16); c.scale(s, s)
        f.text('???', 0, 0, 72, SPARK, ai, MONO, True, align='left'); c.restore()
        words(f, 'Qui en fait un vrai nombre ?', 1500, 50, 26.2, INK, t_out=29.4)

    # S5 — la réponse (30–35.4)
    if 29.9 <= t < 35.4:
        a = ease(seg(t, 30.0, 30.3)) * (1 - seg(t, 34.8, 35.2))
        words(f, 'En Inde, en', 600, 80, 30.0, INK, t_out=34.8)
        p = ease_io(seg(t, 30.4, 31.4))
        big_center(f, f'{int(round(628 * p))}', 960, 260, SPARK, a, bump(t, 31.4, 0.14))
        words(f, 'Brahmagupta écrit', 1150, 66, 31.6, INK, t_out=34.8)
        words(f, 'les règles du zéro.', 1240, 66, 32.0, SPARK, t_out=34.8)
        words(f, 'MacTutor, Univ. St Andrews', 1340, 32, 32.6, MUTED, t_out=34.8, font=MONO, bold=False)

    # S6 — le retournement : « rien » devient un nombre, et donne leur valeur aux positions (35–48.4)
    if 35.0 <= t < 48.4:
        words(f, 'Le secret ?', 900, 130, 35.1, INK, t_out=37.1)
        ga = ease(seg(t, 37.3, 37.7)) * (1 - seg(t, 47.9, 48.3))
        if ga > 0:
            words(f, '« Rien » devient', 450, 80, 37.4, INK, t_out=42.6)
            words(f, 'un nombre.', 550, 80, 37.9, SPARK, t_out=42.6)
            for i, (eq, t0) in enumerate((('5 − 5 = 0', 38.6), ('7 + 0 = 7', 39.6), ('3 × 0 = 0', 40.6))):
                a = ga * ease(seg(t, t0, t0 + 0.3)) * (1 - seg(t, 42.5, 42.8))
                big_center(f, eq, 800 + i * 180, 110, INK if i else SPARK, a, bump(t, t0, 0.12))
            # la valeur de position
            ma = ga * ease(seg(t, 42.8, 43.2))
            words(f, 'Et il tient', 450, 80, 42.9, INK, t_out=47.9)
            words(f, 'la place vide.', 550, 80, 43.3, SPARK, t_out=47.9)
            xs = (310, 540, 770); labels = ('centaines', 'dizaines', 'unités')
            for x, lab in zip(xs, labels):
                f.rect(x - 90, 740, 180, 230, OCEAN, ma, 24)
                f.rect(x - 90, 740, 180, 230, LINE, ma * 0.6, 24)
                f.text(lab, x, 1020, 30, MUTED, ma, MONO, True)
            f.text('2', xs[0], 900, 160, INK, ma, MONO, True)
            f.text('5', xs[2], 900, 160, INK, ma, MONO, True)
            d = ease(seg(t, 45.2, 45.8))
            if d > 0:
                c = f.c; c.save(); c.translate(xs[1], lerp(640, 900, d)); s = bump(t, 45.8, 0.18); c.scale(s, s)
                f.text('0', 0, 0, 160, SPARK, ma * d, MONO, True); c.restore()
            a = ma * ease(seg(t, 43.8, 44.1)) * (1 - seg(t, 45.0, 45.3))
            f.text('25 ? 205 ? 250 ?', W/2, 1200, 64, RED, a, MONO, True)
            a = ma * ease(seg(t, 45.8, 46.1))
            c = f.c; c.save(); c.translate(W/2, 1200); s = bump(t, 45.8, 0.14); c.scale(s, s)
            f.text('205, sans doute possible', 0, 0, 58, SPARK, a, MONO, True); c.restore()

    # S7 — l'escalade : le zéro gagne l'Europe, puis toutes les machines (48–56.4)
    if 48.0 <= t < 56.4:
        out = 1 - seg(t, 55.9, 56.3)
        words(f, 'En 1202, Fibonacci', 460, 72, 48.1, INK, t_out=51.4)
        words(f, 'l’apporte en Europe.', 560, 72, 48.6, SPARK, t_out=51.4)
        a = ease(seg(t, 49.0, 49.3)) * (1 - seg(t, 51.3, 51.6))
        c = f.c; c.save(); c.translate(W/2, 1000); s = bump(t, 49.0, 0.1); c.scale(s, s)
        f.rect(-230, -200, 460, 400, STONE, a * 0.85, 18)
        f.rect(-230, -200, 40, 400, '#a8875c', a, 12)
        f.text('Liber abaci', 20, -40, 54, DEEP, a)
        f.text('0 1 2 3 4', 20, 60, 50, DEEP, a, MONO, True)
        f.text('5 6 7 8 9', 20, 130, 50, DEEP, a, MONO, True)
        c.restore()
        # aujourd'hui : du binaire partout
        a = ease(seg(t, 51.6, 51.9)) * out
        if a > 0:
            for k in range(8):
                for j in range(5):
                    yy = 760 + ((j * 130 + (t - 51.6) * 120 + k * 37) % 650)
                    bit = '0' if (k * 7 + j * 3 + int(t * 2)) % 3 else '1'
                    f.text(bit, 150 + k * 112, yy, 64, SPARK if bit == '0' else MUTED,
                           a * 0.55 * (1 - abs(yy - 1085) / 340), MONO, True)
        words(f, 'Aujourd’hui, ton téléphone', 460, 64, 51.7, INK, t_out=55.9)
        words(f, 'calcule avec des 0 et des 1.', 550, 64, 52.2, SPARK, t_out=55.9)

    # S8 — chute + abonnement (56–66)
    if t >= 56.0:
        a = ease(seg(t, 56.1, 56.4))
        c = f.c; c.save(); c.translate(W/2, 600); s = bump(t, 56.1, 0.12); c.scale(s, s)
        f.circle(0, 0, 110, SPARK, a, stroke=18); c.restore()
        words(f, 'Il a fallu des millénaires', 840, 72, 56.3, INK)
        words(f, 'pour inventer « rien ».', 940, 76, 57.6, SPARK)
        a = ease(seg(t, 60.0, 60.4))
        f.rect(240, 1060, 600, 150, OCEAN, a, 28)
        pa = 0.5 + 0.5 * math.sin((t - 60) * 3)
        f.rect(240, 1060, 600, 150, SPARK, a * 0.25 * pa, 28)
        f.text('Abonne-toi.', W/2, 1155, 62, INK, a)

def sfx_events():
    from sound import pop, tick, whoosh, ding, clink, rise
    ev = []
    ev += [(0.15, pop(440, 0.09)), (1.0, ding(880, amp=0.22))]
    ev += [(x, whoosh(0.5, 0.18)) for x in (12.5, 29.6, 47.9, 55.9)]
    ev += [(11.0, pop(520))]
    ev += [(30.4, rise(1.0, 300, 900, 0.07)), (31.4, ding(1046, amp=0.28)), (35.1, pop(300, 0.15))]
    ev += [(45.8, ding(988, amp=0.24))]
    ev += [(56.3, pop(440)), (60.0, ding(784, amp=0.22))]
    return ev
