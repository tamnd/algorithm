# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/holm-de-lichtenberg-thorup/. The authors are listed in prov/4DN5PG.jsonl.

import random

from holm_de_lichtenberg_thorup import DynamicConnectivity


def _components(n: int, edges: list[tuple[int, int]]) -> list[int]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    lab = [-1] * n
    for s in range(n):
        if lab[s] == -1:
            lab[s] = s
            st = [s]
            while st:
                x = st.pop()
                for y in adj[x]:
                    if lab[y] == -1:
                        lab[y] = s
                        st.append(y)
    return lab


def test_example() -> None:
    g = DynamicConnectivity(6)
    for u, v in [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 5), (5, 3)]:
        g.insert(u, v)
    assert g.connected(0, 5)
    g.delete(2, 3)
    assert not g.connected(0, 5)
    assert g.connected(3, 5)
    g.delete(0, 1)
    assert g.connected(0, 1)
    g.insert(1, 4)
    g.delete(3, 4)
    assert g.connected(0, 3)


def test_random_against_static() -> None:
    rng = random.Random(4)
    for _ in range(300):
        n = rng.randint(1, 10)
        g = DynamicConnectivity(n, seed=rng.randrange(1000))
        edges: list[tuple[int, int]] = []
        for _ in range(rng.randint(0, 60)):
            if edges and rng.random() < 0.45:
                u, v = edges.pop(rng.randrange(len(edges)))
                if rng.random() < 0.5:
                    u, v = v, u
                g.delete(u, v)
            else:
                u, v = rng.randrange(n), rng.randrange(n)
                g.insert(u, v)
                edges.append((u, v))
            lab = _components(n, edges)
            for a in range(n):
                for b in range(n):
                    assert g.connected(a, b) == (lab[a] == lab[b])
            g.check_invariants()


def test_larger_random() -> None:
    rng = random.Random(8)
    n = 120
    g = DynamicConnectivity(n)
    edges: list[tuple[int, int]] = []
    for _ in range(1500):
        if edges and rng.random() < 0.4:
            u, v = edges.pop(rng.randrange(len(edges)))
            g.delete(u, v)
        else:
            u, v = rng.randrange(n), rng.randrange(n)
            g.insert(u, v)
            edges.append((u, v))
        lab = _components(n, edges)
        a, b = rng.randrange(n), rng.randrange(n)
        assert g.connected(a, b) == (lab[a] == lab[b])
    g.check_invariants()
