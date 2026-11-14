# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mcnemar-test/. The authors are listed in prov/H919BT.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

from mcnemar_test import mcnemar_statistic, mcnemar_test

METHODS = ("exact", "asymptotic", "corrected")


def test_page_examples() -> None:
    assert mcnemar_statistic(15, 5) == 5.0
    assert mcnemar_statistic(15, 5, corrected=True) == pytest.approx(4.05)
    assert mcnemar_test(15, 5, "asymptotic") == pytest.approx(0.025347, abs=1e-6)
    assert mcnemar_test(15, 5, "corrected") == pytest.approx(0.044171, abs=1e-6)
    assert mcnemar_test(15, 5, exact=True) == Fraction(5425, 131072)
    assert mcnemar_test(9, 2, "asymptotic") == pytest.approx(0.034808, abs=1e-6)
    assert mcnemar_test(9, 2, "corrected") == pytest.approx(0.070440, abs=1e-6)
    assert mcnemar_test(9, 2, exact=True) == Fraction(67, 1024)
    assert mcnemar_test(6, 1, exact=True) == Fraction(1, 8)
    assert mcnemar_test(6, 1, "asymptotic") == pytest.approx(0.058782, abs=1e-6)


def test_exact_against_enumeration_of_signs() -> None:
    # Under the null, each discordant pair is (yes, no) or (no, yes) with
    # probability 1/2. Enumerate all 2^m outcomes and count the ones whose
    # imbalance |b - c| is at least the observed one.
    for m in range(0, 15):
        outcomes = list(itertools.product((0, 1), repeat=m))
        for b in range(m + 1):
            c = m - b
            extreme = sum(1 for o in outcomes if abs(2 * sum(o) - m) >= abs(b - c))
            assert mcnemar_test(b, c, exact=True) == Fraction(extreme, 2**m)


def test_chi_square_tail_matches_normal_tail() -> None:
    # With 1 degree of freedom, P(chi2 > x) = P(|Z| > sqrt(x)) = erfc(sqrt(x / 2)).
    for b, c in ((15, 5), (9, 2), (40, 61), (0, 7), (300, 250)):
        x = mcnemar_statistic(b, c)
        assert mcnemar_test(b, c, "asymptotic") == pytest.approx(math.erfc(math.sqrt(x / 2)), rel=1e-9, abs=1e-15)


def conditional_size(m: int, method: str) -> Fraction:
    return Fraction(sum(math.comb(m, k) for k in range(m + 1) if mcnemar_test(k, m - k, method) <= 0.05), 2**m)


def test_conditional_sizes() -> None:
    alpha = Fraction(1, 20)
    exact = [conditional_size(m, "exact") for m in range(101)]
    asymptotic = [conditional_size(m, "asymptotic") for m in range(101)]
    corrected = [conditional_size(m, "corrected") for m in range(101)]
    assert all(s <= alpha for s in exact)  # proved
    assert all(s <= alpha for s in corrected)  # measured for m <= 100 only
    assert asymptotic[4] == Fraction(1, 8)  # rejects at b = 4, c = 0
    assert sum(s > alpha for s in asymptotic) == 47
    assert corrected[17] < exact[17]


def unconditional_size(n: int, pi: float, method: str) -> float:
    # n pairs, each discordant with probability pi, split evenly under the null.
    sizes = [float(conditional_size(m, method)) for m in range(n + 1)]
    return math.fsum(math.comb(n, m) * pi**m * (1 - pi) ** (n - m) * sizes[m] for m in range(n + 1))


def test_unconditional_size_exact_and_by_simulation() -> None:
    n, pi = 50, 0.2
    want = {method: unconditional_size(n, pi, method) for method in METHODS}
    assert want["exact"] == pytest.approx(0.02213, abs=1e-5)
    assert want["asymptotic"] == pytest.approx(0.04292, abs=1e-5)
    assert want["corrected"] == pytest.approx(0.02183, abs=1e-5)
    assert unconditional_size(100, 0.3, "asymptotic") > 0.05
    rng = random.Random(1)
    reps = 10000
    hits = dict.fromkeys(METHODS, 0)
    for _ in range(reps):
        b = c = 0
        for _ in range(n):
            u = rng.random()
            if u < pi / 2:
                b += 1
            elif u < pi:
                c += 1
        for method in METHODS:
            hits[method] += mcnemar_test(b, c, method) <= 0.05
    for method in METHODS:
        se = math.sqrt(want[method] * (1 - want[method]) / reps)
        assert abs(hits[method] / reps - want[method]) < 4 * se


def test_symmetry_and_edges() -> None:
    for b, c in ((3, 11), (0, 9), (25, 30)):
        for method in METHODS:
            assert mcnemar_test(b, c, method) == mcnemar_test(c, b, method)
    assert mcnemar_test(0, 0) == 1.0 and mcnemar_test(0, 0, exact=True) == 1
    assert mcnemar_test(7, 7, exact=True) == 1
    assert mcnemar_test(7, 7, "corrected") == 1.0
    assert mcnemar_test(0, 6, exact=True) == Fraction(1, 32)
    assert 0 < mcnemar_test(0, 2000, exact=True) < Fraction(1, 2**1998)


def test_errors() -> None:
    with pytest.raises(ValueError):
        mcnemar_test(-1, 3)
    with pytest.raises(ValueError):
        mcnemar_test(1, 3, "wald")
    with pytest.raises(ValueError):
        mcnemar_test(1.5, 3)  # type: ignore[arg-type]
