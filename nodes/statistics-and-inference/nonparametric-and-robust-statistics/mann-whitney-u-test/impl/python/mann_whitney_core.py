# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mann-whitney-u-test/. The authors are listed in prov/9WF4CP.jsonl.

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


def u_statistic(x: list[float], y: list[float]) -> float:
    """U = #{(i, j) : x_i > y_j} + #{(i, j) : x_i = y_j} / 2, from the rank sum of x."""
    m = len(x)
    r2 = doubled_midranks(list(x) + list(y))
    return (sum(r2[:m]) - m * (m + 1)) / 2


def null_counts_2u(r2: list[int], m: int) -> dict[int, int]:
    """Number of ways to pick the m positions of the first sample, by the value of 2U.

    A subset-sum count over the pooled doubled ranks r2, restricted to subsets of
    size k = min(m, n). If k = n the subset is the second sample, and 2U of the
    first sample is 2mn minus 2U of the second.
    """
    big_n = len(r2)
    n = big_n - m
    k = min(m, n)
    top = sum(sorted(r2)[big_n - k:])  # the largest possible doubled rank sum of k values
    c = [[0] * (top + 1) for _ in range(k + 1)]  # @line L3
    c[0][0] = 1
    for r in r2:  # @line L4
        for j in range(k, 0, -1):  # @line L5
            row, prev = c[j], c[j - 1]
            for s in range(top, r - 1, -1):
                if prev[s - r]:
                    row[s] += prev[s - r]
    out: dict[int, int] = {}
    for s, cnt in enumerate(c[k]):  # @line L6
        if cnt:
            u2 = s - m * (m + 1) if k == m else 2 * m * n - (s - n * (n + 1))
            out[u2] = out.get(u2, 0) + cnt
    return out


def mann_whitney(
    x: list[float], y: list[float], alternative: str = "two-sided", exact: bool = False
) -> tuple[float, float | Fraction]:
    """Mann-Whitney U test of H0: the two samples come from the same distribution.

    Returns (U, p) with U = #{x_i > y_j} + (1/2) #{x_i = y_j}. "greater" is the
    alternative that X tends to be larger than Y. Ties get midranks, and the
    p-value is then exact for the conditional null law given the tie pattern.
    The two-sided p-value doubles the smaller tail. Without ties the null law is
    symmetric about mn/2, and this equals P(|U - mn/2| >= |u - mn/2|); with ties
    the conditional law can be asymmetric, and doubling is still a valid rule.
    """
    if alternative not in ALTERNATIVES:
        raise ValueError("unknown alternative")
    m, n = len(x), len(y)
    if m == 0 or n == 0:
        raise ValueError("both samples must be nonempty")
    r2 = doubled_midranks(list(x) + list(y))  # @line L1
    u2 = sum(r2[:m]) - m * (m + 1)  # @line L2
    counts = null_counts_2u(r2, m)
    upper = sum(c for v, c in counts.items() if v >= u2)  # @line L7
    lower = sum(c for v, c in counts.items() if v <= u2)
    total = math.comb(m + n, m)
    if alternative == "greater":  # @line L8
        p = Fraction(upper, total)
    elif alternative == "less":
        p = Fraction(lower, total)
    else:
        p = min(Fraction(1), Fraction(2 * min(upper, lower), total))
    return u2 / 2, (p if exact else float(p))


def mann_whitney_normal(
    x: list[float], y: list[float], alternative: str = "two-sided", correction: bool = True
) -> tuple[float, float]:
    """Normal approximation with the tie-corrected variance. Returns (z, p)."""
    if alternative not in ALTERNATIVES:
        raise ValueError("unknown alternative")
    m, n = len(x), len(y)
    big_n = m + n
    u = u_statistic(x, y)
    mean = m * n / 2
    ties = sum(t**3 - t for t in tie_sizes(list(x) + list(y)))
    var = m * n / 12 * ((big_n + 1) - ties / (big_n * (big_n - 1)))
    sd = math.sqrt(var)
    c = 0.5 if correction else 0.0
    if alternative == "greater":
        z = (u - mean - c) / sd
        return z, 0.5 * math.erfc(z / math.sqrt(2.0))
    if alternative == "less":
        z = (u - mean + c) / sd
        return z, 0.5 * math.erfc(-z / math.sqrt(2.0))
    z = math.copysign(max(0.0, abs(u - mean) - c), u - mean) / sd
    return z, min(1.0, math.erfc(abs(z) / math.sqrt(2.0)))
