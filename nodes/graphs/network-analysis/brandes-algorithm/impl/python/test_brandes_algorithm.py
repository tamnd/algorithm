# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brandes-algorithm/. The authors are listed in prov/NYWQX3.jsonl.

import random
from fractions import Fraction

from brandes_algorithm import brandes_algorithm, brandes_weighted


def undirected(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def oracle(n: int, arcs: dict[tuple[int, int], int], undirected_graph: bool) -> list[Fraction]:
    """Betweenness by listing every simple path between every ordered pair."""
    out: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for (u, v), length in arcs.items():
        out[u].append((v, length))
    b = [Fraction(0)] * n
    for s in range(n):
        paths: dict[int, list[tuple[int, list[int]]]] = {}
        todo: list[tuple[int, int, list[int]]] = [(s, 0, [s])]
        while todo:
            u, d, p = todo.pop()
            if u != s:
                paths.setdefault(u, []).append((d, p))
            for v, length in out[u]:
                if v not in p:
                    todo.append((v, d + length, p + [v]))
        for t, lst in paths.items():
            best = min(d for d, _ in lst)
            short = [p for d, p in lst if d == best]
            for p in short:
                for x in p[1:-1]:
                    b[x] += Fraction(1, len(short))
    if undirected_graph:
        b = [x / 2 for x in b]
    return b


def close(a: list[float], b: list[Fraction]) -> bool:
    return len(a) == len(b) and all(abs(x - float(y)) < 1e-9 for x, y in zip(a, b))


EXAMPLE = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (4, 6), (5, 6)]


def test_example() -> None:
    assert close(brandes_algorithm(undirected(7, EXAMPLE)), [Fraction(x) for x in [0, 2, 2, 9, 8, 0, 0]])


def test_edges() -> None:
    assert brandes_algorithm([]) == []
    assert brandes_algorithm([[]]) == [0.0]
    assert brandes_algorithm(undirected(3, [(0, 1), (1, 2)])) == [0.0, 1.0, 0.0]
    star = undirected(5, [(0, v) for v in range(1, 5)])
    assert brandes_algorithm(star) == [6.0, 0.0, 0.0, 0.0, 0.0]
    c4 = undirected(4, [(0, 1), (1, 2), (2, 3), (3, 0)])
    assert brandes_algorithm(c4) == [0.5, 0.5, 0.5, 0.5]
    # directed path 0 -> 1 -> 2 and a separate vertex 3
    assert brandes_algorithm([[1], [2], [], []], undirected=False) == [0.0, 1.0, 0.0, 0.0]


def test_weighted_example() -> None:
    # 0-1-2 by two edges of length 1 against the direct edge 0-2 of length 2: a tie
    adj: list[list[tuple[int, float]]] = [[(1, 1), (2, 2)], [(0, 1), (2, 1)], [(1, 1), (0, 2)]]
    assert brandes_weighted(adj) == [0.0, 0.5, 0.0]


def test_long_path_no_recursion() -> None:
    n = 400
    cb = brandes_algorithm(undirected(n, [(i, i + 1) for i in range(n - 1)]))
    assert all(cb[i] == i * (n - 1 - i) for i in range(n))


def test_random_against_oracle() -> None:
    rng = random.Random(90210)
    for _ in range(600):
        n = rng.randint(1, 7)
        directed = rng.random() < 0.5
        weighted = rng.random() < 0.5
        p = rng.random()
        arcs: dict[tuple[int, int], int] = {}
        for u in range(n):
            for v in range(n):
                if u == v or (not directed and v < u) or rng.random() >= p:
                    continue
                length = rng.randint(1, 3) if weighted else 1
                arcs[(u, v)] = length
                if not directed:
                    arcs[(v, u)] = length
        want = oracle(n, arcs, not directed)
        adj: list[list[int]] = [[] for _ in range(n)]
        adjw: list[list[tuple[int, float]]] = [[] for _ in range(n)]
        for (u, v), length in arcs.items():
            adj[u].append(v)
            adjw[u].append((v, length))
        for lst in adjw:
            rng.shuffle(lst)
        assert close(brandes_weighted(adjw, undirected=not directed), want)
        if not weighted:
            assert close(brandes_algorithm(adj, undirected=not directed), want)
