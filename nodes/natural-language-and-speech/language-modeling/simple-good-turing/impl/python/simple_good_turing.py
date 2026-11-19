# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simple-good-turing/. The authors are listed in prov/P5RKY6.jsonl.

"""Simple Good-Turing estimation (Gale and Sampson 1995), in floating point.

The input is the table of counts of counts {r: N_r} of a sample, with r >= 1
and N_r >= 1. The method averages each N_r over the gap to its neighbours
(Z_r = 2 N_r / (t - q)), fits the line log Z_r = a + b log r by least
squares, and uses the smoothed counts r* = (r + 1) S(r + 1) / S(r) with
S(r) = exp(a + b log r) once the raw Turing estimate is no longer
significantly different (1.96 standard deviations). The seen probabilities
are scaled to sum to 1 - N_1 / N.
"""

import math
from typing import Hashable, Mapping

CONFIDENCE = 1.96


def averaged_counts(nr: Mapping[int, int]) -> dict[int, float]:
    """Return {r: Z_r} with Z_r = 2 N_r / (t - q) for the neighbours q < r < t."""
    rs = sorted(nr)
    z = {}
    for j, r in enumerate(rs):
        q = rs[j - 1] if j > 0 else 0
        t = rs[j + 1] if j + 1 < len(rs) else 2 * r - q
        z[r] = 2.0 * nr[r] / (t - q)
    return z


def fit_line(xs: list[float], ys: list[float]) -> tuple[float, float]:
    """Least squares fit of y = a + b x; return (a, b)."""
    m = len(xs)
    mx, my = sum(xs) / m, sum(ys) / m
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    b = sxy / sxx
    return my - b * mx, b


def simple_good_turing_counts(nr: Mapping[int, int], confidence: float = CONFIDENCE):
    """Return (rstar, a, b, switch).

    rstar maps each r to its adjusted count, (a, b) is the fitted line of
    log Z_r against log r, and switch is the smallest r that uses the
    smoothed estimate. Raises ValueError with fewer than two distinct counts.
    """
    rs = sorted(nr)
    if len(rs) < 2:
        raise ValueError("the fit needs at least two distinct counts")
    if rs[0] < 1 or any(nr[r] < 1 for r in rs):
        raise ValueError("counts and counts of counts must be at least 1")
    z = averaged_counts(nr)  # @line L3
    a, b = fit_line([math.log(r) for r in rs], [math.log(z[r]) for r in rs])  # @line L4

    def smooth(r: float) -> float:
        return math.exp(a + b * math.log(r))  # @line L5

    rstar, use_line, switch = {}, False, None  # @line L6
    for r in rs:  # @line L7
        y = (r + 1) * smooth(r + 1) / smooth(r)  # @line L8
        if not use_line:  # @line L9
            n1 = nr.get(r + 1, 0)
            if n1 == 0:
                use_line = True
            else:
                x = (r + 1) * n1 / nr[r]
                sd = math.sqrt((r + 1) ** 2 * n1 / nr[r] ** 2 * (1 + n1 / nr[r]))
                if abs(x - y) <= confidence * sd:
                    use_line = True
        if use_line:
            if switch is None:
                switch = r
            rstar[r] = y  # @line L10
        else:
            rstar[r] = x  # @line L10
    return rstar, a, b, switch


def simple_good_turing(counts: Mapping[Hashable, int], confidence: float = CONFIDENCE):
    """Return (p, p0, rstar, b) for a mapping from each seen type to its count.

    p maps each seen type to its probability, p0 = N_1 / N is the total mass
    of the unseen types, and b is the fitted slope (the method assumes b < -1).
    """
    n = sum(counts.values())  # @line L1
    nr: dict[int, int] = {}
    for r in counts.values():
        nr[r] = nr.get(r, 0) + 1
    p0 = nr.get(1, 0) / n  # @line L2
    rstar, _, b, _ = simple_good_turing_counts(nr, confidence)
    total = sum(nr[r] * rstar[r] for r in nr)  # @line L11
    p = {x: (1 - p0) * rstar[r] / total for x, r in counts.items()}  # @line L12
    return p, p0, rstar, b  # @line L13
