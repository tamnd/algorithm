# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ruling-set/. The authors are listed in prov/GGJNRV.jsonl.

import random

from ruling_set import bit_splitting_ruling_set, ruling_parameters


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


def test_parameters_and_rounds() -> None:
    rng = random.Random(41)
    for adj in [ring(150), grid(12, 12), random_tree(200, rng), bounded_degree(200, 4, rng)]:
        n = len(adj)
        for N in [n, n * n]:
            ids = rng.sample(range(N), n)
            B = (N - 1).bit_length()
            for alpha in [2, 3]:
                rset, rounds = bit_splitting_ruling_set(adj, ids, N, alpha)
                least, greatest = ruling_parameters(adj, rset)
                assert rounds == (alpha - 1) * B
                assert least >= alpha
                assert greatest <= (alpha - 1) * B


def test_path_with_sorted_ids_reaches_depth() -> None:
    # On a path with ids 0..n-1 in order, every node with an odd id has its even neighbour in its group at level 1.
    n = 16
    adj = [[u for u in (v - 1, v + 1) if 0 <= u < n] for v in range(n)]
    rset, rounds = bit_splitting_ruling_set(adj, list(range(n)), n)
    assert rounds == 4
    least, greatest = ruling_parameters(adj, rset)
    assert least >= 2 and greatest <= 4
    assert rset == {0, 2, 4, 6, 8, 10, 12, 14}


def test_mis_is_a_2_1_ruling_set() -> None:
    adj = ring(9)
    mis = {0, 2, 4, 6}
    assert ruling_parameters(adj, mis) == (2, 1)
