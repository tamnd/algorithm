# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incremental-topological-ordering/. The authors are listed in prov/D5SS95.jsonl.

import random

from incremental_topological_ordering import IncrementalTopologicalOrder


def _reaches(n: int, edges: list[tuple[int, int]], s: int, t: int) -> bool:
    adj: list[list[int]] = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
    seen = {s}
    st = [s]
    while st:
        x = st.pop()
        if x == t:
            return True
        for y in adj[x]:
            if y not in seen:
                seen.add(y)
                st.append(y)
    return False


def _valid(g: IncrementalTopologicalOrder, edges) -> None:
    order = g.order()
    assert sorted(order) == list(range(g.n))
    for i, x in enumerate(order):
        assert g.pos[x] == i
    for a, b in edges:
        assert g.pos[a] < g.pos[b]


def test_example() -> None:
    g = IncrementalTopologicalOrder(6)
    for e in [(0, 1), (1, 2), (4, 5), (5, 1)]:
        assert g.add_edge(*e)
    assert g.order() == [0, 4, 5, 3, 1, 2]
    assert g.add_edge(3, 4)
    assert g.order() == [0, 3, 4, 5, 1, 2]
    assert not g.add_edge(2, 3)
    assert g.order() == [0, 3, 4, 5, 1, 2]


def test_random_against_static() -> None:
    rng = random.Random(9)
    for _ in range(500):
        n = rng.randint(1, 9)
        g = IncrementalTopologicalOrder(n)
        edges: list[tuple[int, int]] = []
        for _ in range(rng.randint(0, 30)):
            u, v = rng.randrange(n), rng.randrange(n)
            expect = u != v and not _reaches(n, edges, v, u)
            assert g.add_edge(u, v) == expect
            if expect:
                edges.append((u, v))
            _valid(g, edges)


def test_reversed_chain() -> None:
    n = 1000
    g = IncrementalTopologicalOrder(n)
    edges = [(i + 1, i) for i in range(n - 1)]
    for e in edges:
        assert g.add_edge(*e)
    assert g.order() == list(range(n - 1, -1, -1))
    assert not g.add_edge(0, n - 1)
