# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kou-markowsky-berman/. The authors are listed in prov/97ZJ4F.jsonl.

import itertools
import random

import pytest

from kou_markowsky_berman import kou_markowsky_berman

EXAMPLE = [(0, 1, 4), (0, 2, 3), (1, 2, 1), (1, 3, 2), (2, 3, 4), (2, 4, 5), (3, 4, 7), (3, 5, 6), (4, 5, 2)]


def find_root(parent, x):
    while parent[x] != x:
        x = parent[x]
    return x


def connects(n, edges, chosen, terms):
    parent = list(range(n))
    for i in chosen:
        parent[find_root(parent, edges[i][0])] = find_root(parent, edges[i][1])
    return len({find_root(parent, t) for t in terms}) <= 1


def is_tree(n, edges, chosen):
    parent = list(range(n))
    for i in chosen:
        a, b = find_root(parent, edges[i][0]), find_root(parent, edges[i][1])
        if a == b:
            return False
        parent[a] = b
    used = {x for i in chosen for x in edges[i][:2]}
    return len({find_root(parent, x) for x in used}) <= 1


def weight(edges, chosen):
    return sum(edges[i][2] for i in chosen)


def optimum(n, edges, terms):
    """Least weight of an edge set that connects the terminals, or None."""
    best = None
    for r in range(len(edges) + 1):
        for sub in itertools.combinations(range(len(edges)), r):
            if connects(n, edges, sub, terms):
                w = weight(edges, sub)
                if best is None or w < best:
                    best = w
    return best


def check(n, edges, terms):
    got = kou_markowsky_berman(n, edges, terms)
    opt = optimum(n, edges, terms)
    if opt is None:
        assert got is None
        return
    s = len(set(terms))
    assert got is not None and is_tree(n, edges, got)
    assert connects(n, edges, got, terms)
    for x in {x for i in got for x in edges[i][:2]}:
        if sum(x in edges[i][:2] for i in got) == 1:
            assert x in terms
    w = weight(edges, got)
    assert opt <= w
    if s >= 2:
        assert w * s <= 2 * (s - 1) * opt


def test_example():
    assert kou_markowsky_berman(6, EXAMPLE, [0, 1, 4]) == [0, 2, 5]
    assert weight(EXAMPLE, [0, 2, 5]) == 10
    assert optimum(6, EXAMPLE, [0, 1, 4]) == 9


def test_example_optimal_case():
    got = kou_markowsky_berman(6, EXAMPLE, [0, 3, 5])
    assert weight(EXAMPLE, got) == 12 == optimum(6, EXAMPLE, [0, 3, 5])


def test_all_vertices_terminal_gives_mst():
    got = kou_markowsky_berman(6, EXAMPLE, list(range(6)))
    assert weight(EXAMPLE, got) == 13


def test_star_lower_bound():
    # Hub 0, terminals 1 .. 4 with spokes 1 and a path of edges of weight 1.9.
    edges = [(0, t, 1) for t in range(1, 5)] + [(1, 2, 1.9), (2, 3, 1.9), (3, 4, 1.9)]
    got = kou_markowsky_berman(5, edges, [1, 2, 3, 4])
    assert got == [4, 5, 6]
    assert abs(weight(edges, got) - 5.7) < 1e-9


def test_small_cases():
    assert kou_markowsky_berman(3, [(0, 1, 1)], []) == []
    assert kou_markowsky_berman(3, [(0, 1, 1)], [2]) == []
    assert kou_markowsky_berman(3, [(0, 1, 1)], [1, 1, 0]) == [0]
    assert kou_markowsky_berman(3, [(0, 1, 1)], [0, 2]) is None


def test_zero_weights_parallel_edges_and_loops():
    edges = [(0, 1, 0), (0, 1, 0), (1, 1, 0), (1, 2, 3), (0, 2, 3)]
    got = kou_markowsky_berman(3, edges, [0, 1, 2])
    assert weight(edges, got) == 3 and is_tree(3, edges, got)


def test_negative_weight_rejected():
    with pytest.raises(ValueError):
        kou_markowsky_berman(2, [(0, 1, -1)], [0, 1])


def test_random_against_brute_force():
    rng = random.Random(20261105)
    for trial in range(600):
        n = rng.randint(1, 6)
        m = rng.randint(0, 9)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(0, 5)) for _ in range(m)]
        terms = rng.sample(range(n), rng.randint(0, n))
        check(n, edges, terms)


def test_random_connected_larger():
    rng = random.Random(5)
    for _ in range(60):
        n = rng.randint(4, 8)
        edges = [(v, rng.randrange(v), rng.randint(1, 9)) for v in range(1, n)]
        edges += [(rng.randrange(n), rng.randrange(n), rng.randint(1, 9)) for _ in range(rng.randint(0, 4))]
        terms = rng.sample(range(n), rng.randint(2, n))
        check(n, edges, terms)
