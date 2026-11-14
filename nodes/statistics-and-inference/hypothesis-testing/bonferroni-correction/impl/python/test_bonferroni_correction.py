# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bonferroni-correction/. The authors are listed in prov/DBDQ24.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

from bonferroni_correction import bonferroni_correction, sidak_correction, sidak_level

# The 15 p-values of the worked example of Benjamini and Hochberg (1995).
BH95 = [0.0001, 0.0004, 0.0019, 0.0095, 0.0201, 0.0278, 0.0298, 0.0344, 0.0459, 0.3240, 0.4262, 0.5719, 0.6528, 0.7590, 1.000]


def test_worked_example_by_hand() -> None:
    reject, adjusted = bonferroni_correction(BH95, 0.05)
    # 0.05 / 15 = 0.00333..., so only the first three p-values are at most the level.
    assert [i for i, r in enumerate(reject) if r] == [0, 1, 2]
    assert adjusted[:4] == pytest.approx([0.0015, 0.006, 0.0285, 0.1425])
    assert adjusted[-1] == 1


def test_exact_with_fractions() -> None:
    p = [Fraction(1, 100), Fraction(1, 40), Fraction(1, 30), Fraction(1, 2)]
    reject, adjusted = bonferroni_correction(p, Fraction(1, 20))
    # The level is 1/80: only 1/100 is at most it.
    assert reject == [True, False, False, False]
    assert adjusted == [Fraction(1, 25), Fraction(1, 10), Fraction(2, 15), 1]


def test_boundary_is_rejected() -> None:
    reject, _ = bonferroni_correction([Fraction(1, 40), Fraction(1, 2)], Fraction(1, 20))
    assert reject == [True, False]


def test_adjusted_p_value_matches_rejections() -> None:
    rng = random.Random(11)
    for _ in range(200):
        m = rng.randint(1, 12)
        p = [Fraction(rng.randint(0, 400), 400) for _ in range(m)]
        _, adjusted = bonferroni_correction(p, Fraction(1, 20))
        # For alpha < 1 the cap at 1 does not matter; at alpha = 1 every capped value is "rejected".
        for alpha in [Fraction(k, 100) for k in range(0, 100, 5)]:
            reject, _ = bonferroni_correction(p, alpha)
            assert reject == [a <= alpha for a in adjusted]


def test_invalid_input() -> None:
    assert bonferroni_correction([], 0.05) == ([], [])
    with pytest.raises(ValueError):
        bonferroni_correction([0.2, 1.5], 0.05)
    with pytest.raises(ValueError):
        bonferroni_correction([0.2, float("nan")], 0.05)
    with pytest.raises(ValueError):
        bonferroni_correction([0.2], 1.5)


def test_union_bound_is_attained_exactly() -> None:
    """Reference law: p_i = (U + i/m) mod 1 with U uniform on a grid of N points.

    Every p_i is uniform on the grid, and the events {p_i <= alpha/m} are disjoint, so the
    family-wise error rate of Bonferroni is exactly alpha. We count over all N values of U.
    """
    for m, n_grid, alpha in [(2, 40, Fraction(1, 10)), (4, 80, Fraction(1, 10)), (5, 100, Fraction(1, 20))]:
        hits = 0
        for u in range(1, n_grid + 1):
            p = [Fraction((u + i * n_grid // m - 1) % n_grid + 1, n_grid) for i in range(m)]
            reject, _ = bonferroni_correction(p, alpha)
            hits += any(reject)
        assert Fraction(hits, n_grid) == alpha


def test_exact_fwer_under_independence_on_a_grid() -> None:
    """All m nulls true, independent p-values uniform on {1/N, ..., N/N}: brute force over N^m points.

    The family-wise error rate is 1 - (1 - c/N)^m, where c = #{k : k/N <= alpha/m}, and it is at most alpha.
    """
    n_grid, alpha = 10, Fraction(2, 5)
    for m in [1, 2, 3, 4]:
        grid = [Fraction(k, n_grid) for k in range(1, n_grid + 1)]
        hits = sum(any(bonferroni_correction(list(p), alpha)[0]) for p in itertools.product(grid, repeat=m))
        exact = Fraction(hits, n_grid**m)
        c = sum(1 for g in grid if g <= alpha / m)
        assert exact == 1 - (1 - Fraction(c, n_grid)) ** m
        assert exact <= alpha


def test_monte_carlo_strong_control_with_dependence() -> None:
    """m = 10, m_0 = 6 true nulls with equicorrelated normal statistics (rho = 0.5), 4 false nulls."""
    rng = random.Random(2024)
    nd = __import__("statistics").NormalDist()
    m, m0, alpha, reps = 10, 6, 0.05, 20000
    errors = 0
    for _ in range(reps):
        shared = rng.gauss(0, 1)
        z = [math.sqrt(0.5) * shared + math.sqrt(0.5) * rng.gauss(0, 1) for _ in range(m)]
        z = [zi + (3.0 if i >= m0 else 0.0) for i, zi in enumerate(z)]
        p = [1 - nd.cdf(zi) for zi in z]
        reject, _ = bonferroni_correction(p, alpha)
        errors += any(reject[:m0])
    fwer = errors / reps
    # The union bound gives FWER <= (m0/m) alpha = 0.03. Three standard errors of a proportion near 0.03 are 0.0036.
    assert fwer <= m0 / m * alpha + 0.0036


def test_sidak_is_exact_under_independence() -> None:
    for m in [1, 2, 5, 20, 100]:
        level = sidak_level(0.05, m)
        assert 1 - (1 - level) ** m == pytest.approx(0.05, rel=1e-12)
        assert level >= 0.05 / m  # Sidak is never stricter than Bonferroni
    assert sidak_level(0.05, 15) == pytest.approx(0.0034137, abs=1e-7)
    reject, adjusted = sidak_correction(BH95, 0.05)
    assert [i for i, r in enumerate(reject) if r] == [0, 1, 2]
    assert adjusted[0] == pytest.approx(1 - (1 - 0.0001) ** 15, rel=1e-12)
    assert adjusted[-1] == 1.0


def test_sidak_monte_carlo_fwer() -> None:
    rng = random.Random(7)
    m, reps = 8, 40000
    level = sidak_level(0.05, m)
    hits = sum(any(rng.random() <= level for _ in range(m)) for _ in range(reps))
    # The exact FWER is 0.05; four standard errors are 0.0044.
    assert abs(hits / reps - 0.05) < 0.0044
