# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/seth-implies-ov-lower-bound/. The authors are listed in prov/CX4N6X.jsonl.

import random
from itertools import combinations, product

from seth_implies_ov_lower_bound import (
    assignment_to_pair,
    pair_to_assignment,
    sat_to_ov,
)


def satisfies(clauses, assignment):
    return all(any((lit > 0) == (assignment[abs(lit) - 1] == 1) for lit in c) for c in clauses)


def brute_sat(clauses, nvars):
    return [list(bits) for bits in product((0, 1), repeat=nvars) if satisfies(clauses, bits)]


def brute_ov(a_list, b_list):
    return [
        (i, j)
        for i, a in enumerate(a_list)
        for j, b in enumerate(b_list)
        if all(x * y == 0 for x, y in zip(a, b))
    ]


def check(clauses, nvars):
    a_list, b_list = sat_to_ov(clauses, nvars)
    assert len(a_list) == len(b_list) == 2 ** ((nvars + 1) // 2)
    assert all(len(v) == len(clauses) for v in a_list + b_list)
    sols = brute_sat(clauses, nvars)
    pairs = brute_ov(a_list, b_list)
    assert bool(sols) == bool(pairs)
    # Every orthogonal pair maps to a satisfying assignment.
    for i, j in pairs:
        assert satisfies(clauses, pair_to_assignment(nvars, i, j))
    # Every satisfying assignment maps to an orthogonal pair.
    pair_set = set(pairs)
    for s in sols:
        assert assignment_to_pair(nvars, s) in pair_set
    # For even N the two maps are inverse bijections.
    if nvars % 2 == 0:
        assert sorted(pair_to_assignment(nvars, i, j) for i, j in pairs) == sorted(sols)
    return a_list, b_list, pairs, sols


def test_page_example():
    f = [[1, 3], [-1, 2, -4], [-2, 4], [2, -3]]
    a_list, b_list, pairs, sols = check(f, 4)
    assert ["".join(map(str, v)) for v in a_list] == ["1001", "1010", "0101", "0010"]
    assert ["".join(map(str, v)) for v in b_list] == ["1010", "1100", "0011", "0101"]
    assert pairs == [(1, 3), (2, 0), (3, 1), (3, 3)]
    assert sols == [[0, 1, 1, 1], [1, 0, 0, 0], [1, 1, 0, 1], [1, 1, 1, 1]]
    f2 = f + [[-2, -4]]
    _, _, pairs2, sols2 = check(f2, 4)
    assert pairs2 == [(2, 0)]
    assert sols2 == [[1, 0, 0, 0]]


def test_edges():
    a_list, b_list, pairs, _ = check([], 2)
    assert a_list == [()] * 2 and pairs  # no clauses: every pair is orthogonal
    _, _, pairs, _ = check([[]], 2)
    assert pairs == []  # the empty clause is never satisfied
    check([[1]], 1)  # odd N uses the dummy variable
    check([[1], [-1]], 1)
    try:
        sat_to_ov([[3]], 2)
    except ValueError:
        pass
    else:
        raise AssertionError("a literal outside 1..N must be rejected")


def test_all_small_3cnf():
    # Every formula over x1, x2, x3 with 1 to 3 distinct clauses, each clause
    # a nonempty set of literals on distinct variables.
    clauses = []
    for signs in product((0, 1, -1), repeat=3):
        c = [s * (v + 1) for v, s in enumerate(signs) if s]
        if c:
            clauses.append(c)
    assert len(clauses) == 26
    count = 0
    for r in (1, 2, 3):
        for f in combinations(clauses, r):
            check(list(f), 3)
            count += 1
    assert count == 2951


def test_random_formulas():
    rng = random.Random(20261116)
    for _ in range(400):
        nvars = rng.randint(1, 9)
        m = rng.randint(1, 14)
        f = []
        for _ in range(m):
            width = rng.randint(1, min(4, nvars))
            vs = rng.sample(range(1, nvars + 1), width)
            f.append([v if rng.random() < 0.5 else -v for v in vs])
        check(f, nvars)
