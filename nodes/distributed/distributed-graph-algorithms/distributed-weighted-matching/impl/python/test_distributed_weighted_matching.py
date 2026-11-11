# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-weighted-matching/. The authors are listed in prov/B1T5JR.jsonl.

import math
import random

from distributed_weighted_matching import (
    class_matching,
    edges_of,
    is_maximal_matching,
    locally_heaviest,
    matching_weight,
    max_weight_matching_brute,
)


def path(n: int) -> list[list[int]]:
    return [[u for u in (v - 1, v + 1) if 0 <= u < n] for v in range(n)]


def random_graph(n: int, p: float, rng: random.Random) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u in range(n):
        for v in range(u + 1, n):
            if rng.random() < p:
                adj[u].append(v)
                adj[v].append(u)
    return adj


def bounded_degree(n: int, d: int, rng: random.Random) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for _ in range(n * d):
        u, v = rng.randrange(n), rng.randrange(n)
        if u != v and v not in adj[u] and len(adj[u]) < d and len(adj[v]) < d:
            adj[u].append(v)
            adj[v].append(u)
    return adj


def random_weights(adj: list[list[int]], rng: random.Random, top: float) -> dict[tuple[int, int], float]:
    return {e: math.exp(rng.uniform(0, math.log(top))) for e in edges_of(adj)}


def test_ratios_against_brute_force() -> None:
    rng = random.Random(5)
    for trial in range(40):
        adj = random_graph(8, 0.45, rng)
        if not edges_of(adj):
            continue
        w = random_weights(adj, rng, 100.0)
        opt = max_weight_matching_brute(adj, w)
        for eps in (0.1, 1.0):
            mate, _ = class_matching(adj, w, eps, rng)
            assert is_maximal_matching(adj, mate)
            assert matching_weight(mate, w) >= opt / (2 * (1 + eps)) - 1e-9
        mate, _ = locally_heaviest(adj, w)
        assert is_maximal_matching(adj, mate)
        assert matching_weight(mate, w) >= opt / 2 - 1e-9


def test_increasing_path_rounds() -> None:
    rng = random.Random(9)
    n = 256
    adj = path(n)
    w = {(i, i + 1): float(i + 1) for i in range(n - 1)}
    _, lh_rounds = locally_heaviest(adj, w)
    assert lh_rounds == n // 2
    mate, cl_rounds = class_matching(adj, w, 1.0, rng)
    assert is_maximal_matching(adj, mate)
    classes = math.floor(math.log2(n - 1)) + 1
    # each class is a union of paths; Luby on it needs O(log n) phases of 3 rounds
    assert cl_rounds <= 3 * classes * (4 * math.log2(n))
    assert cl_rounds < lh_rounds


def test_bounded_degree_valid() -> None:
    rng = random.Random(13)
    for _ in range(5):
        adj = bounded_degree(80, 5, rng)
        w = random_weights(adj, rng, 1000.0)
        mate, rounds = class_matching(adj, w, 0.5, rng)
        assert is_maximal_matching(adj, mate)
        assert rounds > 0
