# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tseng-siewiorek-clique-partitioning/. The authors are listed in prov/FCVE23.jsonl.

"""Tseng-Siewiorek greedy clique partitioning of a compatibility graph.

The graph has the vertices 0, ..., n - 1 and a list of undirected edges.
An edge joins two operations or values that may share one unit or register.
The result is a list of cliques that partition the vertices; each clique is
one unit or register. The greedy merges, while an edge remains, the pair of
supernodes with the most common neighbours. Ties go to the merge that deletes
the fewest edges, then to the smallest pair of indices.
"""


def tseng_siewiorek(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    """Return a partition of range(n) into cliques of the graph, by the greedy merge rule."""
    members: dict[int, list[int]] = {}
    nbr: dict[int, set[int]] = {}
    for v in range(n):                                            # @line L1
        members[v] = [v]
        nbr[v] = set()
    for u, v in edges:
        if u != v:
            nbr[u].add(v)
            nbr[v].add(u)
    while any(nbr[v] for v in nbr):                               # @line L2
        best = None
        for i in sorted(nbr):                                     # @line L3
            for j in sorted(nbr[i]):
                if j <= i:
                    continue
                common = len(nbr[i] & nbr[j])
                deleted = len(nbr[i]) + len(nbr[j]) - 1 - common
                key = (-common, deleted, i, j)                    # @line L4
                if best is None or key < best:
                    best = key
        _, _, i, j = best
        members[i] = sorted(members[i] + members[j])              # @line L5
        del members[j]
        keep = (nbr[i] & nbr[j]) - {i, j}                         # @line L6
        for x in nbr[i] | nbr[j]:
            nbr[x].discard(i)
            nbr[x].discard(j)
        del nbr[j]
        nbr[i] = keep
        for x in keep:
            nbr[x].add(i)
    return sorted(members.values())                               # @line L7


def merge_trace(n: int, edges: list[tuple[int, int]]) -> list[tuple[int, int, int, int]]:
    """The merges of the greedy as (i, j, common neighbours, deleted edges), in order."""
    nbr: dict[int, set[int]] = {v: set() for v in range(n)}
    for u, v in edges:
        if u != v:
            nbr[u].add(v)
            nbr[v].add(u)
    out: list[tuple[int, int, int, int]] = []
    while any(nbr[v] for v in nbr):
        best = None
        for i in sorted(nbr):
            for j in sorted(nbr[i]):
                if j > i:
                    common = len(nbr[i] & nbr[j])
                    key = (-common, len(nbr[i]) + len(nbr[j]) - 1 - common, i, j)
                    if best is None or key < best:
                        best = key
        c, d, i, j = best
        out.append((i, j, -c, d))
        keep = (nbr[i] & nbr[j]) - {i, j}
        for x in nbr[i] | nbr[j]:
            nbr[x].discard(i)
            nbr[x].discard(j)
        del nbr[j]
        nbr[i] = keep
        for x in keep:
            nbr[x].add(i)
    return out


def is_clique_partition(n: int, edges: list[tuple[int, int]], parts: list[list[int]]) -> bool:
    """True when parts cover range(n) once each and every part is a clique."""
    adj = {(min(u, v), max(u, v)) for u, v in edges}
    seen = sorted(v for p in parts for v in p)
    if seen != list(range(n)):
        return False
    for p in parts:
        for a in range(len(p)):
            for b in range(a + 1, len(p)):
                if (min(p[a], p[b]), max(p[a], p[b])) not in adj:
                    return False
    return True


def min_clique_partition(n: int, edges: list[tuple[int, int]]) -> int:
    """The least number of cliques that partition the graph, by a dynamic program over subsets."""
    adj = [0] * n
    for u, v in edges:
        if u != v:
            adj[u] |= 1 << v
            adj[v] |= 1 << u
    full = (1 << n) - 1
    clique = [True] * (full + 1)
    for s in range(1, full + 1):
        low = (s & -s).bit_length() - 1
        rest = s & ~(1 << low)
        clique[s] = clique[rest] and (rest & ~adj[low]) == 0
    best = [0] * (full + 1)
    for s in range(1, full + 1):
        low = s & -s
        rest = s & ~low
        value = n + 1
        t = rest
        while True:
            c = t | low
            if clique[c] and 1 + best[s & ~c] < value:
                value = 1 + best[s & ~c]
            if t == 0:
                break
            t = (t - 1) & rest
        best[s] = value
    return best[full]


def interval_compatibility(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Edges between closed integer intervals that do not overlap."""
    n = len(intervals)
    return [(u, v) for u in range(n) for v in range(u + 1, n)
            if intervals[u][1] < intervals[v][0] or intervals[v][1] < intervals[u][0]]


def depth(intervals: list[tuple[int, int]]) -> int:
    """The largest number of closed integer intervals that share one point."""
    if not intervals:
        return 0
    points = sorted({a for a, _ in intervals})
    return max(sum(1 for a, b in intervals if a <= p <= b) for p in points)
