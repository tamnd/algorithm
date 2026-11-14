# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kruskal-wallis-test/. The authors are listed in prov/DCECK4.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

from kruskal_wallis_test import doubled_midranks, h_statistic, kruskal_wallis, labeling_counts

A = [27, 31, 22, 35]
B = [19, 24, 20, 18, 26]
C = [33, 38, 29, 40]


def h_direct(groups: list[list[float]]) -> Fraction:
    """H = (N - 1) SSB / SST on the midranks: a second formula, tie-corrected by itself."""
    pooled = [v for g in groups for v in g]
    big_n = len(pooled)
    ranks = []
    for v in pooled:
        ranks.append(sum(1 for t in pooled if t < v) + Fraction(sum(1 for t in pooled if t == v) + 1, 2))
    mean = Fraction(big_n + 1, 2)
    sst = sum((r - mean) ** 2 for r in ranks)
    ssb, start = Fraction(0), 0
    for g in groups:
        part = ranks[start:start + len(g)]
        ssb += len(g) * (sum(part) / len(g) - mean) ** 2
        start += len(g)
    return (big_n - 1) * ssb / sst if sst else Fraction(0)


def brute_force_p(groups: list[list[float]]) -> Fraction:
    """Share of all distinct assignments of the pooled values to the groups with H >= observed."""
    sizes = [len(g) for g in groups]
    pooled = [v for g in groups for v in g]
    h_obs = h_direct(groups)
    hits = total = 0
    for perm in itertools.permutations(range(len(pooled))):
        cut, start, ok = [], 0, True
        for size in sizes:
            block = perm[start:start + size]
            if list(block) != sorted(block):  # one representative per assignment of positions
                ok = False
                break
            cut.append([pooled[i] for i in block])
            start += size
        if not ok:
            continue
        total += 1
        hits += h_direct(cut) >= h_obs
    return Fraction(hits, total)


def test_page_example() -> None:
    assert h_statistic([A, B, C]) == Fraction(3699, 455)
    assert kruskal_wallis([A, B, C], "exact", exact=True)[1] == Fraction(4, 715)
    assert kruskal_wallis([A, B, C])[1] == pytest.approx(0.0171658, abs=1e-7)
    g2 = [[1, 2, 2, 3], [2, 3, 4, 4], [3, 4, 5, 5]]
    assert h_statistic(g2) == Fraction(1727, 273)
    assert kruskal_wallis(g2, "exact", exact=True)[1] == Fraction(19, 525)


def test_two_formulas_agree() -> None:
    rng = random.Random(1)
    for _ in range(200):
        k = rng.randint(2, 4)
        groups = [[rng.randint(0, 6) for _ in range(rng.randint(1, 5))] for _ in range(k)]
        if len(set(v for g in groups for v in g)) == 1:
            continue  # all values tied: H is 0 by convention
        assert h_statistic(groups) == h_direct(groups)


def test_two_groups_is_mann_whitney_squared() -> None:
    rng = random.Random(2)
    for _ in range(100):
        m, n = rng.randint(1, 7), rng.randint(1, 7)
        x = [rng.randint(0, 5) for _ in range(m)]
        y = [rng.randint(0, 5) for _ in range(n)]
        pooled = x + y
        big_n = m + n
        ties = sum(pooled.count(v) ** 3 - pooled.count(v) for v in set(pooled))
        var = Fraction(m * n, 12) * ((big_n + 1) - Fraction(ties, big_n * (big_n - 1)))
        if var == 0:
            continue
        r2 = doubled_midranks(pooled)
        u = Fraction(sum(r2[:m]), 2) - Fraction(m * (m + 1), 2)
        assert h_statistic([x, y]) == (u - Fraction(m * n, 2)) ** 2 / var


def test_exact_against_all_assignments() -> None:
    rng = random.Random(3)
    for _ in range(25):
        sizes = rng.choice([(2, 2, 2), (1, 2, 3), (3, 3), (2, 2, 3), (1, 1, 2, 2)])
        groups = [[rng.randint(0, 4) for _ in range(s)] for s in sizes]
        if len(set(v for g in groups for v in g)) == 1:
            continue
        assert kruskal_wallis(groups, "exact", exact=True)[1] == brute_force_p(groups)


def test_labeling_counts_total() -> None:
    r2 = doubled_midranks([1, 2, 2, 3, 5, 5, 7, 8, 9])
    counts = labeling_counts(r2, [2, 3, 4])
    assert sum(counts.values()) == math.factorial(9) // (2 * 6 * 24)
    assert all(sum(s) == sum(r2) for s in counts)


def test_exact_critical_value_333() -> None:
    # Sizes 3, 3, 3 without ties: P(H >= 5.6) = 0.05 exactly, and P(H >= 5.991) = 0.0107.
    r2 = [2 * i for i in range(1, 10)]
    counts = labeling_counts(r2, [3, 3, 3])
    total = sum(counts.values())

    def h(sums: tuple[int, ...]) -> Fraction:
        return Fraction(12, 90) * sum(Fraction(s, 2) ** 2 / 3 for s in sums) - 30

    assert total == 1680
    assert Fraction(sum(c for s, c in counts.items() if h(s) >= Fraction(28, 5)), total) == Fraction(1, 20)
    assert Fraction(sum(c for s, c in counts.items() if h(s) >= Fraction(5991, 1000)), total) == Fraction(18, 1680)


def test_chi_square_size_monte_carlo() -> None:
    rng = random.Random(33)
    r, alpha = 1500, 0.05
    hits = sum(kruskal_wallis([[rng.gauss(0.0, 1.0) for _ in range(10)] for _ in range(3)])[1] <= alpha
               for _ in range(r))
    assert abs(hits / r - alpha) <= 4 * math.sqrt(alpha * (1 - alpha) / r)


def test_edges() -> None:
    with pytest.raises(ValueError):
        kruskal_wallis([[1.0]])
    with pytest.raises(ValueError):
        kruskal_wallis([[1.0], []])
    with pytest.raises(ValueError):
        kruskal_wallis([[1.0], [2.0]], method="other")
    assert h_statistic([[1.0, 1.0], [1.0]]) == 0
