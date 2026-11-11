# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-minimum-vertex-cover/. The authors are listed in prov/511N17.jsonl.

import math
import random

from distributed_minimum_vertex_cover import is_vertex_cover, matching_cover, min_vertex_cover_size


def random_graph(n: int, p: float, rng: random.Random) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u in range(n):
        for v in range(u + 1, n):
            if rng.random() < p:
                adj[u].append(v)
                adj[v].append(u)
    return adj


def random_tree(n: int, rng: random.Random) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for v in range(1, n):
        p = rng.randrange(v)
        adj[v].append(p)
        adj[p].append(v)
    return adj


def test_two_approximation_against_brute_force() -> None:
    rng = random.Random(31)
    worst = 0.0
    for trial in range(60):
        n = rng.randint(2, 14)
        adj = random_graph(n, rng.choice([0.15, 0.3, 0.5]), rng) if trial % 3 else random_tree(n, rng)
        opt = min_vertex_cover_size(adj)
        cover, msize, rounds = matching_cover(adj, random.Random(trial))
        assert is_vertex_cover(adj, cover)
        assert len(cover) == 2 * msize
        assert msize <= opt <= len(cover) <= 2 * opt
        m = sum(len(a) for a in adj) // 2
        assert rounds <= 3 * (3 * math.log2(max(m, 2)) + 2)
        if opt:
            worst = max(worst, len(cover) / opt)
    assert worst <= 2


def test_ratio_two_is_reached() -> None:
    # disjoint edges: the matching takes both ends, the optimum one end of each
    adj = [[1], [0], [3], [2], [5], [4]]
    cover, _, _ = matching_cover(adj, random.Random(0))
    assert len(cover) == 6 and min_vertex_cover_size(adj) == 3


def test_brute_force_small_cases() -> None:
    assert min_vertex_cover_size([[1, 2], [0, 2], [0, 1]]) == 2  # triangle
    star = [[1, 2, 3, 4]] + [[0] for _ in range(4)]
    assert min_vertex_cover_size(star) == 1
    c5 = [[(v - 1) % 5, (v + 1) % 5] for v in range(5)]
    assert min_vertex_cover_size(c5) == 3
