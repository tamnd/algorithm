# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hochberg-procedure/. The authors are listed in prov/T4RCRV.jsonl.

import itertools
import math
import random
import statistics
from fractions import Fraction

import pytest

from hochberg_procedure import hochberg

BH95 = [0.0001, 0.0004, 0.0019, 0.0095, 0.0201, 0.0278, 0.0298, 0.0344, 0.0459, 0.3240, 0.4262, 0.5719, 0.6528, 0.7590, 1.000]


def holm_reference(p: list, alpha) -> list[bool]:
    """Holm's step-down rule, written out directly, as the reference for the power comparison."""
    m = len(p)
    order = sorted(range(m), key=lambda i: p[i])
    reject = [False] * m
    for k, i in enumerate(order):
        if (m - k) * p[i] > alpha:
            break
        reject[i] = True
    return reject


def simes_rejects(values: list, alpha) -> bool:
    """The Simes test of an intersection: reject when p_(j) <= j alpha / n for some j."""
    n = len(values)
    return any(v * n <= (j + 1) * alpha for j, v in enumerate(sorted(values)))


def closed_simes(p: list, alpha) -> list[bool]:
    """Brute force: closed testing with Simes local tests (Hommel's procedure), over all 2^m - 1 subsets."""
    m = len(p)
    subsets = [s for size in range(1, m + 1) for s in itertools.combinations(range(m), size)]
    local = {s: simes_rejects([p[j] for j in s], alpha) for s in subsets}
    return [all(local[s] for s in subsets if i in s) for i in range(m)]


def test_hochberg_beats_holm_by_hand() -> None:
    reject, adjusted = hochberg([0.04, 0.045], 0.05)
    # Step-up: p_(2) = 0.045 <= 0.05 / 1, so both are rejected. Holm stops at 0.04 > 0.05 / 2.
    assert reject == [True, True]
    assert holm_reference([0.04, 0.045], 0.05) == [False, False]
    assert adjusted == pytest.approx([0.045, 0.045])


def test_worked_example_by_hand() -> None:
    reject, adjusted = hochberg(BH95, 0.05)
    # From the top: 1.000 > 0.05, 0.7590 > 0.025, ..., 0.0095 > 0.05/12; then 0.0019 <= 0.05/13.
    assert [i for i, r in enumerate(reject) if r] == [0, 1, 2]
    assert adjusted[:4] == pytest.approx([0.0015, 0.0056, 0.0247, 0.114])
    assert adjusted[-1] == 1


def test_exact_fractions() -> None:
    p = [Fraction(1, 10), Fraction(1, 50), Fraction(3, 100), Fraction(1, 30)]
    reject, adjusted = hochberg(p, Fraction(1, 10))
    # Sorted: 1/50, 3/100, 1/30, 1/10 against 1/40, 1/30, 1/20, 1/10. The largest passes, so all are rejected.
    assert reject == [True, True, True, True]
    # Products (m - k + 1) p_(k): 2/25, 9/100, 1/15, 1/10; the running minimum from the top gives these.
    assert adjusted == [Fraction(1, 10), Fraction(1, 15), Fraction(1, 15), Fraction(1, 15)]


def test_superset_of_holm_and_subset_of_closed_simes() -> None:
    rng = random.Random(1988)
    for _ in range(400):
        m = rng.randint(1, 7)
        p = [Fraction(rng.randint(0, 100), 100) ** 2 for _ in range(m)]
        alpha = Fraction(rng.randint(1, 20), 100)
        reject, _ = hochberg(p, alpha)
        holm = holm_reference(p, alpha)
        hommel = closed_simes(p, alpha)
        assert all(r or not h for r, h in zip(reject, holm))  # Holm's rejections are kept
        assert all(h or not r for r, h in zip(reject, hommel))  # every Hochberg rejection is a closed Simes rejection


def test_at_least_as_powerful_as_holm_on_many_float_vectors() -> None:
    rng = random.Random(3)
    for _ in range(5000):
        m = rng.randint(1, 30)
        p = [rng.random() ** 4 for _ in range(m)]
        reject = hochberg(p, 0.05)[0]
        assert sum(reject) >= sum(holm_reference(p, 0.05))
        assert all(r or not h for r, h in zip(reject, holm_reference(p, 0.05)))


def test_adjusted_p_values_match_rejections() -> None:
    rng = random.Random(4)
    for _ in range(300):
        m = rng.randint(1, 10)
        p = [Fraction(rng.randint(0, 200), 200) for _ in range(m)]
        _, adjusted = hochberg(p, Fraction(1, 20))
        for alpha in [Fraction(k, 100) for k in range(0, 100, 3)]:
            assert hochberg(p, alpha)[0] == [a <= alpha for a in adjusted]


def test_invalid_input() -> None:
    assert hochberg([], 0.05) == ([], [])
    with pytest.raises(ValueError):
        hochberg([0.5, 2], 0.05)


def test_exact_fwer_under_independence_on_grids() -> None:
    """Global null, independent p-values uniform on {1/N, ..., 1}, every threshold on the grid; all N^m cases."""
    for m, n_grid, alpha in [(2, 10, Fraction(2, 5)), (3, 20, Fraction(3, 10))]:
        grid = [Fraction(k, n_grid) for k in range(1, n_grid + 1)]
        hits = sum(any(hochberg(list(p), alpha)[0]) for p in itertools.product(grid, repeat=m))
        fwer = Fraction(hits, n_grid**m)
        assert fwer <= alpha
        if m == 2:
            # P(max <= 2/5) + P(min <= 1/5 < 2/5 < max) = 16/100 + 24/100: the Simes bound is attained.
            assert fwer == alpha


def test_monte_carlo_simes_equality_under_independence() -> None:
    rng = random.Random(1986)
    m, alpha, reps = 5, 0.1, 30000
    hits = sum(any(hochberg([rng.random() for _ in range(m)], alpha)[0]) for _ in range(reps))
    # Simes (1986): exactly alpha for continuous independent p-values. Four standard errors are 0.0069.
    assert abs(hits / reps - alpha) < 0.0069


def test_monte_carlo_positive_dependence() -> None:
    """One-sided tests on equicorrelated normals with rho = 0.5 (an MTP2 case), m_0 = 6 of m = 8."""
    rng = random.Random(1998)
    nd = statistics.NormalDist()
    m, m0, alpha, reps, errors = 8, 6, 0.05, 15000, 0
    for _ in range(reps):
        shared = rng.gauss(0, 1)
        z = [math.sqrt(0.5) * shared + math.sqrt(0.5) * rng.gauss(0, 1) + (3.5 if i >= m0 else 0.0) for i in range(m)]
        errors += any(hochberg([1 - nd.cdf(v) for v in z], alpha)[0][:m0])
    assert errors / reps <= alpha + 0.0054  # three standard errors


def test_negative_dependence_breaks_the_guarantee_exactly() -> None:
    """A joint law of two uniform p-values on {1/40, ..., 1} under which Hochberg has FWER 3 alpha / 2.

    With alpha = 1/10: B = {1/40, 2/40} (at most alpha/2), A = {3/40, 4/40} (in (alpha/2, alpha]) and C the other 36 points.
    The pair falls in A x A with probability 1/20, in B x C with 1/20, in C x B with 1/20 and in C x C with 17/20,
    uniformly inside each block. Both marginals are uniform on the grid.
    """
    alpha = Fraction(1, 10)
    grid = [Fraction(k, 40) for k in range(1, 41)]
    b_set, a_set, c_set = grid[:2], grid[2:4], grid[4:]
    law: dict[tuple, Fraction] = {}
    for block, mass in [((a_set, a_set), Fraction(1, 20)), ((b_set, c_set), Fraction(1, 20)), ((c_set, b_set), Fraction(1, 20)), ((c_set, c_set), Fraction(17, 20))]:
        cells = list(itertools.product(*block))
        for cell in cells:
            law[cell] = law.get(cell, 0) + mass / len(cells)
    for coord in (0, 1):
        for g in grid:
            assert sum(w for cell, w in law.items() if cell[coord] == g) == Fraction(1, 40)
    fwer_hochberg = sum(w for cell, w in law.items() if any(hochberg(list(cell), alpha)[0]))
    fwer_holm = sum(w for cell, w in law.items() if any(holm_reference(list(cell), alpha)))
    assert fwer_hochberg == Fraction(3, 2) * alpha
    assert fwer_holm == alpha
