# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alt-godau-algorithm/. The authors are listed in prov/BQ9SVX.jsonl.

from fractions import Fraction
from typing import Optional, Union

Number = Union[int, Fraction]
Point = tuple[Number, Number]
# A real number A + B * sqrt(X) with rational A, B and rational X >= 0.
Surd = tuple[Fraction, Fraction, Fraction]
Interval = Optional[tuple[Surd, Surd]]

ZERO: Surd = (Fraction(0), Fraction(0), Fraction(0))
ONE: Surd = (Fraction(1), Fraction(0), Fraction(0))


def _sgn(x: Fraction) -> int:
    return (x > 0) - (x < 0)


def sign_one_root(a: Fraction, b: Fraction, x: Fraction) -> int:
    """Exact sign of a + b * sqrt(x) for rational a, b and x >= 0."""
    if b == 0 or x == 0:
        return _sgn(a)
    sa, sb = _sgn(a), _sgn(b)
    if sa >= 0 and sb >= 0:
        return 1
    if sa <= 0 and sb <= 0:
        return -1
    d = _sgn(a * a - b * b * x)  # compare |a| with |b| sqrt(x)
    return d if sa > 0 else -d


def sign_two_roots(a: Fraction, b: Fraction, x: Fraction, c: Fraction, y: Fraction) -> int:
    """Exact sign of a + b sqrt(x) + c sqrt(y): compare L = a + b sqrt(x) with R = -c sqrt(y)."""
    sl = sign_one_root(a, b, x)
    sr = 0 if y == 0 else _sgn(-c)
    if sl >= 0 >= sr:
        return 0 if sl == 0 and sr == 0 else 1
    if sl <= 0 <= sr:
        return -1
    s = sign_one_root(a * a + b * b * x - c * c * y, 2 * a * b, x)  # sign of L^2 - R^2
    return s if sl > 0 else -s


def compare(u: Surd, v: Surd) -> int:
    """Exact sign of u - v."""
    return sign_two_roots(u[0] - v[0], u[1], u[2], -v[1], v[2])


def _dist2(p: Point, q: Point) -> Fraction:
    return Fraction((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


def free_interval(x: Point, a: Point, b: Point, eps2: Fraction) -> Interval:
    """The parameters t in [0, 1] with |a + t (b - a) - x|^2 <= eps2, as exact surds, or None."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    wx, wy = a[0] - x[0], a[1] - x[1]
    qa = Fraction(dx * dx + dy * dy)
    qb = Fraction(dx * wx + dy * wy)
    qc = Fraction(wx * wx + wy * wy) - eps2
    if qa == 0:  # degenerate segment: every t or none
        return (ZERO, ONE) if qc <= 0 else None
    disc = qb * qb - qa * qc  # roots t = (-qb -+ sqrt(disc)) / qa
    if disc < 0:
        return None
    lo: Surd = (-qb / qa, Fraction(-1) / qa, disc)
    hi: Surd = (-qb / qa, Fraction(1) / qa, disc)
    if compare(lo, ZERO) < 0:
        lo = ZERO
    if compare(hi, ONE) > 0:
        hi = ONE
    if compare(lo, hi) > 0:
        return None
    return (lo, hi)


def frechet_decide(P: list[Point], Q: list[Point], eps2: Number) -> bool:
    """Decide whether the Frechet distance of the polygonal curves P and Q is at most sqrt(eps2).

    Precondition: P and Q are nonempty lists of points with int or Fraction coordinates, eps2 >= 0.
    Exact, O(p q) arithmetic operations on rationals for p = len(P) - 1 and q = len(Q) - 1 segments.
    """
    e = Fraction(eps2)
    if len(P) == 1 or len(Q) == 1:  # a point against a curve: the farthest vertex decides
        a, B = (P[0], Q) if len(P) == 1 else (Q[0], P)
        return all(_dist2(a, b) <= e for b in B)
    p, q = len(P) - 1, len(Q) - 1
    if _dist2(P[0], Q[0]) > e or _dist2(P[p], Q[q]) > e:  # @line L1
        return False
    L = [[free_interval(P[i], Q[j], Q[j + 1], e) for j in range(q)] for i in range(p + 1)]  # @line L2
    B = [[free_interval(Q[j], P[i], P[i + 1], e) for j in range(q + 1)] for i in range(p)]
    LR: list[list[Interval]] = [[None] * q for _ in range(p + 1)]
    BR: list[list[Interval]] = [[None] * (q + 1) for _ in range(p)]
    LR[0][0] = L[0][0]  # @line L3
    for j in range(1, q):
        prev = LR[0][j - 1]
        LR[0][j] = L[0][j] if prev is not None and compare(prev[1], ONE) == 0 else None
    BR[0][0] = B[0][0]
    for i in range(1, p):
        prev = BR[i - 1][0]
        BR[i][0] = B[i][0] if prev is not None and compare(prev[1], ONE) == 0 else None
    for i in range(p):  # @line L4
        for j in range(q):  # @line L5
            LR[i + 1][j] = _reach(L[i + 1][j], BR[i][j], LR[i][j])  # @line L6
            BR[i][j + 1] = _reach(B[i][j + 1], LR[i][j], BR[i][j])  # @line L7
    top, right = LR[p][q - 1], BR[p - 1][q]
    return (top is not None and compare(top[1], ONE) == 0) or (  # @line L8
        right is not None and compare(right[1], ONE) == 0
    )


def _reach(free: Interval, across: Interval, along: Interval) -> Interval:
    """Reachable part of an exit edge of a cell.

    across: reachable part of the entry edge perpendicular to the exit edge (any free exit point is reachable).
    along: reachable part of the entry edge parallel to it (only exit points at or above its lowest point).
    """
    if free is None:
        return None
    if across is not None:
        return free
    if along is None:
        return None
    lo = free[0] if compare(free[0], along[0]) >= 0 else along[0]
    return (lo, free[1]) if compare(lo, free[1]) <= 0 else None


def _point_segment_dist2(x: Point, a: Point, b: Point) -> Fraction:
    dx, dy = b[0] - a[0], b[1] - a[1]
    den = dx * dx + dy * dy
    if den == 0:
        return _dist2(x, a)
    t = Fraction((x[0] - a[0]) * dx + (x[1] - a[1]) * dy, 1) / den
    t = min(max(t, Fraction(0)), Fraction(1))
    return _dist2(x, (a[0] + t * dx, a[1] + t * dy))


def critical_values(P: list[Point], Q: list[Point]) -> list[Fraction]:
    """Squared critical values of types (a), (b) and (c), without repeats."""
    C = {_dist2(P[0], Q[0]), _dist2(P[-1], Q[-1])}  # type (a)
    for U, V in ((P, Q), (Q, P)):
        for j in range(len(V) - 1):
            a, b = V[j], V[j + 1]
            for x in U:
                C.add(_point_segment_dist2(x, a, b))  # type (b)
            d = (b[0] - a[0], b[1] - a[1])
            for k in range(len(U)):
                for l in range(k + 1, len(U)):
                    n = (U[l][0] - U[k][0], U[l][1] - U[k][1])
                    den = 2 * (d[0] * n[0] + d[1] * n[1])
                    if den == 0:
                        continue
                    rhs = (U[l][0] ** 2 + U[l][1] ** 2) - (U[k][0] ** 2 + U[k][1] ** 2)
                    t = Fraction(rhs - 2 * (a[0] * n[0] + a[1] * n[1]), 1) / den
                    if 0 <= t <= 1:  # the bisector of U[k], U[l] crosses the segment: type (c)
                        C.add(_dist2(U[k], (a[0] + t * d[0], a[1] + t * d[1])))
    return list(C)


def frechet_distance2(P: list[Point], Q: list[Point]) -> Fraction:
    """The exact squared Frechet distance of the polygonal curves P and Q.

    Precondition: P and Q are nonempty lists of points with int or Fraction coordinates.
    Searches the O(p^2 q + p q^2) critical values with the decision procedure:
    O((p^2 q + p q^2) log(p q) + p q log(p q)) time, the simple version of Alt and Godau.
    """
    if len(P) == 1 or len(Q) == 1:  # a point against a curve: the farthest vertex
        a, B = (P[0], Q) if len(P) == 1 else (Q[0], P)
        return max(_dist2(a, b) for b in B)
    C = critical_values(P, Q)  # @line L9
    C.sort()  # @line L10
    lo, hi = 0, len(C) - 1
    while lo < hi:  # @line L11
        mid = (lo + hi) // 2
        if frechet_decide(P, Q, C[mid]):
            hi = mid
        else:
            lo = mid + 1
    return C[lo]  # @line L12
