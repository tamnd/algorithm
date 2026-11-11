# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-connected-components/. The authors are listed in prov/BCTDPX.jsonl.

import math
import random
from collections import deque

from distributed_connected_components import (
    boruvka_components,
    budget,
    label_propagation,
    union_find_labels,
)

EXAMPLE = [(0, 4), (4, 2), (2, 6), (1, 5), (5, 7), (7, 1)]  # node 3 is alone


def random_graph(n: int, p: float, rng: random.Random) -> list[tuple[int, int]]:
    return [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < p]


def same_partition(a: list[int], b: list[int]) -> bool:
    return all((a[u] == a[v]) == (b[u] == b[v]) for u in range(len(a)) for v in range(len(a)))


def hop_dist(n: int, edges: list[tuple[int, int]], s: int) -> list[int]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    d = [-1] * n
    d[s] = 0
    q = deque([s])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if d[v] < 0:
                d[v] = d[u] + 1
                q.append(v)
    return d


def test_example() -> None:
    lp = label_propagation(8, EXAMPLE)
    assert lp["labels"] == [0, 1, 0, 3, 0, 1, 0, 1]
    assert lp["last_change"] == 3  # node 6 is 3 hops from node 0
    bo = boruvka_components(8, EXAMPLE)
    assert same_partition(bo["labels"], union_find_labels(8, EXAMPLE))
    assert bo["fragments"] == [8, 3, 3, 3]
    assert bo["rounds"] == 3 * (3 * 8 + 2)


def test_label_propagation_matches_union_find() -> None:
    rng = random.Random(4)
    for _ in range(200):
        n = rng.randrange(1, 30)
        g = random_graph(n, rng.random() * 0.2, rng)
        st = label_propagation(n, g)
        uf = union_find_labels(n, g)
        assert st["labels"] == uf
        # the last change happens exactly when the farthest node hears its minimum
        far = 0
        for root in set(uf):
            d = hop_dist(n, g, root)
            far = max(far, max(x for x in d if x >= 0))
        assert st["last_change"] == far
        assert st["messages"] <= 2 * len(g) * (far + 1)


def test_boruvka_matches_union_find() -> None:
    rng = random.Random(8)
    for _ in range(120):
        n = rng.randrange(1, 26)
        g = random_graph(n, rng.random() * 0.25, rng)
        st = boruvka_components(n, g)
        uf = union_find_labels(n, g)
        assert same_partition(st["labels"], uf)
        c = len(set(uf))
        # the fragments that are not yet components at least halve in each phase
        for a, b in zip(st["fragments"], st["fragments"][1:]):
            assert b - c <= (a - c) // 2
        phases = math.ceil(math.log2(n)) if n > 1 else 0
        assert st["rounds"] == phases * (3 * n + 2)
        assert all(m <= 2 * len(g) + 4 * n for m in st["phase_messages"])
        assert st["max_bits"] <= budget(n)


def test_path_is_slow_for_label_propagation() -> None:
    # a path whose smallest identifier is at one end: n - 1 rounds
    for n in range(2, 40):
        st = label_propagation(n, [(i, i + 1) for i in range(n - 1)])
        assert st["last_change"] == n - 1
