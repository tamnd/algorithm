# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/offset-trimming/. The authors are listed in prov/MJFVD0.jsonl.

"""Trimming the offset of a closed planar cubic B-spline curve.

The curve C is a closed uniform cubic B-spline with control points
P_0, ..., P_(n-1) and parameter t in [0, n). N is the left unit normal, so
for a counterclockwise curve it points inside, and the raw offset is
g(t) = C(t) + d N(t). The algorithm samples g as a closed polyline, finds
the crossings of non-adjacent segments with a sweep in x and exact
orientation tests, splits the polyline at the crossings, and keeps the
pieces whose middle point is at distance |d| from C.

Points are (x, y) tuples of floats. The orientation tests convert the
coordinates to fractions.Fraction, which is exact for floats, so every sign
decision is exact for the sampled points.
"""

from fractions import Fraction
from math import floor, hypot
from typing import NamedTuple


# ---------------------------------------------------------------- the curve


def de_boor(points, t: float, degree: int):
    """Point of the closed uniform B-spline of `degree` with these control points.

    The knots are the integers, and span i = floor(t) uses the control
    points P_(i - degree), ..., P_i, with indices taken modulo n.
    """
    n = len(points)
    t = t % n
    i = min(int(floor(t)), n - 1)
    d = [points[j % n] for j in range(i - degree, i + 1)]
    return _de_boor_span(d, i, t, degree)


def _de_boor_span(d, i: int, t: float, degree: int):
    """The de Boor triangle on span [i, i + 1) with the local control points d."""
    d = list(d)
    for r in range(1, degree + 1):
        for k in range(degree, r - 1, -1):
            j = i - degree + k  # knot index of d[k]
            alpha = (t - j) / (degree + 1 - r)
            d[k] = ((1 - alpha) * d[k - 1][0] + alpha * d[k][0], (1 - alpha) * d[k - 1][1] + alpha * d[k][1])
    return d[degree]


def curve_point(points, t: float):
    """C(t) of the closed uniform cubic B-spline."""
    return de_boor(points, t, 3)


def curve_derivative(points, t: float):
    """C'(t): the quadratic B-spline with control points P_j - P_(j-1) on the same knots.

    With integer knots the factor 3 / (u_(j+3) - u_j) of the derivative formula is 1,
    and span i uses the differences with j = i - 2, i - 1, i.
    """
    n = len(points)
    t = t % n
    i = min(int(floor(t)), n - 1)
    diffs = []
    for j in range(i - 2, i + 1):
        p, q = points[j % n], points[(j - 1) % n]
        diffs.append((p[0] - q[0], p[1] - q[1]))
    return _de_boor_span(diffs, i, t, 2)


def offset_point(points, t: float, d: float):
    """g(t) = C(t) + d N(t), with N the left unit normal."""
    x, y = curve_point(points, t)
    dx, dy = curve_derivative(points, t)
    s = hypot(dx, dy)
    return (x - d * dy / s, y + d * dx / s)


# ------------------------------------------------------- exact predicates


def orient(a, b, c) -> int:
    """Sign of the cross product (b - a) x (c - a), computed exactly."""
    ax, ay = Fraction(a[0]), Fraction(a[1])
    v = (Fraction(b[0]) - ax) * (Fraction(c[1]) - ay) - (Fraction(b[1]) - ay) * (Fraction(c[0]) - ax)
    return (v > 0) - (v < 0)


def segments_cross(a, b, c, e) -> bool:
    """True when the closed segments ab and ce meet. Collinear overlaps raise ValueError."""
    if a == b or c == e:  # a segment of length zero is a point
        p, (s, r) = (a, (c, e)) if a == b else (c, (a, b))
        return orient(s, r, p) == 0 and _in_box(p, s, r)
    o1, o2, o3, o4 = orient(a, b, c), orient(a, b, e), orient(c, e, a), orient(c, e, b)
    if o1 == o2 == o3 == o4 == 0:
        if (min(a[0], b[0]) <= max(c[0], e[0]) and min(c[0], e[0]) <= max(a[0], b[0])
                and min(a[1], b[1]) <= max(c[1], e[1]) and min(c[1], e[1]) <= max(a[1], b[1])):
            raise ValueError("collinear overlapping offset segments; sample with another m")
        return False
    return o1 * o2 <= 0 and o3 * o4 <= 0


def _dot_sign(a, b, c) -> int:
    """Sign of (b - a) . (c - b), computed exactly."""
    a, b, c = [(Fraction(p[0]), Fraction(p[1])) for p in (a, b, c)]
    v = (b[0] - a[0]) * (c[0] - b[0]) + (b[1] - a[1]) * (c[1] - b[1])
    return (v > 0) - (v < 0)


def _in_box(p, s, r) -> bool:
    return min(s[0], r[0]) <= p[0] <= max(s[0], r[0]) and min(s[1], r[1]) <= p[1] <= max(s[1], r[1])


def crossing_ratio(a, b, c, e) -> Fraction:
    """The exact lam in [0, 1] with a + lam (b - a) on the line ce."""
    bx, by = Fraction(b[0]) - Fraction(a[0]), Fraction(b[1]) - Fraction(a[1])
    ex, ey = Fraction(e[0]) - Fraction(c[0]), Fraction(e[1]) - Fraction(c[1])
    cx, cy = Fraction(c[0]) - Fraction(a[0]), Fraction(c[1]) - Fraction(a[1])
    return (cx * ey - cy * ex) / (bx * ey - by * ex)


# ---------------------------------------------------- the sweep in x


def polyline_crossings(q) -> list:
    """All pairs (i, j), i < j, of non-adjacent segments of the closed polyline q that meet.

    Segment i joins q[i] and q[i + 1], indices modulo m = len(q). Segments
    are sorted by their least x and swept from left to right. Each new
    segment is tested against the active segments whose x range reaches it.
    """
    m = len(q)
    seg = [(q[i], q[(i + 1) % m]) for i in range(m)]
    lo = [min(s[0][0], s[1][0]) for s in seg]
    hi = [max(s[0][0], s[1][0]) for s in seg]
    order = sorted(range(m), key=lambda i: lo[i])
    active = []
    found = []
    for i in order:
        active = [j for j in active if hi[j] >= lo[i]]
        for j in active:
            if (i - j) % m in (1, m - 1):
                continue  # adjacent segments share a vertex
            a, b = seg[i]
            c, e = seg[j]
            if min(a[1], b[1]) > max(c[1], e[1]) or min(c[1], e[1]) > max(a[1], b[1]):
                continue
            if segments_cross(a, b, c, e):
                found.append((min(i, j), max(i, j)))
        active.append(i)
    return sorted(found)


# ------------------------------------------------ distance to the curve


def distance_to_curve(points, p, samples_per_span: int = 48, refine: int = 3) -> float:
    """Distance from p to C: dense sampling, then Newton steps on (C(s) - p) . C'(s) = 0."""
    n = len(points)
    total = n * samples_per_span
    vals = []
    for k in range(total):
        s = k * n / total
        c = curve_point(points, s)
        vals.append((hypot(c[0] - p[0], c[1] - p[1]), s))
    best = min(v[0] for v in vals)
    # Refine at the local minima of the sampled distance.
    cands = [vals[k][1] for k in range(total) if vals[k][0] <= vals[k - 1][0] and vals[k][0] <= vals[(k + 1) % total][0]]
    cands.sort(key=lambda s: hypot(curve_point(points, s)[0] - p[0], curve_point(points, s)[1] - p[1]))
    h = 1e-6
    for s in cands[:refine]:
        for _ in range(30):
            c = curve_point(points, s)
            d1 = curve_derivative(points, s)
            f = (c[0] - p[0]) * d1[0] + (c[1] - p[1]) * d1[1]
            d1b = curve_derivative(points, s + h)
            d1a = curve_derivative(points, s - h)
            d2 = ((d1b[0] - d1a[0]) / (2 * h), (d1b[1] - d1a[1]) / (2 * h))
            fp = d1[0] ** 2 + d1[1] ** 2 + (c[0] - p[0]) * d2[0] + (c[1] - p[1]) * d2[1]
            if fp <= 0:
                break
            step = f / fp
            step = max(-0.5 / samples_per_span, min(0.5 / samples_per_span, step))
            s -= step
            if abs(step) < 1e-14:
                break
        c = curve_point(points, s)
        best = min(best, hypot(c[0] - p[0], c[1] - p[1]))
    return best


# ---------------------------------------------------- the algorithm


class Piece(NamedTuple):
    start: tuple  # (segment index, exact ratio) where the piece begins
    end: tuple  # (segment index, exact ratio) where the piece ends
    polyline: list  # the points of the piece
    middle: tuple  # the point g(t) at the middle parameter
    distance: float  # its distance to C
    kept: bool


def offset_trimming(points, d: float, m: int, tol: float = 1e-7):
    """Trim the offset at signed distance d of the closed cubic B-spline `points`.

    Return (q, crossings, pieces): the sampled raw offset q with m vertices,
    the crossing pairs of its segments, and all pieces between consecutive
    crossing points, each marked kept or removed.
    """
    n = len(points)
    ts = [k * n / m for k in range(m)]
    q = [offset_point(points, t, d) for t in ts]  # @line L1
    for k in range(m):
        a, b, c = q[k - 1], q[k], q[(k + 1) % m]
        if b == c:
            raise ValueError("two consecutive offset samples coincide; sample with another m")
        if orient(a, b, c) == 0 and _dot_sign(a, b, c) < 0:
            raise ValueError("two adjacent offset segments fold back on a line; sample with another m")
    crossings = polyline_crossings(q)  # @line L2
    where = {}  # cut (segment, ratio) -> the crossing point, one float point per crossing
    for i, j in crossings:  # @line L3
        a, b, c, e = q[i], q[(i + 1) % m], q[j], q[(j + 1) % m]
        lam = crossing_ratio(a, b, c, e)
        mu = crossing_ratio(c, e, a, b)
        x = _at(q, j, mu) if mu in (0, 1) else _at(q, i, lam)  # a touching vertex stays exact
        where[_key(i, lam, m)] = x  # @line L4
        where[_key(j, mu, m)] = x  # @line L4
    cuts = sorted(where)  # @line L5
    if not cuts:
        start = (0, Fraction(0))
        where[start] = q[0]
        pairs = [(start, (m, Fraction(0)))]
    else:
        pairs = [(cuts[k], cuts[k + 1]) for k in range(len(cuts) - 1)]
        pairs.append((cuts[-1], (cuts[0][0] + m, cuts[0][1])))
    pieces = []
    for (i0, l0), (i1, l1) in pairs:  # @line L6
        first = where[(i0, l0)]
        last = where[(i1 % m, l1)]
        inner = [q[k % m] for k in range(i0 + 1, i1 + 1)]
        if inner and inner[0] == first:
            inner = inner[1:]
        if inner and inner[-1] == last:
            inner = inner[:-1]
        poly = [first] + inner + [last]
        u0 = (i0 + float(l0)) * n / m
        u1 = (i1 + float(l1)) * n / m
        mid = offset_point(points, (u0 + u1) / 2, d)  # @line L7
        dist = distance_to_curve(points, mid)  # @line L7
        keep = dist >= abs(d) - tol * max(1.0, abs(d))  # @line L8
        pieces.append(Piece((i0, l0), (i1 % m, l1), poly, mid, dist, keep))  # @line L9
    return q, crossings, pieces  # @line L10


def _key(i: int, lam: Fraction, m: int):
    """A cut as (segment, ratio in [0, 1)), so that a vertex has one name."""
    return ((i + 1) % m, Fraction(0)) if lam == 1 else (i, lam)


def _at(q, i, lam):
    m = len(q)
    a, b = q[i % m], q[(i + 1) % m]
    if lam == 0:
        return a
    if lam == 1:
        return b
    f = float(lam)
    return (a[0] + f * (b[0] - a[0]), a[1] + f * (b[1] - a[1]))


def trimmed_offset(points, d: float, m: int, tol: float = 1e-7) -> list:
    """The kept pieces of the trimmed offset, as polylines."""
    return [p.polyline for p in offset_trimming(points, d, m, tol)[2] if p.kept]
