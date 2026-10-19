"""Couverture : la toute première image de chaque vidéo.

C'est elle qui s'affiche dans la grille du profil (Instagram et TikTok).
Elle doit se lire en un coup d'œil, même en tout petit.

Dans l'épisode, déclarer :
    COVER = dict(tag='Maths', l1='Pourquoi le casino', l2='gagne toujours')
- tag : rubrique, en petit (facultatif)
- l1 : début du titre, en blanc
- l2 : la partie qui accroche, en doré
Le titre seul, en très gros. Pas de chiffre isolé : c'est le titre qui parle.

Tout tient dans la zone centrale 1080×1440 (la grille Instagram coupe le haut et le bas).
"""
from lib import *

HOLD = 0.45     # couverture pleine, en secondes
FADE = 0.30     # fondu vers l'épisode
OFFSET = HOLD + FADE

def _fit(f, s, size, maxw, font=DISPLAY, bold=True):
    while size > 30 and f.width(s, size, font, bold) > maxw: size -= 4
    return size

def _lines(f, text, size, maxw):
    out, cur = [], ''
    for w in text.split(' '):
        t = (cur + ' ' + w).strip()
        if f.width(t, size) <= maxw: cur = t
        else: out.append(cur); cur = w
    if cur: out.append(cur)
    return out

def draw_cover(f, cover, a=1.0):
    """Le titre seul, en très gros : c'est lui qui donne envie de cliquer."""
    c = f.c
    g = cairo.RadialGradient(W/2, H*0.45, 50, W/2, H*0.45, H*0.75)
    g.add_color_stop_rgba(0, *hexc(OCEAN, a)); g.add_color_stop_rgba(1, *hexc(DEEP, a))
    c.set_source(g); c.paint()
    # taille la plus grande possible, sur 5 lignes maximum
    size = 150
    while size > 70:
        L1 = _lines(f, cover['l1'], size, 920); L2 = _lines(f, cover['l2'], size, 920)
        if len(L1) + len(L2) <= 5: break
        size -= 6
    lines = [(l, INK) for l in L1] + [(l, SPARK) for l in L2]
    lh = size * 1.08
    y0 = 960 - (len(lines) - 1) * lh / 2 + size * 0.35
    if cover.get('tag'):
        f.text(cover['tag'].upper(), W/2, y0 - size - 40, 34, MUTED, a, MONO, True)
    for i, (l, col) in enumerate(lines):
        f.text(l, W/2, y0 + i * lh, size, col, a)
    f.rect(W/2 - 60, y0 + (len(lines) - 1) * lh + 60, 120, 6, SPARK, a, 3)
    f.text('SOUS LA SURFACE', W/2, 1560, 30, MUTED, a, MONO, True)

def fallback_cover(mod):
    doc = (mod.__doc__ or '').strip().split('\n')[0].split('.')[0]
    words_ = doc.split(' ')
    half = max(1, len(words_) // 2)
    return dict(l1=' '.join(words_[:half]), l2=' '.join(words_[half:]) or ' ')

def wrap_draw(mod, pace=1.0):
    """Renvoie (draw, total) : la couverture puis l'épisode, décalé de OFFSET secondes et ralenti de `pace`."""
    cover = getattr(mod, 'COVER', None) or fallback_cover(mod)
    def draw(f, t):
        if t < OFFSET:
            mod.draw(f, 0.0)
            a = 1.0 if t < HOLD else 1 - ease_io((t - HOLD) / FADE)
            f.c.push_group(); draw_cover(f, cover, 1.0); f.c.pop_group_to_source(); f.c.paint_with_alpha(a)
        else:
            mod.draw(f, (t - OFFSET) / pace)
    return draw, mod.TOTAL * pace + OFFSET
