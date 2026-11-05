# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/frederickson-planar-shortest-paths/. The authors are listed in prov/0AZZWY.jsonl.
import heapq
import random

import pytest

from frederickson_planar_shortest_paths import (
    INF,
    _boundary_search,
    _dijkstra,
    _pieces,
    shortest_paths,
)


def reference(n, arcs, s):
    out = [[] for _ in range(n)]
    for u, v, w in arcs:
        out[u].append((v, w))
    d = [INF] * n
    d[s] = 0
    heap = [(0, s)]
    while heap:
        dd, x = heapq.heappop(heap)
        if dd > d[x]:
            continue
        for y, w in out[x]:
            if dd + w < d[y]:
                d[y] = dd + w
                heapq.heappush(heap, (dd + w, y))
    return d


def random_triangulation(n, rng):
    faces = [(0, 1, 2), (0, 2, 1)]
    E = {(0, 1), (0, 2), (1, 2)}
    for v in range(3, n):
        i = rng.randrange(len(faces))
        a, b, c = faces[i]
        faces[i] = faces[-1]
        faces.pop()
        faces += [(a, b, v), (b, c, v), (c, a, v)]
        E |= {(min(a, v), max(a, v)), (min(b, v), max(b, v)), (min(c, v), max(c, v))}
    return sorted(E)


def both_ways(edges, w=1):
    return [(u, v, w) for u, v in edges] + [(v, u, w) for u, v in edges]


def complete(k):
    return [(i, j) for i in range(k) for j in range(i + 1, k)]


def grid_arcs(k, rng):
    arcs = []
    for i in range(k):
        for j in range(k):
            v = i * k + j
            if j + 1 < k:
                arcs += [(v, v + 1, rng.randint(1, 9)), (v + 1, v, rng.randint(1, 9))]
            if i + 1 < k:
                arcs += [(v, v + k, rng.randint(1, 9)), (v + k, v, rng.randint(1, 9))]
    return arcs


K33 = [(a, b) for a in range(3) for b in range(3, 6)]
SMALL = [
    ("single vertex", 1, [], 0),
    ("one edge", 2, both_ways([(0, 1)], 3), 1),
    ("K4", 4, both_ways(complete(4), 2), 0),
    ("K5, not planar", 5, both_ways(complete(5), 1), 3),
    ("K3,3, not planar", 6, both_ways(K33, 4), 0),
    ("star tree", 8, both_ways([(0, i) for i in range(1, 8)], 5), 3),
    ("path tree", 10, both_ways([(i, i + 1) for i in range(9)], 2), 4),
    ("isolated vertices", 6, both_ways([(0, 1), (2, 3)], 1), 0),
    ("one-way arcs", 4, [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 0, 1)], 2),
    ("zero lengths", 5, both_ways([(0, 1), (1, 2), (2, 3), (3, 4)], 0), 0),
]


@pytest.mark.parametrize("name,n,arcs,s", SMALL, ids=[c[0] for c in SMALL])
@pytest.mark.parametrize("r1,r2", [(None, None), (2, 2), (3, 2), (100, 100)])
def test_small(name, n, arcs, s, r1, r2):
    assert shortest_paths(n, arcs, s, r1, r2) == reference(n, arcs, s)


def test_k4_values():
    arcs = both_ways(complete(4), 2)
    assert shortest_paths(4, arcs, 0, 2, 2) == [0, 2, 2, 2]


def test_trace_example():
    lengths = {(0, 1): 2, (1, 2): 7, (3, 4): 1, (4, 5): 3, (6, 7): 4, (7, 8): 1,
               (0, 3): 5, (3, 6): 1, (1, 4): 1, (4, 7): 6, (2, 5): 1, (5, 8): 2}
    arcs = [(u, v, w) for (u, v), w in lengths.items()]
    arcs += [(v, u, w) for (u, v), w in lengths.items()]
    top = _pieces(range(9), arcs, 5, {0})
    assert [sorted(b) for _, _, b in top] == [[1, 2, 3], [0, 1, 2, 3]]
    tables = []
    for vs, al, bnd in top:
        rows = {}
        for b in bnd:
            d = _dijkstra(al, {b: 0})
            rows[b] = {x: d[x] for x in bnd if x != b and x in d}
        tables.append(rows)
    assert tables[0][1] == {2: 5, 3: 2}
    assert tables[1][0] == {1: 2, 2: 9, 3: 5}
    d = _boundary_search(top, tables, {0: 0})
    assert d == {0: 0, 1: 2, 2: 7, 3: 4}
    assert shortest_paths(9, arcs, 0, 5, 8) == [0, 2, 7, 4, 3, 6, 5, 9, 8]


def test_inner_tables_match_dijkstra():
    rng = random.Random(87)
    for _ in range(30):
        n = rng.randint(10, 80)
        arcs = [(u, v, rng.randint(0, 9)) for u, v in random_triangulation(n, rng)]
        arcs += [(v, u, w + 1) for u, v, w in arcs if rng.random() < 0.5]
        top = _pieces(range(n), arcs, 12, {0})
        for vs, al, bnd in top:
            small = _pieces(vs, al, 3, set(bnd))
            table = []
            for svs, sal, sbnd in small:
                rows = {}
                for b in sbnd:
                    d = _dijkstra(sal, {b: 0})
                    rows[b] = {x: d[x] for x in sbnd if x != b and x in d}
                table.append(rows)
            for b in bnd:
                got = _boundary_search(small, table, {b: 0})
                want = _dijkstra(al, {b: 0})
                for x in bnd:
                    assert got.get(x, INF) == want.get(x, INF)


def test_division_is_edge_partition():
    rng = random.Random(5)
    n = 300
    arcs = both_ways(random_triangulation(n, rng))
    pieces = _pieces(range(n), arcs, 20, {7})
    seen = []
    for vs, al, bnd in pieces:
        seen += al
        for u, v, _ in al:
            assert u in vs and v in vs
    assert sorted(seen) == sorted(arcs)
    count = {}
    for vs, _, _ in pieces:
        for x in vs:
            count[x] = count.get(x, 0) + 1
    for vs, _, bnd in pieces:
        assert set(bnd) == {x for x in vs if count[x] > 1 or x == 7}


def test_random_planar_digraphs():
    rng = random.Random(1987)
    for _ in range(300):
        n = rng.randint(1, 120)
        edges = random_triangulation(n, rng) if n >= 3 else ([(0, 1)] if n == 2 else [])
        rng.shuffle(edges)
        edges = edges[: rng.randint(0, len(edges))]
        arcs = []
        for u, v in edges:
            c = rng.random()
            if c < 0.4:
                arcs.append((u, v, rng.randint(0, 9)))
            elif c < 0.8:
                arcs.append((v, u, rng.randint(0, 9)))
            else:
                arcs += [(u, v, rng.randint(0, 9)), (v, u, rng.randint(0, 9))]
        s = rng.randrange(n)
        want = reference(n, arcs, s)
        for r1, r2 in [(None, None), (8, 2), (30, 4), (3, 2)]:
            assert shortest_paths(n, arcs, s, r1, r2) == want


def test_float_lengths():
    rng = random.Random(3)
    n = 200
    arcs = [(u, v, rng.random()) for u, v in random_triangulation(n, rng)]
    arcs += [(v, u, rng.random()) for u, v, _ in arcs]
    got = shortest_paths(n, arcs, 0, 10, 3)
    want = reference(n, arcs, 0)
    assert all(abs(a - b) < 1e-9 for a, b in zip(got, want))


def test_large_path():
    n = 100000
    arcs = [(i, i + 1, 1) for i in range(n - 1)]
    d = shortest_paths(n, arcs, 0)
    assert d[-1] == n - 1 and d[12345] == 12345
    d = shortest_paths(n, arcs, n - 1)
    assert d[n - 1] == 0 and d[0] == INF


def test_large_grid():
    rng = random.Random(11)
    k = 100
    arcs = grid_arcs(k, rng)
    assert shortest_paths(k * k, arcs, 0) == reference(k * k, arcs, 0)


def test_large_triangulation():
    rng = random.Random(12)
    n = 5000
    arcs = [(u, v, rng.randint(0, 20)) for u, v in random_triangulation(n, rng)]
    arcs += [(v, u, w) for u, v, w in arcs]
    assert shortest_paths(n, arcs, 17) == reference(n, arcs, 17)


def test_bad_input():
    with pytest.raises(ValueError):
        shortest_paths(3, [(0, 1, -1)], 0)
    with pytest.raises(ValueError):
        shortest_paths(3, [(0, 5, 1)], 0)
    with pytest.raises(ValueError):
        shortest_paths(3, [], 3)
