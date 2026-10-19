"""Couverture : la toute première image de chaque vidéo.

C'est elle qui s'affiche dans la grille du profil (Instagram et TikTok).
Elle doit se lire en un coup d'œil, même en tout petit.

Dans l'épisode, déclarer :
    COVER = dict(tag='MATHS', l1='Pourquoi le casino', l2='gagne toujours', big='2,7 %')
- tag : rubrique, en petites capitales dorées (facultatif)
- l1 : première ligne du titre, en blanc
- l2 : deuxième ligne, en doré (le mot qui accroche)
- big : un chiffre ou un mot-choc en très gros (facultatif, mais recommandé)

Tout tient dans la zone centrale 1080×1440 (la grille Instagram coupe le haut et le bas).
"""
from lib import *

HOLD = 0.45     # couverture pleine, en secondes
FADE = 0.30     # fondu vers l'épisode
OFFSET = HOLD + FADE

def _fit(f, s, size, maxw, font=DISPLAY, bold=True):
    while size > 30 and f.width(s, size, font, bold) > maxw: size -= 4
    return size

def draw_cover(f, cover, a=1.0):
    c = f.c
    # fond plein pour masquer l'épisode dessous
    g = cairo.RadialGradient(W/2, H*0.45, 50, W/2, H*0.45, H*0.75)
    g.add_color_stop_rgba(0, *hexc(OCEAN, a)); g.add_color_stop_rgba(1, *hexc(DEEP, a))
    c.set_source(g); c.paint()
    big = cover.get('big')
    y = 760 if big else 900
    if cover.get('tag'):
        f.text(cover['tag'].upper(), W/2, y - 150, 34, SPARK, a, MONO, True)
        f.rect(W/2 - 50, y - 128, 100, 5, SPARK, a, 2)
    s1 = _fit(f, cover['l1'], 104, 940)
    f.text(cover['l1'], W/2, y, s1, INK, a)
    s2 = _fit(f, cover['l2'], 112, 940)
    f.text(cover['l2'], W/2, y + max(s1, s2) * 1.12, s2, SPARK, a)
    if big:
        sb = _fit(f, big, 230, 940, MONO)
        f.text(big, W/2, y + 200 + sb * 0.85, sb, INK, a, MONO)
    f.text('SOUS LA SURFACE', W/2, 1560, 30, MUTED, a, MONO, True)

def fallback_cover(mod):
    doc = (mod.__doc__ or '').strip().split('\n')[0].split('.')[0]
    words_ = doc.split(' ')
    half = max(1, len(words_) // 2)
    return dict(l1=' '.join(words_[:half]), l2=' '.join(words_[half:]) or ' ')

def wrap_draw(mod):
    """Renvoie (draw, total) : la couverture puis l'épisode, décalé de OFFSET secondes."""
    cover = getattr(mod, 'COVER', None) or fallback_cover(mod)
    def draw(f, t):
        if t < OFFSET:
            mod.draw(f, 0.0)
            a = 1.0 if t < HOLD else 1 - ease_io((t - HOLD) / FADE)
            f.c.push_group(); draw_cover(f, cover, 1.0); f.c.pop_group_to_source(); f.c.paint_with_alpha(a)
        else:
            mod.draw(f, t - OFFSET)
    return draw, mod.TOTAL + OFFSET
