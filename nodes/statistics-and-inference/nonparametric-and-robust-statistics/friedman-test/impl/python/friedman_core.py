# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/friedman-test/. The authors are listed in prov/DRZ1M4.jsonl.

import itertools
import math
from fractions import Fraction

from stdist import chi2_sf


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


def q_statistic(blocks: list[list[float]]) -> Fraction:
    """The tie-corrected Friedman statistic as an exact Fraction.

    Q = (k - 1) sum_j (R_j - b (k + 1) / 2)^2 / (sum_ij r_ij^2 - b k (k + 1)^2 / 4).
    Without ties it equals 12 / (b k (k + 1)) sum_j R_j^2 - 3 b (k + 1).
    """
    b, k = len(blocks), len(blocks[0])
    r2 = [doubled_midranks(row) for row in blocks]  # @line L1
    col = [Fraction(sum(row[j] for row in r2), 2) for j in range(k)]  # @line L2
    a = sum(Fraction(v * v, 4) for row in r2 for v in row)  # @line L3
    c = Fraction(b * k * (k + 1) ** 2, 4)
    if a == c:
        return Fraction(0)  # every block is one tie: no information
    centre = Fraction(b * (k + 1), 2)
    return (k - 1) * sum((s - centre) ** 2 for s in col) / (a - c)  # @line L4


def rank_sum_counts(blocks: list[list[float]]) -> dict[tuple[int, ...], int]:
    """Number of the (k!)^b within-block orderings that give each vector of doubled
    column rank sums. A DP over the blocks; the state is the vector of sums so far."""
    k = len(blocks[0])
    counts: dict[tuple[int, ...], int] = {(0,) * k: 1}
    for row in blocks:
        perms = list(itertools.permutations(doubled_midranks(row)))
        nxt: dict[tuple[int, ...], int] = {}
        for sums, cnt in counts.items():
            for perm in perms:
                key = tuple(s + r for s, r in zip(sums, perm))
                nxt[key] = nxt.get(key, 0) + cnt
        counts = nxt
    return counts


def friedman(
    blocks: list[list[float]], method: str = "asymptotic", exact: bool = False
) -> tuple[float, float | Fraction]:
    """Friedman test of H0: within each block the k treatments are exchangeable.

    blocks[i][j] is the response of treatment j in block i. Returns (Q, p).
    method "asymptotic" uses the upper tail of chi-square with k - 1 degrees of
    freedom. method "exact" computes the permutation null: each block's ranks
    are permuted in all k! ways, independently across blocks, and the p-value is
    the share of the (k!)^b outcomes with sum_j R_j^2 at least the observed one.
    """
    if len(blocks) == 0 or len(blocks[0]) < 2 or any(len(r) != len(blocks[0]) for r in blocks):
        raise ValueError("need b >= 1 blocks of the same length k >= 2")
    if method not in ("asymptotic", "exact"):
        raise ValueError("unknown method")
    q = q_statistic(blocks)
    b, k = len(blocks), len(blocks[0])
    if method == "asymptotic":  # @line L5
        return float(q), chi2_sf(float(q), k - 1)
    observed = [sum(doubled_midranks(row)[j] for row in blocks) for j in range(k)]
    target = sum(s * s for s in observed)
    counts = rank_sum_counts(blocks)  # @line L6
    hits = sum(cnt for sums, cnt in counts.items() if sum(s * s for s in sums) >= target)
    p = Fraction(hits, math.factorial(k) ** b)  # @line L7
    return float(q), (p if exact else float(p))  # @line L8
