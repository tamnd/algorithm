# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/frederickson-topology-trees/. The authors are listed in prov/ZS0KCA.jsonl.

import math
import random

from frederickson_topology_trees import DynamicMSF, _key, build_topology_tree


def _kruskal(n: int, weight: dict[tuple[int, int], float]) -> set[tuple[int, int]]:
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    out = set()
    for e in sorted(weight, key=lambda e: _key(e[0], e[1], weight[e])):
        a, b = find(e[0]), find(e[1])
        if a != b:
            parent[a] = b
            out.add(e)
    return out


def _check_clusters(d: DynamicMSF) -> None:
    for c, vs in d.members.items():
        assert vs and all(d.cid[v] == c for v in vs)
        s = next(iter(vs))
        assert d._reach_in_cluster(s, c) == vs  # each cluster is connected in F
    assert sum(len(vs) for vs in d.members.values()) == d.n
    for p, es in d.table.items():
        for e in es:
            assert d._pair(e) == p and e in d.nontree


def test_example() -> None:
    d = DynamicMSF(4)
    for u, v, w in [(0, 1, 1), (0, 2, 5), (0, 3, 4), (1, 2, 2), (1, 3, 6), (2, 3, 3)]:
        d.insert(u, v, w)
    assert d.forest() == {(0, 1), (1, 2), (2, 3)} and d.total() == 6
    d.delete(1, 2)
    assert d.forest() == {(0, 1), (2, 3), (0, 3)} and d.total() == 8


def test_random_against_kruskal() -> None:
    rng = random.Random(4)
    for trial in range(500):
        n = rng.randint(1, 14)
        d = DynamicMSF(n)
        weight: dict[tuple[int, int], float] = {}
        for _ in range(rng.randint(1, 40)):
            if weight and rng.random() < 0.4:
                e = rng.choice(list(weight))
                del weight[e]
                d.delete(*e)
            else:
                u, v = rng.randrange(n), rng.randrange(n)
                if u == v or (min(u, v), max(u, v)) in weight:
                    continue
                w = rng.randint(1, 6)
                weight[(min(u, v), max(u, v))] = w
                d.insert(u, v, w)
            assert d.forest() == _kruskal(n, weight)
            if trial % 5 == 0:
                _check_clusters(d)


def test_larger_graph() -> None:
    rng = random.Random(8)
    n = 60
    d = DynamicMSF(n)
    weight: dict[tuple[int, int], float] = {}
    for step in range(1500):
        if weight and rng.random() < 0.45:
            e = rng.choice(list(weight))
            del weight[e]
            d.delete(*e)
        else:
            u, v = rng.randrange(n), rng.randrange(n)
            if u == v or (min(u, v), max(u, v)) in weight:
                continue
            w = rng.random()
            weight[(min(u, v), max(u, v))] = w
            d.insert(u, v, w)
        if step % 10 == 0:
            assert d.forest() == _kruskal(n, weight)
            _check_clusters(d)
            assert all(len(vs) <= d.z for vs in d.members.values())


def _check_levels(n: int, edges: list[tuple[int, int]], levels) -> None:
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    for i, lev in enumerate(levels):
        assert sorted(v for c in lev for v in c) == list(range(n))
        for c in lev:
            ext = sum(1 for v in c for y in adj[v] if y not in c)
            assert ext <= 3
            s = next(iter(c))
            seen, st = {s}, [s]
            while st:
                x = st.pop()
                for y in adj[x]:
                    if y in c and y not in seen:
                        seen.add(y)
                        st.append(y)
            assert seen == c
            if i:
                kids = [k for k in levels[i - 1] if k <= c]
                assert 1 <= len(kids) <= 2 and frozenset().union(*kids) == c


def _random_tree_deg3(rng: random.Random, n: int) -> list[tuple[int, int]]:
    deg = [0] * n
    edges = []
    for v in range(1, n):
        u = rng.choice([x for x in range(v) if deg[x] < 3])
        deg[u] += 1
        deg[v] += 1
        edges.append((u, v))
    return edges


def test_topology_tree() -> None:
    rng = random.Random(2)
    for _ in range(300):
        n = rng.randint(1, 40)
        edges = _random_tree_deg3(rng, n)
        levels = build_topology_tree(n, edges)
        _check_levels(n, edges, levels)
        assert len(levels[-1]) == 1
        assert len(levels) <= 4 * math.log2(n + 1) + 4
    n = 1024
    path = [(i, i + 1) for i in range(n - 1)]
    assert len(build_topology_tree(n, path)) == 11
