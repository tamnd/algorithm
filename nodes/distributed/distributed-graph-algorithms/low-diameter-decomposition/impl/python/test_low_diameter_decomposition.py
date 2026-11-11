# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/low-diameter-decomposition/. The authors are listed in prov/FW9GHE.jsonl.

import math
import random

from low_diameter_decomposition import cut_fraction, exact_centres, kept_nodes, mpx, strong_radius


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


def graphs(rng: random.Random) -> list[list[list[int]]]:
    return [ring(150), grid(14, 14), random_tree(200, rng), bounded_degree(200, 4, rng)]


def test_distributed_rounds_match_the_definition() -> None:
    rng = random.Random(61)
    for adj in graphs(rng):
        for beta in [0.2, 0.5]:
            centre, delta, _ = mpx(adj, beta, random.Random(7))
            assert centre == exact_centres(adj, delta)


def test_strong_radius_and_rounds() -> None:
    rng = random.Random(62)
    for adj in graphs(rng):
        n = len(adj)
        for beta in [0.1, 0.3, 0.6]:
            for seed in range(5):
                centre, delta, rounds = mpx(adj, beta, random.Random(seed))
                radius = strong_radius(adj, centre)
                assert 0 <= radius <= max(delta)
                # w.h.p. bound with c = 1: max delta <= 2 ln n / beta
                assert max(delta) <= 2 * math.log(n) / beta
                assert rounds <= 2 * math.log(n) / beta + 1


def test_edge_cut_probability_is_order_beta() -> None:
    # Each edge is cut with probability at most 1 - exp(-beta); the mean cut fraction obeys the same bound.
    rng = random.Random(63)
    for adj in [grid(12, 12), random_tree(150, rng), bounded_degree(150, 4, rng)]:
        for beta in [0.05, 0.1, 0.2, 0.4]:
            runs = 40
            mean = sum(cut_fraction(adj, mpx(adj, beta, random.Random(1000 * s + 1))[0]) for s in range(runs)) / runs
            assert mean <= 1 - math.exp(-beta)


def test_kept_nodes_give_one_colour_class() -> None:
    # Kept nodes of different clusters are never adjacent, and a node is kept with probability >= exp(-beta).
    rng = random.Random(64)
    adj = bounded_degree(150, 4, rng)
    kept_total = 0
    runs = 30
    for s in range(runs):
        centre, delta, _ = mpx(adj, 0.5, random.Random(s))
        kept = kept_nodes(adj, delta)
        for v in range(len(adj)):
            for u in adj[v]:
                if kept[u] and kept[v]:
                    assert centre[u] == centre[v]
        kept_total += sum(kept)
    assert kept_total / (runs * len(adj)) >= math.exp(-0.5) - 0.05
