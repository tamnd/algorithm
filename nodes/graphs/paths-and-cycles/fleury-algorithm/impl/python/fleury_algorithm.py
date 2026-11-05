# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fleury-algorithm/. The authors are listed in prov/CVA0RG.jsonl.


def _reachable(inc: list[list[int]], edges: list[tuple[int, int]], used: list[bool], s: int, t: int) -> bool:
    """Is t reachable from s through edges that are not used? Iterative search."""
    if s == t:
        return True
    seen = {s}
    stack = [s]
    while stack:
        x = stack.pop()
        for e in inc[x]:
            if used[e]:
                continue
            a, b = edges[e]
            y = b if a == x else a
            if y == t:
                return True
            if y not in seen:
                seen.add(y)
                stack.append(y)
    return False


def fleury_algorithm(n: int, edges: list[tuple[int, int]]) -> tuple[list[int], list[int]] | None:
    """Return an Eulerian trail of an undirected multigraph, or None if it has none.

    The vertices are 0 .. n-1 and edge i is edges[i] = (u, v). Parallel edges, self-loops
    and isolated vertices are allowed. The result is (walk, trail): walk lists the m + 1
    vertices and trail the m edge numbers, and trail[i] joins walk[i] to walk[i+1].
    The trail starts at an odd vertex if there is one, so it is closed when all degrees
    are even. At each step it leaves the current vertex by an edge that is not a bridge
    of the unused edges, unless that edge is the only one. Time O(m (n + m)).
    """
    m = len(edges)
    if n == 0:
        return ([], []) if m == 0 else None
    if m == 0:
        return ([0], [])
    inc: list[list[int]] = [[] for _ in range(n)]
    deg = [0] * n
    for e, (u, v) in enumerate(edges):
        inc[u].append(e)
        if u != v:
            inc[v].append(e)
        deg[u] += 1
        deg[v] += 1  # a loop adds 2
    used = [False] * m
    odd = [v for v in range(n) if deg[v] % 2 == 1]
    # The Euler condition: 0 or 2 odd vertices and all edges in one component.  @line L1
    if len(odd) > 2:
        return None
    start = odd[0] if odd else edges[0][0]  # @line L2
    if not all(_reachable(inc, edges, used, start, edges[e][0]) for e in range(m)):
        return None
    walk = [start]  # @line L3
    trail: list[int] = []
    left = deg[:]  # the degrees in the graph H of unused edges
    ptr = [0] * n  # unused edges before ptr[u] in inc[u] are skipped for good
    u = start
    while left[u] > 0:  # @line L4
        while used[inc[u][ptr[u]]]:
            ptr[u] += 1
        if left[u] == 1:  # @line L5
            e = inc[u][ptr[u]]
        else:
            # An edge at u that is not a bridge of H. At most one edge at u is a bridge,
            # so at most two candidates are tested.  @line L6
            e = -1
            for i in range(ptr[u], len(inc[u])):
                f = inc[u][i]
                if used[f]:
                    continue
                a, b = edges[f]
                v = b if a == u else a
                used[f] = True
                ok = _reachable(inc, edges, used, u, v)  # f is a bridge iff this fails
                used[f] = False
                if ok:
                    e = f
                    break
        used[e] = True  # @line L7
        trail.append(e)
        a, b = edges[e]
        w = b if a == u else a
        left[u] -= 1
        left[w] -= 1
        u = w  # @line L8
        walk.append(u)
    return walk, trail  # @line L9
