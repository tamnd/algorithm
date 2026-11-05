# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/euler-tour-tree/. The authors are listed in prov/TH5ZDM.jsonl.

import random

from euler_tour_tree import EulerTourForest


def _side(adj: dict[int, set[int]], v: int, p: int) -> set[int]:
    seen, stack = {v}, [v]
    while stack:
        x = stack.pop()
        for y in adj[x]:
            if y not in seen and not (x == v and y == p):
                seen.add(y)
                stack.append(y)
    return seen


def _comp(adj: dict[int, set[int]], v: int) -> set[int]:
    return _side(adj, v, -1)


def _is_tour(tour: list[tuple[int, int]], verts: set[int]) -> bool:
    """A cyclic sequence of arcs and loops is an Euler tour of a tree."""
    walk = [(u, v) for u, v in tour if u != v]
    loops = {u for u, v in tour if u == v}
    if loops != verts:
        return False
    for k in range(len(walk)):
        if walk[k][1] != walk[(k + 1) % len(walk)][0]:
            return False
    return True


def test_example() -> None:
    f = EulerTourForest(6, [1, 2, 3, 4, 5, 6])
    for u, v in [(0, 1), (1, 2), (1, 3), (3, 4)]:
        f.link(u, v)
    assert f.connected(0, 4) and not f.connected(0, 5)
    assert f.component_size(0) == 5 and f.component_sum(2) == 15
    assert f.subtree_sum(3, 1) == 9
    f.cut(1, 3)
    assert not f.connected(0, 4)
    assert f.component_size(0) == 3 and f.component_size(4) == 2
    f.link(4, 5)
    f.link(2, 5)
    assert f.connected(0, 3) and f.component_sum(0) == 21


def test_single_vertex() -> None:
    f = EulerTourForest(1, [7])
    assert f.connected(0, 0)
    assert f.component_size(0) == 1 and f.component_sum(0) == 7
    assert f.tour(0) == [(0, 0)]


def test_random_against_naive() -> None:
    rng = random.Random(4242)
    for trial in range(40):
        n = rng.randint(1, 12)
        vals = [rng.randint(-5, 9) for _ in range(n)]
        f = EulerTourForest(n, list(vals), seed=trial)
        adj: dict[int, set[int]] = {v: set() for v in range(n)}
        edges: set[tuple[int, int]] = set()
        for _ in range(150):
            op = rng.random()
            u, v = rng.randrange(n), rng.randrange(n)
            if op < 0.35 and u != v and v not in _comp(adj, u):
                f.link(u, v)
                adj[u].add(v)
                adj[v].add(u)
                edges.add((min(u, v), max(u, v)))
            elif op < 0.55 and edges:
                a, b = rng.choice(sorted(edges))
                if rng.random() < 0.5:
                    a, b = b, a
                f.cut(a, b)
                adj[a].discard(b)
                adj[b].discard(a)
                edges.discard((min(a, b), max(a, b)))
            elif op < 0.65:
                x = rng.randint(-5, 9)
                f.set_value(u, x)
                vals[u] = x
            elif op < 0.75:
                f.reroot(u)
            for w in range(n):
                c = _comp(adj, w)
                assert f.component_size(w) == len(c)
                assert f.component_sum(w) == sum(vals[x] for x in c)
                assert _is_tour(f.tour(w), c)
            assert f.connected(u, v) == (v in _comp(adj, u))
            for a, b in edges:
                assert f.subtree_sum(a, b) == sum(vals[x] for x in _side(adj, a, b))
                assert f.subtree_sum(b, a) == sum(vals[x] for x in _side(adj, b, a))


def test_long_path_no_recursion_error() -> None:
    n = 3000
    f = EulerTourForest(n, [1] * n)
    for v in range(n - 1):
        f.link(v, v + 1)
    assert f.component_size(0) == n
    assert f.subtree_sum(n // 2, n // 2 - 1) == n - n // 2
    f.cut(1000, 1001)
    assert f.component_size(0) == 1001 and f.component_size(n - 1) == n - 1001
