# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dominator-tree/. The authors are listed in prov/GK1MNC.jsonl.

import random

import pytest

from dominator_tree import DominatorTree

EDGES = [(0, 1), (1, 2), (2, 3), (2, 4), (3, 4), (3, 7), (4, 5), (5, 6), (6, 3), (7, 8), (8, 6)]


def reach(n: int, edges: list[tuple[int, int]], root: int, banned: int) -> set[int]:
    succ: list[list[int]] = [[] for _ in range(n)]
    for a, b in edges:
        succ[a].append(b)
    if banned == root:
        return set()
    seen = {root}
    stack = [root]
    while stack:
        v = stack.pop()
        for w in succ[v]:
            if w != banned and w not in seen:
                seen.add(w)
                stack.append(w)
    return seen


def brute_dominators(n: int, edges: list[tuple[int, int]], root: int) -> dict[int, set[int]]:
    full = reach(n, edges, root, -1)
    dom = {v: {v} for v in full}
    for d in range(n):
        if d in full:
            r = reach(n, edges, root, d)
            for v in full:
                if v not in r:
                    dom[v].add(d)
    return dom


def test_page_example() -> None:
    t = DominatorTree(9, EDGES, 0)
    assert t.idom == [-1, 0, 1, 2, 2, 4, 2, 3, 7]
    assert t.tin == [0, 1, 2, 3, 6, 7, 8, 4, 5]
    assert t.tout == [9, 9, 9, 6, 8, 8, 9, 6, 6]
    assert t.dominates(3, 8)
    assert not t.dominates(4, 6)
    assert not t.dominates(3, 6)
    assert t.dominates(2, 6)
    assert t.dominates(6, 6)
    assert t.dominators(8) == [8, 7, 3, 2, 1, 0]
    assert t.dominators(6) == [6, 2, 1, 0]


def test_single_vertex() -> None:
    t = DominatorTree(1, [], 0)
    assert t.idom == [-1]
    assert t.dominates(0, 0)
    assert t.dominators(0) == [0]


def test_star_and_diamond() -> None:
    n = 7
    edges = [(0, v) for v in range(1, n)] + [(1, 2), (2, 3), (5, 4)]
    t = DominatorTree(n, edges, 0)
    assert t.idom == [-1] + [0] * (n - 1)
    t = DominatorTree(4, [(0, 1), (0, 2), (1, 3), (2, 3)], 0)
    assert t.idom == [-1, 0, 0, 0]
    assert not t.dominates(1, 3)


def test_unreachable_and_loops() -> None:
    t = DominatorTree(5, [(0, 1), (1, 1), (1, 0), (3, 4), (4, 1)], 0)
    assert t.idom == [-1, 0, -1, -1, -1]
    assert t.reachable == [True, True, False, False, False]
    assert not t.dominates(0, 3)
    assert t.dominators(4) == []


def test_long_path() -> None:
    n = 100_000
    edges = [(i, i + 1) for i in range(n - 1)]
    t = DominatorTree(n, edges, 0)
    assert t.idom == [-1] + list(range(n - 1))
    assert t.dominates(10, n - 1)
    assert not t.dominates(n - 1, 10)
    edges2 = edges + [(i, i + 2) for i in range(n - 2)]
    t = DominatorTree(n, edges2, 0)
    # a path with a bypass edge around every vertex: nothing but the root dominates
    assert all(t.idom[v] == 0 for v in range(1, n))
    # a long cycle back to the root
    t = DominatorTree(n, edges + [(n - 1, 0)], 0)
    assert t.idom[n - 1] == n - 2


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        DominatorTree(0, [], 0)
    with pytest.raises(ValueError):
        DominatorTree(2, [(0, 2)], 0)
    t = DominatorTree(2, [(0, 1)], 0)
    with pytest.raises(IndexError):
        t.dominates(0, 5)


def test_random_against_brute_force() -> None:
    rng = random.Random(13)
    for _ in range(600):
        n = rng.randint(1, 12)
        m = rng.randint(0, 3 * n)
        edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(m)]
        root = rng.randrange(n)
        t = DominatorTree(n, edges, root)
        dom = brute_dominators(n, edges, root)
        for v in range(n):
            if v not in dom:
                assert t.idom[v] == -1 and not t.reachable[v]
                continue
            assert set(t.dominators(v)) == dom[v]
            if v != root:
                strict = dom[v] - {v}
                assert t.idom[v] in strict
                assert all(d in dom[t.idom[v]] for d in strict)
            for a in range(n):
                assert t.dominates(a, v) == (a in dom[v])
