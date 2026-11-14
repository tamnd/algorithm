# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wilcoxon-signed-rank-test/. The authors are listed in prov/8KPP1Q.jsonl.

import math
from fractions import Fraction

ALTERNATIVES = ("two-sided", "greater", "less")


def doubled_midranks(values: list[float]) -> list[int]:
    """Return 2 x (midrank of each value), in input order. Doubling keeps midranks integers."""
    n = len(values)
    order = sorted(range(n), key=values.__getitem__)
    r2 = [0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and values[order[j + 1]] == values[order[i]]:
            j += 1
        for t in range(i, j + 1):
            r2[order[t]] = i + j + 2  # 2 x the mean of the ranks i + 1, ..., j + 1
        i = j + 1
    return r2


def tie_sizes(values: list[float]) -> list[int]:
    """Sizes of the groups of equal values."""
    counts: dict[float, int] = {}
    for v in values:
        counts[v] = counts.get(v, 0) + 1
    return list(counts.values())


def signed_rank_counts(r2: list[int]) -> list[int]:
    """c[s] = number of subsets of the doubled ranks r2 with sum s (a subset-sum count)."""
    total = sum(r2)
    c = [0] * (total + 1)
    c[0] = 1
    for r in r2:  # @line L5
        for s in range(total, r - 1, -1):  # @line L6
            c[s] += c[s - r]
    return c


def wilcoxon_signed_rank(
    d: list[float], alternative: str = "two-sided", mu0: float = 0.0, exact: bool = False
) -> tuple[float, float | Fraction]:
    """Wilcoxon signed-rank test of H0: D - mu0 is symmetric about 0.

    Returns (W+, p). Differences equal to mu0 are dropped. Tied |d_i| get
    midranks, and the null law is then the exact conditional law given the
    ranks: the signs are independent fair coins. "greater" is the alternative
    that D tends to exceed mu0. The two-sided p-value doubles the smaller tail;
    the null law is symmetric, so this equals P(|W+ - E W+| >= |w - E W+|).
    """
    if alternative not in ALTERNATIVES:
        raise ValueError("unknown alternative")
    kept = [v - mu0 for v in d if v != mu0]  # @line L1
    n = len(kept)
    r2 = doubled_midranks([abs(v) for v in kept])  # @line L2
    w2 = sum(r for r, v in zip(r2, kept) if v > 0)  # @line L3
    c = signed_rank_counts(r2)  # @line L4
    upper = sum(c[w2:])  # @line L7
    lower = sum(c[: w2 + 1])
    total = 2**n
    if alternative == "greater":  # @line L8
        p = Fraction(upper, total)
    elif alternative == "less":
        p = Fraction(lower, total)
    else:
        p = min(Fraction(1), Fraction(2 * min(upper, lower), total))
    return w2 / 2, (p if exact else float(p))


def wilcoxon_normal(
    d: list[float], alternative: str = "two-sided", mu0: float = 0.0, correction: bool = True
) -> tuple[float, float]:
    """Normal approximation with the tie-corrected variance. Returns (z, p)."""
    if alternative not in ALTERNATIVES:
        raise ValueError("unknown alternative")
    kept = [v - mu0 for v in d if v != mu0]
    n = len(kept)
    if n == 0:
        return 0.0, 1.0
    a = [abs(v) for v in kept]
    w = sum(r for r, v in zip(doubled_midranks(a), kept) if v > 0) / 2
    mean = n * (n + 1) / 4
    var = n * (n + 1) * (2 * n + 1) / 24 - sum(t**3 - t for t in tie_sizes(a)) / 48
    sd = math.sqrt(var)
    c = 0.5 if correction else 0.0
    if alternative == "greater":
        z = (w - mean - c) / sd
        return z, 0.5 * math.erfc(z / math.sqrt(2.0))
    if alternative == "less":
        z = (w - mean + c) / sd
        return z, 0.5 * math.erfc(-z / math.sqrt(2.0))
    z = math.copysign(max(0.0, abs(w - mean) - c), w - mean) / sd
    return z, min(1.0, math.erfc(abs(z) / math.sqrt(2.0)))
