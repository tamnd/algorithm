# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spread-indicator/. The authors are listed in prov/B4114Q.jsonl.

"""Spread indicators (minimization of the objectives; smaller spread is better).

deb_spread: the Delta of Deb, Pratap, Agarwal and Meyarivan (2002) for two
objectives. Sort A by the first objective, let d_i be the N - 1 distances
between neighbours, dbar their mean, and d_f, d_l the distances from the two
extreme points of the reference front to the two end points of A:

    Delta = (d_f + d_l + sum |d_i - dbar|) / (d_f + d_l + (N - 1) dbar)

generalized_spread: the form of Zhou et al. (2006) for any p, with d(x, A) the
distance from x to its nearest other point of A and e_m the extreme points of
the reference set R:

    Delta* = (sum_m d(e_m, A) + sum_x |d(x, A) - dbar|) / (sum_m d(e_m, A) + |A| dbar)

spacing: Schott's standard deviation of the nearest-neighbour L1 distances.
"""

import math
from typing import Sequence

Points = Sequence[Sequence[float]]


def deb_spread(a: Points, first: Sequence[float], last: Sequence[float]) -> float:
    """first is the extreme point with the smallest first objective, last the one with the largest."""
    pts = sorted(a)
    gaps = [math.dist(u, v) for u, v in zip(pts, pts[1:])]
    df, dl = math.dist(first, pts[0]), math.dist(last, pts[-1])
    dbar = sum(gaps) / len(gaps) if gaps else 0.0
    den = df + dl + len(gaps) * dbar
    return (df + dl + sum(abs(g - dbar) for g in gaps)) / den if den else 0.0


def extremes(ref: Points) -> list:
    """For each objective m, the point of ref with the largest value of objective m (ties: smallest others)."""
    p = len(ref[0])
    return [max(ref, key=lambda r: (r[m], [-r[k] for k in range(p) if k != m])) for m in range(p)]


def generalized_spread(a: Points, ref: Points) -> float:
    if len(a) < 2:
        raise ValueError("needs at least two points")
    nn = [min(math.dist(x, y) for j, y in enumerate(a) if j != i) for i, x in enumerate(a)]
    dbar = sum(nn) / len(nn)
    de = sum(min(math.dist(e, x) for x in a) for e in extremes(ref))
    den = de + len(a) * dbar
    return (de + sum(abs(d - dbar) for d in nn)) / den if den else 0.0


def spacing(a: Points) -> float:
    nn = [min(sum(abs(u - v) for u, v in zip(x, y)) for j, y in enumerate(a) if j != i) for i, x in enumerate(a)]
    mean = sum(nn) / len(nn)
    return math.sqrt(sum((d - mean) ** 2 for d in nn) / (len(nn) - 1))
