# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/order-k-voronoi-diagram/. The authors are listed in prov/93B6PD.jsonl.

from fractions import Fraction

Point = tuple[int, int]

FPoint = tuple[Fraction, Fraction]


def clip(poly: list[FPoint], a, b, c) -> list[FPoint]:
    """The part of the convex polygon poly (counterclockwise) where a x + b y <= c. Exact with Fractions."""
    out: list[FPoint] = []
    m = len(poly)
    for k in range(m):
        p, q = poly[k], poly[(k + 1) % m]
        fp, fq = a * p[0] + b * p[1] - c, a * q[0] + b * q[1] - c
        if fp <= 0:
            out.append(p)
        if (fp < 0 < fq) or (fq < 0 < fp):
            t = fp / (fp - fq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    clean: list[FPoint] = []
    for p in out:  # drop repeated and collinear points
        if clean and clean[-1] == p:
            continue
        clean.append(p)
    while len(clean) > 1 and clean[0] == clean[-1]:
        clean.pop()
    k = 0
    while len(clean) >= 3 and k < len(clean):
        p, q, r = clean[k - 1], clean[k], clean[(k + 1) % len(clean)]
        if (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0]) == 0:
            clean.pop(k)
            k = 0
        else:
            k += 1
    return clean if len(clean) >= 3 else []


def box_polygon(box) -> list[FPoint]:
    x0, y0, x1, y1 = (Fraction(v) for v in box)
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def polygon_area(poly: list[FPoint]) -> Fraction:
    """Area of a counterclockwise polygon (shoelace formula)."""
    s = Fraction(0)
    for k in range(len(poly)):
        p, q = poly[k], poly[(k + 1) % len(poly)]
        s += p[0] * q[1] - q[0] * p[1]
    return s / 2


def point_in_convex(poly: list[FPoint], q) -> int:
    """1 if q is strictly inside the convex counterclockwise polygon, 0 on its boundary, -1 outside."""
    worst = 1
    for k in range(len(poly)):
        p, r = poly[k], poly[(k + 1) % len(poly)]
        d = (r[0] - p[0]) * (q[1] - p[1]) - (r[1] - p[1]) * (q[0] - p[0])
        if d < 0:
            return -1
        if d == 0:
            worst = 0
    return worst


def convex_hull(points: list[FPoint]) -> list[FPoint]:
    """Vertices of the convex hull, counterclockwise, without points inside hull edges (monotone chain)."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts
    cross = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower: list[FPoint] = []
    upper: list[FPoint] = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


class OrderKVoronoiDiagram:
    """The order-k Voronoi diagram of integer sites, restricted to a box (x0, y0, x1, y1).

    The cell of a set S of k sites is the convex region where the sites of S are k nearest sites. The cells
    are found level by level: an order-j cell of T is cut into pieces by the ordinary Voronoi diagram of the
    sites not in T; the piece of site t belongs to the order-(j + 1) cell of T + {t}, which is the convex hull
    of its pieces. All arithmetic is exact (Fraction). Only cells with positive area in the box are kept.
    insert marks the diagram as stale; the next query rebuilds it.
    Cost: O(k^2 n^3) clipping steps in this simple form (O(k(n - k)) cells, each cut by O(n) half-planes at
    each of k levels); space O(k(n - k)) cells.
    """

    def __init__(self, k: int, box: tuple[int, int, int, int], points: list[Point] = ()) -> None:
        self.k, self.box = k, box
        self.sites: list[Point] = []
        self.stale = True
        for p in points:
            self.insert(p)

    def insert(self, p: Point) -> bool:
        """Add the site p; return False if it is already a site."""
        if p in self.sites:
            return False
        self.sites.append(p)
        self.stale = True
        return True

    def _build(self) -> None:
        s, n = self.sites, len(self.sites)
        cells: dict[frozenset, list[FPoint]] = {frozenset(): box_polygon(self.box)}  # @line L1
        for _ in range(min(self.k, n)):  # @line L2
            pieces: dict[frozenset, list[FPoint]] = {}
            for t_set, poly in cells.items():  # @line L3
                rest = [i for i in range(n) if i not in t_set]
                for t in rest:  # @line L4
                    piece = poly
                    for u in rest:
                        if u != t and piece:  # keep the points nearer to t than to u
                            piece = clip(piece, 2 * (s[u][0] - s[t][0]), 2 * (s[u][1] - s[t][1]),
                                         s[u][0] ** 2 + s[u][1] ** 2 - s[t][0] ** 2 - s[t][1] ** 2)  # @line L5
                    if piece:
                        pieces.setdefault(t_set | {t}, []).extend(piece)  # @line L6
            cells = {key: convex_hull(pts) for key, pts in pieces.items()}  # @line L7
        self._cells = {frozenset(s[i] for i in key): poly for key, poly in cells.items()} if n >= self.k else {}
        self.stale = False

    def cells(self) -> dict[frozenset, list[FPoint]]:
        """{set of k sites: its cell as a counterclockwise polygon of exact points}."""
        if self.stale:
            self._build()
        return dict(self._cells)

    def locate(self, q: tuple) -> list[frozenset]:
        """The sets of k sites whose closed cell holds q (one set unless q is on a cell boundary)."""
        if self.stale:
            self._build()
        return [key for key, poly in self._cells.items() if point_in_convex(poly, q) >= 0]

    def check_invariant(self) -> None:
        """The cells are convex, counterclockwise, and their areas add up to the area of the box."""
        if self.stale:
            self._build()
        if self._cells:
            x0, y0, x1, y1 = self.box
            assert sum(polygon_area(p) for p in self._cells.values()) == (x1 - x0) * (y1 - y0)
        for poly in self._cells.values():
            for j in range(len(poly)):
                a, b, c = poly[j - 1], poly[j], poly[(j + 1) % len(poly)]
                assert (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]) > 0
