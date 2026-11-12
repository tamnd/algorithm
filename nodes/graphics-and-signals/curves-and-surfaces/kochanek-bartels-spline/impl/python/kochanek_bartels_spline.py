# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kochanek-bartels-spline/. The authors are listed in prov/9M4696.jsonl.

"""Kochanek-Bartels (TCB) splines.

Keys P[0..n] with a tension t, a continuity c and a bias b per key. The curve
runs from P[1] to P[n-1]; P[0] and P[n] only shape the end tangents. Each inner
key has an incoming tangent (the end of the segment that arrives) and an
outgoing tangent (the start of the segment that leaves). Points are tuples;
use fractions.Fraction for exact results.
Cost: O(d) per key for the tangents and O(d) per evaluated point.
"""

from bisect import bisect_right
from typing import List, Optional, Sequence, Tuple

Point = Tuple


def kb_tangents(prev: Point, key: Point, nxt: Point, t=0, c=0, b=0) -> Tuple[Point, Point]:
    """The (incoming, outgoing) tangents at key, per unit of the segment parameter u."""
    din = tuple(y - x for x, y in zip(prev, key))
    dout = tuple(y - x for x, y in zip(key, nxt))
    a_in = (1 - t) * (1 - c) * (1 + b)
    b_in = (1 - t) * (1 + c) * (1 - b)
    a_out = (1 - t) * (1 + c) * (1 + b)
    b_out = (1 - t) * (1 - c) * (1 - b)
    incoming = tuple((a_in * x + b_in * y) / 2 for x, y in zip(din, dout))
    outgoing = tuple((a_out * x + b_out * y) / 2 for x, y in zip(din, dout))
    return incoming, outgoing


def hermite(p0: Point, m0: Point, p1: Point, m1: Point, u, order: int = 0) -> Point:
    """The cubic Hermite segment, or its first derivative in u when order == 1."""
    if order == 0:
        w = (2 * u ** 3 - 3 * u ** 2 + 1, u ** 3 - 2 * u ** 2 + u, u ** 3 - u ** 2, -2 * u ** 3 + 3 * u ** 2)
    else:
        w = (6 * u ** 2 - 6 * u, 3 * u ** 2 - 4 * u + 1, 3 * u ** 2 - 2 * u, -6 * u ** 2 + 6 * u)
    return tuple(w[0] * a + w[1] * m + w[2] * e + w[3] * q for a, m, e, q in zip(p0, m0, m1, p1))


def kb_segment_tangents(points: Sequence[Point], params: Sequence[Tuple], i: int,
                        times: Optional[Sequence] = None) -> Tuple[Point, Point]:
    """The end tangents (in u) of segment i, from P[i] to P[i+1], 1 <= i <= n - 2.

    Without times the parameter is uniform. With key times the tangent at a key is
    turned into a velocity by dividing by the mean of its two interval lengths,
    and then multiplied by the length of the segment (the chain rule), so that
    c = 0 gives a C1 curve in time.
    """
    _, out_i = kb_tangents(points[i - 1], points[i], points[i + 1], *params[i])
    in_j, _ = kb_tangents(points[i], points[i + 1], points[i + 2], *params[i + 1])
    if times is None:
        return out_i, in_j
    h = times[i + 1] - times[i]
    s0 = 2 * h / (times[i + 1] - times[i - 1])
    s1 = 2 * h / (times[i + 2] - times[i])
    return tuple(s0 * x for x in out_i), tuple(s1 * x for x in in_j)


def kb_curve(points: Sequence[Point], params: Sequence[Tuple], s, times: Optional[Sequence] = None,
             order: int = 0) -> Point:
    """Evaluate the curve (order 0) or its velocity (order 1) at s.

    Without times, s is in [1, n - 1] and segment i covers [i, i + 1]. With times,
    s is in [times[1], times[n-1]] and the velocity is d/ds.
    Precondition: n >= 3, one (t, c, b) triple per key, times strictly increasing.
    """
    n = len(points) - 1
    if n < 3 or len(params) != n + 1:
        raise ValueError("need at least four keys and one (t, c, b) per key")
    knots = list(range(n + 1)) if times is None else list(times)
    if any(y <= x for x, y in zip(knots, knots[1:])):
        raise ValueError("times must increase strictly")
    i = min(max(bisect_right(knots, s) - 1, 1), n - 2)
    h = knots[i + 1] - knots[i]
    m0, m1 = kb_segment_tangents(points, params, i, times)
    v = hermite(points[i], m0, points[i + 1], m1, (s - knots[i]) / h, order)
    return v if order == 0 else tuple(x / h for x in v)


def one_sided_velocity(points, params, key: int, side: str, times=None) -> Point:
    """The velocity at key from the segment on its left ("left") or on its right ("right")."""
    knots = list(range(len(points))) if times is None else list(times)
    i = key - 1 if side == "left" else key
    h = knots[i + 1] - knots[i]
    m0, m1 = kb_segment_tangents(points, params, i, times)
    return tuple(x / h for x in (m1 if side == "left" else m0))
