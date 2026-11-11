# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-edge-coloring/. The authors are listed in prov/2M70EM.jsonl.

import math
import random

from distributed_edge_coloring import edges_of, is_proper_edge_coloring, random_trial_edge_coloring


def ring(n: int) -> list[list[int]]:
    return [[(v - 1) % n, (v + 1) % n] for v in range(n)]


def grid(a: int, b: int) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(a * b)]
    for i in range(a):
        for j in range(b):
            v = i * b + j
            if i + 1 < a:
                adj[v].append(v + b)
                adj[v + b].append(v)
            if j + 1 < b:
                adj[v].append(v + 1)
                adj[v + 1].append(v)
    return adj


def random_tree(n: int, rng: random.Random) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for v in range(1, n):
        p = rng.randrange(v)
        adj[v].append(p)
        adj[p].append(v)
    return adj


def bounded_degree(n: int, d: int, rng: random.Random) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for _ in range(n * d):
        u, v = rng.randrange(n), rng.randrange(n)
        if u != v and v not in adj[u] and len(adj[u]) < d and len(adj[v]) < d:
            adj[u].append(v)
            adj[v].append(u)
    return adj


def complete(n: int) -> list[list[int]]:
    return [[u for u in range(n) if u != v] for v in range(n)]


def families(rng: random.Random) -> list[list[list[int]]]:
    return [ring(30), grid(6, 7), random_tree(60, rng), bounded_degree(60, 6, rng), complete(9)]


def test_proper_with_2delta_minus_1_colours() -> None:
    rng = random.Random(7)
    for adj in families(rng):
        colour, rounds = random_trial_edge_coloring(adj, rng)
        delta = max(len(a) for a in adj)
        assert is_proper_edge_coloring(adj, colour)
        assert all(0 <= c <= 2 * delta - 2 for c in colour.values())
        m = len(edges_of(adj))
        # each edge succeeds with probability at least 1/4 per trial: (3/4)^t m < 1/m once t > 2 ln m / ln(4/3)
        assert rounds <= 2 * (2 * math.log(m) / math.log(4 / 3) + 2)


def test_success_rate_at_least_one_quarter() -> None:
    rng = random.Random(11)
    first, total = 0, 0
    for _ in range(20):
        adj = bounded_degree(50, 5, rng)
        stats: list[int] = []
        random_trial_edge_coloring(adj, rng, stats)
        if len(stats) >= 2:
            first += stats[0] - stats[1]
            total += stats[0]
    assert first / total >= 0.25


def test_ring_uses_three_colours_and_checker_rejects() -> None:
    rng = random.Random(3)
    adj = ring(11)
    colour, _ = random_trial_edge_coloring(adj, rng)
    assert set(colour.values()) <= {0, 1, 2}
    bad = dict(colour)
    (u, v) = (0, 1)
    (x, y) = (1, 2)
    bad[(u, v)] = bad[(x, y)]
    assert not is_proper_edge_coloring(adj, bad)
    assert not is_proper_edge_coloring(adj, {})
