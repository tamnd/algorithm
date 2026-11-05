# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gomory-hu-tree/. The authors are listed in prov/85Y2JY.jsonl.

import random
from fractions import Fraction
from itertools import combinations

import pytest

from gomory_hu_tree import GomoryHuTree

P, Q, R, S, U, V = range(6)
SIX = [(P, Q, 1), (P, R, 7), (Q, R, 1), (Q, S, 3), (Q, U, 2), (R, U, 4), (S, U, 1), (S, V, 6), (U, V, 2)]


def cut_value(edges, side):
    return sum(w for u, v, w in edges if (u in side) != (v in side))


def lam_brute(n, edges, a, b):
    """Oracle: the least cut over all vertex sets holding a and not b."""
    others = [v for v in range(n) if v not in (a, b)]
    best = None
    for k in range(len(others) + 1):
        for extra in combinations(others, k):
            c = cut_value(edges, {a, *extra})
            best = c if best is None else min(best, c)
    return best


def check(n, edges, tree):
    assert len(tree.edges()) == max(n - 1, 0)
    for a, b in combinations(range(n), 2):
        lam = lam_brute(n, edges, a, b)
        assert tree.min_cut_value(a, b) == lam
        assert tree.min_cut_value(b, a) == lam
        value, side = tree.min_cut(a, b)
        assert value == lam
        assert a in side and b not in side
        assert cut_value(edges, set(side)) == lam
    if n >= 2:
        value, side = tree.global_min_cut()
        assert 0 < len(side) < n
        assert cut_value(edges, set(side)) == value
        assert value == min(lam_brute(n, edges, a, b) for a, b in combinations(range(n), 2))


def test_six_vertex_example() -> None:
    tree = GomoryHuTree(6, SIX)
    assert tree.parent == [-1, U, P, Q, R, S]
    assert tree.weight[1:] == [7, 8, 6, 6, 8]
    assert tree.edges() == [(P, R, 8), (Q, S, 6), (Q, U, 7), (R, U, 6), (S, V, 8)]
    assert tree.min_cut_value(R, U) == 6
    assert tree.min_cut(R, U) == (6, [P, R])
    assert tree.global_min_cut() == (6, [S, V])
    check(6, SIX, tree)


def test_tiny() -> None:
    assert GomoryHuTree(0, []).edges() == []
    assert GomoryHuTree(1, [(0, 0, 5)]).global_min_cut() is None
    tree = GomoryHuTree(2, [(0, 1, 3), (1, 0, 2)])
    assert tree.edges() == [(0, 1, 5)]
    with pytest.raises(ValueError):
        tree.min_cut_value(1, 1)


def test_disconnected_and_zero_weight() -> None:
    edges = [(0, 1, 4), (2, 3, 0), (3, 4, 2)]
    tree = GomoryHuTree(5, edges)
    check(5, edges, tree)
    assert tree.min_cut_value(0, 3) == 0
    assert tree.min_cut_value(2, 3) == 0
    assert tree.global_min_cut()[0] == 0


def test_running_network_undirected() -> None:
    s, a, b, c, d, t = range(6)
    edges = [(s, a, 10), (s, c, 10), (a, b, 4), (a, c, 2), (a, d, 8), (c, d, 9), (d, b, 6), (b, t, 10), (d, t, 10)]
    tree = GomoryHuTree(6, edges)
    check(6, edges, tree)
    assert sorted(w for _, _, w in tree.edges()) == [20, 20, 20, 21, 21]


def test_fractions_and_floats() -> None:
    edges = [(0, 1, Fraction(1, 3)), (1, 2, Fraction(1, 2)), (0, 2, Fraction(1, 6))]
    check(3, edges, GomoryHuTree(3, edges))
    tree = GomoryHuTree(3, [(0, 1, 0.5), (1, 2, 0.25), (0, 2, 0.25)])
    assert sorted(w for _, _, w in tree.edges()) == [0.5, 0.75]


def test_errors() -> None:
    with pytest.raises(ValueError):
        GomoryHuTree(2, [(0, 1, -1)])
    with pytest.raises(ValueError):
        GomoryHuTree(2, [(0, 2, 1)])


def test_random_against_brute_force() -> None:
    rng = random.Random(8181)
    for _ in range(600):
        n = rng.randint(2, 7)
        edges = []
        for _ in range(rng.randint(0, 14)):
            edges.append((rng.randrange(n), rng.randrange(n), rng.choice([0, 1, 2, 3, 5, 8])))
        check(n, edges, GomoryHuTree(n, edges))


def test_parent_array_is_a_tree_rooted_at_0() -> None:
    rng = random.Random(31)
    for _ in range(100):
        n = rng.randint(1, 8)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(0, 4)) for _ in range(10)]
        tree = GomoryHuTree(n, edges)
        for v in range(1, n):
            x, steps = v, 0
            while x != 0:
                x = tree.parent[x]
                steps += 1
                assert steps < n
            assert tree.depth[v] == steps
