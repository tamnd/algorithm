# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/balls-into-bins-max-load/. The authors are listed in prov/6M248J.jsonl.

"""The maximum load of m balls thrown uniformly into n bins.

throw and max_load simulate the process with a seeded generator.
prob_max_below gives the exact law of the maximum load from the
generating function, and enumerate_max_at_least checks it by brute force.
"""

import itertools
import math
import random
from fractions import Fraction


def throw(n: int, m: int, rng: random.Random) -> list[int]:
    """Throw m balls into n bins, each bin uniform and independent. Return the loads."""
    loads = [0] * n
    for _ in range(m):
        loads[rng.randrange(n)] += 1
    return loads


def max_load(n: int, m: int, rng: random.Random) -> int:
    """The maximum load of one run of the process."""
    return max(throw(n, m, rng))


def prob_max_below(n: int, m: int, k: int) -> Fraction:
    """Exact Pr[max load < k] for m balls in n bins.

    The number of maps from m balls to n bins with all loads below k is
    m! [x^m] (sum_{j<k} x^j / j!)^n, and there are n^m maps in all.
    """
    if k <= 0:
        return Fraction(0)
    base = [Fraction(1, math.factorial(j)) for j in range(min(k, m + 1))]
    poly = [Fraction(1)]
    for _ in range(n):
        new = [Fraction(0)] * min(len(poly) + len(base) - 1, m + 1)
        for a, ca in enumerate(poly):
            if ca == 0:
                continue
            for b, cb in enumerate(base):
                if a + b > m:
                    break
                new[a + b] += ca * cb
        poly = new
    coeff = poly[m] if m < len(poly) else Fraction(0)
    return coeff * math.factorial(m) / Fraction(n) ** m


def prob_max_at_least(n: int, m: int, k: int) -> Fraction:
    """Exact Pr[max load >= k]."""
    return 1 - prob_max_below(n, m, k)


def enumerate_max_at_least(n: int, m: int, k: int) -> Fraction:
    """Pr[max load >= k] by listing all n^m maps from balls to bins."""
    hits = 0
    for bins in itertools.product(range(n), repeat=m):
        loads = [0] * n
        for b in bins:
            loads[b] += 1
        if max(loads, default=0) >= k:
            hits += 1
    return Fraction(hits, n ** m)


def expected_max_load(n: int, m: int) -> Fraction:
    """Exact E[max load] = sum over k >= 1 of Pr[max load >= k]."""
    return sum((prob_max_at_least(n, m, k) for k in range(1, m + 1)), Fraction(0))


def union_bound(n: int, m: int, k: int) -> Fraction:
    """The union bound n * C(m, k) / n^k on Pr[max load >= k]."""
    return min(Fraction(1), n * Fraction(math.comb(m, k), n ** k))


def poisson_prob_max_below(n: int, k: int, mean: float) -> float:
    """Pr[max < k] when the n loads are independent Poisson(mean) variables."""
    p = sum(math.exp(-mean) * mean ** j / math.factorial(j) for j in range(k))
    return p ** n


def light_threshold(n: int) -> float:
    """ln n / ln ln n, the first-order maximum load for m = n."""
    return math.log(n) / math.log(math.log(n))


def heavy_gap_bound(n: int, m: int) -> float:
    """sqrt(6 (m/n) ln n): for m >= 6 n ln n, max load < m/n + this, w.p. >= 1 - 1/n."""
    return math.sqrt(6 * (m / n) * math.log(n))
