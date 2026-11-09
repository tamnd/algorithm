# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/igd-indicator/. The authors are listed in prov/4MNQFD.jsonl.

"""Generational distance, inverted generational distance and IGD+ (minimization).

R is a reference set of points on or near the Pareto front, A the set to judge.

    GD(A, R)   = mean over a in A of min over r in R of |a - r|
    IGD(A, R)  = mean over r in R of min over a in A of |a - r|
    IGD+(A, R) = mean over r in R of min over a in A of d+(r, a),
                 d+(r, a) = |max(a - r, 0)|  (only the parts where a is worse)

All distances are Euclidean. Each value costs O(p |A| |R|).
"""

import math
from typing import Sequence

Points = Sequence[Sequence[float]]


def d_plus(r: Sequence[float], a: Sequence[float]) -> float:
    return math.sqrt(sum(max(u - v, 0) ** 2 for u, v in zip(a, r)))


def gd(a: Points, ref: Points) -> float:
    return sum(min(math.dist(x, r) for r in ref) for x in a) / len(a)


def igd(a: Points, ref: Points) -> float:
    return sum(min(math.dist(x, r) for x in a) for r in ref) / len(ref)


def igd_plus(a: Points, ref: Points) -> float:
    return sum(min(d_plus(r, x) for x in a) for r in ref) / len(ref)


def delta_p(a: Points, ref: Points, q: float = 1) -> float:
    """The averaged Hausdorff distance of Schuetze et al. with power means of order q."""
    g = (sum(min(math.dist(x, r) for r in ref) ** q for x in a) / len(a)) ** (1 / q)
    i = (sum(min(math.dist(x, r) for x in a) ** q for r in ref) / len(ref)) ** (1 / q)
    return max(g, i)
