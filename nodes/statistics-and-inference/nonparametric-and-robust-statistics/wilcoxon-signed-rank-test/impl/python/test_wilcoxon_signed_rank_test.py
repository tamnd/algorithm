# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wilcoxon-signed-rank-test/. The authors are listed in prov/8KPP1Q.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

from wilcoxon_signed_rank_test import (
    doubled_midranks, signed_rank_counts, tie_sizes, wilcoxon_normal, wilcoxon_signed_rank,
)

# Cushny and Peebles (1905), as used by Student (1908): extra hours of sleep under two drugs.
DRUG_1 = [0.7, -1.6, -0.2, -1.2, -0.1, 3.4, 3.7, 0.8, 0.0, 2.0]
DRUG_2 = [1.9, 0.8, 1.1, 0.1, -0.1, 4.4, 5.5, 1.6, 4.6, 3.4]
DIFF = [round(b - a, 1) for a, b in zip(DRUG_1, DRUG_2)]
MIXED = [1.8, -0.6, 3.1, 2.4, -1.3, 0.9, 2.2, 0.0, 1.5, -0.4]


def brute_force(d: list[float]) -> tuple[Fraction, Fraction, Fraction]:
    """W+ and its tails by listing all 2^n sign vectors on the observed |d| (midranks)."""
    kept = [v for v in d if v != 0]
    n = len(kept)
    a = [abs(v) for v in kept]
    ranks = []
    for v in a:  # midrank = (number below) + (number equal + 1) / 2
        below = sum(1 for t in a if t < v)
        equal = sum(1 for t in a if t == v)
        ranks.append(below + Fraction(equal + 1, 2))
    w = sum(r for r, v in zip(ranks, kept) if v > 0)
    upper = lower = 0
    for signs in itertools.product((0, 1), repeat=n):
        t = sum(r for r, e in zip(ranks, signs) if e)
        upper += t >= w
        lower += t <= w
    return w, Fraction(upper, 2**n), Fraction(lower, 2**n)


def test_page_examples() -> None:
    assert wilcoxon_signed_rank(DIFF, exact=True) == (45.0, Fraction(1, 256))
    assert wilcoxon_signed_rank(MIXED, exact=True) == (38.0, Fraction(19, 256))
    assert wilcoxon_signed_rank(MIXED, "greater", exact=True) == (38.0, Fraction(19, 512))
    assert wilcoxon_normal(DIFF)[1] == pytest.approx(0.0090906980, abs=1e-9)
    assert wilcoxon_normal(MIXED)[1] == pytest.approx(0.0755605675, abs=1e-9)
    assert signed_rank_counts([2, 4, 6, 8])[::2] == [1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1]
    assert signed_rank_counts([2, 5, 5, 8]) == [1, 0, 1, 0, 0, 2, 0, 2, 1, 0, 2, 0, 1, 2, 0, 2,
                                                0, 0, 1, 0, 1]


def test_against_all_sign_vectors() -> None:
    rng = random.Random(3)
    for _ in range(150):
        n = rng.randint(0, 11)
        d = [rng.choice([-1, 1]) * rng.randint(0, 6) for _ in range(n)]  # many ties and zeros
        w, upper, lower = brute_force(d)
        got_w, got_g = wilcoxon_signed_rank(d, "greater", exact=True)
        assert got_w == float(w)
        assert got_g == upper
        assert wilcoxon_signed_rank(d, "less", exact=True)[1] == lower
        assert wilcoxon_signed_rank(d, exact=True)[1] == min(Fraction(1), 2 * min(upper, lower))


def test_counts_match_subsets() -> None:
    for n in range(0, 11):
        r2 = [2 * i for i in range(1, n + 1)]
        c = signed_rank_counts(r2)
        want = [0] * len(c)
        for mask in range(2**n):
            want[sum(r for i, r in enumerate(r2) if mask >> i & 1)] += 1
        assert c == want


def test_null_mean_and_variance() -> None:
    for values in ([1, 2, 3, 4, 5, 6, 7, 8], [1, 1, 2, 3, 3, 3, 4, 5, 5]):
        n = len(values)
        r2 = doubled_midranks(values)
        c = signed_rank_counts(r2)
        total = 2**n
        mean = sum(Fraction(s, 2) * cnt for s, cnt in enumerate(c)) / total
        var = sum(Fraction(s, 2) ** 2 * cnt for s, cnt in enumerate(c)) / total - mean**2
        ties = sum(t**3 - t for t in tie_sizes(values))
        assert mean == Fraction(n * (n + 1), 4)
        assert var == Fraction(n * (n + 1) * (2 * n + 1), 24) - Fraction(ties, 48)


def test_null_is_symmetric() -> None:
    c = signed_rank_counts(doubled_midranks([1, 2, 2, 3, 5, 5, 5, 8]))
    assert c == c[::-1]


def test_critical_value_n20() -> None:
    c = signed_rank_counts([2 * i for i in range(1, 21)])
    assert Fraction(sum(c[: 2 * 52 + 1]), 2**20) <= Fraction(25, 1000)
    assert Fraction(sum(c[: 2 * 53 + 1]), 2**20) > Fraction(25, 1000)


def test_size_under_symmetry_monte_carlo() -> None:
    rng = random.Random(5)
    n, r, alpha = 15, 2000, 0.05
    hits = sum(wilcoxon_signed_rank([rng.gauss(0.0, 1.0) for _ in range(n)])[1] <= alpha
               for _ in range(r))
    assert hits / r <= alpha + 4 * math.sqrt(alpha * (1 - alpha) / r)


def test_skewed_null_median_is_not_enough() -> None:
    # Median 0 but not symmetric: the test rejects far more often than alpha.
    rng = random.Random(11)
    n, r, alpha = 20, 2000, 0.05
    hits = sum(wilcoxon_signed_rank([rng.expovariate(1.0) - math.log(2.0)
                                     for _ in range(n)])[1] <= alpha for _ in range(r))
    assert hits / r > alpha + 4 * math.sqrt(alpha * (1 - alpha) / r)


def test_edges() -> None:
    assert wilcoxon_signed_rank([0.0, 0.0], exact=True) == (0.0, 1)
    assert wilcoxon_normal([0.0]) == (0.0, 1.0)
    with pytest.raises(ValueError):
        wilcoxon_signed_rank([1.0], "both")
    assert wilcoxon_signed_rank([3.0, 4.0], mu0=3.0, exact=True) == (1.0, 1)
