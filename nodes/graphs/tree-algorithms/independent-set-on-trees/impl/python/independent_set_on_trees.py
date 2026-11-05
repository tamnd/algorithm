# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/independent-set-on-trees/. The authors are listed in prov/EAW1JK.jsonl.

from collections import deque


def max_weight_independent_set(
    n: int, edges: list[tuple[int, int]], weight: list[int], root: int = 0
) -> tuple[int, list[int]]:
    """Return (best, S): a maximum-weight independent set S of a tree and its weight.

    The tree has the vertices 0 .. n-1 (n >= 1) and is given by its n - 1
    undirected edges; it is unrooted, and `root` only fixes the order of the
    work. weight[v] is the integer weight of vertex v and may be zero or
    negative. S is sorted. The time and the extra memory are O(n); there is
    no recursion, so a path of 10^5 vertices is fine.
    """
    if n < 1 or len(edges) != n - 1 or len(weight) != n:
        raise ValueError("a tree needs n >= 1 vertices, n - 1 edges and n weights")
    adj: list[list[int]] = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    parent = [-1] * n
    seen = [False] * n
    seen[root] = True
    order = [root]  # @line L1
    queue = deque([root])
    while queue:
        x = queue.popleft()
        for y in adj[x]:
            if not seen[y]:
                seen[y] = True
                parent[y] = x
                order.append(y)
                queue.append(y)
    if len(order) != n:
        raise ValueError("the edges do not connect all vertices")
    take_in = [0] * n
    take_out = [0] * n
    for v in reversed(order):  # @line L2
        take_in[v] += weight[v]  # @line L3
        p = parent[v]
        if p >= 0:  # @line L4
            take_in[p] += take_out[v]
            take_out[p] += max(take_in[v], take_out[v])
    best = max(take_in[root], take_out[root])  # @line L5
    chosen = [False] * n
    for v in order:  # @line L6
        p = parent[v]
        if p >= 0 and chosen[p]:  # @line L7
            continue
        chosen[v] = take_in[v] > take_out[v]  # @line L8
    return best, [v for v in range(n) if chosen[v]]  # @line L9
