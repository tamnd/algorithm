# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lloyds-algorithm/. The authors are listed in prov/3SPGGR.jsonl.

from fractions import Fraction

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


def voronoi_cells(sites: list[FPoint], box) -> list[list[FPoint]]:
    """The Voronoi cell of each site (distinct sites in the box) clipped to the box, by half-plane clipping.
    O(n^2) clipping steps of O(n) each."""
    cells = []
    for i, s in enumerate(sites):
        poly = box_polygon(box)
        for j, t in enumerate(sites):
            if j != i and poly:  # keep the points x with |x - s| <= |x - t|
                poly = clip(poly, 2 * (t[0] - s[0]), 2 * (t[1] - s[1]), t[0] ** 2 + t[1] ** 2 - s[0] ** 2 - s[1] ** 2)
        cells.append(poly)
    return cells


def moments(poly: list[FPoint]) -> tuple:
    """Area, first moments (integral of x, of y) and second moment (integral of x^2 + y^2) of a polygon."""
    a = mx = my = m2 = Fraction(0)
    for k in range(len(poly)):
        (x0, y0), (x1, y1) = poly[k], poly[(k + 1) % len(poly)]
        c = x0 * y1 - x1 * y0
        a += c
        mx += (x0 + x1) * c
        my += (y0 + y1) * c
        m2 += (x0 * x0 + x0 * x1 + x1 * x1 + y0 * y0 + y0 * y1 + y1 * y1) * c
    return a / 2, mx / 6, my / 6, m2 / 12


def centroid(poly: list[FPoint]) -> FPoint:
    """The centroid (center of mass) of a polygon with positive area."""
    a, mx, my, _ = moments(poly)
    return (mx / a, my / a)


def energy(sites: list[FPoint], box) -> Fraction:
    """The quantization energy: the integral over the box of the squared distance to the nearest site."""
    total = Fraction(0)
    for s, poly in zip(sites, voronoi_cells(sites, box)):
        a, mx, my, m2 = moments(poly)
        total += m2 - 2 * (s[0] * mx + s[1] * my) + (s[0] ** 2 + s[1] ** 2) * a
    return total


def lloyd(sites: list[tuple], box: tuple, steps: int) -> list[FPoint]:
    """Lloyd's algorithm: move each site to the centroid of its Voronoi cell in the box, steps times.

    Precondition: the sites lie in the closed box (x0, y0, x1, y1) with x0 < x1 and y0 < y1; repeated sites
    are merged. Exact arithmetic (Fraction). The energy never increases.
    Cost: O(n^3) per step with this clipping (O(n log n) with a Voronoi algorithm); space O(n).
    """
    current = [(Fraction(x), Fraction(y)) for x, y in dict.fromkeys(sites)]
    for _ in range(steps):  # @line L1
        cells = voronoi_cells(current, box)  # @line L2
        new = []
        for poly in cells:  # @line L3
            new.append(centroid(poly))  # @line L4
        current = new  # @line L5
    return current  # @line L6
