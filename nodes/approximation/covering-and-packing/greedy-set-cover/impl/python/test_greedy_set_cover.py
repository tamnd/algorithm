# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-set-cover/. The authors are listed in prov/YWN3V4.jsonl.

import random
from fractions import Fraction
from itertools import combinations

import pytest

from greedy_set_cover import greedy_set_cover, harmonic


def brute_opt(universe, sets, costs):
    best = None
    for r in range(len(sets) + 1):
        for c in combinations(range(len(sets)), r):
            if set().union(*[sets[i] for i in c]) >= universe:
                v = sum(costs[i] for i in c)
                if best is None or v < best:
                    best = v
    return best


def solve_square(a, b):
    """Solve a square system exactly; return None if it is singular."""
    k = len(a)
    m = [[Fraction(x) for x in row] + [Fraction(y)] for row, y in zip(a, b)]
    for c in range(k):
        p = next((r for r in range(c, k) if m[r][c] != 0), None)
        if p is None:
            return None
        m[c], m[p] = m[p], m[c]
        for r in range(k):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [m[r][t] - f * m[c][t] for t in range(k + 1)]
    return [m[i][k] / m[i][i] for i in range(k)]


def lp_value(universe, sets, costs):
    """min c.x subject to sum over S_j containing e of x_j >= 1, x >= 0.

    Exact, by enumerating the vertices of the polyhedron. For tiny instances only.
    """
    m = len(sets)
    rows = [([1 if e in s else 0 for s in sets], 1) for e in sorted(universe)]
    rows += [([1 if t == j else 0 for t in range(m)], 0) for j in range(m)]
    best = None
    for pick in combinations(range(len(rows)), m):
        x = solve_square([rows[i][0] for i in pick], [rows[i][1] for i in pick])
        if x is None:
            continue
        if all(sum(a * v for a, v in zip(r, x)) >= rhs for r, rhs in rows):
            val = sum(Fraction(c) * v for c, v in zip(costs, x))
            if best is None or val < best:
                best = val
    return best


def random_instance(rng, n, m, max_cost):
    universe = set(range(n))
    while True:
        sets = [set(e for e in range(n) if rng.random() < 0.4) for _ in range(m)]
        if set().union(*sets) == universe and all(sets):
            costs = [rng.randint(1, max_cost) for _ in range(m)]
            return universe, sets, costs


def test_example_page():
    universe = set(range(1, 8))
    sets = [{1, 2, 3, 5}, {3, 4, 6, 7}, {2, 5, 6}, {3, 7}, {1, 2, 4, 7}]
    costs = [3, 4, 4, 2, 1]
    chosen, price = greedy_set_cover(universe, sets, costs)
    assert chosen == [4, 0, 1]
    assert sum(costs[j] for j in chosen) == 8
    assert price[1] == Fraction(1, 4) and price[3] == Fraction(3, 2) and price[6] == 4
    assert brute_opt(universe, sets, costs) == 7
    assert lp_value(universe, sets, costs) == 6


def test_random_against_brute_force_and_lp():
    rng = random.Random(1974)
    for trial in range(120):
        n, m = rng.randint(1, 7), rng.randint(1, 6)
        universe, sets, costs = random_instance(rng, n, m, 5)
        chosen, price = greedy_set_cover(universe, sets, costs)
        assert set().union(*[sets[j] for j in chosen]) == universe
        alg = sum(costs[j] for j in chosen)
        assert sum(price.values()) == alg
        d = max(len(s) for s in sets)
        opt = brute_opt(universe, sets, costs)
        assert alg <= harmonic(d) * opt
        # dual fitting: y_e = price_e / H_d is a feasible dual solution
        for s, c in zip(sets, costs):
            assert sum(price[e] for e in s) <= harmonic(len(s)) * c
        if m <= 5:
            lp = lp_value(universe, sets, costs)
            assert sum(price.values()) / harmonic(d) <= lp <= opt
            assert alg <= harmonic(d) * lp


def test_unit_costs():
    rng = random.Random(1979)
    for trial in range(200):
        n, m = rng.randint(1, 8), rng.randint(1, 7)
        universe, sets, _ = random_instance(rng, n, m, 1)
        chosen, _ = greedy_set_cover(universe, sets)
        opt = brute_opt(universe, sets, [1] * m)
        assert len(chosen) <= harmonic(max(len(s) for s in sets)) * opt


def test_weighted_tight_family():
    # singletons {i} of cost 1/i and one set of all n elements of cost 1 + eps
    eps = Fraction(1, 1000)
    for n in range(1, 10):
        universe = set(range(1, n + 1))
        sets = [{i} for i in range(1, n + 1)] + [set(universe)]
        costs = [Fraction(1, i) for i in range(1, n + 1)] + [1 + eps]
        chosen, _ = greedy_set_cover(universe, sets, costs)
        assert chosen == list(range(n - 1, -1, -1))
        assert sum(costs[j] for j in chosen) == harmonic(n)


def test_unweighted_two_rows_family():
    # two rows of 2^k - 1 elements; block i has 2^(i-1) columns
    for k in range(2, 7):
        width = 2**k - 1
        top = {(0, c) for c in range(width)}
        bottom = {(1, c) for c in range(width)}
        blocks, start = [], 0
        for i in range(1, k + 1):
            cols = range(start, start + 2 ** (i - 1))
            blocks.append({(r, c) for r in (0, 1) for c in cols})
            start += 2 ** (i - 1)
        sets = [top, bottom] + blocks
        chosen, _ = greedy_set_cover(top | bottom, sets)
        assert len(chosen) == k
        assert chosen == [2 + i for i in range(k - 1, -1, -1)]


def test_no_cover():
    with pytest.raises(ValueError):
        greedy_set_cover({1, 2, 3}, [{1}, {2}])


def test_empty_universe():
    assert greedy_set_cover(set(), [{1}]) == ([], {})
