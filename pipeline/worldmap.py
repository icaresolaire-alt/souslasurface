"""Carte du monde pour les épisodes de géographie (contours Natural Earth 1:50m, domaine public).

Exemple :
    from worldmap import WorldMap, ROUTE_SHANGHAI_ROTTERDAM, PORTS
    M = WorldMap(lon=(-15, 130), lat=(-5, 60), x=60, y=560, w=960)   # cadrage Europe -> Asie
    M.draw(f, a)                                   # les continents
    M.route(f, ROUTE_SHANGHAI_ROTTERDAM, p, a)     # la route tracée jusqu'à p (0..1)
    M.port(f, *PORTS['Shanghai'], 'Shanghai', a)   # un point légendé
"""
import json, math, os
from lib import *

LAND = '#1d3b50'       # continents, un ton au-dessus du fond
COAST = '#2c5068'      # liseré des côtes

_DATA = None
def _land():
    global _DATA
    if _DATA is None:
        d = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'ne_50m_land.geojson')))
        polys = []
        for ft in d['features']:
            g = ft['geometry']
            parts = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
            for poly in parts:
                polys.append(poly[0])            # contour extérieur seulement
        _DATA = polys
    return _DATA

# Ports et points de passage (lon, lat)
PORTS = {
    'Shanghai': (121.5, 31.2), 'Singapour': (103.8, 1.3), 'Rotterdam': (4.4, 51.9), 'Le Havre': (0.1, 49.5),
    'Suez': (32.55, 29.95), 'Panama': (-79.6, 9.1), 'Los Angeles': (-118.25, 33.7), 'New York': (-74.0, 40.7),
    'Ormuz': (56.3, 26.6), 'Malacca': (100.0, 3.5), 'Gibraltar': (-5.6, 36.0), 'Bab-el-Mandeb': (43.4, 12.6),
    'Cap de Bonne-Espérance': (18.5, -34.4),
}
# Route maritime réaliste (passe en mer) : Shanghai -> détroit de Malacca -> Suez -> Gibraltar -> Manche -> Rotterdam
ROUTE_SHANGHAI_ROTTERDAM = [
    (122.3, 30.8), (121.0, 26.5), (119.6, 23.5), (115.0, 18.0), (109.5, 10.0), (105.0, 2.5), (103.9, 1.2),
    (100.5, 3.8), (97.5, 6.0), (90.0, 6.0), (81.0, 5.5), (72.0, 8.5), (60.0, 12.0), (50.0, 12.5), (43.4, 12.6),
    (40.5, 16.5), (37.0, 22.0), (34.0, 27.0), (32.55, 29.9), (32.3, 31.4), (25.0, 33.8), (15.0, 37.0),
    (8.0, 37.8), (0.0, 36.6), (-5.6, 35.95), (-9.6, 37.0), (-10.0, 43.0), (-6.0, 48.3), (-2.0, 49.9),
    (2.0, 51.0), (4.0, 52.0),
]

class WorldMap:
    def __init__(self, lon=(-180, 180), lat=(-60, 80), x=40, y=500, w=1000):
        self.lon0, self.lon1 = lon; self.lat0, self.lat1 = lat
        self.x, self.y, self.w = x, y, w
        self.k = w / (self.lon1 - self.lon0)                  # pixels par degré
        self.cos = math.cos(math.radians((self.lat0 + self.lat1) / 2))
        self.h = (self.lat1 - self.lat0) * self.k / self.cos * self.cos  # équirectangulaire
        self._cache = None

    def xy(self, lon, lat):
        return self.x + (lon - self.lon0) * self.k, self.y + (self.lat1 - lat) * self.k

    def _projected(self):
        if self._cache is None:
            out = []
            for ring in _land():
                lons = [p[0] for p in ring]; lats = [p[1] for p in ring]
                if max(lons) < self.lon0 - 5 or min(lons) > self.lon1 + 5 or max(lats) < self.lat0 - 5 or min(lats) > self.lat1 + 5:
                    continue
                out.append([self.xy(lo, la) for lo, la in ring])
            self._cache = out
        return self._cache

    def draw(self, f, a=1.0, land=LAND, coast=COAST):
        if a <= 0: return
        c = f.c; c.save()
        c.rectangle(self.x, self.y, self.w, self.h); c.clip()
        for ring in self._projected():
            c.move_to(*ring[0])
            for p in ring[1:]: c.line_to(*p)
            c.close_path()
        f.color(land, a); c.fill_preserve()
        f.color(coast, a); c.set_line_width(1.5); c.stroke()
        c.restore()

    def _cumul(self, pts):
        d = [0.0]
        for i in range(1, len(pts)): d.append(d[-1] + math.dist(pts[i-1], pts[i]))
        return d

    def point_on(self, lonlat, p):
        pts = [self.xy(*q) for q in lonlat]; d = self._cumul(pts); target = p * d[-1]
        for i in range(1, len(pts)):
            if d[i] >= target:
                u = (target - d[i-1]) / max(1e-9, d[i] - d[i-1])
                return lerp(pts[i-1][0], pts[i][0], u), lerp(pts[i-1][1], pts[i][1], u)
        return pts[-1]

    def route(self, f, lonlat, p=1.0, a=1.0, col=SPARK, width=6, ghost=True):
        """Trace la route jusqu'à la fraction p, avec la route complète en pointillés discrets derrière."""
        pts = [self.xy(*q) for q in lonlat]
        if ghost: f.line(pts, INK, a * 0.25, 3, [8, 10])
        if p <= 0: return
        d = self._cumul(pts); target = p * d[-1]; seg_pts = [pts[0]]
        for i in range(1, len(pts)):
            if d[i] <= target: seg_pts.append(pts[i])
            else:
                u = (target - d[i-1]) / max(1e-9, d[i] - d[i-1])
                seg_pts.append((lerp(pts[i-1][0], pts[i][0], u), lerp(pts[i-1][1], pts[i][1], u))); break
        f.line(seg_pts, col, a, width)

    def port(self, f, lon, lat, label='', a=1.0, col=SPARK, r=11, size=32, dy=-26, bold=True, align='center'):
        x, y = self.xy(lon, lat)
        f.circle(x, y, r, col, a)
        if label: f.text(label, x, y + dy, size, INK, a, DISPLAY, bold, align)
