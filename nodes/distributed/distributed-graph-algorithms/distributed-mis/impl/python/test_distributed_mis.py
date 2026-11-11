# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-mis/. The authors are listed in prov/CESMCY.jsonl.

import math
import random

from distributed_mis import coloring_from_mis, is_mis, luby_mis_local, mis_from_coloring


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


def families(rng: random.Random) -> list[list[list[int]]]:
    return [
        ring(200),
        grid(15, 15),
        random_tree(300, rng),
        bounded_degree(300, 5, rng),
        random_graph(200, 0.1, rng),
        [[u for u in range(30) if u != v] for v in range(30)],
        [[] for _ in range(4)],
    ]


def greedy_coloring(adj: list[list[int]]) -> list[int]:
    col = [-1] * len(adj)
    for v in range(len(adj)):
        used = {col[u] for u in adj[v]}
        col[v] = min(c for c in range(len(adj[v]) + 1) if c not in used)
    return col


def test_luby_valid_and_within_bound() -> None:
    rng = random.Random(11)
    for adj in families(rng):
        n = len(adj)
        for seed in range(5):
            member, rounds = luby_mis_local(adj, random.Random(seed))
            assert is_mis(adj, member)
            # Pr[phases > (c + 2) log2 n + 2] <= n^(-c); here c = 1, two rounds per phase
            assert rounds <= 2 * (3 * math.log2(max(n, 2)) + 2)


def test_live_edges_halve_on_average() -> None:
    rng = random.Random(12)
    adj = random_graph(300, 0.05, rng)
    before = after = 0
    for seed in range(20):
        stats: list[int] = []
        luby_mis_local(adj, random.Random(seed), stats)
        stats.append(0)
        before += sum(stats[:-1])
        after += sum(stats[1:])
    assert after <= before / 2


def test_mis_from_coloring_takes_k_rounds() -> None:
    rng = random.Random(13)
    for adj in families(rng):
        col = greedy_coloring(adj)
        k = max(col, default=-1) + 1
        member, rounds = mis_from_coloring(adj, col, k)
        assert is_mis(adj, member)
        assert rounds == k


def test_coloring_from_mis_of_product_graph() -> None:
    rng = random.Random(14)
    for adj in [ring(31), grid(6, 6), bounded_degree(60, 4, rng), random_tree(50, rng)]:
        delta = max(len(a) for a in adj)
        col, _ = coloring_from_mis(adj, delta, random.Random(1))
        assert all(0 <= c <= delta for c in col)
        assert all(col[u] != col[v] for v in range(len(adj)) for u in adj[v])


def test_small_cases_by_hand() -> None:
    # isolated nodes all join in the first phase
    member, rounds = luby_mis_local([[] for _ in range(3)], random.Random(0))
    assert member == [True, True, True] and rounds == 2
    # complete graph: exactly one node joins, in one phase
    k5 = [[u for u in range(5) if u != v] for v in range(5)]
    member, rounds = luby_mis_local(k5, random.Random(0))
    assert sum(member) == 1 and rounds == 2
