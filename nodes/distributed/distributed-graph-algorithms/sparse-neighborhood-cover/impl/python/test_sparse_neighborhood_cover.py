# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sparse-neighborhood-cover/. The authors are listed in prov/FFF7KM.jsonl.

import random

from sparse_neighborhood_cover import av_cover, ball, overlap, strong_radius


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


def test_cover_every_ball_with_bounded_radius_and_overlap() -> None:
    rng = random.Random(71)
    for adj in [ring(60), grid(8, 8), random_tree(80, rng), bounded_degree(80, 3, rng), bounded_degree(80, 5, rng)]:
        n = len(adj)
        for r in [1, 2]:
            for k in [1, 2, 3, 6]:
                clusters, phases = av_cover(adj, r, k)
                for v in range(n):
                    b = set(ball(adj, v, r))
                    assert any(b <= c for _, c in clusters)
                for start, c in clusters:
                    radius = strong_radius(adj, start, c)
                    assert 0 <= radius <= (2 * k - 1) * r
                assert phases <= k * n ** (1 / k) + 1e-9
                assert overlap(n, clusters) <= phases


def test_k_one_gives_the_balls_themselves() -> None:
    adj = grid(5, 5)
    # With k = 1 the kernel never grows, so the clusters are exactly the n balls, and the overlap is the largest ball.
    clusters, phases = av_cover(adj, 1, 1)
    assert phases <= 25
    assert overlap(25, clusters) == 5
    assert sorted(len(c) for _, c in clusters) == sorted(len(ball(adj, v, 1)) for v in range(25))


def test_large_k_on_a_path_gives_few_overlaps() -> None:
    n = 32
    adj = [[u for u in (v - 1, v + 1) if 0 <= u < n] for v in range(n)]
    clusters, _ = av_cover(adj, 1, 5)
    assert overlap(n, clusters) <= 5 * n ** (1 / 5)
    assert all(0 <= strong_radius(adj, s, c) <= 9 for s, c in clusters)
