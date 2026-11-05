# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/online-bridge-finding/. The authors are listed in prov/6AA8GQ.jsonl.

import random

from online_bridge_finding import OnlineBridges


def _static(n: int, edges: list[tuple[int, int]]) -> tuple[int, list[int], list[int]]:
    """Bridges by an iterative low-link DFS; returns (count, 2ECC labels, CC labels)."""
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        adj[u].append((v, i))
        adj[v].append((u, i))
    tin = [-1] * n
    low = [0] * n
    is_bridge = [False] * len(edges)
    timer = 0
    for s in range(n):
        if tin[s] != -1:
            continue
        tin[s] = low[s] = timer
        timer += 1
        stack = [(s, -1, 0)]
        while stack:
            v, pe, i = stack.pop()
            if i < len(adj[v]):
                stack.append((v, pe, i + 1))
                w, e = adj[v][i]
                if e == pe:
                    continue
                if tin[w] == -1:
                    tin[w] = low[w] = timer
                    timer += 1
                    stack.append((w, e, 0))
                else:
                    low[v] = min(low[v], tin[w])
            elif pe != -1:
                u = edges[pe][0] if edges[pe][1] == v else edges[pe][1]
                low[u] = min(low[u], low[v])
                if low[v] > tin[u]:
                    is_bridge[pe] = True

    def label(skip_bridges: bool) -> list[int]:
        lab = [-1] * n
        for s in range(n):
            if lab[s] == -1:
                lab[s] = s
                st = [s]
                while st:
                    x = st.pop()
                    for y, e in adj[x]:
                        if lab[y] == -1 and not (skip_bridges and is_bridge[e]):
                            lab[y] = s
                            st.append(y)
        return lab

    return sum(is_bridge), label(True), label(False)


def test_example() -> None:
    g = OnlineBridges(7)
    counts = []
    for u, v in [(0, 1), (1, 2), (2, 3), (3, 4), (1, 5), (5, 6), (4, 2), (6, 0), (3, 3), (0, 1)]:
        g.add_edge(u, v)
        counts.append(g.bridges)
    assert counts == [1, 2, 3, 4, 5, 6, 4, 1, 1, 1]
    assert g.is_bridge(2, 1) and not g.is_bridge(0, 6)


def test_random_against_static() -> None:
    rng = random.Random(99)
    for _ in range(500):
        n = rng.randint(1, 9)
        g = OnlineBridges(n)
        edges: list[tuple[int, int]] = []
        for _ in range(rng.randint(0, 14)):
            u, v = rng.randrange(n), rng.randrange(n)
            g.add_edge(u, v)
            edges.append((u, v))
            cnt, ecc, cc = _static(n, edges)
            assert g.bridges == cnt
            for a in range(n):
                for b in range(n):
                    assert g.two_edge_connected(a, b) == (ecc[a] == ecc[b])
                    assert g.connected(a, b) == (cc[a] == cc[b])


def test_long_path_then_cycle() -> None:
    n = 20000
    g = OnlineBridges(n)
    for i in range(n - 1):
        g.add_edge(i, i + 1)
    assert g.bridges == n - 1
    g.add_edge(0, n - 1)
    assert g.bridges == 0
