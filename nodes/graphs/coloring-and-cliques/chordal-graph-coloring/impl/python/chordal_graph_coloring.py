# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chordal-graph-coloring/. The authors are listed in prov/JWQZ4N.jsonl.

from collections.abc import Sequence


def mcs_order(adj: Sequence[Sequence[int]]) -> list[int]:
    """Maximum cardinality search: each next vertex has the most visited neighbours.

    Buckets indexed by the number of visited neighbours; ties go to the vertex
    that entered its bucket last. Time O(n + m).
    """
    n = len(adj)
    weight = [0] * n
    buckets: list[dict[int, None]] = [{} for _ in range(n + 1)]
    for v in range(n):
        buckets[0][v] = None
    visited = [False] * n
    order: list[int] = []
    j = 0
    for _ in range(n):
        while not buckets[j]:
            j -= 1
        v, _none = buckets[j].popitem()
        visited[v] = True
        order.append(v)
        for w in adj[v]:
            if not visited[w]:
                del buckets[weight[w]][w]
                weight[w] += 1
                buckets[weight[w]][w] = None
        j += 1
    return order


def chordal_graph_coloring(adj: Sequence[Sequence[int]]) -> list[int] | None:
    """Optimal coloring of a chordal graph, or None if the graph is not chordal.

    adj[v] lists the neighbours of v (vertices 0 .. n-1, each edge in both lists,
    no self-loops, no parallel edges). Runs maximum cardinality search; the
    reverse of its visit order is a perfect elimination ordering exactly when
    the graph is chordal, which is checked in linear time. Then colors greedily
    in visit order, which uses omega(G) = chi(G) colors (colors start at 1).
    Time O(n + m), extra space O(n + m).
    """
    n = len(adj)
    order = mcs_order(adj)  # @line L1
    pos = [0] * n
    for i, v in enumerate(order):
        pos[v] = i
    earlier: list[list[int]] = [[] for _ in range(n)]
    checks: list[list[int]] = [[] for _ in range(n)]
    for v in order:  # @line L2
        earlier[v] = [w for w in adj[v] if pos[w] < pos[v]]  # @line L3
        if earlier[v]:  # @line L4
            p = max(earlier[v], key=lambda w: pos[w])
            for w in earlier[v]:
                if w != p:
                    checks[p].append(w)
    mark = [-1] * n
    for u in range(n):  # @line L5
        for w in adj[u]:
            mark[w] = u
        for w in checks[u]:
            if mark[w] != u:
                return None
    c = [0] * n
    used = [-1] * (n + 2)
    for v in order:  # @line L6
        for w in earlier[v]:  # @line L7
            used[c[w]] = v
        k = 1
        while used[k] == v:
            k += 1
        c[v] = k
    return c  # @line L8
