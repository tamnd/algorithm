# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sweep-representation/. The authors are listed in prov/QNVPYX.jsonl.

"""Sweep representations of solids: extrusions and full revolutions of a polygon.

An Extrusion holds a simple polygon X in the plane z = 0 and a vector d with
d_z != 0. Its solid is the union of X + t d over t in [0, 1].

A Revolution holds a simple polygon X in the (r, z) half-plane r >= 0. Its
solid is the union over all angles a of the polygon turned by a about the
z axis.

Both classify a point with rational coordinates as IN, ON or OUT with exact
Fraction arithmetic. The revolution never computes the radius sqrt(x^2 + y^2):
it compares its square with the square of a rational number.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Callable, Sequence

IN, ON, OUT = "IN", "ON", "OUT"

Num = Fraction | int
Point2 = tuple[Fraction, Fraction]
Point3 = tuple[Fraction, Fraction, Fraction]


def _sign(v: Num) -> int:
    return (v > 0) - (v < 0)


def _cross(o: Point2, a: Point2, b: Point2) -> Fraction:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def _on_segment(p: Point2, a: Point2, b: Point2) -> bool:
    return (_cross(a, b, p) == 0
            and min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
            and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))


def _segments_meet(a: Point2, b: Point2, c: Point2, d: Point2) -> bool:
    d1, d2 = _sign(_cross(a, b, c)), _sign(_cross(a, b, d))
    d3, d4 = _sign(_cross(c, d, a)), _sign(_cross(c, d, b))
    if d1 * d2 < 0 and d3 * d4 < 0:
        return True
    return (_on_segment(c, a, b) or _on_segment(d, a, b)
            or _on_segment(a, c, d) or _on_segment(b, c, d))


def area2(poly: Sequence[Point2]) -> Fraction:
    """Twice the signed area of a polygon (positive if counterclockwise)."""
    n = len(poly)
    return sum((poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1]
                for i in range(n)), Fraction(0))


def is_simple(poly: Sequence[Point2]) -> bool:
    """True if the closed polygon has at least 3 vertices, nonzero area and no
    two edges that meet except adjacent edges at their common vertex. O(n^2)."""
    n = len(poly)
    if n < 3 or area2(poly) == 0:
        return False
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        if a == b:
            return False
        for j in range(i + 1, n):
            c, d = poly[j], poly[(j + 1) % n]
            if j == i + 1 or (i == 0 and j == n - 1):
                # adjacent edges: they may share only the common vertex
                shared = b if j == i + 1 else a
                other = d if j == i + 1 else c
                far = a if j == i + 1 else b
                if _cross(far, shared, other) == 0 and \
                        (_on_segment(other, far, shared) or _on_segment(far, shared, other)):
                    return False
                continue
            if _segments_meet(a, b, c, d):
                return False
    return True


def classify_profile(poly: Sequence[Point2], cmp_u: Callable[[Fraction], int],
                     z: Fraction) -> str:
    """Classify the point (u, z) against the closed polygon, where u is known
    only through cmp_u(q) = sign(u - q) for rational q. Crossing number with a
    ray towards +u and the half-open rule on vertices. O(n)."""
    inside = False
    n = len(poly)
    for i in range(n):
        (ar, az), (br, bz) = poly[i], poly[(i + 1) % n]
        if az == bz:
            if z == az and cmp_u(min(ar, br)) >= 0 and cmp_u(max(ar, br)) <= 0:
                return ON
            continue
        if min(az, bz) <= z <= max(az, bz):
            rc = ar + (z - az) * (br - ar) / (bz - az)
            c = cmp_u(rc)
            if c == 0:
                return ON
            if (az > z) != (bz > z) and c < 0:
                inside = not inside
    return IN if inside else OUT


def cmp_rational(u: Fraction) -> Callable[[Fraction], int]:
    return lambda q: _sign(u - q)


def cmp_sqrt(s: Fraction) -> Callable[[Fraction], int]:
    """sign(sqrt(s) - q) for s >= 0, exactly, by comparing s with q^2."""
    def cmp(q: Fraction) -> int:
        if q < 0:
            return 1
        return _sign(s - q * q)
    return cmp


def _f(v: Num) -> Fraction:
    return Fraction(v)


class Extrusion:
    """The translational sweep of a polygon X in z = 0 along the vector d.

    Precondition: X is simple and d_z != 0. classify and volume take O(n) time
    for n vertices; the representation takes Theta(n) space.
    """

    def __init__(self, profile: Sequence[tuple[Num, Num]], d: tuple[Num, Num, Num]):
        self.profile: list[Point2] = [(_f(x), _f(y)) for x, y in profile]
        self.d: Point3 = (_f(d[0]), _f(d[1]), _f(d[2]))

    def check_invariant(self) -> bool:
        return self.d[2] != 0 and is_simple(self.profile)

    def classify(self, p: tuple[Num, Num, Num]) -> str:
        px, py, pz = _f(p[0]), _f(p[1]), _f(p[2])
        dx, dy, dz = self.d
        t = pz / dz  # @line L1
        if t < 0 or t > 1:  # @line L2
            return OUT
        q = (px - t * dx, py - t * dy)  # @line L3
        c = classify_profile(self.profile, cmp_rational(q[0]), q[1])  # @line L4
        if c != OUT and (t == 0 or t == 1):  # @line L5
            return ON
        return c  # @line L6

    def volume(self) -> Fraction:
        """The exact volume: area(X) times |d_z| (Cavalieri)."""
        return abs(area2(self.profile)) / 2 * abs(self.d[2])


class Revolution:
    """The full rotational sweep of a polygon X in the half-plane r >= 0 of
    the (r, z) plane about the z axis.

    Precondition: X is simple and every vertex has r >= 0. classify and
    volume take O(n) time; the representation takes Theta(n) space.
    """

    def __init__(self, profile: Sequence[tuple[Num, Num]]):
        self.profile: list[Point2] = [(_f(r), _f(z)) for r, z in profile]

    def check_invariant(self) -> bool:
        return all(r >= 0 for r, _ in self.profile) and is_simple(self.profile)

    def _axis_covers(self, z: Fraction) -> bool:
        """True if edges of X on the axis r = 0 contain (0, z) and reach both
        above and below it."""
        up = down = False
        n = len(self.profile)
        for i in range(n):
            (ar, az), (br, bz) = self.profile[i], self.profile[(i + 1) % n]
            if ar == 0 and br == 0 and min(az, bz) <= z <= max(az, bz):
                up = up or max(az, bz) > z
                down = down or min(az, bz) < z
        return up and down

    def classify(self, p: tuple[Num, Num, Num]) -> str:
        px, py, pz = _f(p[0]), _f(p[1]), _f(p[2])
        s = px * px + py * py  # @line L7
        c = classify_profile(self.profile, cmp_sqrt(s), pz)  # @line L8
        if s > 0 or c == OUT:  # @line L9
            return c
        if self._axis_covers(pz):  # @line L10
            return IN
        return ON  # @line L11

    def volume_over_pi(self) -> Fraction:
        """The exact volume divided by pi. By Pappus, V = 2 pi times the first
        moment of X about the axis, and the moment of a polygon is
        (1/6) sum (r_i + r_{i+1}) (r_i z_{i+1} - r_{i+1} z_i)."""
        poly, n = self.profile, len(self.profile)
        m = sum(((poly[i][0] + poly[(i + 1) % n][0])
                 * (poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1])
                 for i in range(n)), Fraction(0)) / 6
        return 2 * abs(m)
