# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-apsp/. The authors are listed in prov/5J9KE7.jsonl.

import random

from distributed_apsp import bfs_all, leaf_lower_bound_graph, pipelined_apsp


def random_connected(n: int, p: float, rng: random.Random) -> list[tuple[int, int]]:
    edges = {(rng.randrange(v), v) for v in range(1, n)}
    edges |= {(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < p}
    return sorted(edges)


def check(n: int, edges: list[tuple[int, int]]) -> dict:
    st = pipelined_apsp(n, edges)
    oracle = bfs_all(n, edges)
    diam = max(max(row) for row in oracle)
    ecc_root = max(oracle[0])
    # exact distances at every node
    for w in range(n):
        assert st["dist"][w] == {u: oracle[u][w] for u in range(n)}
    # no collisions: one wave message per link per round, one new wave per node per round
    if n > 1:
        assert st["max_link_load"] == 1
        assert st["max_new_per_node"] == 1
    # the start rounds of two waves differ by more than the distance of the sources
    for u in range(n):
        for v in range(n):
            if u != v:
                assert abs(st["start"][u] - st["start"][v]) >= oracle[u][v] + 1
    # the round bounds
    assert st["setup_rounds"] <= 2 * ecc_root + 2
    assert st["rounds"] <= st["setup_rounds"] + 3 * n + diam - 3 + (1 if n == 1 else 0)
    return st


def test_example() -> None:
    edges = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (4, 5)]
    st = check(6, edges)
    assert st["setup_rounds"] == 8
    assert st["start"] == [9, 11, 23, 13, 15, 17]
    assert st["rounds"] == 25


def test_random_graphs() -> None:
    rng = random.Random(5)
    for _ in range(120):
        n = rng.randrange(1, 30)
        check(n, random_connected(n, rng.random() * 0.3, rng))


def test_paths_cycles_stars() -> None:
    for n in range(2, 30):
        check(n, [(i, i + 1) for i in range(n - 1)])
        check(n, [(0, i) for i in range(1, n)])
        if n >= 3:
            check(n, [(i, (i + 1) % n) for i in range(n)])


def test_counting_bound_graph() -> None:
    rng = random.Random(9)
    for _ in range(20):
        bits = [rng.randrange(2) for _ in range(rng.randrange(1, 25))]
        n, edges = leaf_lower_bound_graph(bits)
        st = check(n, edges)
        # the leaf 0 learns every bit through its one link
        assert [3 - st["dist"][0][3 + i] for i in range(len(bits))] == bits
