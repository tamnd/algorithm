# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/circular-binary-segmentation/. The authors are listed in prov/6NYYG1.jsonl.
"""Circular binary segmentation (CBS) of Olshen, Venkatraman, Lucito and Wigler (2004).

The input is a list x of numbers along a chromosome, for example log2 ratios of
read depth in windows. Positions are 0-based and segments are half-open, so the
segment (lo, hi) holds x[lo], ..., x[hi - 1].

The statistic of an arc (i, j) of a segment y of length n compares the mean of
y[i:j] with the mean of the rest of y, as if y were bent into a circle:

    Z(i, j) = |mean(y[i:j]) - mean(rest)| / (s * sqrt(1 / k + 1 / (n - k))),  k = j - i,

with s the sample standard deviation of y. The test statistic is the largest
Z over the arcs with 1 <= k <= n - 1. Its p-value comes from random
permutations of y. Because s does not change under a permutation, the test is
exact for exchangeable data at any choice of s.

What this code leaves out compared with the DNAcopy package: the early stop of
the permutation count and the tail approximation of Venkatraman and Olshen
(2007), the check that removes a split whose parts do not differ enough, the
minimum width of an arc, outlier smoothing and weights.
"""

from __future__ import annotations

import math
import random
from typing import List, Sequence, Tuple


def max_arc(y: Sequence[float]) -> Tuple[float, int, int]:
    """Return (T, i, j): the largest arc statistic of y and its arc y[i:j].

    Ties go to the first arc in the order of i, then j. A constant y gives (0.0, 0, n).
    """
    n = len(y)
    S = [0.0] * (n + 1)  # @line L12
    for k in range(n):
        S[k + 1] = S[k] + y[k]
    mean = S[n] / n
    var = sum((v - mean) ** 2 for v in y) / (n - 1) if n > 1 else 0.0
    s = math.sqrt(var)  # @line L13
    if s == 0.0:
        return 0.0, 0, n
    best, bi, bj = -1.0, 0, n
    for i in range(n):  # @line L14
        for j in range(i + 1, n + 1):
            k = j - i
            if k == n:
                continue
            inside = S[j] - S[i]
            d = inside / k - (S[n] - inside) / (n - k)  # @line L15
            z = abs(d) / (s * math.sqrt(1.0 / k + 1.0 / (n - k)))  # @line L16
            if z > best:
                best, bi, bj = z, i, j
    return best, bi, bj  # @line L17


def permutation_p_value(y: Sequence[float], t_obs: float, rng: random.Random, n_perm: int) -> float:
    """(count + 1) / (n_perm + 1), where count is the number of shuffles with T >= t_obs.

    Draw order: n_perm calls of rng.shuffle on one working copy of y.
    """
    work = list(y)
    count = 0
    tol = 1e-12 * max(1.0, t_obs)
    for _ in range(n_perm):
        rng.shuffle(work)
        if max_arc(work)[0] >= t_obs - tol:  # @line L6
            count += 1
    return (count + 1) / (n_perm + 1)  # @line L7


def cbs(x: Sequence[float], rng: random.Random, alpha: float = 0.01, n_perm: int = 199) -> List[int]:
    """Return the sorted change points of x: each b with 0 < b < len(x) where a new segment starts.

    Segments are tested in a fixed order (a stack; the left part is tested
    first), so a seed gives the same result on every run.
    """
    n = len(x)
    stack = [(0, n)]  # @line L1
    cuts: List[int] = []
    while stack:  # @line L2
        lo, hi = stack.pop()  # @line L3
        y = x[lo:hi]  # @line L4
        if len(y) < 2:
            continue
        t, i, j = max_arc(y)  # @line L5
        if t == 0.0:
            continue
        p = permutation_p_value(y, t, rng, n_perm)
        if p <= alpha:  # @line L8
            parts = [lo] + [lo + b for b in (i, j) if 0 < b < hi - lo] + [hi]
            cuts.extend(parts[1:-1])  # @line L9
            for a, b in reversed(list(zip(parts, parts[1:]))):  # @line L10
                stack.append((a, b))
    return sorted(cuts)  # @line L11


def segment_means(x: Sequence[float], cuts: Sequence[int]) -> List[Tuple[int, int, float]]:
    """The segments (lo, hi, mean) between the change points."""
    bounds = [0] + list(cuts) + [len(x)]
    return [(a, b, sum(x[a:b]) / (b - a)) for a, b in zip(bounds, bounds[1:])]
