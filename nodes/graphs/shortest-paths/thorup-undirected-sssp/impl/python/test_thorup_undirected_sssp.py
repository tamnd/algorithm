# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/thorup-undirected-sssp/. The authors are listed in prov/J10R6J.jsonl.

import heapq
import math
import random

import pytest

from thorup_undirected_sssp import thorup_undirected_sssp

S, A, B, C, D = range(5)
EXAMPLE = [(S, A, 1), (A, B, 2), (S, C, 5), (B, C, 1), (C, D, 3), (B, D, 6)]


def dijkstra(n, edges, s):
    """Independent oracle: Dijkstra with a binary heap on the undirected graph."""
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    dist = [None] * n
    heap = [(0, s)]
    while heap:
        d, u = heapq.heappop(heap)
        if dist[u] is not None:
            continue
        dist[u] = d
        for v, w in adj[u]:
            if dist[v] is None:
                heapq.heappush(heap, (d + w, v))
    return dist


def test_example_and_trace():
    trace = []
    assert thorup_undirected_sssp(5, EXAMPLE, S, trace) == [0, 1, 3, 4, 7]
    assert trace[0] == (3, S, math.inf)
    assert (1, B, 4) in trace and (1, B, 6) in trace
    assert sum(1 for level, _, _ in trace if level == 0) == 5


def test_unreachable_vertices():
    assert thorup_undirected_sssp(4, [(0, 1, 3), (2, 3, 1)], 0) == [0, 3, None, None]
    assert thorup_undirected_sssp(1, [], 0) == [0]


def test_rejects_negative_zero_and_non_integer_weights():
    for bad in (-2, 0, 1.5, True):
        with pytest.raises(ValueError):
            thorup_undirected_sssp(2, [(0, 1, bad)], 0)


def test_parallel_edges_and_self_loops():
    edges = [(0, 1, 9), (0, 1, 4), (1, 1, 1), (1, 2, 4), (0, 2, 9)]
    assert thorup_undirected_sssp(3, edges, 0) == [0, 4, 8]


def test_large_weights():
    edges = [(0, 1, 2**40), (1, 2, 1), (0, 2, 2**40 + 2)]
    assert thorup_undirected_sssp(3, edges, 0) == [0, 2**40, 2**40 + 1]


def test_random_against_dijkstra():
    rng = random.Random(20261105)
    for _ in range(1500):
        n = rng.randint(1, 12)
        m = rng.randint(0, 3 * n)
        weights = rng.choice([[1, 2, 3], [1, 2, 4, 8, 16, 32], list(range(1, 100))])
        edges = [(rng.randrange(n), rng.randrange(n), rng.choice(weights)) for _ in range(m)]
        s = rng.randrange(n)
        assert thorup_undirected_sssp(n, edges, s) == dijkstra(n, edges, s)
