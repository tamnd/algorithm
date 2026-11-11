# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-maximal-matching/. The authors are listed in prov/YK5M1K.jsonl.

import math
import random

from distributed_maximal_matching import is_maximal_matching, luby_matching_local


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


def random_graph(n: int, p: float, rng: random.Random) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u in range(n):
        for v in range(u + 1, n):
            if rng.random() < p:
                adj[u].append(v)
                adj[v].append(u)
    return adj


def test_valid_and_within_bound() -> None:
    rng = random.Random(21)
    graphs = [ring(201), grid(15, 15), random_tree(300, rng), bounded_degree(300, 5, rng), random_graph(150, 0.1, rng)]
    graphs.append([[u for u in range(25) if u != v] for v in range(25)])
    graphs.append([[] for _ in range(3)])
    for adj in graphs:
        m = sum(len(a) for a in adj) // 2
        for seed in range(5):
            mate, rounds = luby_matching_local(adj, random.Random(seed))
            assert is_maximal_matching(adj, mate)
            # Luby on the line graph (m nodes): (c + 2) log2 m + 2 phases with c = 1, three rounds per phase
            assert rounds <= 3 * (3 * math.log2(max(m, 2)) + 2)


def test_progress_per_phase() -> None:
    rng = random.Random(22)
    adj = random_graph(200, 0.05, rng)
    total_before = total_after = 0
    for seed in range(20):
        stats: list[int] = []
        luby_matching_local(adj, random.Random(seed), stats)
        stats.append(0)
        total_before += sum(stats[:-1])
        total_after += sum(stats[1:])
    # the live edges of G fall by a constant factor per phase on average
    assert total_after <= 0.75 * total_before


def test_small_cases() -> None:
    # a single edge is matched in one phase
    mate, rounds = luby_matching_local([[1], [0]], random.Random(0))
    assert mate == [1, 0] and rounds == 3
    # a star: exactly one edge, in one phase
    star = [[1, 2, 3, 4]] + [[0] for _ in range(4)]
    mate, rounds = luby_matching_local(star, random.Random(0))
    assert is_maximal_matching(star, mate) and sum(1 for x in mate if x >= 0) == 2 and rounds == 3
    # no edges: no rounds
    assert luby_matching_local([[], []], random.Random(0)) == ([-1, -1], 0)
