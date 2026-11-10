# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gas-model/. The authors are listed in prov/Z8G7PR.jsonl.

import heapq
import random
from fractions import Fraction

from gas_model import (VertexCut, cut_fraction, demo_graph, expected_replication, random_cut,
                       run_pagerank, run_sssp)


def power_iteration(n, edges, k, alpha):
    outdeg = [0] * n
    for u, _, _ in edges:
        outdeg[u] += 1
    x = [Fraction(1, n)] * n
    for _ in range(k):
        y = [(1 - alpha) / n] * n
        for u, v, _ in edges:
            y[v] += alpha * x[u] / outdeg[u]
        x = y
    return x


def dijkstra(n, edges, s):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [float("inf")] * n
    dist[s] = 0
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(pq, (d + w, v))
    return dist


def test_pagerank_matches_power_iteration():
    rng = random.Random(4)
    alpha = Fraction(85, 100)
    for trial in range(20):
        n = rng.randint(2, 12)
        edges = demo_graph(rng, n, rng.randint(0, 3 * n))
        p = rng.randint(1, 5)
        k = rng.randint(1, 6)
        cut = random_cut(n, edges, p, rng)
        x, log = run_pagerank(cut, alpha, k)
        assert x == power_iteration(n, edges, k, alpha)
        assert len(log) == k
        rf_words = sum(len(a) - 1 for a in cut.span)
        for step in log:
            assert step["apply"] == rf_words           # every vertex is active
            assert step["gather"] <= rf_words
            assert step["gather"] + step["apply"] <= 2 * rf_words


def test_sssp_matches_dijkstra():
    rng = random.Random(5)
    for trial in range(40):
        n = rng.randint(2, 25)
        edges = demo_graph(rng, n, rng.randint(0, 3 * n))
        cut = random_cut(n, edges, rng.randint(1, 6), rng)
        s = rng.randrange(n)
        dist, log = run_sssp(cut, s)
        assert dist == dijkstra(n, edges, s)


def test_one_machine_has_no_communication():
    rng = random.Random(6)
    edges = demo_graph(rng, 10, 20)
    cut = VertexCut(10, edges, [0] * len(edges))
    assert cut.replication_factor() == 1
    _, log = run_sssp(cut, 0)
    assert all(sum(step.values()) == 0 for step in log)


def test_random_vertex_cut_replication_matches_theorem():
    rng = random.Random(7)
    n = 60
    edges = demo_graph(rng, n, 240)
    for p in (2, 4, 8, 16):
        trials = 300
        avg = sum(random_cut(n, edges, p, rng).replication_factor() for _ in range(trials)) / trials
        assert abs(avg - expected_replication(n, edges, p)) < 0.02 * p ** 0.5


def test_random_edge_cut_fraction():
    rng = random.Random(8)
    n = 60
    edges = demo_graph(rng, n, 240)
    for p in (2, 4, 8):
        trials = 300
        avg = sum(cut_fraction(n, edges, p, rng) for _ in range(trials)) / trials
        assert abs(avg - (1 - 1 / p)) < 0.01
