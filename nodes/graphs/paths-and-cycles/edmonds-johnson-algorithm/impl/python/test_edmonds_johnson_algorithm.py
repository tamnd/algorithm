# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/edmonds-johnson-algorithm/. The authors are listed in prov/Y06F76.jsonl.

import heapq
import random

import pytest

from edmonds_johnson_algorithm import edmonds_johnson_algorithm

EXAMPLE = [(0, 1, 1), (1, 2, 2), (2, 3, 1), (3, 0, 3), (0, 2, 4), (1, 3, 5)]


def check_walk(n: int, edges: list[tuple[int, int, float]], walk: list[int], trail: list[int]) -> float:
    """Check that (walk, trail) is a closed walk using every edge; return its weight."""
    assert len(walk) == len(trail) + 1 and walk[0] == walk[-1]
    assert set(trail) == set(range(len(edges)))
    for i, e in enumerate(trail):
        u, v, _ = edges[e]
        assert sorted((u, v)) == sorted((walk[i], walk[i + 1]))
    return sum(edges[e][2] for e in trail)


def brute_force(n: int, edges: list[tuple[int, int, float]]) -> float | None:
    """Dijkstra over the states (vertex, set of edges used so far), from an end of edge 0."""
    m = len(edges)
    if m == 0:
        return 0
    full = (1 << m) - 1
    s = edges[0][0]
    dist = {(s, 0): 0.0}
    heap = [(0.0, s, 0)]
    while heap:
        d, x, mask = heapq.heappop(heap)
        if (x, mask) == (s, full):
            return d
        if d > dist[(x, mask)]:
            continue
        for e, (a, b, w) in enumerate(edges):
            if x in (a, b):
                y = b if a == x else a
                state = (y, mask | 1 << e)
                if d + w < dist.get(state, float("inf")):
                    dist[state] = d + w
                    heapq.heappush(heap, (d + w, y, mask | 1 << e))
    return None


def test_example() -> None:
    cost, walk, trail = edmonds_johnson_algorithm(4, EXAMPLE)
    assert cost == 18
    assert check_walk(4, EXAMPLE, walk, trail) == 18


def test_edge_cases() -> None:
    assert edmonds_johnson_algorithm(0, []) == (0, [], [])
    assert edmonds_johnson_algorithm(3, []) == (0, [0], [])
    # Eulerian input: nothing is repeated
    tri = [(0, 1, 2), (1, 2, 3), (2, 0, 4)]
    assert edmonds_johnson_algorithm(5, tri)[0] == 9  # isolated vertices 3 and 4
    # a self-loop alone, and a loop on a single edge
    assert edmonds_johnson_algorithm(1, [(0, 0, 5)]) == (5, [0, 0], [0])
    assert edmonds_johnson_algorithm(2, [(0, 1, 2), (1, 1, 1)])[0] == 5
    # parallel edges: two odd vertices joined three times
    assert edmonds_johnson_algorithm(2, [(0, 1, 1), (0, 1, 7), (0, 1, 3)])[0] == 12
    # K4 with unit weights
    k4 = [(a, b, 1) for a in range(4) for b in range(a + 1, 4)]
    assert edmonds_johnson_algorithm(4, k4)[0] == 8
    # edges in two components
    assert edmonds_johnson_algorithm(4, [(0, 1, 1), (2, 3, 1)]) is None
    with pytest.raises(ValueError):
        edmonds_johnson_algorithm(2, [(0, 1, -1)])


def test_random_against_brute_force() -> None:
    rng = random.Random(20261105)
    for _ in range(600):
        n = rng.randint(1, 6)
        m = rng.randint(0, 8)
        edges = [(rng.randrange(n), rng.randrange(n), rng.randint(0, 9)) for _ in range(m)]
        res = edmonds_johnson_algorithm(n, edges)
        expected = brute_force(n, edges)
        if expected is None:
            assert res is None
        else:
            assert res is not None and res[0] == expected
            if m:
                assert check_walk(n, edges, res[1], res[2]) == expected
