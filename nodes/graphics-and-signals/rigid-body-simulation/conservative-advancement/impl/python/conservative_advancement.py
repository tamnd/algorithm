# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conservative-advancement/. The authors are listed in prov/C2728X.jsonl.

"""Conservative advancement for two convex polygons with linear and angular velocity.

A body is a convex polygon with its vertices in local coordinates around its center of rotation,
a start position c0 and angle theta0, a constant velocity v and a constant angular velocity omega.
At time t its vertices are c0 + v t + R(theta0 + omega t) p.

conservative_advancement walks forward in time. At each time it computes the distance d and the
unit normal n from the closest point of B to the closest point of A. No point of the two bodies
can close the gap along n faster than mu = -n . (vA - vB) + |omegaA| rA + |omegaB| rB, where r is
the largest distance of a vertex from the center. So the bodies cannot touch before t + d / mu,
and the walk steps there. It stops when d <= tol (a time of impact, from below) or when the time
passes T or mu <= 0 (no contact in the interval). Floats are used, and tol must be positive.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

Vec = tuple[float, float]


@dataclass(frozen=True)
class Body:
    local: list[Vec]  # counterclockwise convex polygon around the center of rotation
    c0: Vec
    theta0: float
    v: Vec
    omega: float

    def at(self, t: float) -> list[Vec]:
        th = self.theta0 + self.omega * t
        c, s = math.cos(th), math.sin(th)
        cx, cy = self.c0[0] + self.v[0] * t, self.c0[1] + self.v[1] * t
        return [(cx + c * x - s * y, cy + s * x + c * y) for x, y in self.local]

    def radius(self) -> float:
        return max(math.hypot(x, y) for x, y in self.local)


def _closest_on_segment(p: Vec, a: Vec, b: Vec) -> Vec:
    ex, ey = b[0] - a[0], b[1] - a[1]
    L = ex * ex + ey * ey
    lam = 0.0 if L == 0 else ((p[0] - a[0]) * ex + (p[1] - a[1]) * ey) / L
    lam = min(1.0, max(0.0, lam))
    return (a[0] + lam * ex, a[1] + lam * ey)


def _orient(a: Vec, b: Vec, c: Vec) -> float:
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def _inside(P: list[Vec], x: Vec) -> bool:
    return all(_orient(P[i], P[(i + 1) % len(P)], x) >= 0 for i in range(len(P)))


def _segments_cross(a: Vec, b: Vec, c: Vec, d: Vec) -> bool:
    # a proper crossing; touching cases give a distance of 0 below
    return _orient(a, b, c) * _orient(a, b, d) < 0 and _orient(c, d, a) * _orient(c, d, b) < 0


def polygon_distance(P: list[Vec], Q: list[Vec]) -> tuple[float, Vec, Vec]:
    """The distance of two convex polygons and a closest pair (pa on P, pb on Q); 0 if they meet."""
    for i in range(len(P)):
        for j in range(len(Q)):
            if _segments_cross(P[i], P[(i + 1) % len(P)], Q[j], Q[(j + 1) % len(Q)]):
                return 0.0, P[i], P[i]
    if _inside(Q, P[0]):
        return 0.0, P[0], P[0]
    if _inside(P, Q[0]):
        return 0.0, Q[0], Q[0]
    best = (math.inf, P[0], Q[0])
    for X, Y, flip in ((P, Q, False), (Q, P, True)):
        for x in X:
            for k in range(len(Y)):
                y = _closest_on_segment(x, Y[k], Y[(k + 1) % len(Y)])
                d = math.hypot(x[0] - y[0], x[1] - y[1])
                if d < best[0]:
                    best = (d, y, x) if flip else (d, x, y)
    return best


def conservative_advancement(A: Body, B: Body, T: float = 1.0, tol: float = 1e-6, max_iter: int = 100000):
    """The first time in [0, T] at which the distance is at most tol, or None, and the step count.

    The returned time is never later than the first time of contact.
    """
    rA, rB = A.radius(), B.radius()
    spin = abs(A.omega) * rA + abs(B.omega) * rB
    dv = (A.v[0] - B.v[0], A.v[1] - B.v[1])
    t = 0.0  # @line L1
    for steps in range(max_iter):  # @line L2
        d, pa, pb = polygon_distance(A.at(t), B.at(t))  # @line L3
        if d <= tol:  # @line L4
            return t, steps
        n = ((pa[0] - pb[0]) / d, (pa[1] - pb[1]) / d)  # @line L5
        mu = -(n[0] * dv[0] + n[1] * dv[1]) + spin  # @line L6
        if mu <= 0:  # @line L7
            return None, steps
        t += d / mu  # @line L8
        if t > T:  # @line L9
            return None, steps + 1
    raise RuntimeError("conservative advancement did not reach tol in max_iter steps")
