# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/set-cover-primal-dual/. The authors are listed in prov/24X7Z1.jsonl.

import random
from fractions import Fraction
from itertools import combinations, product

import pytest

from set_cover_primal_dual import set_cover_primal_dual


def brute_opt(universe, sets, costs):
    best = None
    for r in range(len(sets) + 1):
        for c in combinations(range(len(sets)), r):
            if set().union(*[sets[i] for i in c]) >= set(universe):
                v = sum(costs[i] for i in c)
                if best is None or v < best:
                    best = v
    return best


def solve_square(a, b):
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
    """Exact LP optimum by enumeration of vertices. For tiny instances only."""
    m = len(sets)
    rows = [([1 if e in s else 0 for s in sets], 1) for e in universe]
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


def check_run(universe, sets, costs):
    chosen, y = set_cover_primal_dual(universe, sets, costs)
    assert set().union(*[sets[j] for j in chosen]) >= set(universe)
    # y is dual feasible and each chosen set is tight
    for j, s in enumerate(sets):
        load = sum(y[e] for e in s if e in y)
        assert load <= costs[j]
        if j in chosen:
            assert load == costs[j]
    assert all(v >= 0 for v in y.values())
    f = max(sum(1 for s in sets if e in s) for e in universe)
    alg = sum(costs[j] for j in chosen)
    assert alg <= f * sum(y.values())
    return chosen, y, alg, f


def test_example_page():
    universe = list(range(1, 8))
    sets = [{1, 2, 3, 5}, {3, 4, 6, 7}, {2, 5, 6}, {3, 7}, {1, 2, 4, 7}]
    costs = [3, 4, 4, 2, 1]
    chosen, y, alg, f = check_run(universe, sets, costs)
    assert chosen == [4, 0, 3, 1]
    assert alg == 10 and f == 3
    assert {e: v for e, v in y.items() if v} == {1: 1, 3: 2, 6: 2}
    assert lp_value(universe, sets, costs) == 6
    assert brute_opt(universe, sets, costs) == 7


def test_random_against_brute_force_and_lp():
    rng = random.Random(1981)
    for trial in range(150):
        n, m = rng.randint(1, 7), rng.randint(1, 5)
        universe = list(range(n))
        sets = [set(e for e in universe if rng.random() < 0.45) for _ in range(m)]
        if set().union(*sets) != set(universe):
            continue
        costs = [rng.randint(0, 5) for _ in range(m)]
        chosen, y, alg, f = check_run(universe, sets, costs)
        opt = brute_opt(universe, sets, costs)
        lp = lp_value(universe, sets, costs)
        assert sum(y.values()) <= lp <= opt
        assert alg <= f * opt


def test_vertex_cover_case_is_two_approximation():
    rng = random.Random(1985)
    for trial in range(100):
        nv = rng.randint(2, 7)
        edges = [e for e in combinations(range(nv), 2) if rng.random() < 0.5]
        if not edges:
            continue
        sets = [{e for e in edges if v in e} for v in range(nv)]
        w = [rng.randint(1, 6) for _ in range(nv)]
        chosen, y, alg, f = check_run(edges, sets, w)
        assert f <= 2
        assert alg <= 2 * brute_opt(edges, sets, w)


def test_tight_family_complete_f_partite():
    # parts V_1..V_f of size k; elements are the f-tuples; set (i, v) holds the tuples with v in place i
    for f, k in [(2, 2), (2, 4), (3, 2), (3, 3), (4, 2)]:
        universe = list(product(range(k), repeat=f))
        sets = [{t for t in universe if t[i] == v} for i in range(f) for v in range(k)]
        costs = [1] * len(sets)
        chosen, y, alg, ff = check_run(universe, sets, costs)
        assert ff == f
        assert alg == f * k
        assert brute_opt(universe, sets, costs) == k


def test_uncoverable_element():
    with pytest.raises(ValueError):
        set_cover_primal_dual([1, 2], [{1}], [1])
