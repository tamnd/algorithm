# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterative-mapreduce/. The authors are listed in prov/T3JHYW.jsonl.

import random
from collections import deque
from fractions import Fraction

from iterative_mapreduce import min_label_components, pagerank_rounds, rounds_for_error


def random_adj(rng, n, ring=True):
    """Every vertex has an out-edge. Without the ring, some vertices may
    have no in-edge."""
    adj = []
    for u in range(n):
        out = {rng.randrange(n) for _ in range(rng.randint(1, 3))}
        if ring:
            out.add((u + 1) % n)
        adj.append(sorted(out))
    return adj


def power_iteration(adj, alpha, k):
    n = len(adj)
    x = [Fraction(1, n)] * n
    for _ in range(k):
        y = [(1 - alpha) / n] * n
        for u in range(n):
            for v in adj[u]:
                y[v] += alpha * x[u] / len(adj[u])
        x = y
    return x


def test_pagerank_rounds_match_power_iteration_and_volume():
    rng = random.Random(1)
    alpha = Fraction(85, 100)
    for trial in range(40):
        n = rng.randint(1, 15)
        adj = random_adj(rng, n, ring=trial % 2 == 0)
        m = sum(len(a) for a in adj)
        k = rng.randint(0, 6)
        plain, vol = pagerank_rounds(adj, alpha, k)
        cached, vol_c = pagerank_rounds(adj, alpha, k, cache_graph=True)
        assert plain == cached == power_iteration(adj, alpha, k)
        assert vol == [n + m] * k
        assert vol_c == [m] * k


def test_round_bound_for_l1_error():
    rng = random.Random(2)
    alpha = 0.85
    for _ in range(10):
        adj = random_adj(rng, rng.randint(2, 30))
        star, _ = pagerank_rounds(adj, alpha, 250)  # the error is below 2 * 0.85^250
        for eps in (0.5, 0.1, 1e-3):
            k = rounds_for_error(alpha, eps)
            x, _ = pagerank_rounds(adj, alpha, k)
            assert sum(abs(a - b) for a, b in zip(x, star)) <= eps
    assert rounds_for_error(0.85, 1e-3) == 47
    assert rounds_for_error(0.85, 1e-6) == 90


def test_min_label_components():
    rng = random.Random(3)
    for _ in range(40):
        n = rng.randint(1, 30)
        edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(0, n))]
        labels, rounds = min_label_components(n, edges)
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
        # The label is the smallest vertex of the component, found by BFS.
        far = 0
        for v in range(n):
            dist = {v: 0}
            queue = deque([v])
            while queue:
                x = queue.popleft()
                for y in adj[x]:
                    if y not in dist:
                        dist[y] = dist[x] + 1
                        queue.append(y)
            low = min(dist)
            assert labels[v] == low
            far = max(far, dist[low])
        # Round t gives each vertex the least label within distance t; one more round sees no change.
        assert rounds == far + 1
