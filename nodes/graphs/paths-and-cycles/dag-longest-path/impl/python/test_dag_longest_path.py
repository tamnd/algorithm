# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dag-longest-path/. The authors are listed in prov/K16C2B.jsonl.

import random

import pytest

from dag_longest_path import NEG_INF, dag_longest_path, longest_path_anywhere, path_to

EXAMPLE = [(0, 1, 3), (0, 2, 2), (1, 3, 4), (2, 3, 6), (2, 4, 1), (3, 5, 2), (4, 5, 5)]


def all_paths(n: int, edges: list[tuple[int, int, float]], s: int) -> list[tuple[float, list[int]]]:
    """Every path from s, with its weight, found by plain search. Exponential."""
    out: list[list[tuple[int, float]]] = [[] for _ in range(n)]
    for u, v, w in edges:
        out[u].append((v, w))
    result: list[tuple[float, list[int]]] = []
    todo: list[tuple[float, list[int]]] = [(0, [s])]
    while todo:
        weight, path = todo.pop()
        result.append((weight, path))
        for v, w in out[path[-1]]:
            assert v not in path  # the graph is acyclic
            todo.append((weight + w, path + [v]))
    return result


def random_dag(rng: random.Random, n: int, m: int) -> list[tuple[int, int, float]]:
    rank = list(range(n))
    rng.shuffle(rank)
    edges = []
    for _ in range(m):
        a, b = rng.sample(range(n), 2)
        if rank[a] > rank[b]:
            a, b = b, a
        edges.append((a, b, rng.randint(-5, 9)))
    return edges


def path_weight(edges: list[tuple[int, int, float]], path: list[int]) -> float:
    best: dict[tuple[int, int], float] = {}
    for u, v, w in edges:
        best[(u, v)] = max(best.get((u, v), NEG_INF), w)
    return sum(best[(path[i], path[i + 1])] for i in range(len(path) - 1))


def test_example() -> None:
    dist, parent = dag_longest_path(6, EXAMPLE, 0)
    assert dist == [0, 3, 2, 8, 3, 10]
    assert path_to(parent, 0, 5) == [0, 2, 3, 5]
    assert longest_path_anywhere(6, EXAMPLE) == (10, [0, 2, 3, 5])


def test_edge_cases() -> None:
    assert dag_longest_path(1, [], 0) == ([0], [None])
    # isolated and unreachable vertices keep -inf
    dist, _ = dag_longest_path(3, [(1, 2, 4)], 0)
    assert dist == [0, NEG_INF, NEG_INF]
    # parallel arcs: the heavier one counts
    assert dag_longest_path(2, [(0, 1, 1), (0, 1, 7)], 0)[0] == [0, 7]
    # negative weights are allowed
    assert dag_longest_path(3, [(0, 1, -2), (1, 2, -3), (0, 2, -9)], 0)[0] == [0, -2, -5]
    assert longest_path_anywhere(0, []) == (0, [])
    assert longest_path_anywhere(2, [(0, 1, -4)])[0] == 0


def test_cycles_rejected() -> None:
    with pytest.raises(ValueError):
        dag_longest_path(1, [(0, 0, 1)], 0)  # a self-loop
    with pytest.raises(ValueError):
        dag_longest_path(3, [(0, 1, 1), (1, 2, 1), (2, 1, 1)], 0)
    with pytest.raises(ValueError):
        longest_path_anywhere(2, [(0, 1, 1), (1, 0, 1)])


def test_long_path() -> None:
    n = 100_000
    edges = [(i, i + 1, 1) for i in range(n - 1)]
    dist, parent = dag_longest_path(n, edges, 0)
    assert dist[-1] == n - 1
    assert len(path_to(parent, 0, n - 1)) == n


def test_random_against_brute_force() -> None:
    rng = random.Random(20261105)
    for _ in range(800):
        n = rng.randint(1, 7)
        edges = random_dag(rng, n, rng.randint(0, 12)) if n > 1 else []
        s = rng.randrange(n)
        dist, parent = dag_longest_path(n, edges, s)
        paths = all_paths(n, edges, s)
        for v in range(n):
            ws = [w for w, p in paths if p[-1] == v]
            assert dist[v] == (max(ws) if ws else NEG_INF)
            if ws:
                p = path_to(parent, s, v)
                assert p[0] == s and path_weight(edges, p) == dist[v]
        best = max(w for t in range(n) for w, _ in all_paths(n, edges, t))
        weight, p = longest_path_anywhere(n, edges)
        assert weight == best and path_weight(edges, p) == best
