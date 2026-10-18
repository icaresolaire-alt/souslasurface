"""Typographie cinétique : mots qui surgissent, rebonds, grands chiffres centrés."""
import math
from lib import *

# ---------- typographie cinétique ----------
def words(f, text, y, size, t0, col=INK, per=0.11, t_out=None, font=DISPLAY, bold=True):
    """Ligne centrée dont les mots surgissent un par un avec un léger rebond."""
    ws = text.split(' ')
    space = f.width(' ', size, font, bold) * 1.5
    widths = [f.width(w, size, font, bold) for w in ws]
    x = W/2 - (sum(widths) + space * (len(ws) - 1)) / 2
    out = 1.0 if t_out is None else 1 - seg(f.t, t_out, t_out + 0.25)
    for i, (w, wd) in enumerate(zip(ws, widths)):
        p = seg(f.t, t0 + i * per, t0 + i * per + 0.22)
        if p > 0 and out > 0:
            s = 1 + 0.10 * math.sin(math.pi * p) if p < 1 else 1.0
            c = f.c; c.save(); c.translate(x + wd/2, y - size*0.35); c.scale(s, s)
            f.text(w, 0, size*0.35, size, col, ease(p) * out, font, bold)
            c.restore()
        x += wd + space

def bump(t, t0, amp=0.18, dur=0.35):
    p = seg(t, t0, t0 + dur)
    return 1 + amp * math.sin(math.pi * p) if 0 < p < 1 else 1.0

def big_center(f, s, y, size, col, a, scale=1.0, font=MONO):
    c = f.c; c.save(); c.translate(W/2, y); c.scale(scale, scale)
    f.text(s, 0, 0, size, col, a, font, True); c.restore()

