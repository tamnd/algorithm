# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/even-tarjan-vertex-connectivity/. The authors are listed in prov/NX705H.jsonl.

import itertools
import random

from even_tarjan_vertex_connectivity import local_connectivity, vertex_connectivity


def connected(n: int, edges: list[tuple[int, int]], removed: set[int]) -> bool:
    left = [v for v in range(n) if v not in removed]
    if len(left) <= 1:
        return True
    seen = {left[0]}
    stack = [left[0]]
    while stack:
        a = stack.pop()
        for u, v in edges:
            for x, y in ((u, v), (v, u)):
                if x == a and y not in removed and y not in seen:
                    seen.add(y)
                    stack.append(y)
    return len(seen) == len(left)


def brute(n: int, edges: list[tuple[int, int]]) -> int:
    """The least |X| with G - X disconnected (and at least 2 vertices left), else n - 1."""
    for size in range(n - 1):
        for x in itertools.combinations(range(n), size):
            if not connected(n, edges, set(x)):
                return size
    return n - 1


def two_k4() -> list[tuple[int, int]]:
    edges = [(a, b) for a in range(4) for b in range(a + 1, 4)]
    edges += [(a + 4, b + 4) for a, b in edges]
    return edges + [(3, 4), (3, 5)]


def test_example() -> None:
    assert vertex_connectivity(8, two_k4()) == 1
    nb = [set() for _ in range(8)]
    for u, v in two_k4():
        nb[u].add(v)
        nb[v].add(u)
    assert local_connectivity(nb, 0, 4, 7) == 1
    assert local_connectivity(nb, 4, 6, 7) == 3


def test_page_example() -> None:
    # The page names the vertices 1 .. 8; here they are 0 .. 7.
    edges = [(0, 1), (0, 1), (7, 7)]
    edges += [(h, x) for h in (0, 1) for x in range(2, 8)]
    edges += [(2, 3), (3, 4), (4, 2), (5, 6), (6, 7), (7, 5)]
    assert len(edges) == 21
    assert vertex_connectivity(8, edges) == 2
    nb = [set() for _ in range(8)]
    for u, v in edges:
        if u != v:
            nb[u].add(v)
            nb[v].add(u)
    assert [local_connectivity(nb, 2, j, 7) for j in (5, 6, 7)] == [2, 2, 2]


def test_known_graphs() -> None:
    cycle = [(i, (i + 1) % 6) for i in range(6)]
    assert vertex_connectivity(6, cycle) == 2
    k5 = [(a, b) for a in range(5) for b in range(a + 1, 5)]
    assert vertex_connectivity(5, k5) == 4
    k23 = [(a, b) for a in range(2) for b in range(2, 5)]
    assert vertex_connectivity(5, k23) == 2
    outer = [(i, (i + 1) % 5) for i in range(5)]
    spokes = [(i, i + 5) for i in range(5)]
    inner = [(5 + i, 5 + (i + 2) % 5) for i in range(5)]
    assert vertex_connectivity(10, outer + spokes + inner) == 3  # Petersen
    cube = [(a, a ^ (1 << b)) for a in range(8) for b in range(3) if a < a ^ (1 << b)]
    assert vertex_connectivity(8, cube) == 3


def test_edges() -> None:
    assert vertex_connectivity(1, []) == 0
    assert vertex_connectivity(1, [(0, 0)]) == 0
    assert vertex_connectivity(2, []) == 0
    assert vertex_connectivity(2, [(0, 1), (0, 1), (1, 0)]) == 1  # K2, parallel edges
    assert vertex_connectivity(3, [(0, 1), (0, 1), (1, 2), (2, 2)]) == 1
    assert vertex_connectivity(4, [(0, 1), (2, 3)]) == 0
    assert vertex_connectivity(4, [(0, 1), (1, 2), (2, 0)]) == 0  # isolated vertex 3


def test_long_path() -> None:
    n = 20000
    nb = [set() for _ in range(n)]
    for v in range(n - 1):
        nb[v].add(v + 1)
        nb[v + 1].add(v)
    assert local_connectivity(nb, 0, n - 1, n) == 1
    ring = [(v, (v + 1) % n) for v in range(n)]
    nb2 = [set() for _ in range(n)]
    for u, v in ring:
        nb2[u].add(v)
        nb2[v].add(u)
    assert local_connectivity(nb2, 0, n // 2, n) == 2
    m = 400  # the first pass runs m - 2 flows from vertex 0, so the time is quadratic
    assert vertex_connectivity(m, [(v, v + 1) for v in range(m - 1)]) == 1


def test_random() -> None:
    rng = random.Random(1975)
    for _ in range(700):
        n = rng.randint(1, 7)
        p = rng.random()
        edges = [(a, b) for a in range(n) for b in range(a + 1, n) if rng.random() < p]
        edges += [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(0, 3))]
        assert vertex_connectivity(n, edges) == brute(n, edges)
