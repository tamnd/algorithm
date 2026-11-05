# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/karger-klein-tarjan-mst/. The authors are listed in prov/YYGGT8.jsonl.

import random


def karger_klein_tarjan_mst(
    n: int, edges: list[tuple[int, int, float]], rng: random.Random | None = None
) -> list[int]:
    """Return the indices of a minimum spanning forest, by Karger, Klein and Tarjan.

    The vertices are 0 .. n - 1 and edges[i] = (u, v, w) is an undirected
    edge. Weights may tie (ties are broken by the edge index, so the answer
    is the unique forest that is minimum for the order by (w, i)); the graph
    may be disconnected, and parallel edges and self-loops are allowed.

    The algorithm is random, but its answer is not: the coins only change
    the running time. Each call does two Boruvka steps, samples half of the
    remaining edges, solves the sample, drops the edges that the sample's
    forest proves heavy, and solves the rest.

    Cost: this version checks heaviness with binary lifting instead of a
    linear-time verification algorithm, so it takes O(m log n) expected
    time instead of O(m); O(n + m) expected space.
    """
    rng = rng if rng is not None else random.Random()
    work = [(u, v, (w, i)) for i, (u, v, w) in enumerate(edges) if u != v]
    return sorted(_msf(n, work, rng))


def _msf(n, edges, rng):
    """Minimum spanning forest of a graph with distinct keys; original indices."""
    if not edges:  # @line L1
        return []
    chosen: list[int] = []
    for _ in range(2):  # @line L2
        n, edges, picked = _boruvka_step(n, edges)
        chosen += picked
        if not edges:
            return chosen
    sample = [e for e in edges if rng.random() < 0.5]  # @line L3
    forest = _msf(n, sample, rng)  # @line L4
    light = _drop_heavy(n, edges, set(forest))  # @line L5
    return chosen + _msf(n, light, rng)  # @line L6


def _boruvka_step(n, edges):
    """Pick the lightest edge at each vertex, contract, drop loops and isolated vertices."""
    best = [None] * n
    for e in edges:
        u, v, key = e
        for x in (u, v):
            if best[x] is None or key < best[x][2]:
                best[x] = e
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    picked = []
    for e in best:
        if e is None:
            continue
        a, b = find(e[0]), find(e[1])
        if a != b:
            parent[a] = b
            picked.append(e[2][1])
    label: dict[int, int] = {}
    out = []
    for u, v, key in edges:
        a, b = find(u), find(v)
        if a != b:
            a = label.setdefault(a, len(label))
            b = label.setdefault(b, len(label))
            out.append((a, b, key))
    return len(label), out, picked


def _drop_heavy(n, edges, forest_ids):
    """Keep the edges that are not F-heavy, where F is the forest given by its ids."""
    adj: list[list[tuple[int, tuple]]] = [[] for _ in range(n)]
    for u, v, key in edges:
        if key[1] in forest_ids:
            adj[u].append((v, key))
            adj[v].append((u, key))
    depth = [-1] * n
    root = [-1] * n
    up = [list(range(n))]
    mx: list[list[tuple | None]] = [[None] * n]
    for s in range(n):
        if depth[s] >= 0:
            continue
        depth[s] = 0
        root[s] = s
        stack = [s]
        while stack:
            x = stack.pop()
            for y, key in adj[x]:
                if depth[y] < 0:
                    depth[y] = depth[x] + 1
                    root[y] = s
                    up[0][y] = x
                    mx[0][y] = key
                    stack.append(y)
    j = 1
    while (1 << j) < n:
        prev_up, prev_mx = up[-1], mx[-1]
        up.append([prev_up[prev_up[x]] for x in range(n)])
        mx.append([_max(prev_mx[x], prev_mx[prev_up[x]]) for x in range(n)])
        j += 1

    def path_max(a, b):
        best = None
        if depth[a] < depth[b]:
            a, b = b, a
        d = depth[a] - depth[b]
        k = 0
        while d:
            if d & 1:
                best = _max(best, mx[k][a])
                a = up[k][a]
            d >>= 1
            k += 1
        if a == b:
            return best
        for k in range(len(up) - 1, -1, -1):
            if up[k][a] != up[k][b]:
                best = _max(best, _max(mx[k][a], mx[k][b]))
                a, b = up[k][a], up[k][b]
        return _max(best, _max(mx[0][a], mx[0][b]))

    keep = []
    for u, v, key in edges:
        if root[u] != root[v] or key <= path_max(u, v):
            keep.append((u, v, key))
    return keep


def _max(a, b):
    if a is None:
        return b
    if b is None:
        return a
    return a if a > b else b
