# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/itai-rodeh-girth-algorithm/. The authors are listed in prov/SX075V.jsonl.

from collections import deque


def itai_rodeh_girth_algorithm(
    n: int, edges: list[tuple[int, int]]
) -> tuple[list[int], list[int]] | None:
    """Return a shortest cycle of an undirected graph, or None if it is a forest.

    The graph has the vertices 0 .. n-1 and the undirected edges edges[i] = (u, v),
    numbered by i; self-loops, parallel edges and isolated vertices are allowed. The
    result (vs, es) has len(vs) == len(es) == girth, and es[i] joins vs[i] to
    vs[(i + 1) % girth]. One breadth-first search runs from every vertex.
    Time O(n (n + m)), extra space O(n + m).
    """
    inc: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for e, (u, v) in enumerate(edges):
        inc[u].append((e, v))
        inc[v].append((e, u))  # a loop appears twice at its vertex

    def search(r: int, record: bool) -> tuple[list[int], list[int], list[int]]:
        nonlocal best, found
        dist = [-1] * n  # @line L3
        pv = [-1] * n
        pe = [-1] * n
        dist[r] = 0
        queue = deque([r])
        while queue:  # @line L4
            u = queue.popleft()  # @line L5
            for e, v in inc[u]:  # @line L6
                if dist[v] < 0:  # @line L7
                    dist[v] = dist[u] + 1
                    pv[v], pe[v] = u, e
                    queue.append(v)
                elif record and e != pe[u] and dist[u] + dist[v] + 1 < best:  # @line L8
                    best = dist[u] + dist[v] + 1  # @line L9
                    found = (r, e, u, v)
        return dist, pv, pe

    best = n + 1  # @line L1
    found = (-1, -1, -1, -1)
    for r in range(n):  # @line L2
        search(r, True)
    if found[0] < 0:  # @line L10
        return None
    r, e, a, b = found
    dist, pv, pe = search(r, False)  # @line L11
    left_v, left_e, right_v, right_e = [a], [], [b], []
    while a != b:  # climb to the lowest common ancestor
        if dist[a] >= dist[b]:
            left_e.append(pe[a])
            a = pv[a]
            left_v.append(a)
        else:
            right_e.append(pe[b])
            b = pv[b]
            right_v.append(b)
    return left_v[::-1] + right_v[:-1], left_e[::-1] + [e] + right_e  # @line L12
