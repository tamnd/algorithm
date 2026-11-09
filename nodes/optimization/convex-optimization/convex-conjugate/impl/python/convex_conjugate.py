# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/convex-conjugate/. The authors are listed in prov/VCH05B.jsonl.

"""Discrete Legendre-Fenchel transform in one variable.

Given samples (x_i, f_i) and slopes s_j, compute
    f*(s_j) = max_i (s_j * x_i - f_i).
The maximum over all samples equals the maximum over the vertices of the
lower convex hull of the samples, and the optimal vertex moves right as s
grows. So after sorting, one hull pass and one merge pass give all values
in O(n log n + k log k) time. Exact with Fractions or ints.
"""

from fractions import Fraction

Num = int | Fraction


def lower_hull(points: list[tuple[Num, Num]]) -> list[tuple[Num, Num]]:
    """Vertices of the lower convex hull, by increasing x. Equal x keeps the lowest value."""
    pts = sorted(points)
    hull: list[tuple[Num, Num]] = []
    for p in pts:
        if hull and hull[-1][0] == p[0]:
            continue  # same x, larger or equal value: never on the lower hull
        while len(hull) >= 2:
            (x1, y1), (x2, y2) = hull[-2], hull[-1]
            # drop hull[-1] if it is on or above the segment hull[-2] -> p
            if (y2 - y1) * (p[0] - x1) >= (p[1] - y1) * (x2 - x1):
                hull.pop()
            else:
                break
        hull.append(p)
    return hull


def discrete_conjugate(xs: list[Num], fs: list[Num], slopes: list[Num]) -> list[Num]:
    """Return [max_i (s * xs[i] - fs[i]) for s in slopes]."""
    if not xs:
        raise ValueError("need at least one sample")
    hull = lower_hull(list(zip(xs, fs)))
    order = sorted(range(len(slopes)), key=lambda j: slopes[j])
    out: list[Num] = [0] * len(slopes)
    v = 0
    for j in order:
        s = slopes[j]
        # advance while the next hull edge has slope below s
        while v + 1 < len(hull):
            (x1, y1), (x2, y2) = hull[v], hull[v + 1]
            if (y2 - y1) < s * (x2 - x1):
                v += 1
            else:
                break
        x, y = hull[v]
        out[j] = s * x - y
    return out
