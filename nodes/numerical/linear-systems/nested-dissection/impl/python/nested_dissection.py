# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nested-dissection/. The authors are listed in prov/F4FW9V.jsonl.

"""Nested dissection orderings of a sparse symmetric matrix.

A graph is a list adj with adj[v] the neighbours of v (no self loops).
An ordering is a list order; vertex order[k] is eliminated k-th.

nested_dissection works on any graph, with separators taken from breadth-first
level structures (George and Liu's automatic nested dissection, simplified).
grid_nested_dissection orders a k1 x k2 grid by geometric line separators.
Both are iterative: the dissection tree is processed with an explicit stack.
"""

from collections import deque


def graph_from_edges(n: int, edges) -> list[list[int]]:
    adj = [set() for _ in range(n)]
    for v, w in edges:
        if v != w:
            adj[v].add(w)
            adj[w].add(v)
    return [sorted(s) for s in adj]


def grid_graph(k1: int, k2: int) -> list[list[int]]:
    """5-point grid with k1 rows and k2 columns, vertex i * k2 + j."""
    e = []
    for i in range(k1):
        for j in range(k2):
            v = i * k2 + j
            if j + 1 < k2:
                e.append((v, v + 1))
            if i + 1 < k1:
                e.append((v, v + k2))
    return graph_from_edges(k1 * k2, e)


def _bfs_levels(adj, root, inside):
    seen = {root}
    levels = [[root]]
    while True:
        nxt = []
        for v in levels[-1]:
            for w in adj[v]:
                if w in inside and w not in seen:
                    seen.add(w)
                    nxt.append(w)
        if not nxt:
            return levels
        levels.append(nxt)


def _components(adj, inside):
    left = set(inside)
    comps = []
    while left:
        s = min(left)
        left.discard(s)
        comp, q = [s], deque([s])
        while q:
            v = q.popleft()
            for w in adj[v]:
                if w in left:
                    left.discard(w)
                    comp.append(w)
                    q.append(w)
        comps.append(comp)
    return comps


def level_separator(adj, part):
    """A vertex separator of the connected subgraph induced by part: the middle
    level of a breadth-first level structure from a pseudo-peripheral vertex,
    trimmed to the vertices with a neighbour in the next level."""
    inside = set(part)
    r = min(part, key=lambda v: (sum(w in inside for w in adj[v]), v))
    levels = _bfs_levels(adj, r, inside)
    while True:  # pseudo-peripheral root (George and Liu)
        x = min(levels[-1], key=lambda v: (sum(w in inside for w in adj[v]), v))
        lx = _bfs_levels(adj, x, inside)
        if len(lx) <= len(levels):
            break
        levels = lx
    if len(levels) < 3:
        return None
    half, acc, mid = len(part) / 2, 0, 1
    for i, lev in enumerate(levels):
        acc += len(lev)
        if acc >= half:
            mid = min(max(i, 1), len(levels) - 2)
            break
    nxt = set(levels[mid + 1])
    return [v for v in levels[mid] if any(w in nxt for w in adj[v])]


def _local_minimum_degree(adj, part):
    inside = set(part)
    g = {v: {w for w in adj[v] if w in inside} for v in part}
    out = []
    while g:
        v = min(g, key=lambda x: (len(g[x]), x))
        nb = g.pop(v)
        for w in nb:
            g[w].discard(v)
            g[w] |= nb - {w}
        out.append(v)
    return out


def nested_dissection(adj, leaf: int = 8, separators=None) -> list[int]:
    """Nested dissection order of all vertices. Parts with at most leaf vertices,
    or without a level separator, are ordered by minimum degree.
    If separators is a list, the separators found are appended to it."""
    n = len(adj)
    order: list[int] = []  # @line L1
    stack = [("split", list(range(n)))]
    while stack:  # @line L2
        kind, part = stack.pop()  # @line L3
        if kind == "emit":  # @line L4
            order.extend(part)
            continue
        comps = _components(adj, part)  # @line L5
        if len(comps) > 1:
            for c in reversed(comps):
                stack.append(("split", c))
            continue
        sep = level_separator(adj, part) if len(part) > leaf else None
        if sep is None:  # @line L6
            order.extend(_local_minimum_degree(adj, part))
            continue
        if separators is not None:
            separators.append(sep)
        rest = set(part) - set(sep)  # @line L7
        pieces = _components(adj, rest)  # @line L8
        stack.append(("emit", sep))  # @line L9
        for c in reversed(pieces):
            stack.append(("split", c))
    return order  # @line L10


def grid_nested_dissection(k1: int, k2: int, leaf: int = 1) -> list[int]:
    """Geometric nested dissection of the k1 x k2 grid: split the longer side by
    its middle line, order both halves, then the line."""
    order: list[int] = []
    stack = [("split", 0, k1, 0, k2)]
    while stack:
        task = stack.pop()
        if task[0] == "emit":
            order.extend(task[1])
            continue
        _, r0, r1, c0, c1 = task
        h, w = r1 - r0, c1 - c0
        if h <= 0 or w <= 0:
            continue
        if h * w <= leaf or (h <= 2 and w <= 2):
            order.extend(i * k2 + j for i in range(r0, r1) for j in range(c0, c1))
            continue
        if h >= w:
            m = r0 + h // 2
            line = [m * k2 + j for j in range(c0, c1)]
            halves = [(r0, m, c0, c1), (m + 1, r1, c0, c1)]
        else:
            m = c0 + w // 2
            line = [i * k2 + m for i in range(r0, r1)]
            halves = [(r0, r1, c0, m), (r0, r1, m + 1, c1)]
        stack.append(("emit", line))
        for a, b, c, d in reversed(halves):
            stack.append(("split", a, b, c, d))
    return order


def _numbers(order):
    f = [0] * len(order)
    for k, v in enumerate(order):
        f[v] = k
    return f


def cholesky_pattern(adj, order) -> list[set[int]]:
    """Exact symbolic Cholesky: cols[k] = rows i > k with l_ik != 0 (new numbers)."""
    f = _numbers(order)
    n = len(adj)
    later = [set(f[w] for w in adj[v]) for v in order]
    cols = []
    for k in range(n):
        s = {i for i in later[k] if i > k}
        cols.append(s)
        for i in s:
            later[i] |= s - {i}
    return cols


def fill_and_flops(adj, order) -> tuple[int, int]:
    """(nonzeros of L below the diagonal, sum_k c_k^2)."""
    cols = cholesky_pattern(adj, order)
    return sum(len(c) for c in cols), sum(len(c) ** 2 for c in cols)


def cholesky_float(a, order):
    """Cholesky of P A P^T in floating point (dense storage, sparse loops)."""
    import math
    n = len(a)
    b = [[float(a[i][j]) for j in order] for i in order]
    for k in range(n):
        if b[k][k] <= 0:
            raise ValueError("not positive definite")
        d = math.sqrt(b[k][k])
        b[k][k] = d
        col = [i for i in range(k + 1, n) if b[i][k] != 0]
        for i in col:
            b[i][k] /= d
        for j in col:
            ljk = b[j][k]
            for i in col:
                if i >= j:
                    b[i][j] -= b[i][k] * ljk
    return [[b[i][j] if j <= i else 0.0 for j in range(n)] for i in range(n)]
