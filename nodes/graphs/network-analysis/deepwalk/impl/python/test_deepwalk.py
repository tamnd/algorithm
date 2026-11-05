# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deepwalk/. The authors are listed in prov/0SCSY9.jsonl.

import math
import random

from deepwalk import deepwalk, deepwalk_with_tree, dot, hs_probability, random_walk, tree_path, window_pairs


def undirected(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def cosine(a: list[float], b: list[float]) -> float:
    return dot(a, b) / math.sqrt(dot(a, a) * dot(b, b))


def pairs_oracle(walk: list[int], w: int) -> list[tuple[int, int]]:
    out = []
    for j, a in enumerate(walk):
        for k, b in enumerate(walk):
            if 0 < abs(j - k) <= w:
                out.append((a, b))
    return out


def loss(adj: list[list[int]], phi: list[list[float]], psi: list[list[float]], walks: list[list[int]], w: int) -> float:
    n = len(adj)
    return -sum(math.log(hs_probability(phi[a], psi, n, b)) for walk in walks for a, b in window_pairs(walk, w))


EXAMPLE = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (4, 6), (5, 6)]


def test_example() -> None:
    adj = undirected(7, EXAMPLE)
    phi = deepwalk(adj, d=8, w=2, gamma=20, t=10, alpha=0.05, seed=0)
    assert phi == deepwalk(adj, d=8, w=2, gamma=20, t=10, alpha=0.05, seed=0)
    for a, b in [(0, 1), (1, 2), (5, 6), (4, 5)]:
        assert cosine(phi[a], phi[b]) > 0.5
    for a, b in [(0, 5), (1, 6), (0, 6)]:
        assert cosine(phi[a], phi[b]) < 0.0


def test_edges() -> None:
    assert deepwalk([]) == []
    rng = random.Random(3)
    assert random_walk([[]], 0, 5, rng) == [0]
    assert random_walk([[1], [2], []], 0, 10, rng) == [0, 1, 2]
    assert window_pairs([7], 3) == []
    assert window_pairs([1, 2, 3], 1) == [(1, 2), (2, 1), (2, 3), (3, 2)]
    assert tree_path(1, 0) == []
    assert tree_path(4, 0) == [(0, 1), (1, 1)]
    assert tree_path(4, 3) == [(0, -1), (2, -1)]
    # an isolated vertex keeps its initial vector
    a = deepwalk([[1], [0], []], d=4, gamma=3, seed=9)
    b = deepwalk([[1], [0], []], d=4, gamma=0, seed=9)
    assert a[2] == b[2]


def test_training_lowers_the_loss() -> None:
    adj = undirected(7, EXAMPLE)
    rng = random.Random(11)
    walks = [random_walk(adj, v, 10, rng) for v in range(7) for _ in range(5)]
    phi0, psi0 = deepwalk_with_tree(adj, d=8, gamma=0, seed=2)
    pairs = sum(len(window_pairs(wk, 2)) for wk in walks)
    before = loss(adj, phi0, psi0, walks, 2)
    # with all inner-node vectors 0, each branch has probability 1/2
    assert abs(before - sum(len(tree_path(7, b)) for wk in walks for _, b in window_pairs(wk, 2)) * math.log(2)) < 1e-9
    phi1, psi1 = deepwalk_with_tree(adj, d=8, gamma=20, seed=2)
    after = loss(adj, phi1, psi1, walks, 2)
    assert after < 0.9 * before
    assert pairs > 0


def test_random_against_oracle() -> None:
    rng = random.Random(2014)
    for _ in range(600):
        n = rng.randint(1, 10)
        directed = rng.random() < 0.5
        adj: list[list[int]] = [[] for _ in range(n)]
        for _ in range(rng.randint(0, 2 * n)):
            u, v = rng.randrange(n), rng.randrange(n)
            if u == v:
                continue
            adj[u].append(v)
            if not directed:
                adj[v].append(u)
        t = rng.randint(1, 8)
        start = rng.randrange(n)
        walk = random_walk(adj, start, t, rng)
        assert walk[0] == start and 1 <= len(walk) <= t
        assert all(walk[i + 1] in adj[walk[i]] for i in range(len(walk) - 1))
        assert len(walk) == t or not adj[walk[-1]]
        w = rng.randint(1, 4)
        assert sorted(window_pairs(walk, w)) == sorted(pairs_oracle(walk, w))
        d = rng.randint(1, 5)
        phi_v = [rng.uniform(-2, 2) for _ in range(d)]
        psi = [[rng.uniform(-2, 2) for _ in range(d)] for _ in range(max(n - 1, 0))]
        total = sum(hs_probability(phi_v, psi, n, u) for u in range(n))
        assert abs(total - 1.0) < 1e-9
        leaves = {tuple(tree_path(n, u)) for u in range(n)}
        assert len(leaves) == n
