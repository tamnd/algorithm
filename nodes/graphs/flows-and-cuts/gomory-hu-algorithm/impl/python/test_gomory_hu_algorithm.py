# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gomory-hu-algorithm/. The authors are listed in prov/PSCBG5.jsonl.

import random
from fractions import Fraction
from itertools import combinations

import pytest

from gomory_hu_algorithm import gomory_hu_algorithm

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


def path_min(n, tree, a, b):
    """Least weight on the tree path from a to b, and the tree edge achieving it."""
    adj = [[] for _ in range(n)]
    for i, (x, y, w) in enumerate(tree):
        adj[x].append((y, w, i))
        adj[y].append((x, w, i))
    stack = [(a, -1, None, None)]
    while stack:
        v, par, best, arg = stack.pop()
        if v == b:
            return best, arg
        for y, w, i in adj[v]:
            if y != par:
                if best is None or w < best:
                    stack.append((y, v, w, i))
                else:
                    stack.append((y, v, best, arg))
    raise AssertionError("tree is not connected")


def side_without(n, tree, i, a):
    """Vertices on the side of a after deleting tree edge i."""
    adj = [[] for _ in range(n)]
    for j, (x, y, _) in enumerate(tree):
        if j != i:
            adj[x].append(y)
            adj[y].append(x)
    seen = {a}
    stack = [a]
    while stack:
        v = stack.pop()
        for y in adj[v]:
            if y not in seen:
                seen.add(y)
                stack.append(y)
    return seen


def check(n, edges, tree):
    assert len(tree) == n - 1
    for a, b in combinations(range(n), 2):
        lam, i = path_min(n, tree, a, b)
        assert lam == lam_brute(n, edges, a, b)
        side = side_without(n, tree, i, a)
        assert b not in side
        assert cut_value(edges, side) == lam


def test_six_vertex_example() -> None:
    log = []
    tree = gomory_hu_algorithm(6, SIX, lambda s, t, lam, xs, xt: log.append((s, t, lam, xs, xt)))
    assert log == [
        (P, Q, 6, [P, R], [Q, S, U, V]),
        (P, R, 8, [P], [R]),
        (Q, S, 6, [Q, U], [S, V]),
        (Q, U, 7, [Q], [U]),
        (S, V, 8, [S], [V]),
    ]
    assert tree == [(P, R, 8), (Q, U, 7), (R, U, 6), (S, U, 6), (S, V, 8)]
    check(6, SIX, tree)


def test_tiny() -> None:
    assert gomory_hu_algorithm(0, []) == []
    assert gomory_hu_algorithm(1, [(0, 0, 5)]) == []
    assert gomory_hu_algorithm(2, [(0, 1, 3), (1, 0, 2)]) == [(0, 1, 5)]


def test_disconnected_and_zero_weight() -> None:
    edges = [(0, 1, 4), (2, 3, 0), (3, 4, 2)]
    tree = gomory_hu_algorithm(5, edges)
    check(5, edges, tree)
    assert path_min(5, tree, 0, 3)[0] == 0
    assert path_min(5, tree, 2, 3)[0] == 0


def test_no_edges() -> None:
    tree = gomory_hu_algorithm(4, [])
    assert [w for _, _, w in tree] == [0, 0, 0]


def test_running_network_undirected() -> None:
    s, a, b, c, d, t = range(6)
    edges = [(s, a, 10), (s, c, 10), (a, b, 4), (a, c, 2), (a, d, 8), (c, d, 9), (d, b, 6), (b, t, 10), (d, t, 10)]
    tree = gomory_hu_algorithm(6, edges)
    check(6, edges, tree)
    assert sorted(w for _, _, w in tree) == [20, 20, 20, 21, 21]


def test_fractions_and_floats() -> None:
    edges = [(0, 1, Fraction(1, 3)), (1, 2, Fraction(1, 2)), (0, 2, Fraction(1, 6))]
    tree = gomory_hu_algorithm(3, edges)
    check(3, edges, tree)
    tree = gomory_hu_algorithm(3, [(0, 1, 0.5), (1, 2, 0.25), (0, 2, 0.25)])
    assert sorted(w for _, _, w in tree) == [0.5, 0.75]


def test_parallel_edges() -> None:
    edges = [(0, 1, 1), (0, 1, 2), (1, 2, 1)]
    tree = gomory_hu_algorithm(3, edges)
    check(3, edges, tree)


def test_errors() -> None:
    with pytest.raises(ValueError):
        gomory_hu_algorithm(2, [(0, 1, -1)])
    with pytest.raises(ValueError):
        gomory_hu_algorithm(2, [(0, 2, 1)])


def test_random_against_brute_force() -> None:
    rng = random.Random(4242)
    for _ in range(600):
        n = rng.randint(2, 7)
        edges = []
        for _ in range(rng.randint(0, 14)):
            u, v = rng.randrange(n), rng.randrange(n)
            edges.append((u, v, rng.choice([0, 1, 2, 3, 5, 8])))
        tree = gomory_hu_algorithm(n, edges)
        check(n, edges, tree)


def test_at_most_n_minus_1_distinct_values() -> None:
    rng = random.Random(77)
    for _ in range(50):
        n = rng.randint(2, 7)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(0, 9)) for _ in range(12)]
        values = {lam_brute(n, edges, a, b) for a, b in combinations(range(n), 2)}
        assert len(values) <= n - 1
