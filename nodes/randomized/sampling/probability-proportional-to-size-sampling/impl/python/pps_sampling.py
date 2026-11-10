# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/probability-proportional-to-size-sampling/. The authors are listed in prov/G2PZNC.jsonl.

"""Probability proportional to size (PPS) sampling.

With replacement: m independent draws with Pr[i] = x_i / X, and the
Hansen-Hurwitz estimate (1/m) sum y_i X / x_i of the total Y.

Without replacement: systematic PPS gives each unit the inclusion
probability pi_i = a_i / D exactly, with integer a_i <= D and sum a_i = n D.
The Horvitz-Thompson estimate sum_{i in S} y_i / pi_i is unbiased for Y.
"""

import bisect
import math
import random
from fractions import Fraction
from typing import Dict, List, Sequence, Tuple


def prefix_sums(a: Sequence[int]) -> List[int]:
    out, s = [], 0
    for v in a:
        s += v
        out.append(s)
    return out


def pps_draw(prefix: Sequence[int], rng: random.Random) -> int:
    """One draw with Pr[i] = x_i / X, exact with integer sizes."""
    r = rng.randrange(prefix[-1])
    return bisect.bisect_right(prefix, r)


def hansen_hurwitz(draws: Sequence[int], x: Sequence[int], y: Sequence) -> Fraction:
    """The Hansen-Hurwitz estimate of the total from draws made with Pr[i] = x_i / X."""
    big_x = sum(x)
    return sum((Fraction(y[i]) * big_x / x[i] for i in draws), Fraction(0)) / len(draws)  # @line L2


def pps_with_replacement(x: Sequence[int], y: Sequence, m: int, rng: random.Random) -> Fraction:
    prefix = prefix_sums(x)
    draws = [pps_draw(prefix, rng) for _ in range(m)]  # @line L1
    return hansen_hurwitz(draws, x, y)


def inclusion_probabilities(x: Sequence, n: int) -> List[Fraction]:
    """pi_i = n x_i / X, with units where this exceeds 1 taken with certainty.

    The cap is applied again on the remaining units until no value exceeds 1.
    """
    if not 0 < n <= len(x):
        raise ValueError("need 0 < n <= N")
    if any(v <= 0 for v in x):
        raise ValueError("sizes must be positive")
    certain = set()
    while True:
        rest = [i for i in range(len(x)) if i not in certain]
        k = n - len(certain)
        total = sum(Fraction(x[i]) for i in rest)
        pi = [Fraction(1)] * len(x)
        for i in rest:
            pi[i] = k * Fraction(x[i]) / total
        over = [i for i in rest if pi[i] > 1]
        if not over:
            return pi
        certain.update(over)


def integer_form(pi: Sequence[Fraction]) -> Tuple[List[int], int, int]:
    """Write pi_i = a_i / D with integers. Returns (a, D, n) where sum a = n D."""
    d = 1
    for p in pi:
        d = d * p.denominator // math.gcd(d, p.denominator)
    a = [int(p * d) for p in pi]
    s = sum(pi)
    if s.denominator != 1 or any(not 0 <= p <= 1 for p in pi):
        raise ValueError("the pi_i must lie in [0, 1] and sum to an integer")
    return a, d, int(s)


def systematic_from_start(a: Sequence[int], d: int, n: int, t: int) -> List[int]:
    """The units hit by the points t, t + D, ..., t + (n - 1) D."""
    sample, low, point = [], 0, t
    for i, ai in enumerate(a):  # @line L4
        high = low + ai
        if len(sample) < n and low <= point < high:  # @line L4
            sample.append(i)  # @line L4
            point += d
        low = high
    return sample  # @line L5


def systematic_pps(a: Sequence[int], d: int, n: int, rng: random.Random) -> List[int]:
    """Systematic PPS: unit i is in the sample with probability a_i / D exactly."""
    if any(ai > d for ai in a) or sum(a) != n * d:
        raise ValueError("need a_i <= D and sum a_i = n D")
    t = rng.randrange(d)  # @line L3
    return systematic_from_start(a, d, n, t)


def systematic_pps_float(pi: Sequence[float], rng: random.Random) -> List[int]:
    """The floating-point form: points u, u + 1, ... with u uniform in [0, 1)."""
    u = rng.random()
    sample, low = [], 0.0
    for i, p in enumerate(pi):
        high = low + p
        if low <= u < high:
            sample.append(i)
            u += 1.0
        low = high
    return sample


def horvitz_thompson(sample: Sequence[int], y: Sequence, pi: Sequence) -> Fraction:
    """The Horvitz-Thompson estimate of the total."""
    return sum((Fraction(y[i]) / pi[i] for i in sample), Fraction(0))  # @line L6


def poisson_sample(pi: Sequence[float], rng: random.Random) -> List[int]:
    """Poisson sampling: each unit independently with probability pi_i."""
    return [i for i, p in enumerate(pi) if rng.random() < p]


def ht_variance(y: Sequence, pi: Sequence[Fraction], pij: Dict[Tuple[int, int], Fraction]) -> Fraction:
    """Var of the HT estimate: sum_i sum_j (pi_ij - pi_i pi_j) y_i y_j / (pi_i pi_j), with pi_ii = pi_i."""
    total = Fraction(0)
    for i in range(len(y)):
        for j in range(len(y)):
            p = pi[i] if i == j else pij.get((min(i, j), max(i, j)), Fraction(0))
            total += (p - pi[i] * pi[j]) * Fraction(y[i]) * Fraction(y[j]) / (pi[i] * pi[j])
    return total
