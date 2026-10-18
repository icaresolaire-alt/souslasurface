"""Mini moteur d'animation verticale 1080x1920 (Cairo -> ffmpeg)."""
import cairo, subprocess, math

W, H, FPS = 1080, 1920, 30

def hexc(h, a=1.0):
    h = h.lstrip('#')
    return (int(h[0:2], 16)/255, int(h[2:4], 16)/255, int(h[4:6], 16)/255, a)

DEEP = '#081722'; OCEAN = '#0e2233'; INK = '#eaf1ec'; MUTED = '#8fa8a0'
SPARK = '#f2b544'; EARTH = '#4a9b7a'; LINE = '#22394a'; CAPITAL = '#3b5a6e'; RED = '#e0705a'

DISPLAY = 'Inter Display'
MONO = 'DejaVu Sans Mono'

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(x):
    x = clamp(x); return 1 - (1 - x) ** 3
def ease_io(x):
    x = clamp(x); return x * x * (3 - 2 * x)
def seg(t, a, b): return clamp((t - a) / (b - a)) if b > a else float(t >= a)
def lerp(a, b, x): return a + (b - a) * x

def fmt_int(n): return f"{int(round(n)):,}".replace(',', ' ')
def fmt_pct(p, d=1):
    s = f"{p*100:.{d}f}".replace('.', ',')
    return s + ' %'

class Frame:
    def __init__(self):
        self.s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
        self.c = cairo.Context(self.s)
        g = cairo.RadialGradient(W/2, H*0.45, 50, W/2, H*0.45, H*0.75)
        g.add_color_stop_rgba(0, *hexc(OCEAN)); g.add_color_stop_rgba(1, *hexc(DEEP))
        self.c.set_source(g); self.c.paint()

    def color(self, col, a=1.0):
        r, g, b, _ = hexc(col); self.c.set_source_rgba(r, g, b, a)

    def text(self, s, x, y, size, col=INK, a=1.0, font=DISPLAY, bold=True, align='center', anchor='baseline'):
        if a <= 0 or not s: return 0
        c = self.c
        c.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
        c.set_font_size(size)
        ext = c.text_extents(s)
        if align == 'center': xx = x - ext.x_advance / 2
        elif align == 'right': xx = x - ext.x_advance
        else: xx = x
        yy = y
        if anchor == 'middle': yy = y + size * 0.35
        self.color(col, a); c.move_to(xx, yy); c.show_text(s)
        return ext.x_advance

    def width(self, s, size, font=DISPLAY, bold=True):
        self.c.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
        self.c.set_font_size(size); return self.c.text_extents(s).x_advance

    def wrap(self, s, x, y, size, maxw, col=INK, a=1.0, lh=1.22, bold=True, font=DISPLAY):
        """Texte centré multi-lignes ; '\n' force un retour."""
        lines = []
        for para in s.split('\n'):
            cur = ''
            for w in para.split(' '):
                t = (cur + ' ' + w).strip()
                if self.width(t, size, font, bold) <= maxw: cur = t
                else: lines.append(cur); cur = w
            lines.append(cur)
        for i, l in enumerate(lines):
            self.text(l, x, y + i * size * lh, size, col, a, font, bold)
        return len(lines) * size * lh

    def rect(self, x, y, w, h, col, a=1.0, r=0):
        c = self.c; self.color(col, a)
        if r <= 0: c.rectangle(x, y, w, h)
        else:
            r = min(r, abs(w)/2, abs(h)/2)
            c.new_sub_path()
            c.arc(x+w-r, y+r, r, -math.pi/2, 0); c.arc(x+w-r, y+h-r, r, 0, math.pi/2)
            c.arc(x+r, y+h-r, r, math.pi/2, math.pi); c.arc(x+r, y+r, r, math.pi, 1.5*math.pi)
            c.close_path()
        c.fill()

    def circle(self, x, y, r, col, a=1.0, stroke=0):
        self.color(col, a); self.c.new_sub_path(); self.c.arc(x, y, r, 0, 2*math.pi)
        if stroke: self.c.set_line_width(stroke); self.c.stroke()
        else: self.c.fill()

    def line(self, pts, col, a=1.0, width=3, dash=None):
        c = self.c; self.color(col, a); c.set_line_width(width)
        c.set_line_join(cairo.LINE_JOIN_ROUND); c.set_line_cap(cairo.LINE_CAP_ROUND)
        if dash: c.set_dash(dash)
        for i, (x, y) in enumerate(pts):
            (c.move_to if i == 0 else c.line_to)(x, y)
        c.stroke(); c.set_dash([])

    def chrome(self, t, total, series='EN 30 SECONDES', num=''):
        """Bandeau de série en haut + barre de progression."""
        self.text(series, W/2, 150, 30, MUTED, 1, MONO, True)
        if num: self.text(num, W/2, 195, 26, SPARK, 1, MONO, True)
        self.rect(80, 96, W-160, 6, LINE, 0.8, 3)
        self.rect(80, 96, (W-160) * clamp(t/total), 6, SPARK, 0.9, 3)

    def bytes(self):
        self.s.flush(); return bytes(self.s.get_data())

def render(path, duration, draw, audio=None):
    n = int(duration * FPS)
    ain = ['-i', audio] if audio else ['-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo']
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra',
                          '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          *ain,
                          '-shortest', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20',
                          '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', path],
                         stdin=subprocess.PIPE)
    for i in range(n):
        f = Frame(); draw(f, i / FPS); p.stdin.write(f.bytes())
    p.stdin.close(); p.wait()

def still(path, t, draw):
    f = Frame(); draw(f, t); f.s.write_to_png(path)
