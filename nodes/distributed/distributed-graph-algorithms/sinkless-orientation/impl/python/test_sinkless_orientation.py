# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sinkless-orientation/. The authors are listed in prov/T5PX1A.jsonl.

import random

from sinkless_orientation import edges, is_sinkless, random_orientation, repair, sinks


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


def cubic(n: int, rng: random.Random) -> list[list[int]]:
    """A 3-regular graph: a Hamiltonian cycle plus a random perfect matching (n even)."""
    while True:
        perm = list(range(n))
        rng.shuffle(perm)
        adj = ring(n)
        ok = True
        for i in range(0, n, 2):
            u, v = perm[i], perm[i + 1]
            if v in adj[u]:
                ok = False
                break
            adj[u].append(v)
            adj[v].append(u)
        if ok:
            return adj


def test_repair_gives_valid_orientations() -> None:
    rng = random.Random(81)
    families = [ring(30), grid(9, 9), random_tree(80, rng), bounded_degree(120, 3, rng), bounded_degree(120, 5, rng), cubic(100, rng)]
    for adj in families:
        for seed in range(5):
            start = random_orientation(adj, random.Random(seed))
            orient, _ = repair(adj, start)
            assert is_sinkless(adj, orient)
            # only edges on reversed paths changed, and no new sinks appeared
            assert sinks(adj, orient) == []


def test_random_start_has_about_one_eighth_sinks_on_cubic_graphs() -> None:
    rng = random.Random(82)
    adj = cubic(200, rng)
    total = sum(len(sinks(adj, random_orientation(adj, random.Random(s)))) for s in range(200))
    assert abs(total / (200 * 200) - 1 / 8) < 0.01


def test_checker_rejects_sinks_and_accepts_free_nodes() -> None:
    # K4: node 0 with all edges pointing in is a sink.
    adj = [[1, 2, 3], [0, 2, 3], [0, 1, 3], [0, 1, 2]]
    bad = {e: (0 if 0 in e else max(e)) for e in edges(adj)}
    assert sinks(adj, bad) == [0]
    assert not is_sinkless(adj, bad)
    good, moved = repair(adj, bad)
    assert is_sinkless(adj, good) and moved >= 1
    # On a path every node is free, so every orientation is accepted.
    path = [[1], [0, 2], [1]]
    assert is_sinkless(path, {(0, 1): 1, (1, 2): 1})


def test_a_tree_with_all_inner_degrees_three_uses_the_leaves() -> None:
    # A complete binary tree: inner nodes have degree 3 (the root has 2), and the leaves are free.
    # Both "all edges to the root" and "all edges to the leaves" are sinkless, since only free nodes are sinks.
    n = 63
    adj: list[list[int]] = [[] for _ in range(n)]
    for v in range(1, n):
        p = (v - 1) // 2
        adj[v].append(p)
        adj[p].append(v)
    toward_root = {(min(v, (v - 1) // 2), max(v, (v - 1) // 2)): (v - 1) // 2 for v in range(1, n)}
    assert is_sinkless(adj, toward_root)
    toward_leaves = {e: max(e) for e in edges(adj)}
    assert is_sinkless(adj, toward_leaves)
    orient, moved = repair(adj, toward_leaves)
    assert orient == toward_leaves and moved == 0
