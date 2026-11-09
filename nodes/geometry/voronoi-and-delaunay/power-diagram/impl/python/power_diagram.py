# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/power-diagram/. The authors are listed in prov/N5KV10.jsonl.

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


def power(q: tuple, site: Point, w: int) -> Fraction:
    """The power of the point q with respect to the circle with center site and squared radius w."""
    return (q[0] - site[0]) ** 2 + (q[1] - site[1]) ** 2 - w


class PowerDiagram:
    """The power diagram (Laguerre diagram) of integer sites with integer weights (squared radii).

    The cell of site p with weight w is the set of points x where |x - p|^2 - w is smallest. Cells are
    convex; some are empty (redundant sites). The cells are computed by clipping a box with the power
    bisectors, which are straight lines. The box holds every point where three bisectors of a site meet and
    a point of every bisector, so it meets every cell with nonempty interior, and a cell is unbounded
    exactly when its clipped polygon touches the box boundary. Exact arithmetic (Fraction).
    insert marks the diagram as stale; the next query rebuilds it.
    Cost: O(n^3) for the box and O(n^2) clipping steps of O(n) each, so O(n^3) time; O(n^2) space.
    Optimal algorithms (lifting to a 3D lower hull) take O(n log n) time.
    """

    def __init__(self, sites: list[tuple[Point, int]] = ()) -> None:
        self.sites: list[Point] = []
        self.weights: list[int] = []
        self.stale = True
        for p, w in sites:
            self.insert(p, w)

    def insert(self, p: Point, w: int) -> bool:
        """Add the site p with weight w; return False if p is already a site (the old weight stays)."""
        if p in self.sites:
            return False
        self.sites.append(p)
        self.weights.append(w)
        self.stale = True
        return True

    def _bisector(self, i: int, j: int) -> tuple:
        """(a, b, c) such that a x + b y <= c holds where site i has power at most that of site j."""
        (pi, wi), (pj, wj) = (self.sites[i], self.weights[i]), (self.sites[j], self.weights[j])
        return (2 * (pj[0] - pi[0]), 2 * (pj[1] - pi[1]),
                pj[0] ** 2 + pj[1] ** 2 - wj - pi[0] ** 2 - pi[1] ** 2 + wi)

    def _box(self) -> tuple:
        s, n = self.sites, len(self.sites)
        pts: list[tuple] = list(s)
        for i in range(n):
            for j in range(i + 1, n):
                a, b, c = self._bisector(i, j)
                pts.append((Fraction(a * c, a * a + b * b), Fraction(b * c, a * a + b * b)))
                for k in range(j + 1, n):
                    a2, b2, c2 = self._bisector(i, k)
                    det = a * b2 - a2 * b
                    if det != 0:  # the radical center of i, j, k
                        pts.append((Fraction(c * b2 - c2 * b, det), Fraction(a * c2 - a2 * c, det)))
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        return (min(xs) - 1, min(ys) - 1, max(xs) + 1, max(ys) + 1)

    def _build(self) -> None:
        n = len(self.sites)
        self._cells: dict[Point, tuple[list[FPoint], bool]] = {}
        self.box = self._box() if n else (-1, -1, 1, 1)  # @line L1
        x0, y0, x1, y1 = self.box
        for i in range(n):  # @line L2
            poly = box_polygon(self.box)  # @line L3
            for j in range(n):  # @line L4
                if j != i and poly:
                    poly = clip(poly, *self._bisector(i, j))  # @line L5
            if poly:  # @line L6
                bounded = all(x0 < v[0] < x1 and y0 < v[1] < y1 for v in poly)
                self._cells[self.sites[i]] = (poly, bounded)
        self.stale = False  # @line L7

    def cells(self) -> dict[Point, tuple[list[FPoint], bool]]:
        """{site: (cell clipped to the box as a counterclockwise polygon, cell is bounded)} for the sites
        whose cell has nonempty interior."""
        if self.stale:
            self._build()
        return dict(self._cells)

    def is_redundant(self, p: Point) -> bool:
        """True if the site p has a cell with empty interior."""
        if self.stale:
            self._build()
        return p not in self._cells

    def vertices(self) -> list[FPoint]:
        """The vertices of the diagram (cell corners not on the box boundary), sorted."""
        if self.stale:
            self._build()
        x0, y0, x1, y1 = self.box
        return sorted({v for poly, _ in self._cells.values() for v in poly if x0 < v[0] < x1 and y0 < v[1] < y1})

    def locate(self, q: tuple) -> list[Point]:
        """The sites of smallest power at q (several only when q is on a cell boundary)."""
        if not self.sites:
            return []
        pw = [power(q, p, w) for p, w in zip(self.sites, self.weights)]
        best = min(pw)
        return [p for p, v in zip(self.sites, pw) if v == best]

    def check_invariant(self) -> None:
        """The cells are convex counterclockwise polygons that tile the box."""
        if self.stale:
            self._build()
        if self.sites:
            x0, y0, x1, y1 = self.box
            assert sum(polygon_area(poly) for poly, _ in self._cells.values()) == (x1 - x0) * (y1 - y0)
        for poly, _ in self._cells.values():
            for k in range(len(poly)):
                a, b, c = poly[k - 1], poly[k], poly[(k + 1) % len(poly)]
                assert (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]) > 0
