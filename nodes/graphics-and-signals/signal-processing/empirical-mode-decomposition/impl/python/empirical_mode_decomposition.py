# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/empirical-mode-decomposition/. The authors are listed in prov/H7DRYS.jsonl.

"""Empirical mode decomposition by sifting (Huang et al. 1998), one common variant.

EMD is a heuristic. Nothing here proves that sifting converges or that the
modes mean anything. Two things do hold, and the tests check them:
  1. completeness: the IMFs and the residue add up to the input exactly,
     because every subtraction is done in exact rational arithmetic;
  2. each IMF meets the stopping rule that ended its sifting, or its sifting
     hit the cap, and the info says which.

Choices made here (other codes choose differently):
  - envelopes: natural cubic splines through the extrema and both end samples;
    linear interpolation if there are only two knots;
  - stopping rule: |#extrema - #zero crossings| <= 1 and
    SD = sum (h_prev - h)^2 / sum h_prev^2 < sd_limit, or max_sifts sifts;
  - the outer loop ends when the residue has fewer than 2 extrema, or at max_imfs.
"""

from fractions import Fraction
from typing import Sequence


def extrema(h: Sequence) -> tuple[list[int], list[int]]:
    """Interior local maxima and minima. A flat top counts once, at its left end."""
    maxima, minima = [], []
    for i in range(1, len(h) - 1):
        if h[i] > h[i - 1] and h[i] >= h[i + 1]:
            maxima.append(i)
        elif h[i] < h[i - 1] and h[i] <= h[i + 1]:
            minima.append(i)
    return maxima, minima


def zero_crossings(h: Sequence) -> int:
    """Sign changes, with exact zeros skipped."""
    signs = [1 if v > 0 else -1 for v in h if v != 0]
    return sum(1 for a, b in zip(signs, signs[1:]) if a != b)


def natural_spline(knots: Sequence[int], values: Sequence[float], n: int) -> list[float]:
    """The natural cubic spline through (knots, values), sampled at 0 .. n-1 (Thomas solve)."""
    m = len(knots)
    if m == 2:
        (a, b), (ya, yb) = knots, values
        return [ya + (yb - ya) * (i - a) / (b - a) for i in range(n)]
    hs = [knots[i + 1] - knots[i] for i in range(m - 1)]
    # Second derivatives M[0] = M[m-1] = 0; tridiagonal system for M[1 .. m-2].
    sub = [hs[i - 1] for i in range(1, m - 1)]
    diag = [2 * (hs[i - 1] + hs[i]) for i in range(1, m - 1)]
    sup = [hs[i] for i in range(1, m - 1)]
    rhs = [6 * ((values[i + 1] - values[i]) / hs[i] - (values[i] - values[i - 1]) / hs[i - 1]) for i in range(1, m - 1)]
    k = len(diag)
    for i in range(1, k):
        f = sub[i] / diag[i - 1]
        diag[i] -= f * sup[i - 1]
        rhs[i] -= f * rhs[i - 1]
    inner = [0.0] * k
    for i in range(k - 1, -1, -1):
        inner[i] = (rhs[i] - (sup[i] * inner[i + 1] if i + 1 < k else 0.0)) / diag[i]
    second = [0.0] + inner + [0.0]
    out = []
    seg = 0
    for x in range(n):
        while seg < m - 2 and x > knots[seg + 1]:
            seg += 1
        a, b, h = knots[seg], knots[seg + 1], hs[seg]
        u, v = (b - x) / h, (x - a) / h
        out.append(u * values[seg] + v * values[seg + 1] + ((u**3 - u) * second[seg] + (v**3 - v) * second[seg + 1]) * h * h / 6)
    return out


def envelope_mean(h: Sequence) -> list[float]:
    n = len(h)
    maxima, minima = extrema(h)
    fl = [float(v) for v in h]
    upper_knots = [0] + maxima + [n - 1]
    lower_knots = [0] + minima + [n - 1]
    upper = natural_spline(upper_knots, [fl[i] for i in upper_knots], n)  # @line L5
    lower = natural_spline(lower_knots, [fl[i] for i in lower_knots], n)  # @line L5
    return [(a + b) / 2 for a, b in zip(upper, lower)]


def sift_once(h: Sequence[Fraction]) -> list[Fraction]:
    """h minus the mean of its envelopes. The float mean is turned into an exact Fraction first."""
    return [v - Fraction(m) for v, m in zip(h, envelope_mean(h))]


def sd(prev: Sequence[Fraction], cur: Sequence[Fraction]) -> Fraction:
    return sum((a - b) ** 2 for a, b in zip(prev, cur)) / sum(a * a for a in prev)


def meets_rule(prev: Sequence[Fraction], cur: Sequence[Fraction], sd_limit: Fraction) -> bool:
    maxima, minima = extrema(cur)
    return abs(len(maxima) + len(minima) - zero_crossings(cur)) <= 1 and sd(prev, cur) < sd_limit


def emd(x: Sequence[int], max_imfs: int = 8, max_sifts: int = 50, sd_limit: Fraction = Fraction(1, 100)) -> tuple[list[list[Fraction]], list[Fraction], list[dict]]:
    """Returns (imfs, residue, info); info[k] has the sift count and why sifting stopped."""
    residue = [Fraction(v) for v in x]  # @line L1
    imfs, info = [], []
    while len(imfs) < max_imfs:  # @line L2
        maxima, minima = extrema(residue)
        if len(maxima) + len(minima) < 2:
            break
        h = residue  # @line L3
        reason = "cap"
        sifts = 0
        prev = h
        while sifts < max_sifts:  # @line L4
            prev, h = h, sift_once(h)  # @line L5 L6
            sifts += 1
            if meets_rule(prev, h, sd_limit):  # @line L7
                reason = "rule"
                break
        imfs.append(h)  # @line L8
        info.append({"sifts": sifts, "reason": reason, "prev": prev})
        residue = [a - b for a, b in zip(residue, h)]  # @line L9
    return imfs, residue, info  # @line L10
