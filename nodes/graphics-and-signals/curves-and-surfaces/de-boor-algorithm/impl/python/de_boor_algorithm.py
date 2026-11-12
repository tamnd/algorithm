# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/de-boor-algorithm/. The authors are listed in prov/TVCVSK.jsonl.

"""De Boor's algorithm: evaluate a B-spline curve by repeated convex combinations.

A curve of degree p has control points P_0, ..., P_n (tuples of numbers of any
dimension) and a non-decreasing knot vector t_0, ..., t_m with m = n + p + 1.
The domain is [t_p, t_(n+1)]. Knots, parameters and coordinates may be int or
Fraction; with Fraction every result is exact.
"""

from fractions import Fraction
from typing import Sequence, Tuple, Union

Number = Union[int, Fraction]
Point = Tuple[Number, ...]


def find_span(knots: Sequence[Number], p: int, u: Number) -> int:
    """Return mu in [p, n] with t_mu <= u < t_(mu+1); at u = t_(n+1) the last nonempty span.

    Precondition: t_p <= u <= t_(n+1) and t_p < t_(n+1). Cost: O(log m).
    """
    n = len(knots) - p - 2
    if p < 0 or n < p:
        raise ValueError("need at least p + 1 control points")
    if not knots[p] <= u <= knots[n + 1] or knots[p] == knots[n + 1]:
        raise ValueError("u must lie in the domain [t_p, t_(n+1)]")
    if u == knots[n + 1]:
        mu = n
        while knots[mu] == knots[mu + 1]:
            mu -= 1
        return mu
    lo, hi = p, n + 1  # invariant: t_lo <= u < t_hi
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if u < knots[mid]:
            hi = mid
        else:
            lo = mid
    return lo


def de_boor(knots: Sequence[Number], p: int, ctrl: Sequence[Point], u: Number) -> Tuple[Fraction, ...]:
    """Return the point C(u) = sum_i N_(i,p)(u) P_i of the B-spline curve.

    Precondition: len(knots) == len(ctrl) + p + 1 and u in [t_p, t_(n+1)].
    Cost: O(log m) for the span search, then p(p + 1)/2 convex combinations
    of points, so O(p^2 d) arithmetic operations in dimension d, and O(p d)
    extra space.
    """
    if len(knots) != len(ctrl) + p + 1:
        raise ValueError("need len(knots) == len(ctrl) + p + 1")
    mu = find_span(knots, p, u)  # @line L1
    d = [tuple(Fraction(c) for c in ctrl[mu - p + j]) for j in range(p + 1)]  # @line L2
    for r in range(1, p + 1):  # @line L3
        for j in range(p, r - 1, -1):  # @line L4
            i = mu - p + j
            alpha = Fraction(u - knots[i]) / (knots[i + p - r + 1] - knots[i])  # @line L5
            d[j] = tuple((1 - alpha) * a + alpha * b for a, b in zip(d[j - 1], d[j]))  # @line L6
    return d[p]  # @line L7


def nurbs_point(
    knots: Sequence[Number],
    p: int,
    ctrl: Sequence[Point],
    weights: Sequence[Number],
    u: Number,
) -> Tuple[Fraction, ...]:
    """Evaluate a NURBS curve: run de Boor on (w_i P_i, w_i) and divide by the last coordinate.

    Precondition: as for de_boor, and every weight is positive. Cost: as for
    de_boor in dimension d + 1, plus d divisions.
    """
    if len(weights) != len(ctrl) or any(w <= 0 for w in weights):
        raise ValueError("need one positive weight for each control point")
    homogeneous = [tuple(w * c for c in pt) + (w,) for pt, w in zip(ctrl, weights)]
    *xs, w = de_boor(knots, p, homogeneous, u)
    return tuple(x / w for x in xs)
