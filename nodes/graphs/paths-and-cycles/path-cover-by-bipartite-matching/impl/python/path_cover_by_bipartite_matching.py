# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/path-cover-by-bipartite-matching/. The authors are listed in prov/775KP1.jsonl.


def path_cover_by_bipartite_matching(n: int, arcs: list[tuple[int, int]]) -> list[list[int]]:
    """Return a minimum set of vertex-disjoint paths that covers every vertex of a DAG.

    Precondition: the directed graph with vertices 0 .. n-1 and arcs (u, v) is acyclic;
    parallel arcs are allowed. Raises ValueError if it has a cycle (a self-loop
    included). Each path is a list of vertices in arc order; the paths are sorted by
    their first vertex. The number of paths is n minus a maximum matching of the split
    graph, found by Kuhn's augmenting paths in O(n m) time and O(n + m) extra space.
    """
    _check_acyclic(n, arcs)
    adj: list[list[int]] = [[] for _ in range(n)]  # @line L1
    for u, v in arcs:
        adj[u].append(v)
    match_left: list[int | None] = [None] * n  # @line L2
    match_right: list[int | None] = [None] * n
    for root in range(n):  # @line L3
        visited = [False] * n  # @line L4
        ptr = [0] * n
        stack = [root]  # @line L5
        via: list[int] = []
        while stack:  # @line L6
            u = stack[-1]
            if ptr[u] == len(adj[u]):  # @line L7
                stack.pop()
                if via:
                    via.pop()
                continue
            v = adj[u][ptr[u]]  # @line L8
            ptr[u] += 1
            if visited[v]:
                continue
            visited[v] = True
            via.append(v)
            if match_right[v] is None:  # @line L9
                for x, y in zip(stack, via):  # @line L10
                    match_left[x] = y
                    match_right[y] = x
                break
            stack.append(match_right[v])  # @line L11
    paths: list[list[int]] = []
    for s in range(n):  # @line L12
        if match_right[s] is None:
            path = [s]  # @line L13
            while match_left[path[-1]] is not None:
                path.append(match_left[path[-1]])
            paths.append(path)
    return paths  # @line L14


def _check_acyclic(n: int, arcs: list[tuple[int, int]]) -> None:
    indeg = [0] * n
    out: list[list[int]] = [[] for _ in range(n)]
    for u, v in arcs:
        out[u].append(v)
        indeg[v] += 1
    queue = [v for v in range(n) if indeg[v] == 0]
    seen = 0
    while queue:
        u = queue.pop()
        seen += 1
        for v in out[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)
    if seen != n:
        raise ValueError("the graph has a directed cycle")
