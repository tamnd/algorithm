# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/branch-and-reduce/. The authors are listed in prov/HSNMTD.jsonl.

import random

from branch_and_reduce import cycles_mis, max_independent_set

CUBE = [(u, u ^ (1 << b)) for u in range(8) for b in range(3) if u < u ^ (1 << b)]


def brute(n, edges):
    adj = [0] * n
    for u, v in edges:
        if u != v:
            adj[u] |= 1 << v
            adj[v] |= 1 << u
    best = 0
    for mask in range(1 << n):
        if all(not (mask >> v & 1) or not (adj[v] & mask) for v in range(n)):
            best = max(best, bin(mask).count("1"))
    return best


def is_independent(vs, edges):
    s = set(vs)
    return len(s) == len(vs) and all(not (u in s and v in s) for u, v in edges if u != v)


def test_example_of_the_page() -> None:
    stats: dict[str, int] = {}
    size, vs = max_independent_set(8, CUBE, stats)
    assert size == 4 and vs == [0, 3, 5, 6]
    assert stats == {"nodes": 5, "leaves": 3, "reductions": 9}


def test_edge_cases() -> None:
    assert max_independent_set(0, []) == (0, [])
    assert max_independent_set(1, []) == (1, [0])
    assert max_independent_set(3, []) == (3, [0, 1, 2])
    assert max_independent_set(2, [(0, 1)])[0] == 1
    assert max_independent_set(2, [(0, 0)]) == (2, [0, 1])
    k5 = [(u, v) for u in range(5) for v in range(u + 1, 5)]
    assert max_independent_set(5, k5)[0] == 1


def test_cycles() -> None:
    for k in range(3, 12):
        edges = [(i, (i + 1) % k) for i in range(k)]
        size, vs = max_independent_set(k, edges)
        assert size == k // 2 and is_independent(vs, edges)
        g = {i: {(i - 1) % k, (i + 1) % k} for i in range(k)}
        assert len(cycles_mis(g)) == k // 2


def test_petersen() -> None:
    edges = [(i, (i + 1) % 5) for i in range(5)] + [(i, i + 5) for i in range(5)]
    edges += [(5 + i, 5 + (i + 2) % 5) for i in range(5)]
    size, vs = max_independent_set(10, edges)
    assert size == 4 and is_independent(vs, edges)


def test_long_path_and_grid() -> None:
    n = 3000
    size, vs = max_independent_set(n, [(i, i + 1) for i in range(n - 1)])
    assert size == n // 2 + n % 2
    w = 6
    grid = [(r * w + c, r * w + c + 1) for r in range(w) for c in range(w - 1)]
    grid += [(r * w + c, (r + 1) * w + c) for r in range(w - 1) for c in range(w)]
    size, vs = max_independent_set(w * w, grid)
    assert size == w * w // 2 and is_independent(vs, grid)


def test_random_against_brute_force() -> None:
    rng = random.Random(1977)
    for _ in range(700):
        n = rng.randint(0, 13)
        p = rng.random()
        edges = [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < p]
        size, vs = max_independent_set(n, edges)
        assert size == brute(n, edges) == len(vs)
        assert is_independent(vs, edges)
