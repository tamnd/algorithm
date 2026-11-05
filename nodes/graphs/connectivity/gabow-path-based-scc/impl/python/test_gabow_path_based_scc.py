# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gabow-path-based-scc/. The authors are listed in prov/X5MM3D.jsonl.

import random

from gabow_path_based_scc import strong_components


def reach(n: int, edges: list[tuple[int, int]]) -> list[set[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    out = []
    for s in range(n):
        seen = {s}
        stack = [s]
        while stack:
            for w in adj[stack.pop()]:
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
        out.append(seen)
    return out


def check(n: int, edges: list[tuple[int, int]]) -> None:
    comp, c = strong_components(n, edges)
    r = reach(n, edges)
    assert sorted(set(comp)) == list(range(c))
    for u in range(n):
        for v in range(n):
            assert (comp[u] == comp[v]) == (v in r[u] and u in r[v])
    for u, v in edges:
        assert comp[u] >= comp[v]  # reverse topological numbering


def test_page_example() -> None:
    edges = [(0, 1), (1, 2), (2, 0), (2, 3), (1, 3), (3, 4), (4, 3),
             (4, 5), (0, 5), (5, 6), (6, 5), (6, 7), (7, 7)]
    assert strong_components(8, edges) == ([3, 3, 3, 2, 2, 1, 1, 0], 4)
    check(8, edges)


def test_edge_cases() -> None:
    assert strong_components(0, []) == ([], 0)
    assert strong_components(1, []) == ([0], 1)
    assert strong_components(1, [(0, 0), (0, 0)]) == ([0], 1)
    assert strong_components(2, [(0, 1), (0, 1)]) == ([1, 0], 2)
    assert strong_components(2, [(0, 1), (1, 0), (1, 0)]) == ([0, 0], 1)
    assert strong_components(3, []) == ([0, 1, 2], 3)
    check(4, [(0, 1), (1, 0), (2, 3), (3, 2), (1, 2)])


def test_long_path_and_cycle() -> None:
    n = 20000
    path = [(v, v + 1) for v in range(n - 1)]
    comp, c = strong_components(n, path)
    assert c == n and comp == [n - 1 - v for v in range(n)]
    comp, c = strong_components(n, path + [(n - 1, 0)])
    assert c == 1 and set(comp) == {0}
    back = [(v + 1, v) for v in range(n - 1)]
    comp, c = strong_components(n, path + back)
    assert c == 1


def test_random() -> None:
    rng = random.Random(2000)
    for _ in range(600):
        n = rng.randint(0, 9)
        m = rng.randint(0, 3 * n) if n else 0
        edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(m)]
        check(n, edges)
