# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/congest-model/. The authors are listed in prov/ECCJVR.jsonl.

import random
from collections import deque

import pytest

from congest_model import (
    CongestViolation,
    Gather,
    SmallestFirst,
    SyncBFS,
    all_ids_lower_bound,
    bits,
    budget,
    dumbbell,
    run,
)


def edges_to_adj(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in sorted(edges):
        adj[u].append(v)
        adj[v].append(u)
    return adj


def make_graph(kind, n, seed):
    rng = random.Random(seed)
    edges = {(rng.randrange(v), v) for v in range(1, n)}
    if kind == "path":
        edges = {(v - 1, v) for v in range(1, n)}
    elif kind == "gnp":
        for u in range(n):
            for v in range(u + 1, n):
                if rng.random() < 0.2:
                    edges.add((u, v))
    adj = edges_to_adj(n, edges)
    for nbrs in adj:
        rng.shuffle(nbrs)
    return adj


def bfs(adj, s):
    dist = {s: 0}
    q = deque([s])
    while q:
        u = q.popleft()
        for w in adj[u]:
            if w not in dist:
                dist[w] = dist[u] + 1
                q.append(w)
    return [dist[v] for v in range(len(adj))]


def diameter(adj):
    return max(max(bfs(adj, s)) for s in range(len(adj)))


def cases():
    kinds = ["tree", "path", "gnp"]
    for seed in range(30):
        n = 2 + (seed * 7) % 40
        yield make_graph(kinds[seed % 3], n, seed), random.Random(seed)


def knows_all(n):
    return lambda states: all(len(s[1]) == n for s in states)


def test_budget_and_encoding():
    assert budget(1, 3) == 3 and budget(7, 3) == 9 and budget(8, 3) == 12
    assert bits(255) <= 2 + 2 * 9 + 1
    assert bits((5, 7)) > bits(5) + bits(7)


def test_bfs_fits_in_congest():
    for adj, rng in cases():
        n = len(adj)
        ids = rng.sample(range(1, n * n + 2), n)
        states, stats = run(adj, ids, [1] + [0] * (n - 1), SyncBFS(), n, c=3)
        assert [s[1] for s in states] == bfs(adj, 0)
        assert stats["max_bits"] <= budget(n, 3)
        assert stats["rounds"] == n


def test_smallest_first_learns_all_ids_within_n_plus_d():
    for adj, rng in cases():
        n = len(adj)
        ids = rng.sample(range(1, n * n + 2), n)
        # identifiers up to n^2 + 1 need about 4 log2 n bits in this code, hence c = 6
        states, stats = run(adj, ids, [0] * n, SmallestFirst(), 4 * n, c=6, stop=knows_all(n))
        assert all(s[1] == frozenset(ids) for s in states)
        assert stats["rounds"] <= n + diameter(adj)


def test_dumbbell_gap_between_local_and_congest():
    for n in (16, 32, 64):
        adj = dumbbell(n)
        ids = list(range(1, n + 1))
        assert diameter(adj) == 3
        # LOCAL: gathering the whole graph needs D + 1 = 4 rounds, with big messages.
        states, stats = run(adj, ids, [0] * n, Gather(), 4, mode="LOCAL")
        assert all(len(s[3]) == n for s in states)
        assert stats["max_bits"] > budget(n, 3)
        with pytest.raises(CongestViolation):
            run(adj, ids, [0] * n, Gather(), 4, mode="CONGEST", c=3)
        # CONGEST: one identifier per round crosses the bridge in each direction.
        states, stats = run(adj, ids, [0] * n, SmallestFirst(), 4 * n, c=3, stop=knows_all(n))
        assert n // 2 <= stats["rounds"] <= n + 3
        b = budget(n, 3)
        lb = all_ids_lower_bound(n, n * n, b)
        assert lb >= n / (2 * 3 + 2) - 1  # Omega(n / c) rounds for any algorithm
        assert stats["rounds"] >= lb
