# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-diameter/. The authors are listed in prov/5JD8RM.jsonl.

import random

from distributed_diameter import (
    adjacency,
    bfs,
    brute_diameter,
    exact_diameter,
    three_halves_estimate,
    two_approx,
)


def random_connected(n: int, p: float, rng: random.Random) -> list[tuple[int, int]]:
    edges = {(rng.randrange(v), v) for v in range(1, n)}
    edges |= {(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < p}
    return sorted(edges)


def graphs():
    rng = random.Random(11)
    for _ in range(100):
        n = rng.randrange(1, 28)
        yield n, random_connected(n, rng.random() * 0.25, rng)
    for n in range(2, 25):
        yield n, [(i, i + 1) for i in range(n - 1)]
        if n >= 3:
            yield n, [(i, (i + 1) % n) for i in range(n)]


def test_example() -> None:
    edges = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (4, 5)]
    st = exact_diameter(6, edges)
    assert st["ecc"] == [4, 3, 3, 2, 3, 4]
    assert st["diameter"] == [4] * 6
    assert st["phase_rounds"] == (8, 17, 5, 4)


def test_exact_matches_brute_force() -> None:
    for n, edges in graphs():
        st = exact_diameter(n, edges)
        d = brute_diameter(n, edges)
        assert st["diameter"] == [d] * n
        adj = adjacency(n, edges)
        assert st["ecc"] == [max(bfs(adj, v)) for v in range(n)]
        if n > 1:
            assert st["max_link_load"] == 1
        # O(n) rounds: tree, waves, convergecast and broadcast
        r_tree, r_waves, r_cast, depth = st["phase_rounds"]
        e = max(bfs(adj, 0))
        assert r_tree <= 2 * e + 2
        assert r_waves <= 3 * n + d
        assert r_cast <= e + 1 and depth == e


def test_two_approximation() -> None:
    for n, edges in graphs():
        e, d = two_approx(n, edges), brute_diameter(n, edges)
        assert e <= d <= 2 * e


def test_three_halves_estimate() -> None:
    rng = random.Random(3)
    hits = total = 0
    for n, edges in graphs():
        est, hit = three_halves_estimate(n, edges, rng)
        d = brute_diameter(n, edges)
        assert est <= d
        total += 1
        if hit:
            hits += 1
            assert est >= (2 * d) // 3
    assert hits >= 0.95 * total
