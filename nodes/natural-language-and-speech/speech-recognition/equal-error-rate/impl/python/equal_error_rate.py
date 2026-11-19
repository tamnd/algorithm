# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/equal-error-rate/. The authors are listed in prov/QFSA7K.jsonl.

"""Equal error rate of a detector on a finite list of trials.

A trial is accepted when its score is at least the threshold t. For a list of
target scores and a list of nontarget scores,

    Pmiss(t) = (number of target scores < t) / (number of targets),
    Pfa(t)   = (number of nontarget scores >= t) / (number of nontargets).

On a finite list the two rates move in steps, so they are rarely equal at any
threshold. eer_rocch follows Brummer and de Villiers (BOSARIS): it takes the
lower convex hull of the operating points (the ROC convex hull) and returns
the rate where the hull crosses the line Pmiss = Pfa. eer_nearest returns the
mean of the two rates at the threshold where they are closest. All rates are
exact fractions.
"""

from bisect import bisect_left
from fractions import Fraction
from typing import List, Sequence, Tuple

Point = Tuple[Fraction, Fraction]  # (Pfa, Pmiss)


def operating_points(targets: Sequence[float], nontargets: Sequence[float]) -> List[Tuple[float, Fraction, Fraction]]:
    """Return (t, Pfa, Pmiss) for t at every distinct score and at +infinity, in increasing t."""
    if not targets or not nontargets:
        raise ValueError("need at least one target and one nontarget score")
    tar, non = sorted(targets), sorted(nontargets)
    nt, nn = len(tar), len(non)
    out = []
    for t in sorted(set(tar) | set(non)) + [float("inf")]:
        pmiss = Fraction(bisect_left(tar, t), nt)
        pfa = Fraction(nn - bisect_left(non, t), nn)
        out.append((t, pfa, pmiss))
    return out


def cross(o: Point, a: Point, b: Point) -> Fraction:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def lower_hull(points: Sequence[Point]) -> List[Point]:
    """Return the lower convex hull of the points, from the smallest Pfa to the largest."""
    hull: List[Point] = []
    for p in sorted(set(points)):
        while len(hull) >= 2 and cross(hull[-2], hull[-1], p) <= 0:
            hull.pop()
        hull.append(p)
    return hull


def rocch(targets: Sequence[float], nontargets: Sequence[float]) -> List[Point]:
    """Return the vertices (Pfa, Pmiss) of the ROC convex hull."""
    pts = [(pfa, pmiss) for _, pfa, pmiss in operating_points(targets, nontargets)]  # @line L1
    pts += [(Fraction(0), Fraction(1)), (Fraction(1), Fraction(0))]  # @line L2
    # Keep only the vertices from (0, 1) down to the first point with Pmiss = 0.
    hull = lower_hull(pts)  # @line L3
    k = next(i for i, p in enumerate(hull) if p[1] == 0)
    return hull[: k + 1]


def eer_rocch(targets: Sequence[float], nontargets: Sequence[float]) -> Fraction:
    """Return the equal error rate of the ROC convex hull."""
    hull = rocch(targets, nontargets)
    if len(hull) == 1:  # the point (0, 0): the scores separate the classes
        return Fraction(0)
    for (f1, m1), (f2, m2) in zip(hull, hull[1:]):
        if m1 >= f1 and m2 <= f2:  # @line L4
            df, dm = f2 - f1, m2 - m1
            s = (m1 - f1) / (df - dm)  # @line L5
            return f1 + s * df  # @line L6
    raise AssertionError("the hull always crosses Pmiss = Pfa")


def eer_nearest(targets: Sequence[float], nontargets: Sequence[float]) -> Fraction:
    """Return (Pfa + Pmiss) / 2 at the threshold where |Pfa - Pmiss| is smallest (the first such threshold)."""
    best = min(operating_points(targets, nontargets), key=lambda r: abs(r[1] - r[2]))
    return (best[1] + best[2]) / 2


def min_dcf(targets: Sequence[float], nontargets: Sequence[float], p_target: Fraction,
            c_miss: Fraction = Fraction(1), c_fa: Fraction = Fraction(1)) -> Fraction:
    """Return min over thresholds of c_miss p_target Pmiss + c_fa (1 - p_target) Pfa."""
    return min(c_miss * p_target * pm + c_fa * (1 - p_target) * pf
               for _, pf, pm in operating_points(targets, nontargets))
