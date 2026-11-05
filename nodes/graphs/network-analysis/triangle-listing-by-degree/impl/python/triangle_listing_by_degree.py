# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/triangle-listing-by-degree/. The authors are listed in prov/94JZ51.jsonl.


def triangles_by_degree(n: int, edges: list[tuple[int, int]]) -> list[tuple[int, int, int]]:
    """List every triangle of a simple undirected graph exactly once.

    The vertices are 0 .. n-1 and edges is a list of pairs {u, v} with u != v
    and no repeated edge. Each triangle is returned once, as (u, v, w) with
    rank(u) < rank(v) < rank(w), where rank(x) = (degree(x), x).
    Time O(n + m^(3/2)) and O(n + a(G) m); extra space O(n + m).
    """
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        if u == v or not (0 <= u < n and 0 <= v < n):
            raise ValueError("bad edge")
        adj[u].append(v)
        adj[v].append(u)
    d = [len(adj[v]) for v in range(n)]  # @line L1
    out = [[w for w in adj[v] if (d[v], v) < (d[w], w)] for v in range(n)]  # @line L2
    mark = [False] * n  # @line L3
    tri: list[tuple[int, int, int]] = []  # @line L4
    for u in range(n):  # @line L5
        for v in out[u]:  # @line L6
            mark[v] = True
        for v in out[u]:  # @line L7
            for w in out[v]:  # @line L8
                if mark[w]:  # @line L9
                    tri.append((u, v, w))
        for v in out[u]:  # @line L10
            mark[v] = False
    return tri  # @line L11


def local_counts(n: int, edges: list[tuple[int, int]]) -> list[int]:
    """Return t(v), the number of triangles that contain each vertex v."""
    t = [0] * n
    for a, b, c in triangles_by_degree(n, edges):
        t[a] += 1
        t[b] += 1
        t[c] += 1
    return t
