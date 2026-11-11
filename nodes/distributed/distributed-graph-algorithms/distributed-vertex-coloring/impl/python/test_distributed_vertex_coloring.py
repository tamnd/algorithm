# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-vertex-coloring/. The authors are listed in prov/5JYM67.jsonl.

import math
import random

from distributed_vertex_coloring import random_trial_coloring


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


def random_graph(n: int, p: float, rng: random.Random) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u in range(n):
        for v in range(u + 1, n):
            if rng.random() < p:
                adj[u].append(v)
                adj[v].append(u)
    return adj


def complete(n: int) -> list[list[int]]:
    return [[u for u in range(n) if u != v] for v in range(n)]


def families(rng: random.Random) -> list[list[list[int]]]:
    return [ring(101), grid(20, 20), random_graph(300, 0.02, rng), random_graph(200, 0.2, rng), complete(40), [[] for _ in range(5)]]


def test_proper_and_within_c_log_n_rounds() -> None:
    rng = random.Random(6)
    for adj in families(rng):
        n = len(adj)
        delta = max((len(a) for a in adj), default=0)
        for seed in range(5):
            col, rounds = random_trial_coloring(adj, delta, random.Random(seed))
            assert all(0 <= c <= delta for c in col)
            assert all(col[u] != col[v] for v in range(n) for u in adj[v])
            # (c + 1) log_{4/3} n phases with c = 1, two rounds per phase
            assert rounds <= 2 * math.ceil(2 * math.log(max(n, 2)) / math.log(4 / 3))


def test_success_rate_per_phase_at_least_a_quarter() -> None:
    rng = random.Random(7)
    adj = random_graph(400, 0.05, rng)
    delta = max(len(a) for a in adj)
    live_total = kept_total = 0
    for seed in range(10):
        stats: list[tuple[int, int]] = []
        random_trial_coloring(adj, delta, random.Random(seed), stats)
        live_total += sum(s[0] for s in stats)
        kept_total += sum(s[1] for s in stats)
    assert kept_total / live_total >= 0.25
