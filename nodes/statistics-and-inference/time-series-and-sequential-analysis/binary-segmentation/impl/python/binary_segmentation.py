# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binary-segmentation/. The authors are listed in prov/PQ8R7K.jsonl.
"""Binary segmentation and wild binary segmentation for changes in the mean.

For the segment x_(s+1)..x_e and a split point b with s < b < e, the CUSUM
contrast is

    C(s, b, e) = sqrt((b - s)(e - b) / (e - s)) * |mean(x_(s+1..b)) - mean(x_(b+1..e))|.

C(s, b, e)^2 equals the drop in the residual sum of squares when the segment
is cut at b. Binary segmentation cuts at the best b when the contrast exceeds
a threshold zeta and recurses on both halves. With prefix sums each contrast
costs O(1), so one segment of length L costs O(L), each level of the
recursion tree costs O(n), and the whole run costs O(n (m + 1)) for m
change points found: O(n log n) for balanced splits and O(n^2) in the worst case.
"""

import math
import random
from collections.abc import Sequence


def prefix_sums(xs: Sequence[float]) -> list[float]:
    out = [0]
    for x in xs:
        out.append(out[-1] + x)
    return out


def contrast(p: Sequence[float], s: int, b: int, e: int) -> float:
    """C(s, b, e) from prefix sums p. Precondition: s < b < e. O(1)."""
    left = (p[b] - p[s]) / (b - s)
    right = (p[e] - p[b]) / (e - b)
    return math.sqrt((b - s) * (e - b) / (e - s)) * abs(left - right)


def contrast_squared(p: Sequence, s: int, b: int, e: int):
    """C(s, b, e)^2 in the arithmetic of p (exact for Fractions)."""
    left = (p[b] - p[s]) / (b - s)
    right = (p[e] - p[b]) / (e - b)
    return (b - s) * (e - b) * (left - right) ** 2 / (e - s)


def best_split(p: Sequence[float], s: int, e: int) -> tuple[int, float]:
    """The smallest b in (s, e) that maximizes C(s, b, e), and the maximum. O(e - s)."""
    best_b, best_c = s + 1, -1.0
    for b in range(s + 1, e):
        c = contrast(p, s, b, e)
        if c > best_c:
            best_b, best_c = b, c
    return best_b, best_c


def binary_segmentation(xs: Sequence[float], zeta: float) -> list[int]:
    """Change points (as last indices of segments, 1-based) found by binary segmentation."""
    p = prefix_sums(xs)  # @line L1
    stack = [(0, len(xs))]  # @line L1
    cps = []  # @line L1
    while stack:  # @line L2
        s, e = stack.pop()  # @line L3
        if e - s < 2:  # @line L3
            continue
        b, c = best_split(p, s, e)  # @line L4
        if c <= zeta:  # @line L5
            continue
        cps.append(b)  # @line L6
        stack.append((s, b))  # @line L6
        stack.append((b, e))  # @line L6
    return sorted(cps)  # @line L7


def random_intervals(n: int, m: int, rng: random.Random) -> list[tuple[int, int]]:
    """m random intervals (s, e) with 0 <= s < e - 1 < n, drawn uniformly over pairs."""
    out = []
    while len(out) < m:
        s, e = sorted(rng.sample(range(n + 1), 2))
        if e - s >= 2:
            out.append((s, e))
    return out


def wild_binary_segmentation(xs: Sequence[float], zeta: float, intervals: Sequence[tuple[int, int]]) -> list[int]:
    """Fryzlewicz's WBS: on each segment, search the full segment and every drawn interval inside it.

    Cost O(sum of interval lengths) per segment visited, so O(M n) per level
    for M intervals.
    """
    p = prefix_sums(xs)
    stack = [(0, len(xs))]
    cps = []
    while stack:
        s, e = stack.pop()
        if e - s < 2:
            continue
        cands = [(s, e)] + [(a, b) for a, b in intervals if s <= a and b <= e]
        best = (-1.0, 0)
        for a, b in cands:
            split, c = best_split(p, a, b)
            if c > best[0]:
                best = (c, split)
        c, split = best
        if c <= zeta:
            continue
        cps.append(split)
        stack.append((s, split))
        stack.append((split, e))
    return sorted(cps)


def default_threshold(n: int, sigma: float = 1.0, factor: float = 1.3) -> float:
    """zeta = factor * sigma * sqrt(2 log n), the form used by Fryzlewicz (2014) for WBS."""
    return factor * sigma * math.sqrt(2.0 * math.log(n))
