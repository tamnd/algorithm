# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tree-structured-csp/. The authors are listed in prov/G0H16E.jsonl.

import itertools
import random

import pytest

from tree_structured_csp import count_tree, directed, solve_tree


def solutions(domains, cons):
    rel = directed(cons)
    return [t for t in itertools.product(*[sorted(d) for d in domains])
            if all((t[i], t[j]) in r for (i, j), r in rel.items())]


def random_forest_csp(rng: random.Random, n: int, d: int, tight: float):
    labels = list(range(n))
    rng.shuffle(labels)
    cons = {}
    for v in range(1, n):
        if rng.random() < 0.85:
            p = rng.randrange(v)
            i, j = labels[p], labels[v]
            if rng.random() < 0.5:
                i, j = j, i
            cons[(i, j)] = {(a, b) for a in range(d) for b in range(d) if rng.random() > tight}
    domains = [{a for a in range(d) if rng.random() > 0.15} for _ in range(n)]
    return domains, cons


def test_example() -> None:
    lt = {(a, b) for a in range(1, 4) for b in range(1, 4) if a < b}
    ne = {(a, b) for a in range(1, 4) for b in range(1, 4) if a != b}
    # A=0, B=1, C=2, D=3, E=4; tree edges A-B, A-C, B-D, C-E
    cons = {(0, 1): lt, (0, 2): ne, (3, 1): lt, (4, 2): lt}
    doms = [{1, 2, 3}] * 5
    assert solve_tree(doms, cons) == [1, 2, 2, 1, 1]
    assert count_tree(doms, cons) == len(solutions(doms, cons)) == 13


def test_edges() -> None:
    assert solve_tree([], {}) == []
    assert count_tree([], {}) == 1
    assert solve_tree([{4}], {}) == [4]
    assert solve_tree([set(), {1}], {}) is None
    assert count_tree([set(), {1}], {}) == 0
    assert count_tree([{0, 1}, {0, 1, 2}], {}) == 6
    assert solve_tree([{0}, {0}], {(0, 1): {(0, 1)}}) is None


def test_cycle_is_rejected() -> None:
    ne = {(0, 1), (1, 0)}
    with pytest.raises(ValueError):
        solve_tree([{0, 1}] * 3, {(0, 1): ne, (1, 2): ne, (2, 0): ne})


def test_random_against_brute_force() -> None:
    rng = random.Random(7)
    for _ in range(500):
        n, d = rng.randint(1, 7), rng.randint(1, 3)
        domains, cons = random_forest_csp(rng, n, d, rng.random() * 0.7)
        sols = solutions(domains, cons)
        got = solve_tree(domains, cons)
        if sols:
            assert got is not None and tuple(got) in set(sols)
        else:
            assert got is None
        assert count_tree(domains, cons) == len(sols)
