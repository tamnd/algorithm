# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mst-preorder-walk-tsp/. The authors are listed in prov/98SJR0.jsonl.

import itertools
import random
from fractions import Fraction

from mst_preorder_walk_tsp import mst_preorder_tour, prim_parents, tour_cost

POINTS = [(5, 1), (6, 5), (0, 0), (8, 0), (5, 4), (0, 4), (3, 0)]


def manhattan(points):
    return [[abs(p[0] - q[0]) + abs(p[1] - q[1]) for q in points] for p in points]


def brute_force_opt(cost):
    n = len(cost)
    if n <= 1:
        return 0
    return min(tour_cost(cost, [0, *p]) for p in itertools.permutations(range(1, n)))


def tree_cost(cost, parent):
    return sum(cost[v][p] for v, p in enumerate(parent) if p >= 0)


def full_walk(parent, order, root):
    """The full walk of the tree: each edge down and later back up (the Euler circuit of the doubled tree)."""
    n = len(parent)
    children = [[] for _ in range(n)]
    for v in order:
        if parent[v] >= 0:
            children[parent[v]].append(v)
    walk, stack = [root], [(root, 0)]
    while stack:
        v, i = stack.pop()
        if i < len(children[v]):
            stack.append((v, i + 1))
            w = children[v][i]
            walk.append(w)
            stack.append((w, 0))
        elif stack:
            walk.append(stack[-1][0])
    return walk


def shortcut(walk):
    seen, out = set(), []
    for v in walk:
        if v not in seen:
            seen.add(v)
            out.append(v)
    return out


def random_metric(rng):
    n = rng.randrange(1, 8)
    if rng.random() < 0.5:
        return manhattan([(rng.randrange(10), rng.randrange(10)) for _ in range(n)])
    c = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            c[i][j] = c[j][i] = rng.choice((1, 2))
    return c


def test_example() -> None:
    cost = manhattan(POINTS)
    parent, order = prim_parents(cost)
    assert tree_cost(cost, parent) == 19
    assert "".join("ABCDEFG"[v] for v in order) == "AEBGCDF"
    walk = full_walk(parent, order, 0)
    assert "".join("ABCDEFG"[v] for v in walk) == "AEBEAGCFCGADA"
    tour = mst_preorder_tour(cost)
    assert "".join("ABCDEFG"[v] for v in tour) == "AEBGCFD"
    assert tour_cost(cost, tour) == 36
    assert brute_force_opt(cost) == 28


def test_edges() -> None:
    assert mst_preorder_tour([]) == []
    assert mst_preorder_tour([[0]]) == [0]
    assert mst_preorder_tour([[0, 4], [4, 0]]) == [0, 1]
    # A path-shaped tree of 1500 vertices: no recursion limit is hit.
    n = 1500
    line = [[abs(i - j) for j in range(n)] for i in range(n)]
    assert mst_preorder_tour(line) == list(range(n))


def test_against_brute_force() -> None:
    rng = random.Random(7)
    for _ in range(600):
        cost = random_metric(rng)
        n = len(cost)
        tour = mst_preorder_tour(cost)
        assert sorted(tour) == list(range(n))
        parent, order = prim_parents(cost)
        assert tour == shortcut(full_walk(parent, order, 0))
        opt = brute_force_opt(cost)
        mst = tree_cost(cost, parent)
        alg = tour_cost(cost, tour)
        assert mst <= opt <= alg <= 2 * mst
        if n >= 1:
            assert alg * n <= 2 * (n - 1) * opt


def test_tight_example() -> None:
    for k in (5, 7, 9):
        n = k + 1
        c = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                rim = i > 0 and (j - i) % k in (2, k - 2)
                c[i][j] = c[j][i] = 1 if i == 0 or rim else 2
        tour = mst_preorder_tour(c)
        assert tour == list(range(n))
        assert tour_cost(c, tour) == 2 * k
        if k <= 7:
            assert brute_force_opt(c) == n
        assert Fraction(tour_cost(c, tour), n) == 2 - Fraction(2, n)
