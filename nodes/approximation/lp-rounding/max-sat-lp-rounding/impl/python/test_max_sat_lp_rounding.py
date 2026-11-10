# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/max-sat-lp-rounding/. The authors are listed in prov/TE21R0.jsonl.

import random
from fractions import Fraction
from itertools import product

import pytest

from max_sat_lp_rounding import (
    derandomize,
    deterministic_max_sat,
    expected_weight,
    max_sat_lp_rounding,
    satisfied_weight,
    solve_max_sat_lp,
)

HALF = Fraction(1, 2)


def brute_opt(n, clauses, weights):
    return max(satisfied_weight(clauses, weights, a) for a in product([False, True], repeat=n))


def prob(a, p):
    r = Fraction(1)
    for v, q in zip(a, p):
        r *= q if v else 1 - q
    return r


def exact_expectation(n, clauses, weights, p):
    """E[W] by summing over all 2^n assignments, an oracle independent of expected_weight."""
    return sum(prob(a, p) * satisfied_weight(clauses, weights, a) for a in product([False, True], repeat=n))


def exact_best_of_two(n, clauses, weights, y):
    """E[max(W(a), W(b))] with a from the LP coins and b from fair coins, over all 4^n outcomes."""
    total = Fraction(0)
    for a in product([False, True], repeat=n):
        pa = prob(a, y)
        if pa == 0:
            continue
        wa = satisfied_weight(clauses, weights, a)
        for b in product([False, True], repeat=n):
            total += pa * prob(b, [HALF] * n) * max(wa, satisfied_weight(clauses, weights, b))
    return total


EX_CLAUSES = [[-2], [-1, -2], [-1, 3], [1, 2], [-3, 2, -1]]
EX_WEIGHTS = [2, 4, 1, 2, 2]


def test_example():
    lp, y, z = solve_max_sat_lp(3, EX_CLAUSES, EX_WEIGHTS)
    assert lp == Fraction(31, 3)
    assert y == [Fraction(2, 3), Fraction(1, 3), Fraction(2, 3)]
    assert z == [Fraction(2, 3), 1, 1, 1, 1]
    assert brute_opt(3, EX_CLAUSES, EX_WEIGHTS) == 10
    assert expected_weight(EX_CLAUSES, EX_WEIGHTS, y) == Fraction(221, 27)
    assert expected_weight(EX_CLAUSES, EX_WEIGHTS, [HALF] * 3) == 8
    assert exact_best_of_two(3, EX_CLAUSES, EX_WEIGHTS, y) == Fraction(1949, 216)
    a, w, lp2 = deterministic_max_sat(3, EX_CLAUSES, EX_WEIGHTS)
    assert a == [False, True, True] and w == 9 and lp2 == lp


def test_gap_instance():
    clauses = [[1, 2], [1, -2], [-1, 2], [-1, -2]]
    lp, y, z = solve_max_sat_lp(2, clauses, [1] * 4)
    assert lp == 4 and brute_opt(2, clauses, [1] * 4) == 3


def test_edge_cases():
    rng = random.Random(0)
    assert max_sat_lp_rounding(0, [], [], rng) == ([], 0, 0)
    assert deterministic_max_sat(1, [[1], [-1]], [3, 1])[1] == 3
    with pytest.raises(ValueError):
        max_sat_lp_rounding(1, [[1, 1]], [1], rng)
    with pytest.raises(ValueError):
        max_sat_lp_rounding(1, [[2]], [1], rng)
    with pytest.raises(ValueError):
        max_sat_lp_rounding(1, [[1]], [-1], rng)
    with pytest.raises(ValueError):
        deterministic_max_sat(1, [[]], [1])


def test_randomized_run_is_consistent():
    rng = random.Random(3)
    for _ in range(30):
        a, w, lp = max_sat_lp_rounding(3, EX_CLAUSES, EX_WEIGHTS, rng)
        assert w == satisfied_weight(EX_CLAUSES, EX_WEIGHTS, a) <= 10 <= lp


def test_random_against_brute_force():
    rng = random.Random(1994)
    for _ in range(500):
        n = rng.randint(1, 4)
        clauses = []
        for _ in range(rng.randint(1, 6)):
            vs = rng.sample(range(1, n + 1), rng.randint(1, n))
            clauses.append([v if rng.random() < 0.5 else -v for v in vs])
        weights = [rng.randint(0, 5) for _ in clauses]
        lp, y, z = solve_max_sat_lp(n, clauses, weights)
        opt = brute_opt(n, clauses, weights)
        assert opt <= lp
        ea = exact_expectation(n, clauses, weights, y)
        eb = exact_expectation(n, clauses, weights, [HALF] * n)
        assert ea == expected_weight(clauses, weights, y)
        # the per-clause bound 1 - (1 - 1/k)^k for LP rounding
        bound = sum(w * zj * (1 - (1 - Fraction(1, len(cl))) ** len(cl)) for cl, w, zj in zip(clauses, weights, z))
        assert ea >= bound
        assert 4 * (ea + eb) >= 6 * lp
        a = derandomize(n, clauses, weights, y)
        assert satisfied_weight(clauses, weights, a) >= ea
        a, w, _ = deterministic_max_sat(n, clauses, weights)
        assert w == satisfied_weight(clauses, weights, a)
        assert 4 * w >= 3 * lp >= 3 * opt
        if n <= 3:
            assert 4 * exact_best_of_two(n, clauses, weights, y) >= 3 * lp
