# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tree-diameter-double-sweep/. The authors are listed in prov/EZ41AA.jsonl.

Edge = tuple[int, int, int]


def distances(adj: list[list[tuple[int, int]]], s: int) -> tuple[list[int], list[int]]:
    """Distances and parents from s in a tree, by an iterative depth-first search.

    adj[u] lists the pairs (v, w) of the neighbours of u and the edge lengths.
    The parent of s is -1. Time Theta(n), no recursion.
    """
    n = len(adj)
    dist = [0] * n
    par = [-1] * n
    seen = [False] * n
    seen[s] = True  # @line L9
    stack = [s]
    while stack:  # @line L10
        u = stack.pop()  # @line L11
        for v, w in adj[u]:  # @line L12
            if not seen[v]:
                seen[v] = True
                dist[v] = dist[u] + w  # @line L13
                par[v] = u
                stack.append(v)  # @line L14
    return dist, par  # @line L15


def tree_diameter(n: int, edges: list[Edge]) -> tuple[int, list[int]]:
    """Return (D, path): the diameter of a tree and one diametral path.

    The tree is free, with the vertices 0 .. n-1 (n >= 1) and the n - 1 edges
    (u, v, w), where w >= 0 is the length. For an unweighted tree use w = 1.
    The path lists the vertices from one end a to the other end b. Time and
    extra space Theta(n). The result can be wrong if some w is negative.
    """
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    dist, _ = distances(adj, 0)  # @line L1
    a = max(range(n), key=dist.__getitem__)  # @line L2
    dist, par = distances(adj, a)  # @line L3
    b = max(range(n), key=dist.__getitem__)  # @line L4
    path = [b]  # @line L5
    while path[-1] != a:  # @line L6
        path.append(par[path[-1]])  # @line L7
    path.reverse()
    return dist[b], path  # @line L8
