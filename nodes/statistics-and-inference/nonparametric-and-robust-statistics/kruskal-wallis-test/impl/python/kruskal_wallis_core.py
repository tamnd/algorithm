# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kruskal-wallis-test/. The authors are listed in prov/DCECK4.jsonl.

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


def tie_sizes(values: list[float]) -> list[int]:
    """Sizes of the groups of equal values."""
    counts: dict[float, int] = {}
    for v in values:
        counts[v] = counts.get(v, 0) + 1
    return list(counts.values())


def h_statistic(groups: list[list[float]]) -> Fraction:
    """The tie-corrected Kruskal-Wallis H as an exact Fraction (the inputs are compared only)."""
    sizes = [len(g) for g in groups]
    big_n = sum(sizes)
    pooled = [v for g in groups for v in g]
    r2 = doubled_midranks(pooled)  # @line L1
    sums, start = [], 0
    for size in sizes:  # @line L2
        sums.append(Fraction(sum(r2[start:start + size]), 2))
        start += size
    h = Fraction(12, big_n * (big_n + 1)) * sum(s * s / size for s, size in zip(sums, sizes))
    h -= 3 * (big_n + 1)  # @line L3
    c = 1 - Fraction(sum(t**3 - t for t in tie_sizes(pooled)), big_n**3 - big_n)  # @line L4
    return h / c if c > 0 else Fraction(0)


def labeling_counts(r2: list[int], sizes: list[int]) -> dict[tuple[int, ...], int]:
    """Number of ways to split the pooled doubled ranks into groups of the given sizes,
    by the vector of doubled rank sums of the groups. A DP over the pooled values whose
    state is (group sizes filled so far, rank sums so far)."""
    k = len(sizes)
    states: dict[tuple[tuple[int, ...], tuple[int, ...]], int] = {((0,) * k, (0,) * k): 1}
    for r in r2:
        nxt: dict[tuple[tuple[int, ...], tuple[int, ...]], int] = {}
        for (filled, sums), cnt in states.items():
            for i in range(k):
                if filled[i] < sizes[i]:
                    key = (filled[:i] + (filled[i] + 1,) + filled[i + 1:],
                           sums[:i] + (sums[i] + r,) + sums[i + 1:])
                    nxt[key] = nxt.get(key, 0) + cnt
        states = nxt
    out: dict[tuple[int, ...], int] = {}
    for (_, sums), cnt in states.items():
        out[sums] = out.get(sums, 0) + cnt
    return out


def kruskal_wallis(
    groups: list[list[float]], method: str = "asymptotic", exact: bool = False
) -> tuple[float, float | Fraction]:
    """Kruskal-Wallis test of H0: the k groups come from the same distribution.

    Returns (H, p). method "asymptotic" uses the upper tail of chi-square with
    k - 1 degrees of freedom. method "exact" counts every split of the pooled
    ranks into groups of the given sizes (the permutation null, exact and
    conditional on the ties); the p-value is the share of splits whose
    sum of R_i^2 / n_i is at least the observed one. exact=True returns a Fraction.
    """
    if len(groups) < 2 or any(len(g) == 0 for g in groups):
        raise ValueError("need at least two nonempty groups")
    if method not in ("asymptotic", "exact"):
        raise ValueError("unknown method")
    h = h_statistic(groups)
    k = len(groups)
    if method == "asymptotic":  # @line L5
        return float(h), chi2_sf(float(h), k - 1)
    sizes = [len(g) for g in groups]
    pooled = [v for g in groups for v in g]
    r2 = doubled_midranks(pooled)
    lcm = math.lcm(*sizes)

    def score(sums: tuple[int, ...]) -> int:
        # (4 lcm) x sum R_i^2 / n_i, an integer, increasing in H.
        return sum(s * s * (lcm // size) for s, size in zip(sums, sizes))

    observed, start = [], 0
    for size in sizes:
        observed.append(sum(r2[start:start + size]))
        start += size
    target = score(tuple(observed))
    counts = labeling_counts(r2, sizes)  # @line L6
    hits = sum(cnt for sums, cnt in counts.items() if score(sums) >= target)  # @line L7
    total = math.factorial(sum(sizes))
    for size in sizes:
        total //= math.factorial(size)
    p = Fraction(hits, total)
    return float(h), (p if exact else float(p))  # @line L8
