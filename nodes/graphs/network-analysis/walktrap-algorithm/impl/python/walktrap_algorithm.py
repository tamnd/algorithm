# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/walktrap-algorithm/. The authors are listed in prov/78KW1X.jsonl.

import math


def modularity(
    n: int, edges: list[tuple[int, int, float]], parts: list[list[int]]
) -> float:
    """Return the modularity of a partition of an undirected weighted graph."""
    total = sum(w for _, _, w in edges)
    if total == 0:
        return 0.0
    label = [0] * n
    for c, part in enumerate(parts):
        for v in part:
            label[v] = c
    inside = [0.0] * len(parts)
    degree = [0.0] * len(parts)
    for u, v, w in edges:
        degree[label[u]] += w
        degree[label[v]] += w
        if label[u] == label[v]:
            inside[label[u]] += w
    return sum(inside[c] / total - (degree[c] / (2 * total)) ** 2 for c in range(len(parts)))


def walktrap(
    n: int,
    edges: list[tuple[int, int] | tuple[int, int, float]],
    t: int = 4,
) -> tuple[list[list[int]], list[tuple[int, int, float]]]:
    """Cluster an undirected graph by the Walktrap method of Pons and Latapy.

    The vertices are 0 .. n-1 and each edge is (u, v) with weight 1 or
    (u, v, w) with w > 0; self-loops in the input are not allowed. Every
    vertex gets an extra loop of weight 1. Walks have t steps.

    Returns (parts, merges): parts is the partition with the largest
    modularity among those of the dendrogram (the earliest one if several
    tie), each part sorted, parts sorted by smallest vertex; merges lists
    (a, b, delta_sigma) in merge order, where the community created by the
    k-th merge (counting from 0) gets the id n + k.
    """
    if n < 0 or t < 1:
        raise ValueError("n must be non-negative and t positive")
    wedges: list[tuple[int, int, float]] = []
    a: list[dict[int, float]] = [{v: 1.0} for v in range(n)]  # @line L1
    for e in edges:
        u, v = e[0], e[1]
        w = float(e[2]) if len(e) == 3 else 1.0
        if not (0 <= u < n and 0 <= v < n) or u == v or not w > 0.0:
            raise ValueError("bad edge")
        wedges.append((u, v, w))
        a[u][v] = a[u].get(v, 0.0) + w
        a[v][u] = a[v].get(u, 0.0) + w
    d = [sum(a[v].values()) for v in range(n)]
    vec: dict[int, list[float]] = {}
    for i in range(n):  # @line L2
        row = [0.0] * n
        row[i] = 1.0
        for _ in range(t):
            nxt = [0.0] * n
            for x in range(n):
                if row[x]:
                    share = row[x] / d[x]
                    for y, w in a[x].items():
                        nxt[y] += share * w
            row = nxt
        vec[i] = [row[k] / math.sqrt(d[k]) for k in range(n)]
    size = {i: 1 for i in range(n)}
    members = {i: [i] for i in range(n)}
    nbr: dict[int, set[int]] = {i: {j for j in a[i] if j != i} for i in range(n)}

    def cost(c1: int, c2: int) -> float:
        s1, s2 = size[c1], size[c2]
        dist2 = sum((x - y) ** 2 for x, y in zip(vec[c1], vec[c2]))
        return s1 * s2 / (s1 + s2) * dist2 / n

    delta: dict[tuple[int, int], float] = {}
    for i in range(n):  # @line L3
        for j in nbr[i]:
            if i < j:
                delta[(i, j)] = cost(i, j)
    parts_seq = [[[i] for i in range(n)]]  # @line L4
    merges: list[tuple[int, int, float]] = []
    while delta:  # @line L5
        best = min(delta.values())
        tol = 1e-12 * max(1.0, abs(best))
        c1, c2 = min(p for p, v in delta.items() if v <= best + tol)  # @line L6
        c3 = n + len(merges)
        merges.append((c1, c2, delta[(c1, c2)]))
        s1, s2 = size[c1], size[c2]
        vec[c3] = [(s1 * x + s2 * y) / (s1 + s2) for x, y in zip(vec[c1], vec[c2])]  # @line L7
        size[c3] = s1 + s2
        members[c3] = members[c1] + members[c2]
        nbr[c3] = (nbr[c1] | nbr[c2]) - {c1, c2}
        for c in (c1, c2):
            for x in nbr[c]:
                nbr[x].discard(c)
                delta.pop((min(c, x), max(c, x)), None)
            del vec[c], size[c], members[c], nbr[c]
        for x in nbr[c3]:  # @line L8
            nbr[x].add(c3)
            delta[(x, c3)] = cost(x, c3)
        parts_seq.append([sorted(m) for m in members.values()])  # @line L9
    best_q = -math.inf
    best_parts: list[list[int]] = []
    for parts in parts_seq:  # @line L10
        q = modularity(n, wedges, parts)
        if q > best_q + 1e-12:
            best_q, best_parts = q, parts
    return sorted(best_parts), merges
