# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lp-rounding-set-cover/. The authors are listed in prov/596RD9.jsonl.

import random
from fractions import Fraction

import pytest

from lp_rounding_set_cover import (
    inclusion_probabilities,
    lp_rounding_set_cover,
    repair,
    rounds,
    solve_set_cover_lp,
)


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


def exact_expectation(n, sets, costs, p):
    """E[cost] and E[number of uncovered elements before repair], over all 2^m coin outcomes."""
    m = len(sets)
    e_cost = Fraction(0)
    e_unc = Fraction(0)
    for mask in range(1 << m):
        pr = Fraction(1)
        for j in range(m):
            pr *= p[j] if mask >> j & 1 else 1 - p[j]
        if pr == 0:
            continue
        picked = {j for j in range(m) if mask >> j & 1}
        cov = set()
        for j in picked:
            cov |= set(sets[j])
        e_unc += pr * (n - len(cov & set(range(n))))
        e_cost += pr * sum(costs[j] for j in repair(n, sets, costs, picked))
    return e_cost, e_unc


def fano_like():
    # elements and sets are the nonzero vectors of F_2^3; S_v = {u : <u, v> = 1}
    vecs = list(range(1, 8))
    dot = lambda a, b: bin(a & b).count("1") % 2
    return [{i for i, u in enumerate(vecs) if dot(u, v)} for v in vecs]


def test_example_exact_expectation():
    sets = fano_like()
    lp, x = solve_set_cover_lp(7, sets, [1] * 7)
    assert lp == Fraction(7, 4) and x == [Fraction(1, 4)] * 7
    assert brute_opt(7, sets, [1] * 7) == 3
    t = rounds(7)
    assert t == 2
    p = inclusion_probabilities(x, t)
    assert p == [Fraction(7, 16)] * 7
    e_cost, e_unc = exact_expectation(7, sets, [1] * 7, p)
    assert e_cost == Fraction(965028091, 268435456)
    assert e_unc == 7 * Fraction(3, 4) ** 8
    assert e_cost <= (t + 1) * lp


def test_edge_cases():
    rng = random.Random(0)
    assert lp_rounding_set_cover(0, [], [], rng) == (set(), [], 0, 0)
    chosen, x, lp, t = lp_rounding_set_cover(1, [{0}], [5], rng)
    assert chosen == {0} and lp == 5 and t == 1
    with pytest.raises(ValueError):
        lp_rounding_set_cover(2, [{0}], [1], rng)
    with pytest.raises(ValueError):
        lp_rounding_set_cover(1, [{0}], [-1], rng)
    assert rounds(2) == 1 and rounds(3) == 2 and rounds(8) == 3 and rounds(21) == 4


def test_output_is_always_a_cover():
    rng = random.Random(77)
    for _ in range(200):
        m = rng.randint(1, 6)
        n = rng.randint(1, 8)
        sets = [set(rng.sample(range(n), rng.randint(0, n))) for _ in range(m)]
        sets[rng.randrange(m)] |= set(range(n)) - set().union(*sets)
        costs = [rng.randint(0, 6) for _ in range(m)]
        chosen, x, lp, t = lp_rounding_set_cover(n, sets, costs, rng)
        assert covers(n, sets, chosen)
        assert lp <= brute_opt(n, sets, costs)


def test_exact_expectation_against_bound():
    rng = random.Random(1987)
    for _ in range(500):
        m = rng.randint(1, 5)
        n = rng.randint(1, 7)
        sets = [set(rng.sample(range(n), rng.randint(0, n))) for _ in range(m)]
        sets[rng.randrange(m)] |= set(range(n)) - set().union(*sets)
        costs = [rng.randint(0, 6) for _ in range(m)]
        lp, x = solve_set_cover_lp(n, sets, costs)
        opt = brute_opt(n, sets, costs)
        t = rounds(n)
        p = inclusion_probabilities(x, t)
        e_cost, e_unc = exact_expectation(n, sets, costs, p)
        assert lp <= opt <= e_cost
        # each set enters with probability at most t x_j
        assert all(pj <= t * xj for pj, xj in zip(p, x))
        # each element stays uncovered with probability at most e^-t <= 1/n
        assert e_unc <= 1
        assert e_cost <= (t + 1) * lp
