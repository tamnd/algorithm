# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/network-decomposition/. The authors are listed in prov/1Q6NFT.jsonl.

import math
import random

from network_decomposition import check_decomposition, linial_saks, mis_via_decomposition


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


def is_mis(adj: list[list[int]], member: list[bool]) -> bool:
    return all(
        (not member[v] or not any(member[u] for u in adj[v])) and (member[v] or any(member[u] for u in adj[v]))
        for v in range(len(adj))
    )


def graphs(rng: random.Random) -> list[list[list[int]]]:
    return [ring(120), grid(12, 12), random_tree(200, rng), bounded_degree(200, 4, rng)]


def test_decomposition_meets_its_bounds() -> None:
    rng = random.Random(51)
    for adj in graphs(rng):
        n = len(adj)
        B = 3 * (n - 1).bit_length()
        for seed in range(4):
            ids = random.Random(seed).sample(range(n * n), n)
            centre, colour, phases, rounds = linial_saks(adj, ids, random.Random(seed))
            assert all(c >= 0 for c in colour)
            diameter = check_decomposition(adj, centre, colour)
            assert diameter <= 2 * (B - 1)
            # the proved bound: (c + 1) log_{4/3} n phases with c = 1, w.h.p.; in practice about log2 n
            assert phases <= 2 * math.log(n) / math.log(4 / 3)
            assert rounds == phases * B


def test_each_phase_clusters_about_half() -> None:
    # Each node is clustered in the first phase with probability exactly 1/2 (up to the cut at B).
    # The events are strongly correlated inside one run, so average over many runs.
    rng = random.Random(52)
    adj = bounded_degree(60, 4, rng)
    joined = 0
    runs = 400
    for seed in range(runs):
        stats: list[tuple[int, int]] = []
        linial_saks(adj, list(range(60)), random.Random(seed), stats)
        joined += stats[0][1]
    assert 0.45 <= joined / (60 * runs) <= 0.55


def test_mis_in_colours_times_diameter_rounds() -> None:
    rng = random.Random(53)
    for adj in graphs(rng):
        n = len(adj)
        centre, colour, phases, _ = linial_saks(adj, list(range(n)), random.Random(1))
        diameter = check_decomposition(adj, centre, colour)
        member, rounds = mis_via_decomposition(adj, centre, colour, diameter)
        assert is_mis(adj, member)
        assert rounds == phases * (diameter + 2)
