# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/holm-bonferroni-method/. The authors are listed in prov/7A4AQ3.jsonl.

import itertools
import math
import random
import statistics
from fractions import Fraction

import pytest

from holm_bonferroni_method import holm

BH95 = [0.0001, 0.0004, 0.0019, 0.0095, 0.0201, 0.0278, 0.0298, 0.0344, 0.0459, 0.3240, 0.4262, 0.5719, 0.6528, 0.7590, 1.000]


def closed_bonferroni(p: list, alpha) -> tuple[list[bool], list]:
    """Brute force: closed testing with a Bonferroni local test for every intersection H_I.

    H_I is rejected when |I| min_(i in I) p_i <= alpha. H_i is rejected when every H_I
    with i in I is rejected. The adjusted p-value of H_i is max over I containing i of
    min(1, |I| min_(j in I) p_j). All 2^m - 1 nonempty subsets are enumerated.
    """
    m = len(p)
    adjusted = [0] * m
    for size in range(1, m + 1):
        for subset in itertools.combinations(range(m), size):
            p_local = min(1, size * min(p[j] for j in subset))
            for i in subset:
                adjusted[i] = max(adjusted[i], p_local)
    reject = [all(min(1, len(s) * min(p[j] for j in s)) <= alpha for size in range(1, m + 1) for s in itertools.combinations(range(m), size) if i in s) for i in range(m)]
    return reject, adjusted


def test_worked_example_by_hand() -> None:
    reject, adjusted = holm(BH95, 0.05)
    # 0.0001 <= 0.05/15, 0.0004 <= 0.05/14, 0.0019 <= 0.05/13, and 0.0095 > 0.05/12 = 0.004167 stops.
    assert [i for i, r in enumerate(reject) if r] == [0, 1, 2]
    assert adjusted[:5] == pytest.approx([0.0015, 0.0056, 0.0247, 0.114, 0.2211])


def test_holm_beats_bonferroni_by_hand() -> None:
    p = [Fraction(5, 1000), Fraction(11, 1000), Fraction(2, 100), Fraction(4, 100)]
    reject, adjusted = holm(p, Fraction(1, 20))
    # 0.005 <= 0.0125, 0.011 <= 0.01667, 0.02 <= 0.025, 0.04 <= 0.05: all four.
    assert reject == [True, True, True, True]
    assert adjusted == [Fraction(1, 50), Fraction(33, 1000), Fraction(1, 25), Fraction(1, 25)]
    # Bonferroni at 0.05/4 = 0.0125 rejects only the first two.
    assert [4 * v <= Fraction(1, 20) for v in p] == [True, True, False, False]


def test_stops_at_first_failure() -> None:
    p = [Fraction(1, 100), Fraction(3, 100), Fraction(1, 1000)]
    reject, _ = holm(p, Fraction(1, 20))
    # Sorted: 0.001 <= 0.05/3 yes, 0.01 <= 0.025 yes, 0.03 <= 0.05 yes.
    assert reject == [True, True, True]
    reject, _ = holm([Fraction(1, 50), Fraction(1, 50), Fraction(9, 10)], Fraction(1, 20))
    # 0.02 <= 0.05/3 fails, so nothing is rejected, even though 0.02 <= 0.05/2.
    assert reject == [False, False, False]


def test_equals_closed_testing_with_bonferroni_local_tests() -> None:
    rng = random.Random(1979)
    for _ in range(300):
        m = rng.randint(1, 8)
        denom = rng.choice([20, 100, 400])
        p = [Fraction(rng.randint(0, denom), denom) for _ in range(m)]
        alpha = Fraction(rng.randint(1, 19), 100)
        assert holm(p, alpha) == closed_bonferroni(p, alpha)


def test_at_least_as_many_rejections_as_bonferroni() -> None:
    rng = random.Random(5)
    for _ in range(2000):
        m = rng.randint(1, 20)
        p = [rng.random() ** 3 for _ in range(m)]
        reject, adjusted = holm(p, 0.05)
        for i in range(m):
            if p[i] * m <= 0.05:
                assert reject[i]
            assert adjusted[i] <= min(1, m * p[i])


def test_adjusted_p_values_match_rejections_and_are_monotone() -> None:
    rng = random.Random(8)
    for _ in range(300):
        m = rng.randint(1, 10)
        p = [Fraction(rng.randint(0, 200), 200) for _ in range(m)]
        _, adjusted = holm(p, Fraction(1, 20))
        order = sorted(range(m), key=lambda i: p[i])
        assert all(adjusted[order[k]] <= adjusted[order[k + 1]] for k in range(m - 1))
        for alpha in [Fraction(k, 100) for k in range(0, 100, 3)]:
            reject, _ = holm(p, alpha)
            assert reject == [a <= alpha for a in adjusted]


def test_ties_get_the_same_decision() -> None:
    reject, adjusted = holm([0.01, 0.01, 0.01, 0.5], 0.05)
    assert reject == [True, True, True, False]
    assert adjusted[0] == adjusted[1] == adjusted[2] == pytest.approx(0.04)


def test_invalid_input() -> None:
    assert holm([], 0.05) == ([], [])
    with pytest.raises(ValueError):
        holm([0.1, -0.1], 0.05)


def test_exact_fwer_by_enumeration_on_a_grid() -> None:
    """m = 3, m_0 = 2 true nulls with independent p-values uniform on {1/10, ..., 1}; the false null has p = 1/1000.

    Count the 100 cases exactly; the family-wise error rate is at most alpha = 2/5.
    """
    alpha = Fraction(2, 5)
    grid = [Fraction(k, 10) for k in range(1, 11)]
    bad = 0
    for a, b in itertools.product(grid, repeat=2):
        reject, _ = holm([a, b, Fraction(1, 1000)], alpha)
        bad += reject[0] or reject[1]
    # With H_3 rejected first, the two nulls face 1/5 and then 2/5:
    # a false rejection needs min(a, b) <= 1/5, which has 100 - 64 = 36 cases.
    assert bad == 36
    assert Fraction(bad, 100) <= alpha


def test_monte_carlo_strong_control_under_negative_dependence() -> None:
    """m_0 = 5 nulls with p_i = (U + i/5) mod 1, which is the worst case for the union bound, and 3 strong false nulls."""
    rng = random.Random(31)
    alpha, reps, errors = 0.05, 20000, 0
    for _ in range(reps):
        u = rng.random()
        p = [(u + i / 5) % 1 for i in range(5)] + [1e-6, 2e-6, 3e-6]
        reject, _ = holm(p, alpha)
        errors += any(reject[:5])
    # After the 3 false nulls fall, each null faces alpha/5 at the first step; the events are disjoint,
    # so the exact FWER is 5 * alpha/5 = alpha. Four standard errors are 0.0062.
    assert abs(errors / reps - alpha) < 0.0062


def test_monte_carlo_fwer_with_correlated_normals() -> None:
    rng = random.Random(77)
    nd = statistics.NormalDist()
    m, m0, alpha, reps, errors = 10, 7, 0.05, 10000, 0
    for _ in range(reps):
        shared = rng.gauss(0, 1)
        z = [math.sqrt(0.6) * shared + math.sqrt(0.4) * rng.gauss(0, 1) + (4.0 if i >= m0 else 0.0) for i in range(m)]
        reject, _ = holm([1 - nd.cdf(v) for v in z], alpha)
        errors += any(reject[:m0])
    assert errors / reps <= alpha + 0.0066  # three standard errors of a proportion near 0.05
