# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/eppstein-galil-italiano-nissenzweig/. The authors are listed in prov/7VG548.jsonl.

import random

from eppstein_galil_italiano_nissenzweig import SparsifiedMSF


def _msf(n: int, edges: dict[int, tuple[int, int, float]]) -> set[int]:
    """Static Kruskal on the whole current graph, ties broken by id."""
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    out = set()
    for e in sorted(edges, key=lambda e: (edges[e][2], e)):
        u, v, _ = edges[e]
        a, b = find(u), find(v)
        if a != b:
            parent[a] = b
            out.add(e)
    return out


def test_example() -> None:
    s = SparsifiedMSF(4)
    ids = {}
    for name, (u, v, w) in {"01": (0, 1, 1), "02": (0, 2, 5), "03": (0, 3, 4),
                            "12": (1, 2, 2), "13": (1, 3, 6), "23": (2, 3, 3)}.items():
        ids[name] = s.insert(u, v, w)
    assert s.weight() == 6
    s.delete(ids["12"])
    assert s.weight() == 8
    assert {s.edges[e][:2] for e in s.forest()} == {(0, 1), (2, 3), (0, 3)}


def test_random_against_kruskal() -> None:
    rng = random.Random(31)
    for _ in range(500):
        n = rng.randint(1, 7)
        s = SparsifiedMSF(n)
        alive: list[int] = []
        for _ in range(rng.randint(0, 40)):
            if alive and rng.random() < 0.4:
                e = alive.pop(rng.randrange(len(alive)))
                s.delete(e)
            else:
                u, v = rng.randrange(n), rng.randrange(n)
                alive.append(s.insert(u, v, rng.randint(1, 6)))
            assert set(s.forest()) == _msf(n, s.edges)
            # every node holds a forest, so at most n - 1 edges
            assert all(len(c) <= max(0, n - 1) for c in s.cert)


def test_dense_graph() -> None:
    rng = random.Random(5)
    n = 30
    s = SparsifiedMSF(n)
    ids = [s.insert(u, v, rng.random()) for u in range(n) for v in range(u + 1, n)]
    rng.shuffle(ids)
    for e in ids[:200]:
        s.delete(e)
        assert set(s.forest()) == _msf(n, s.edges)
