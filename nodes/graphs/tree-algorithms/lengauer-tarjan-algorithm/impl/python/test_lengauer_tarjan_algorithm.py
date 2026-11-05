# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lengauer-tarjan-algorithm/. The authors are listed in prov/206HCM.jsonl.

import random

import pytest

from lengauer_tarjan_algorithm import lengauer_tarjan, semidominators

EDGES = [(0, 1), (1, 2), (2, 3), (2, 4), (3, 4), (3, 7), (4, 5), (5, 6), (6, 3), (7, 8), (8, 6)]


def reach(n: int, succ: list[list[int]], root: int, banned: int) -> set[int]:
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


def brute_idom(n: int, edges: list[tuple[int, int]], root: int) -> list[int]:
    succ: list[list[int]] = [[] for _ in range(n)]
    for a, b in edges:
        succ[a].append(b)
    full = reach(n, succ, root, -1)
    dom = {v: {v} for v in full}
    for d in full:
        r = reach(n, succ, root, d)
        for v in full:
            if v not in r:
                dom[v].add(d)
    out = [-1] * n
    for v in full:
        if v != root:
            strict = dom[v] - {v}
            out[v] = max(strict, key=lambda x: len(dom[x]))
    return out


def test_page_example() -> None:
    assert lengauer_tarjan(9, EDGES, 0) == [-1, 0, 1, 2, 2, 4, 2, 3, 7]
    assert semidominators(9, EDGES, 0) == [-1, 0, 1, 2, 2, 4, 3, 3, 7]


def test_single_vertex() -> None:
    assert lengauer_tarjan(1, [], 0) == [-1]
    assert lengauer_tarjan(1, [(0, 0)], 0) == [-1]


def test_star_and_diamond() -> None:
    n = 8
    edges = [(0, v) for v in range(1, n)] + [(3, 4), (4, 5), (7, 1)]
    assert lengauer_tarjan(n, edges, 0) == [-1] + [0] * (n - 1)
    assert lengauer_tarjan(4, [(0, 1), (0, 2), (1, 3), (2, 3)], 0) == [-1, 0, 0, 0]


def test_unreachable_and_other_root() -> None:
    edges = [(0, 1), (1, 2), (3, 2), (2, 0)]
    assert lengauer_tarjan(4, edges, 0) == [-1, 0, 1, -1]
    assert lengauer_tarjan(4, edges, 3) == [2, 0, 3, -1]


def test_long_paths() -> None:
    n = 100_000
    path = [(i, i + 1) for i in range(n - 1)]
    assert lengauer_tarjan(n, path, 0) == [-1] + list(range(n - 1))
    # back edges to the root and bypass edges around every vertex
    idom = lengauer_tarjan(n, path + [(i, 0) for i in range(n)], 0)
    assert idom == [-1] + list(range(n - 1))
    idom = lengauer_tarjan(n, path + [(i, i + 2) for i in range(n - 2)], 0)
    assert idom == [-1] + [0] * (n - 1)
    # edges from the far end back to every vertex: EVAL climbs and compresses
    # long forest paths, and the answer is still the path itself
    idom = lengauer_tarjan(n, path + [(n - 1, i) for i in range(1, n - 1)], 0)
    assert idom == [-1] + list(range(n - 1))
    # the root also enters the far end of a long cycle: idom of the far end is 0
    idom = lengauer_tarjan(n, path + [(0, n - 1), (n - 1, 1)], 0)
    assert idom == [-1, 0] + list(range(1, n - 2)) + [0]


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        lengauer_tarjan(0, [], 0)
    with pytest.raises(ValueError):
        lengauer_tarjan(2, [(0, 3)], 0)
    with pytest.raises(ValueError):
        lengauer_tarjan(2, [], 2)


def test_random_against_brute_force() -> None:
    rng = random.Random(29)
    for _ in range(800):
        n = rng.randint(1, 12)
        m = rng.randint(0, 3 * n)
        edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(m)]
        root = rng.randrange(n)
        assert lengauer_tarjan(n, edges, root) == brute_idom(n, edges, root)
