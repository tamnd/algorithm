# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/block-cut-tree/. The authors are listed in prov/FD84D6.jsonl.

import random

from block_cut_tree import BlockCutTree


def joined(n: int, edges: list[tuple[int, int]], u: int, v: int, removed: int = -1) -> bool:
    adj: list[list[int]] = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    seen = {u}
    stack = [u]
    while stack:
        a = stack.pop()
        for b in adj[a]:
            if b != removed and b not in seen:
                seen.add(b)
                stack.append(b)
    return v in seen


def brute_same_block(n: int, edges: list[tuple[int, int]], u: int, v: int) -> bool:
    """Adjacent, or joined and not separated by any one other vertex (Menger)."""
    if any({a, b} == {u, v} for a, b in edges):
        return True
    if not joined(n, edges, u, v):
        return False
    return all(joined(n, edges, u, v, x) for x in range(n) if x not in (u, v))


def check(n: int, edges: list[tuple[int, int]]) -> None:
    t = BlockCutTree(n, edges)
    t.check_invariant()
    for u in range(n):
        for v in range(n):
            if u == v:
                continue
            assert t.same_block(u, v) == brute_same_block(n, edges, u, v)
            if not joined(n, edges, u, v):
                continue
            for x in range(n):
                if x not in (u, v):
                    assert t.separates(x, u, v) == (not joined(n, edges, u, v, x))


def test_example() -> None:
    edges = [(0, 1), (0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 5), (5, 3), (5, 6), (6, 6)]
    t = BlockCutTree(7, edges)
    t.check_invariant()
    assert t.blocks == [[5, 6], [3, 4, 5], [2, 3], [0, 1, 2]]
    assert t.cuts == [2, 3, 5]
    assert t.num_nodes == 7
    assert t.separates(3, 0, 6) and not t.separates(3, 4, 5)
    assert t.separates(2, 1, 4) and not t.separates(2, 0, 1)
    assert t.same_block(2, 3) and t.same_block(3, 5) and not t.same_block(2, 5)
    check(7, edges)


def test_edges() -> None:
    t = BlockCutTree(0, [])
    t.check_invariant()
    assert t.num_nodes == 0
    t = BlockCutTree(3, [(1, 1), (1, 1)])  # isolated vertices and loops only
    t.check_invariant()
    assert t.blocks == [[0], [1], [2]] and t.cuts == []
    check(3, [(1, 1)])
    check(2, [(0, 1), (0, 1)])
    check(4, [(0, 1), (0, 2), (0, 3)])  # a star: one cut node, three blocks
    check(5, [(0, 1), (1, 2), (2, 0), (0, 3), (3, 4), (4, 0)])  # a bowtie
    check(6, [(0, 1), (2, 3), (3, 4), (4, 2), (5, 5)])  # three components


def test_long_path() -> None:
    n = 20000
    t = BlockCutTree(n, [(i, i + 1) for i in range(n - 1)])
    t.check_invariant()
    assert len(t.cuts) == n - 2
    assert t.separates(n // 2, 0, n - 1) and not t.same_block(0, 2)


def test_random() -> None:
    rng = random.Random(1966)
    for _ in range(600):
        n = rng.randint(1, 7)
        m = rng.randint(0, 10)
        edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(m)]
        check(n, edges)
