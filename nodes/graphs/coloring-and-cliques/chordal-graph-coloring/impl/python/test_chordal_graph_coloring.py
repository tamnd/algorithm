# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chordal-graph-coloring/. The authors are listed in prov/JWQZ4N.jsonl.

import itertools
import random

from chordal_graph_coloring import chordal_graph_coloring, mcs_order


def make(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def proper(adj: list[list[int]], c: list[int]) -> bool:
    return all(c[u] != c[v] for u in range(len(adj)) for v in adj[u])


def chi(adj: list[list[int]]) -> int:
    n = len(adj)
    for k in range(n + 1):
        for col in itertools.product(range(k), repeat=n):
            if proper(adj, list(col)):
                return k
    return n


def chordal_brute(adj: list[list[int]]) -> bool:
    """No induced cycle of length >= 4: no vertex set of size >= 4 inducing a connected 2-regular graph."""
    n = len(adj)
    nb = [set(a) for a in adj]
    for r in range(4, n + 1):
        for s in itertools.combinations(range(n), r):
            ss = set(s)
            if all(len(nb[v] & ss) == 2 for v in s):
                seen = {s[0]}
                stack = [s[0]]
                while stack:
                    u = stack.pop()
                    for w in nb[u] & ss:
                        if w not in seen:
                            seen.add(w)
                            stack.append(w)
                if len(seen) == r:
                    return False
    return True


def random_chordal(rng: random.Random, n: int) -> list[tuple[int, int]]:
    """Add vertices one at a time, each adjacent to a clique of the earlier ones."""
    edges: list[tuple[int, int]] = []
    nb: list[set[int]] = []
    for v in range(n):
        cand = [u for u in range(v) if rng.random() < 0.6]
        rng.shuffle(cand)
        clique: list[int] = []
        for u in cand:
            if all(u in nb[x] for x in clique):
                clique.append(u)
        nb.append(set(clique))
        for u in clique:
            nb[u].add(v)
            edges.append((u, v))
    perm = list(range(n))
    rng.shuffle(perm)
    return [(perm[u], perm[v]) for u, v in edges]


def test_example() -> None:
    edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5), (2, 6), (3, 6), (4, 6)]
    adj = make(7, edges)
    assert mcs_order(adj) == [6, 4, 3, 2, 1, 0, 5]
    assert chordal_graph_coloring(adj) == [2, 1, 4, 3, 2, 1, 1]
    assert chordal_graph_coloring(make(7, edges[:9] + [(0, 6), (5, 6)])) is None


def test_edges() -> None:
    assert chordal_graph_coloring([]) == []
    assert chordal_graph_coloring([[]]) == [1]
    assert chordal_graph_coloring(make(3, [])) == [1, 1, 1]
    for n in range(1, 8):
        c = chordal_graph_coloring(make(n, list(itertools.combinations(range(n), 2))))
        assert c is not None and sorted(c) == list(range(1, n + 1))
    assert chordal_graph_coloring(make(3, [(0, 1), (1, 2), (2, 0)])) is not None
    for n in range(4, 10):
        assert chordal_graph_coloring(make(n, [(i, (i + 1) % n) for i in range(n)])) is None
    path = make(6, [(i, i + 1) for i in range(5)])
    assert max(chordal_graph_coloring(path) or [0]) == 2
    assert chordal_graph_coloring(make(4, [(0, 2), (0, 3), (1, 2), (1, 3)])) is None


def test_random_chordal_optimal() -> None:
    rng = random.Random(17)
    for _ in range(500):
        n = rng.randrange(0, 8)
        adj = make(n, random_chordal(rng, n))
        c = chordal_graph_coloring(adj)
        assert c is not None
        assert proper(adj, c)
        assert max(c, default=0) == chi(adj)


def test_random_against_brute_force() -> None:
    rng = random.Random(23)
    for _ in range(700):
        n = rng.randrange(0, 8)
        p = rng.random()
        edges = [e for e in itertools.combinations(range(n), 2) if rng.random() < p]
        adj = make(n, edges)
        c = chordal_graph_coloring(adj)
        assert (c is not None) == chordal_brute(adj)
        if c is not None:
            assert proper(adj, c)
            assert max(c, default=0) == chi(adj)
