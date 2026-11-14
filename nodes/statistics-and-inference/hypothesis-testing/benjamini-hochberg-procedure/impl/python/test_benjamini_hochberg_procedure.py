# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/benjamini-hochberg-procedure/. The authors are listed in prov/MA7Z7G.jsonl.

import itertools
import math
import random
import statistics
from fractions import Fraction

import pytest

from benjamini_hochberg_procedure import bh, bh_linear

BH95 = [0.0001, 0.0004, 0.0019, 0.0095, 0.0201, 0.0278, 0.0298, 0.0344, 0.0459, 0.3240, 0.4262, 0.5719, 0.6528, 0.7590, 1.000]


def bh_brute_force(p: list, q) -> list[bool]:
    """Brute force from the self-consistency characterization: the largest set S with m p_i <= |S| q for all i in S.

    For each size s from m down to 1, S must be {i : m p_i <= s q}; it works when it has at least s elements.
    The answer is checked against every subset for small m in a separate test.
    """
    m = len(p)
    for s in range(m, 0, -1):
        chosen = [m * v <= s * q for v in p]
        if sum(chosen) >= s:
            return chosen
    return [False] * m


def test_worked_example_by_hand() -> None:
    reject, adjusted = bh(BH95, 0.05)
    # k q / m = k / 300: 0.0095 <= 4/300 = 0.01333, but 0.0201 > 5/300, 0.0278 > 6/300, ..., 0.0459 > 9/300.
    assert [i for i, r in enumerate(reject) if r] == [0, 1, 2, 3]
    assert adjusted[:6] == pytest.approx([0.0015, 0.003, 0.0095, 0.035625, 0.0603, 15 * 0.0298 / 7], abs=1e-9)
    # The sixth adjusted value is a running minimum: 15 * 0.0278 / 6 = 0.0695 is larger than 15 * 0.0298 / 7.
    assert bh_linear(BH95, 0.05) == reject


def test_step_up_rejects_p_values_above_their_own_threshold() -> None:
    p = [Fraction(1, 100), Fraction(3, 100), Fraction(28, 1000), Fraction(4, 100)]
    reject, _ = bh(p, Fraction(1, 10))
    # Thresholds k/40: 0.025, 0.05, 0.075, 0.1. Sorted 0.01, 0.028, 0.03, 0.04: k = 4 passes.
    assert reject == [True, True, True, True]
    reject, _ = bh([Fraction(3, 100), Fraction(3, 100), Fraction(9, 10)], Fraction(1, 20))
    # 0.9 > 0.05; 0.03 <= 2 * 0.05 / 3 = 0.0333, so both 0.03 are rejected, though 0.03 > 0.05/3.
    assert reject == [True, True, False]


def test_self_consistency_by_subset_enumeration() -> None:
    rng = random.Random(95)
    for _ in range(200):
        m = rng.randint(1, 8)
        p = [Fraction(rng.randint(0, 40), 40) for _ in range(m)]
        q = Fraction(rng.randint(1, 10), 20)
        best: tuple = ()
        for size in range(m, 0, -1):
            for s in itertools.combinations(range(m), size):
                if all(m * p[i] <= size * q for i in s):
                    best = s
                    break
            if best:
                break
        expected = [i in best for i in range(m)]
        assert bh(p, q)[0] == expected == bh_brute_force(p, q) == bh_linear(p, q)


def test_linear_version_matches_sorting_version_on_floats() -> None:
    rng = random.Random(6)
    for _ in range(3000):
        m = rng.randint(1, 40)
        p = [rng.random() ** rng.choice([1, 3, 6]) for _ in range(m)]
        if rng.random() < 0.3:  # exact ties and values on the thresholds
            p = [round(v * 20) / 20 for v in p]
        q = rng.choice([0.05, 0.1, 0.2])
        assert bh_linear(p, q) == bh(p, q)[0] == bh_brute_force(p, q)


def test_adjusted_p_values_match_rejections() -> None:
    rng = random.Random(7)
    for _ in range(300):
        m = rng.randint(1, 10)
        p = [Fraction(rng.randint(0, 100), 100) for _ in range(m)]
        _, adjusted = bh(p, Fraction(1, 10))
        for q in [Fraction(k, 100) for k in range(1, 100, 4)]:
            assert bh(p, q)[0] == [a <= q for a in adjusted]


def test_invalid_input() -> None:
    assert bh([], 0.1) == ([], [])
    assert bh_linear([], 0.1) == []
    with pytest.raises(ValueError):
        bh([0.5], 0)
    with pytest.raises(ValueError):
        bh_linear([1.5], 0.1)


def exact_fdr_on_grid(m: int, m0: int, q: Fraction, false_p: list) -> Fraction:
    """FDR by summing over all 10^m0 values of independent null p-values, each uniform on {1/10, ..., 1}."""
    grid = [Fraction(k, 10) for k in range(1, 11)]
    total = Fraction(0)
    for nulls in itertools.product(grid, repeat=m0):
        p = list(nulls) + false_p
        reject, _ = bh(p, q)
        r = sum(reject)
        v = sum(reject[:m0])
        if r:
            total += Fraction(v, r)
    return total / 10**m0


def test_fdr_equals_m0_over_m_times_q_exactly() -> None:
    """m = 4 and q = 2/5, so every threshold k q / m = k / 10 is a grid point and P(p_i <= k q / m) = k q / m exactly."""
    m, q = 4, Fraction(2, 5)
    rng = random.Random(2001)
    for m0 in range(1, m + 1):
        for _ in range(2 if m0 < m else 1):
            false_p = [Fraction(rng.randint(0, 1000), 1000) for _ in range(m - m0)]
            assert exact_fdr_on_grid(m, m0, q, false_p) == Fraction(m0, m) * q


def test_monte_carlo_fdr_independent_normals() -> None:
    rng = random.Random(1995)
    nd = statistics.NormalDist()
    m, m0, q, reps = 20, 15, 0.1, 6000
    total = 0.0
    for _ in range(reps):
        z = [rng.gauss(0, 1) + (2.5 if i >= m0 else 0.0) for i in range(m)]
        reject = bh_linear([nd.cdf(-v) for v in z], q)
        r = sum(reject)
        total += sum(reject[:m0]) / r if r else 0.0
    # Exact value (m0/m) q = 0.075. The standard deviation of the false discovery proportion is below 0.25,
    # so four standard errors are below 0.013.
    assert abs(total / reps - m0 / m * q) < 0.013


def test_monte_carlo_fdr_under_positive_dependence() -> None:
    """One-sided tests on equicorrelated normals (rho = 0.5) are PRDS: the FDR is at most (m0/m) q."""
    rng = random.Random(29)
    nd = statistics.NormalDist()
    m, m0, q, reps = 20, 15, 0.1, 6000
    total = 0.0
    for _ in range(reps):
        shared = rng.gauss(0, 1)
        z = [math.sqrt(0.5) * shared + math.sqrt(0.5) * rng.gauss(0, 1) + (2.5 if i >= m0 else 0.0) for i in range(m)]
        reject, _ = bh([nd.cdf(-v) for v in z], q)
        r = sum(reject)
        total += sum(reject[:m0]) / r if r else 0.0
    assert total / reps <= m0 / m * q + 0.013
