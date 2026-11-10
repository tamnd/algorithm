# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/frequency-rounding-set-cover/. The authors are listed in prov/7N315T.jsonl.

import random
from fractions import Fraction
from itertools import combinations

import pytest

from frequency_rounding_set_cover import frequency_rounding_set_cover, solve_set_cover_lp


def brute_opt(n, sets, costs):
    best = None
    for mask in range(1 << len(sets)):
        cov = set()
        for j, s in enumerate(sets):
            if mask >> j & 1:
                cov |= set(s)
        if cov >= set(range(n)):
            c = sum(costs[j] for j in range(len(sets)) if mask >> j & 1)
            if best is None or c < best:
                best = c
    return best


def covers(n, sets, chosen):
    cov = set()
    for j in chosen:
        cov |= set(sets[j])
    return cov >= set(range(n))


def test_example():
    # the page uses elements 1..7; here they are 0..6
    sets = [{3, 4, 6}, {0, 1, 2, 3, 5, 6}, {5, 6}, {0, 2, 3, 4}, {0, 1, 4, 5}]
    costs = [1, 4, 3, 3, 2]
    chosen, x, lp, f = frequency_rounding_set_cover(7, sets, costs)
    assert f == 3 and lp == Fraction(14, 3)
    assert x == [Fraction(1, 3), Fraction(2, 3), 0, Fraction(1, 3), Fraction(1, 3)]
    assert chosen == {0, 1, 3, 4}
    assert sum(costs[j] for j in chosen) == 10
    assert brute_opt(7, sets, costs) == 5


def test_edge_cases():
    assert frequency_rounding_set_cover(0, [], []) == (set(), [], 0, 0)
    chosen, x, lp, f = frequency_rounding_set_cover(1, [{0}], [5])
    assert chosen == {0} and lp == 5 and f == 1
    with pytest.raises(ValueError):
        frequency_rounding_set_cover(2, [{0}], [1])
    with pytest.raises(ValueError):
        frequency_rounding_set_cover(1, [{0}], [-1])


def test_vertex_cover_is_f_equal_2():
    # the triangle as a set system: elements are edges, sets are vertices
    sets = [{0, 2}, {0, 1}, {1, 2}]
    chosen, x, lp, f = frequency_rounding_set_cover(3, sets, [1, 1, 1])
    assert f == 2 and lp == Fraction(3, 2) and chosen == {0, 1, 2}


def test_tight_family():
    # elements are the f-subsets of k > f sets; the LP optimum x = 1/f is unique,
    # LP = k/f, OPT = k - f + 1, ALG = k
    for f in (2, 3):
        for k in range(f + 1, 7):
            elems = list(combinations(range(k), f))
            sets = [{i for i, e in enumerate(elems) if j in e} for j in range(k)]
            chosen, x, lp, ff = frequency_rounding_set_cover(len(elems), sets, [1] * k)
            assert ff == f and lp == Fraction(k, f)
            assert brute_opt(len(elems), sets, [1] * k) == k - f + 1
            assert len(chosen) == k


def test_random_against_brute_force():
    rng = random.Random(31)
    for _ in range(500):
        m = rng.randint(1, 6)
        n = rng.randint(1, 7)
        sets = [set() for _ in range(m)]
        for e in range(n):
            for j in rng.sample(range(m), rng.randint(1, min(m, 3))):
                sets[j].add(e)
        costs = [rng.randint(0, 7) for _ in range(m)]
        chosen, x, lp, f = frequency_rounding_set_cover(n, sets, costs)
        opt = brute_opt(n, sets, costs)
        alg = sum(costs[j] for j in chosen)
        assert covers(n, sets, chosen)
        assert all(sum(x[j] for j in range(m) if e in sets[j]) >= 1 for e in range(n))
        assert f == max(sum(1 for s in sets if e in s) for e in range(n))
        assert lp <= opt <= alg <= f * lp


def test_lp_value_matches_dual_bound():
    rng = random.Random(5)
    for _ in range(50):
        m, n = 4, 5
        sets = [set(rng.sample(range(n), rng.randint(1, n))) for _ in range(m)]
        missing = set(range(n)) - set().union(*sets)
        sets[0] |= missing
        costs = [rng.randint(1, 5) for _ in range(m)]
        lp, x = solve_set_cover_lp(n, sets, costs)
        assert lp <= brute_opt(n, sets, costs)
