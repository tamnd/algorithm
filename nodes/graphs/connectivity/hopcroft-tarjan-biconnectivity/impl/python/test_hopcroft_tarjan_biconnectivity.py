# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hopcroft-tarjan-biconnectivity/. The authors are listed in prov/B1ZMBY.jsonl.

import random

from hopcroft_tarjan_biconnectivity import biconnectivity


def count_components(n: int, alive: list[bool], edges: list[tuple[int, int]]) -> int:
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        if alive[u] and alive[v]:
            parent[find(u)] = find(v)
    return len({find(v) for v in range(n) if alive[v]})


def oracle(n: int, edges: list[tuple[int, int]]):
    """Articulation points and bridges by removal; blocks by Menger on the subdivision."""
    every = [True] * n
    c = count_components(n, every, edges)
    aps = []
    for v in range(n):
        alive = [x != v for x in range(n)]
        if count_components(n, alive, edges) > c:
            aps.append(v)
    bridges = [
        i
        for i, (u, v) in enumerate(edges)
        if u != v and count_components(n, every, edges[:i] + edges[i + 1 :]) > c
    ]
    # Subdivide edge i by the vertex n + i. Two non-loop edges i, j lie on a common
    # cycle iff n + i and n + j are joined after the removal of any one other vertex.
    m = len(edges)
    sub = []
    for i, (u, v) in enumerate(edges):
        if u != v:
            sub += [(u, n + i), (n + i, v)]
    big = n + m
    real = [i for i in range(m) if edges[i][0] != edges[i][1]]
    label = {i: i for i in range(m)}

    def joined(a: int, b: int, cut: int) -> bool:
        alive = [x != cut for x in range(big)]
        parent = list(range(big))

        def find(x: int) -> int:
            while parent[x] != x:
                x = parent[x]
            return x

        for x, y in sub:
            if alive[x] and alive[y]:
                parent[find(x)] = find(y)
        return find(a) == find(b)

    for a in real:
        for b in real:
            if a < b and all(
                joined(n + a, n + b, x) for x in range(-1, big) if x not in (n + a, n + b)
            ):
                la, lb = label[a], label[b]
                for k in label:
                    if label[k] == lb:
                        label[k] = la
    groups: dict[int, list[int]] = {}
    for i in range(m):
        groups.setdefault(label[i], []).append(i)
    blocks = sorted(sorted(g) for g in groups.values())
    return aps, bridges, blocks


def check(n: int, edges: list[tuple[int, int]]) -> None:
    aps, bridges, blocks = biconnectivity(n, edges)
    want_aps, want_bridges, want_blocks = oracle(n, edges)
    assert aps == want_aps
    assert bridges == want_bridges
    assert sorted(blocks) == want_blocks


def test_example() -> None:
    edges = [(0, 1), (0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 5), (5, 3), (5, 6), (6, 6)]
    aps, bridges, blocks = biconnectivity(7, edges)
    assert aps == [2, 3, 5]
    assert bridges == [4, 8]
    assert blocks == [[9], [8], [5, 6, 7], [4], [0, 1, 2, 3]]
    check(7, edges)


def test_edges() -> None:
    assert biconnectivity(0, []) == ([], [], [])
    assert biconnectivity(1, []) == ([], [], [])
    assert biconnectivity(1, [(0, 0), (0, 0)]) == ([], [], [[0], [1]])
    assert biconnectivity(2, [(0, 1)]) == ([], [0], [[0]])
    assert biconnectivity(2, [(0, 1), (1, 0)]) == ([], [], [[0, 1]])
    assert biconnectivity(3, [(0, 1), (1, 2)]) == ([1], [0, 1], [[1], [0]])
    star = [(0, i) for i in range(1, 5)]
    assert biconnectivity(5, star)[0] == [0]
    bowtie = [(0, 1), (1, 2), (2, 0), (0, 3), (3, 4), (4, 0)]
    assert biconnectivity(5, bowtie)[0] == [0]
    check(4, [(1, 2), (2, 3), (3, 1)])


def test_long_path() -> None:
    n = 20000
    edges = [(i, i + 1) for i in range(n - 1)]
    aps, bridges, blocks = biconnectivity(n, edges)
    assert aps == list(range(1, n - 1))
    assert bridges == list(range(n - 1)) and len(blocks) == n - 1


def test_random() -> None:
    rng = random.Random(1973)
    for _ in range(600):
        n = rng.randint(1, 7)
        m = rng.randint(0, 10)
        edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(m)]
        check(n, edges)
